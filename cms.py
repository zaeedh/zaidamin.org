"""
Academic Content Management System (CMS) Engine for zaidamin.org
Author: Antigravity & Dr. Zaid Amin
Supports:
- Articles & Essays (data/articles.json)
- Publications & Citations (data/publications.json)
- Recent Media & Talks (data/talks.json)
- Achievements & CV (data/cv_data.json)
"""

import json
import os
import sys
import re
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DIST_DATA_DIR = BASE_DIR / "dist" / "data"

def load_json(name):
    p = DATA_DIR / name
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(DIST_DATA_DIR / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def rebuild_site():
    print("[CMS] Compiling website via build.py...")
    ret = subprocess.run([sys.executable, str(BASE_DIR / "build.py")], capture_output=True, text=True)
    if ret.returncode == 0:
        print("[CMS] Website compiled successfully.")
        return True
    else:
        print("[CMS ERROR] Rebuild failed:\n", ret.stderr)
        return False

def deploy_to_live():
    print("[CMS] Deploying live to zaidamin.org...")
    subprocess.run([sys.executable, str(BASE_DIR / "deploy.py")])

# 1. Articles Operations
def list_articles(limit=10):
    arts = load_json("articles.json")
    print(f"\n--- ARTICLES ARCHIVE (Total: {len(arts)}) ---")
    for a in arts[:limit]:
        print(f"[{a.get('date', '')}] {a.get('id')}: {a.get('title')} ({a.get('category')})")

# 2. Publications Operations
def list_pubs(limit=10):
    pubs = load_json("publications.json")
    print(f"\n--- PUBLICATIONS ARCHIVE (Total: {len(pubs)}) ---")
    for p in pubs[:limit]:
        print(f"[{p.get('year')}] {p.get('id')}: {p.get('title')} ({p.get('category')}) - {p.get('venue')}")

# 3. Talks Operations
def list_talks():
    data = load_json("talks.json")
    talks = data.get("talks", []) if isinstance(data, dict) else data
    print(f"\n--- MEDIA & TALKS (Total: {len(talks)}) ---")
    for t in talks:
        print(f"[{t.get('year')}] {t.get('title')} ({t.get('role')}) - {t.get('event')}")

# 4. CV Operations
def list_cv():
    cv = load_json("cv_data.json")
    items = cv.get("achievements_and_grants", [])
    print(f"\n--- ACHIEVEMENTS & CV (Total: {len(items)}) ---")
    for a in items:
        print(f"[{a.get('year')}] {a.get('title')} ({a.get('badge')}) - {a.get('organization')}")

def count_all():
    arts = load_json("articles.json")
    pubs = load_json("publications.json")
    talks_data = load_json("talks.json")
    talks = talks_data.get("talks", []) if isinstance(talks_data, dict) else talks_data
    cv = load_json("cv_data.json")
    achievements = cv.get("achievements_and_grants", [])

    print("=" * 50)
    print("   ZAIDAMIN.ORG CONTENT AUDIT & INVENTORY")
    print("=" * 50)
    print(f" - Articles & Essays (Activity & Project): {len(arts)}")
    print(f" - Publications & Preprints:              {len(pubs)}")
    print(f" - Media & Invited Talks:                 {len(talks)}")
    print(f" - Achievements, Awards & Grants:         {len(achievements)}")
    print("=" * 50)

def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "count"

    if cmd in ["count", "status", "info"]:
        count_all()
    elif cmd in ["articles", "art"]:
        list_articles(int(args[1]) if len(args) > 1 else 15)
    elif cmd in ["pubs", "publications"]:
        list_pubs(int(args[1]) if len(args) > 1 else 15)
    elif cmd in ["talks", "media"]:
        list_talks()
    elif cmd in ["cv", "achievements"]:
        list_cv()
    elif cmd in ["rebuild", "build"]:
        rebuild_site()
    elif cmd in ["deploy", "publish"]:
        deploy_to_live()
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python cms.py [count|articles|pubs|talks|cv|rebuild|deploy]")

if __name__ == "__main__":
    main()
