"""
Academic Content Management System (CMS) Engine for zaidamin.org
Author: Antigravity & Dr. Zaid Amin
"""

import json
import os
import sys
import re
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARTICLES_FILE = BASE_DIR / "data" / "articles.json"

CATEGORIES = [
    "AI & Cybernetics",
    "Digital Ethics & HCI",
    "Research & Methodology",
    "Pedagogy & Education",
    "Philosophy & Society",
    "Epistemic & Media",
    "Essays & Perspectives"
]

def load_articles():
    if not ARTICLES_FILE.exists():
        return []
    with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_articles(articles):
    os.makedirs(ARTICLES_FILE.parent, exist_ok=True)
    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"[CMS] Successfully saved {len(articles)} articles to {ARTICLES_FILE}")

def slugify(title):
    clean = re.sub(r'[^\w\s-]', '', title.lower())
    clean = re.sub(r'[-\s]+', '-', clean).strip('-')
    parts = clean.split('-')[:8]
    return '-'.join(parts) if parts else "article"

def calculate_reading_time(content):
    plain = re.sub(r'<[^>]+>', ' ', content)
    words = len(plain.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"

def add_article(title, category, content_html, excerpt="", tags=None, image="", date=None):
    articles = load_articles()
    slug = slugify(title)
    
    # Ensure slug uniqueness
    existing_slugs = {a["id"] for a in articles}
    if slug in existing_slugs:
        slug = f"{slug}-{int(datetime.now().timestamp())}"

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    year = date[:4]

    if not tags:
        tags = [category]
    elif isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    if not excerpt:
        plain = re.sub(r'<[^>]+>', ' ', content_html)
        plain = ' '.join(plain.split())
        excerpt = plain[:240] + "..." if len(plain) > 240 else plain

    reading_time = calculate_reading_time(content_html)

    new_article = {
        "id": slug,
        "title": title.strip(),
        "date": date,
        "year": year,
        "category": category,
        "tags": tags,
        "reading_time": reading_time,
        "excerpt": excerpt,
        "image": image,
        "content_html": content_html,
        "author": "Dr. Zaid Amin"
    }

    # Add to beginning (newest first)
    articles.insert(0, new_article)
    save_articles(articles)
    return new_article

def update_article(slug, data):
    articles = load_articles()
    for idx, a in enumerate(articles):
        if a["id"] == slug:
            for k, v in data.items():
                if k != "id": # preserve id
                    a[k] = v
            # recalculate reading time if content changed
            if "content_html" in data:
                a["reading_time"] = calculate_reading_time(data["content_html"])
            save_articles(articles)
            return a
    return None

def delete_article(slug):
    articles = load_articles()
    new_articles = [a for a in articles if a["id"] != slug]
    if len(new_articles) < len(articles):
        save_articles(new_articles)
        return True
    return False

def rebuild_site():
    print("[CMS] Rebuilding site via build.py...")
    res = subprocess.run([sys.executable, str(BASE_DIR / "build.py")], capture_output=True, text=True)
    if res.returncode == 0:
        print("[CMS] Build complete!")
        return True, res.stdout
    else:
        print("[CMS] Build failed:\n", res.stderr)
        return False, res.stderr

def deploy_to_live():
    print("[CMS] Publishing changes to GitHub via deploy.py...")
    res = subprocess.run([sys.executable, str(BASE_DIR / "deploy.py")], capture_output=True, text=True)
    if res.returncode == 0:
        print("[CMS] Deployment successful!")
        return True, res.stdout
    else:
        print("[CMS] Deployment failed:\n", res.stderr)
        return False, res.stderr

def print_help():
    print("""
Academic CMS Engine CLI - zaidamin.org
Usage:
  python cms.py list                  - List all articles with IDs and categories
  python cms.py count                 - Show total articles and category breakdown
  python cms.py rebuild               - Rebuild all HTML pages via build.py
  python cms.py deploy                - Publish changes to live domain via deploy.py
  python cms.py add                   - Interactive wizard to write and add an article
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "list":
        arts = load_articles()
        print(f"Total Articles: {len(arts)}")
        for idx, a in enumerate(arts[:20]):
            print(f"[{idx+1:02d}] {a['date']} | {a['category']:<22} | {a['title'][:50]} (ID: {a['id']})")
        if len(arts) > 20:
            print(f"... and {len(arts) - 20} more articles.")
    elif cmd == "count":
        arts = load_articles()
        print(f"Total Articles: {len(arts)}")
        cats = {}
        for a in arts:
            c = a.get("category", "Uncategorized")
            cats[c] = cats.get(c, 0) + 1
        for c, count in sorted(cats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {c}: {count}")
    elif cmd == "rebuild":
        rebuild_site()
    elif cmd == "deploy":
        rebuild_site()
        deploy_to_live()
    elif cmd == "add":
        print("--- Add New Article Wizard ---")
        title = input("Article Title: ").strip()
        print("Categories:")
        for idx, c in enumerate(CATEGORIES):
            print(f"  [{idx+1}] {c}")
        c_choice = input("Select Category (1-7) or enter custom: ").strip()
        if c_choice.isdigit() and 1 <= int(c_choice) <= len(CATEGORIES):
            category = CATEGORIES[int(c_choice) - 1]
        else:
            category = c_choice if c_choice else "Essays & Perspectives"
        tags = input("Tags (comma-separated): ").strip()
        excerpt = input("Excerpt / Summary: ").strip()
        print("Enter article content (HTML or plain text). Press Ctrl+Z (or Ctrl+D) on empty line when done:")
        content = sys.stdin.read().strip()
        if title and content:
            art = add_article(title, category, content, excerpt=excerpt, tags=tags)
            print(f"Successfully added article: {art['title']} (ID: {art['id']})")
            rebuild_site()
        else:
            print("Title and content are required.")
    else:
        print_help()

