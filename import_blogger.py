import urllib.request
import json
import ssl
import re
import html
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

FEED_URL = "https://zaidamin.blogspot.com/feeds/posts/default?alt=json&max-results=500"

def clean_html_text(raw_html):
    if not raw_html:
        return ""
    # Remove script and style tags
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw_html, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Unescape HTML entities
    text = html.unescape(text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

def extract_hero_image(entry, content_html):
    # 1. Check media$thumbnail
    thumb = entry.get('media$thumbnail', {}).get('url', '')
    if thumb:
        # Upgrade blogger thumbnail to high resolution
        # Replace /s72-c/, /s320/, /w640-h413-c/, etc. with /s1600/
        high_res = re.sub(r'/s[0-9]+(-[a-z0-9\-]+)?/', '/s1600/', thumb)
        high_res = re.sub(r'/w[0-9]+-h[0-9]+(-[a-z0-9\-]+)?/', '/s1600/', high_res)
        return high_res
    
    # 2. Check images inside content
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content_html)
    if imgs:
        img_url = imgs[0]
        high_res = re.sub(r'/s[0-9]+(-[a-z0-9\-]+)?/', '/s1600/', img_url)
        return high_res
        
    return ""

def fetch_all_posts():
    print(f"Fetching posts from: {FEED_URL}")
    req = urllib.request.Request(FEED_URL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    with urllib.request.urlopen(req, timeout=25, context=ctx) as res:
        feed_data = json.loads(res.read().decode('utf-8'))
        
    entries = feed_data.get('feed', {}).get('entry', [])
    print(f"Total entries fetched: {len(entries)}")
    
    posts = []
    for entry in entries:
        title = entry.get('title', {}).get('$t', '').strip()
        if not title:
            continue
            
        published = entry.get('published', {}).get('$t', '')[:10]
        updated = entry.get('updated', {}).get('$t', '')[:10]
        
        # Link
        post_url = ""
        for l in entry.get('link', []):
            if l.get('rel') == 'alternate':
                post_url = l.get('href', '')
                break
                
        # Categories / Tags
        tags = [c.get('term', '').strip() for c in entry.get('category', []) if c.get('term')]
        
        # Content & Excerpt
        content_html = entry.get('content', {}).get('$t', '') or entry.get('summary', {}).get('$t', '')
        plain_text = clean_html_text(content_html)
        
        # Excerpt (up to 280 chars)
        if len(plain_text) > 280:
            excerpt = plain_text[:280].rsplit(' ', 1)[0] + '...'
        else:
            excerpt = plain_text
            
        # Hero Image
        hero_img = extract_hero_image(entry, content_html)
        
        # Year
        year = published[:4] if published else "2026"
        
        posts.append({
            "title": title,
            "published": published,
            "year": year,
            "url": post_url,
            "tags": tags,
            "excerpt": excerpt,
            "image": hero_img
        })
        
    return posts

if __name__ == '__main__':
    posts = fetch_all_posts()
    out_file = Path('data') / 'blogger_posts.json'
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(posts)} articles to {out_file}")
    
    # Print sample of latest 5
    for i, p in enumerate(posts[:5]):
        print(f"[{i+1}] {p['published']} | {p['title']}")
        print(f"    Tags: {p['tags']}")
        print(f"    Image: {p['image'][:80]}..." if p['image'] else "    Image: None")
        print(f"    Excerpt: {p['excerpt'][:120]}...\n")
