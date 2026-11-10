"""
Academic Golden Ratio Static Site Generator - zaidamin.org
Epigraph (Qur'an 31:27) • Option 1 Storm Banner Across All Pages • Wardiere Showcase Layout
Author: Antigravity AI & Dr. Zaid Amin
"""

import json
import os
import re
import shutil
import html
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DIST_DIR = BASE_DIR / "dist"
ASSETS_DIR = BASE_DIR / "assets"

def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)

def render_lotus_symbol_svg():
    return '''<svg class="lotus-svg lotus-hybrid-svg" width="24" height="24" viewBox="0 0 100 86" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <!-- Premium Multi-Tiered Golden Lotus Gradient matching user reference -->
    <linearGradient id="lotusGoldLuxeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#fffceb" stop-opacity="0.95" />
      <stop offset="25%" stop-color="#fae6a0" stop-opacity="0.88" />
      <stop offset="65%" stop-color="#d4af37" stop-opacity="0.78" />
      <stop offset="100%" stop-color="#854d0e" stop-opacity="0.92" />
    </linearGradient>

    <!-- Warm Volumetric Stamen Halo Gradient -->
    <radialGradient id="lotusStamenRadial" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fef08a" stop-opacity="0.95" />
      <stop offset="45%" stop-color="#fb923c" stop-opacity="0.50" />
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0" />
    </radialGradient>

    <filter id="lotusGlowFilter" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3.2" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Ambient Living Core Halo -->
  <circle cx="50" cy="70" r="14" fill="url(#lotusStamenRadial)" class="lotus-halo" filter="url(#lotusGlowFilter)" />

  <g transform="translate(50, 70)">
    <!-- LAYER 1: Default 9-Petal Multi-Tiered Translucent Golden Lotus (Resting State with Breathing Shimmer) -->
    <g class="lotus-gold-layer">
      <!-- Far Outer Horizontal Bottom Wings (Cradle) -->
      <path class="gold-petal gp-wing-left"  d="M 0 0 C -9 -14, -13 -32, 0 -48 C 13 -32, 9 -14, 0 0 Z" />
      <path class="gold-petal gp-wing-right" d="M 0 0 C -9 -14, -13 -32, 0 -48 C 13 -32, 9 -14, 0 0 Z" />
      <!-- Outer Mid Tier -->
      <path class="gold-petal gp-out-left"   d="M 0 0 C -10 -15, -14 -35, 0 -51 C 14 -35, 10 -15, 0 0 Z" />
      <path class="gold-petal gp-out-right"  d="M 0 0 C -10 -15, -14 -35, 0 -51 C 14 -35, 10 -15, 0 0 Z" />
      <!-- Mid Tier -->
      <path class="gold-petal gp-mid-left"   d="M 0 0 C -11 -16, -14.5 -38, 0 -54 C 14.5 -38, 11 -16, 0 0 Z" />
      <path class="gold-petal gp-mid-right"  d="M 0 0 C -11 -16, -14.5 -38, 0 -54 C 14.5 -38, 11 -16, 0 0 Z" />
      <!-- Inner Pair -->
      <path class="gold-petal gp-in-left"    d="M 0 0 C -10.5 -16, -13.5 -38, 0 -53 C 13.5 -38, 10.5 -16, 0 0 Z" />
      <path class="gold-petal gp-in-right"   d="M 0 0 C -10.5 -16, -13.5 -38, 0 -53 C 13.5 -38, 10.5 -16, 0 0 Z" />
      <!-- Center Apex Petal (Tallest) -->
      <path class="gold-petal gp-center"     d="M 0 0 C -10.5 -17, -13.5 -40, 0 -56 C 13.5 -40, 10.5 -17, 0 0 Z" />
    </g>

    <!-- LAYER 2: Sacred 7-Petal Rainbow Chakra Blossom (Awakens upon Hover/Click from Bud to Full Bloom) -->
    <g class="lotus-rainbow-layer">
      <!-- Outer Left: Sunbeam Golden Yellow -->
      <path class="rainbow-petal p-yellow" fill="#FACC15" d="M 0 0 C -12.5 -13, -13.5 -35, 0 -48 C 13.5 -35, 12.5 -13, 0 0 Z" />
      <!-- Outer Right: Fresh Spring Green -->
      <path class="rainbow-petal p-green"  fill="#4ADE80" d="M 0 0 C -12.5 -13, -13.5 -35, 0 -48 C 13.5 -35, 12.5 -13, 0 0 Z" />
      <!-- Mid Left: Warm Sunset Orange -->
      <path class="rainbow-petal p-orange" fill="#FB923C" d="M 0 0 C -14 -14, -14.5 -38, 0 -52 C 14.5 -38, 14 -14, 0 0 Z" />
      <!-- Mid Right: Turquoise Aqua Cyan -->
      <path class="rainbow-petal p-cyan"   fill="#38BDF8" d="M 0 0 C -14 -14, -14.5 -38, 0 -52 C 14.5 -38, 14 -14, 0 0 Z" />
      <!-- Inner Left: Radiant Rose Pink -->
      <path class="rainbow-petal p-pink"   fill="#F472B6" d="M 0 0 C -14.5 -15, -15 -41, 0 -56 C 15 -41, 14.5 -15, 0 0 Z" />
      <!-- Inner Right: Sky Cerulean Blue -->
      <path class="rainbow-petal p-blue"   fill="#60A5FA" d="M 0 0 C -14.5 -15, -15 -41, 0 -56 C 15 -41, 14.5 -15, 0 0 Z" />
      <!-- Center Crown: Sacred Royal Violet -->
      <path class="rainbow-petal p-violet" fill="#A855F7" d="M 0 0 C -15 -16, -15.5 -44, 0 -60 C 15.5 -44, 15 -16, 0 0 Z" />
    </g>
  </g>
</svg>'''

def render_svg_icon(name):
    icons = {
        "scholar": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 24a7 7 0 1 1 0-14 7 7 0 0 1 0 14zm0-24L0 9.5l4.8 3.8v6.7L12 24l7.2-4v-6.7l4.8-3.8L12 0zm0 3.7l7.1 5.8-7.1 5.8-7.1-5.8 7.1-5.8z"/></svg>',
        "orcid": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.306v7.444h2.297c2.359 0 3.8-1.381 3.8-3.722 0-2.203-1.406-3.722-3.8-3.722h-2.297z"/></svg>',
        "github": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>',
        "linkedin": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>',
        "email": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>',
        "sciprofiles": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>',
        "researchgate": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19.586 0c-.818 0-1.508.19-2.073.565-.563.377-.97.936-1.213 1.68a3.193 3.193 0 0 0-.112.437 8.365 8.365 0 0 0-.078.53 9 9 0 0 0-.05.572c-.01.199-.02.403-.02.613v.143c0 .01.01.02.01.03v.01c.285 2.115 1.5 3.336 3.642 3.664.13.02.26.03.39.03.88 0 1.62-.26 2.22-.78.6-.52.9-1.23.9-2.13 0-.9-.3-1.61-.9-2.13-.6-.52-1.34-.78-2.22-.78l-.49.03v-.02zm-8.8 8.08c-1.5 0-2.77.53-3.8 1.58-1.03 1.05-1.55 2.37-1.55 3.96 0 1.6.52 2.92 1.55 3.96 1.03 1.05 2.3 1.58 3.8 1.58 1.5 0 2.76-.53 3.8-1.58 1.03-1.04 1.55-2.36 1.55-3.96 0-1.59-.52-2.91-1.55-3.96-1.04-1.05-2.3-1.58-3.8-1.58zm0 2.1c.88 0 1.62.33 2.22 1 .6.67.9 1.48.9 2.44 0 .96-.3 1.77-.9 2.44-.6.67-1.34 1-2.22 1-.88 0-1.62-.33-2.22-1-.6-.67-.9-1.48-.9-2.44 0-.96.3-1.77.9-2.44.6-.67 1.34-1 2.22-1z"/></svg>',
        "arrow-right": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>',
        "arrow-left": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>',
        "external": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>',
        "download": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>',
        "search": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
    }
    return icons.get(name, "")

def get_page_browser_title(page_key, default_title=""):
    try:
        profile = load_json("profile.json")
        pt = profile.get("page_titles", {})
        if page_key in pt and str(pt[page_key]).strip():
            return str(pt[page_key]).strip()
        if page_key == "home" and profile.get("site_title", "").strip():
            return str(profile.get("site_title")).strip()
    except Exception:
        pass
    return default_title

def get_html_head(title="Dr. Zaid Amin | Academic & Computational Researcher | zaidamin.org", description=""):
    profile = load_json("profile.json")
    ga_snippet = ""
    analytics_file = DATA_DIR / "analytics.json"
    if analytics_file.exists():
        try:
            analytics_cfg = load_json("analytics.json")
            ga_id = analytics_cfg.get("ga_measurement_id", "").strip()
            if analytics_cfg.get("ga_enabled") and ga_id:
                ga_snippet = f'''
  <!-- Google tag (gtag.js) GA4 Real-Time Analytics (Option 2) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{ga_id}', {{ 'anonymize_ip': true }});
  </script>'''
        except Exception:
            ga_snippet = ""

    if not description:
        description = profile["short_bio"]

    schema_json = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": profile["name"],
        "url": "https://zaidamin.org",
        "jobTitle": profile["title"],
        "worksFor": {
            "@type": "CollegeOrUniversity",
            "name": profile["affiliation"]["institution"],
            "url": profile["affiliation"]["website"]
        },
        "alumniOf": [
            {"@type": "CollegeOrUniversity", "name": "Universiti Kebangsaan Malaysia (UKM)"},
            {"@type": "CollegeOrUniversity", "name": "Universitas Bina Darma"}
        ],
        "knowsAbout": profile["research_keywords"],
        "sameAs": [
            profile["social_links"]["orcid"],
            profile["social_links"]["scholar"],
            profile["social_links"]["github"],
            profile["social_links"]["linkedin"],
            profile["social_links"]["sciprofiles"]
        ]
    }

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Force HTTPS Protocol & Auto-Upgrade Insecure Resources -->
  <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
  <script>
    if (location.protocol === 'http:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {{
      location.replace('https://' + location.hostname + location.pathname + location.search + location.hash);
    }}
  </script>
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="author" content="Dr. Zaid Amin">
  <link rel="canonical" href="https://zaidamin.org/">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://zaidamin.org/">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">

  <!-- Google Scholar Indexing -->
  <meta name="citation_author" content="Amin, Zaid">
  <meta name="citation_author_institution" content="INTI International University">

  <!-- JSON-LD -->
  <script type="application/ld+json">
  {json.dumps(schema_json, indent=2)}
  </script>

  <!-- Typography & Styling -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Inter:wght@400;500;600;700;800;900&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css?v=4.1">
  <!-- High-Definition Monogram Favicon Suite (Dr. Zaid Amin) -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <!-- Enterprise Cyber Threat Defense & Zero-Vulnerability Architecture -->
  <meta http-equiv="X-Content-Type-Options" content="nosniff">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=()">

  <!-- Seamless Address Bar Immersion & Native PWA App Manifest -->
  <meta name="theme-color" content="#020b14">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <link rel="manifest" href="site.webmanifest">
  {ga_snippet}
</head>
<body>
"""

def get_navigation_data():
    try:
        data = load_json("navigation.json")
        if data and isinstance(data, dict) and "main_menu" in data:
            if "footer_links" not in data:
                data["footer_links"] = [
                    {"id": "team", "label": "Research Team", "url": "research-team.html", "target": "_self", "icon": "👥", "enabled": True},
                    {"id": "supervision", "label": "Supervision Lab", "url": "prospective-students.html", "target": "_self", "icon": "🎓", "enabled": True},
                    {"id": "activity", "label": "Activity & Essays", "url": "research.html#articles", "target": "_self", "icon": "📑", "enabled": True},
                    {"id": "publications", "label": "Publications", "url": "publications.html", "target": "_self", "icon": "📚", "enabled": True},
                    {"id": "contact", "label": "Contact Inquiry", "url": "mailto:zaid.amin@newinti.edu.my", "target": "_self", "icon": "✉️", "enabled": True}
                ]
            if "page_shortcuts" not in data:
                data["page_shortcuts"] = [
                    {
                        "id": "pub_team_pill",
                        "page": "publications.html",
                        "page_label": "Research & Publications (publications.html)",
                        "label": "Research Team Shortcut Pill",
                        "display_text": "👥 Research Team ↗",
                        "title": "View Research Team & Supervision Roster",
                        "url": "research-team.html",
                        "target": "_self",
                        "icon": "👥",
                        "enabled": True,
                        "description": "Category navigation shortcut pill in the Publications page header"
                    }
                ]
            return data
    except Exception:
        pass
    return {
        "main_menu": [
            {"id": "home", "label": "Home", "short_label": "Home", "url": "index.html", "target": "_self", "icon": "home", "enabled": True, "active_pages": ["home"], "has_dropdown": False, "dropdown_items": []},
            {"id": "publications", "label": "Research & Pubs", "short_label": "Research", "url": "publications.html", "target": "_self", "icon": "none", "enabled": True, "active_pages": ["publications", "team"], "has_dropdown": True, "dropdown_items": [
                {"id": "team", "label": "Research Team", "url": "research-team.html", "target": "_self", "icon": "✦", "enabled": True, "active_pages": ["team"]}
            ]},
            {"id": "research", "label": "Activity & Project", "short_label": "Activity", "url": "research.html", "target": "_self", "icon": "none", "enabled": True, "active_pages": ["research", "articles"], "has_dropdown": False, "dropdown_items": []},
            {"id": "talks", "label": "Media & Talks", "short_label": "Media", "url": "talks.html", "target": "_self", "icon": "none", "enabled": True, "active_pages": ["talks"], "has_dropdown": False, "dropdown_items": []},
            {"id": "cv", "label": "Achievement & CV", "short_label": "CV", "url": "cv.html", "target": "_self", "icon": "none", "enabled": True, "active_pages": ["cv", "achievements"], "has_dropdown": False, "dropdown_items": []}
        ]
    }

def render_subpage_nav(active_page="home"):
    nav_data = get_navigation_data()
    items = nav_data.get("main_menu", [])
    html_items = []
    for item in items:
        if not item.get("enabled", True):
            continue
        item_id = item.get("id", "")
        url = item.get("url", "#")
        label = item.get("label", "")
        target = item.get("target", "_self")
        target_attr = f' target="{target}"' if target and target != "_self" else ""
        icon = item.get("icon", "none")
        active_pages = item.get("active_pages", [item_id])
        
        is_active = (active_page in active_pages) or (active_page == item_id)
        
        if icon == "home" or item_id == "home":
            active_class = "active" if is_active else ""
            html_items.append(f'''<a href="{url}" class="main-menu-link {active_class}" title="{label}" aria-label="{label}"{target_attr}>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px;" aria-hidden="true">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
            </a>''')
            continue
            
        dropdown_items = [d for d in item.get("dropdown_items", []) if d.get("enabled", True)]
        if item.get("has_dropdown", False) and dropdown_items:
            for d in dropdown_items:
                if active_page in d.get("active_pages", [d.get("id")]):
                    is_active = True
                    break
            active_class = "active" if is_active else ""
            sub_links = []
            for d in dropdown_items:
                d_url = d.get("url", "#")
                d_label = d.get("label", "")
                d_target = d.get("target", "_self")
                d_target_attr = f' target="{d_target}"' if d_target and d_target != "_self" else ""
                d_active = "active" if active_page in d.get("active_pages", [d.get("id")]) else ""
                sparkle = f'<span class="nav-team-sparkle">{d.get("icon", "✦")}</span>' if d.get("icon") else ''
                sub_links.append(f'''<a href="{d_url}" class="nav-dropdown-team-link {d_active}" role="menuitem" title="{d_label}"{d_target_attr}>
                  <div class="nav-team-label-wrap">
                    {sparkle}
                    <span class="nav-team-label">{d_label}</span>
                  </div>
                  <span class="nav-team-arrow">&nearr;</span>
                </a>''')
            rendered_sub = "\n                ".join(sub_links)
            html_items.append(f'''<div class="nav-dropdown-item">
              <a href="{url}" class="main-menu-link {active_class}" aria-haspopup="true" aria-expanded="false" title="{label}"{target_attr}>
                {label} <span class="nav-chevron">▾</span>
              </a>
              <div class="nav-dropdown-menu" role="menu">
                {rendered_sub}
              </div>
            </div>''')
        else:
            active_class = "active" if is_active else ""
            html_items.append(f'''<a href="{url}" class="main-menu-link {active_class}" title="{label}"{target_attr}>{label}</a>''')
            
    rendered_menu = "\n            ".join(html_items)
    return f'''<nav class="top-epigraph-menu" id="top-main-nav" aria-label="Main Navigation">
            {rendered_menu}
          </nav>'''

def render_homepage_nav():
    nav_data = get_navigation_data()
    items = nav_data.get("main_menu", [])
    html_items = []
    for item in items:
        if not item.get("enabled", True):
            continue
        item_id = item.get("id", "")
        url = item.get("url", "#")
        label = item.get("label", "")
        short_label = item.get("short_label") or label
        target = item.get("target", "_self")
        target_attr = f' target="{target}"' if target and target != "_self" else ""
        icon = item.get("icon", "none")
        
        if icon == "home" or item_id == "home":
            html_items.append(f'''<a href="{url}" class="ref-menu-tab tab-home active" title="{label}" aria-label="{label}"{target_attr}>
            <svg class="tab-icon-home" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </a>''')
            continue
            
        dropdown_items = [d for d in item.get("dropdown_items", []) if d.get("enabled", True)]
        if item.get("has_dropdown", False) and dropdown_items:
            sub_links = []
            for d in dropdown_items:
                d_url = d.get("url", "#")
                d_label = d.get("label", "")
                d_target = d.get("target", "_self")
                d_target_attr = f' target="{d_target}"' if d_target and d_target != "_self" else ""
                sparkle = f'<span class="ref-team-sparkle">{d.get("icon", "✦")}</span>' if d.get("icon") else ''
                sub_links.append(f'''<a href="{d_url}" class="ref-dropdown-team-link" role="menuitem" title="{d_label}"{d_target_attr}>
                <div class="ref-team-label-wrap">
                  {sparkle}
                  <span class="ref-team-label">{d_label}</span>
                </div>
                <span class="ref-team-arrow">&nearr;</span>
              </a>''')
            rendered_sub = "\n              ".join(sub_links)
            html_items.append(f'''<div class="ref-menu-dropdown-wrapper">
            <a href="{url}" class="ref-menu-tab" title="{label}" aria-haspopup="true" aria-expanded="false"{target_attr}>
              <span class="tab-txt-full">{label} <span class="ref-chevron">▾</span></span>
              <span class="tab-txt-compact">{short_label} <span class="ref-chevron">▾</span></span>
            </a>
            <div class="ref-menu-dropdown-menu" role="menu">
              {rendered_sub}
            </div>
          </div>''')
        else:
            html_items.append(f'''<a href="{url}" class="ref-menu-tab" title="{label}"{target_attr}>
            <span class="tab-txt-full">{label}</span>
            <span class="tab-txt-compact">{short_label}</span>
          </a>''')
            
    rendered_menu = "\n          ".join(html_items)
    return f'''<nav class="ref-top-menu-bar" aria-label="Main Navigation">
          {rendered_menu}
        </nav>'''

def get_page_header(active_page="home"):
    profile = load_json("profile.json")
    social = profile.get("social_links", {})
    cluster_cfg = profile.get("top_cluster", {})

    items_def = [
        ("scholar", "Google Scholar", social.get("scholar", ""), "scholar"),
        ("orcid", "ORCID", social.get("orcid", ""), "orcid"),
        ("github", "GitHub", social.get("github", ""), "github"),
        ("linkedin", "LinkedIn", social.get("linkedin", ""), "linkedin"),
        ("email", "Institutional Email", social.get("email", ""), "email"),
        ("sciprofiles", "SciProfiles", social.get("sciprofiles", ""), "sciprofiles"),
        ("researchgate", "ResearchGate", social.get("researchgate", ""), "researchgate"),
    ]

    pills_html = []
    for key, def_label, val, icon in items_def:
        cfg = cluster_cfg.get(key, {})
        is_enabled = cfg.get("enabled", True if key in ["scholar", "orcid", "github", "linkedin", "email"] else False)
        if not is_enabled or not val:
            continue
        label = cfg.get("label", def_label)
        if key in ["email", "personal_email"]:
            href = val if val.startswith("mailto:") else f"mailto:{val}"
            target_str = ""
        else:
            href = val
            if not href.startswith("http://") and not href.startswith("https://") and not href.startswith("//"):
                href = f"https://{href}"
            target_str = ' target="_blank" rel="noopener"'
        pills_html.append(f'<a href="{href}"{target_str} class="top-link-pill" title="{label}">{render_svg_icon(icon)} <span>{label}</span></a>')

    scholarly_links_rendered = "\n              ".join(pills_html)
    epigraph_title = profile.get("epigraph", "Das Sein, Das Sollen.")
    star_svg = '''<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" class="david-star-svg">
      <polygon points="12,2 20.66,17 3.34,17" />
      <polygon points="12,22 3.34,7 20.66,7" />
    </svg>'''

    # Option 1 Storm Banner Configuration (CMS Managed & Device Responsive)
    storm_cfg = profile.get("storm_banner", {})
    storm_enabled = storm_cfg.get("enabled", True)
    vis_mode = storm_cfg.get("visibility_mode", "desktop_only")
    hide_mobile = storm_cfg.get("hide_on_mobile", True)
    hide_tablet = storm_cfg.get("hide_on_tablet", True)
    hide_desktop = storm_cfg.get("hide_on_desktop", False)

    vis_classes = []
    if not storm_enabled or vis_mode == "hidden":
        vis_classes.append("storm-banner-disabled")
    elif vis_mode == "desktop_only" or (hide_mobile and hide_tablet and not hide_desktop):
        vis_classes.append("storm-banner-hide-mobile-tablet")
    elif hide_mobile and not hide_tablet and not hide_desktop:
        vis_classes.append("storm-banner-hide-mobile")
    elif hide_desktop and not hide_mobile and not hide_tablet:
        vis_classes.append("storm-banner-hide-desktop")

    media_type = storm_cfg.get("media_type", "image")
    img_url = storm_cfg.get("image_url", "assets/images/lighthouse-banner.webp")
    img_fallback = storm_cfg.get("image_fallback", "assets/images/lighthouse-banner.jpg")
    img_alt = storm_cfg.get("image_alt", "Lighthouse Storm over Ocean")
    vid_url = storm_cfg.get("video_url", "")
    vid_poster = storm_cfg.get("video_fallback_poster") or img_url
    vid_auto = "autoplay" if storm_cfg.get("video_autoplay", True) else ""
    vid_loop = "loop" if storm_cfg.get("video_loop", True) else ""
    vid_muted = "muted" if storm_cfg.get("video_muted", True) else ""

    if media_type == "video" and vid_url:
        media_html = f'''<video class="lighthouse-bg-video" {vid_auto} {vid_loop} {vid_muted} playsinline poster="{vid_poster}">
        <source src="{vid_url}" type="video/mp4">
        <picture>
          <source srcset="{img_url}" type="image/webp">
          <img src="{img_fallback}" class="lighthouse-bg-img" alt="{img_alt}" width="2048" height="790">
        </picture>
      </video>'''
    else:
        media_html = f'''<picture>
        <source srcset="{img_url}" type="image/webp">
        <img src="{img_fallback}" class="lighthouse-bg-img" alt="{img_alt}" width="2048" height="790">
      </picture>'''

    rain_canvas_html = '<canvas id="rain-canvas"></canvas>' if storm_cfg.get("enable_rain_effect", True) else ''

    quote_html = ''
    if storm_cfg.get("show_quote", True):
        q_text = storm_cfg.get("quote_text", "If all the trees on earth were pens and the ocean were ink, refilled by seven other oceans, the Words of Allah would not be exhausted. Surely Allah is Almighty, All-Wise.")
        q_cite = storm_cfg.get("quote_cite", "Qur’an 31:27")
        quote_html = f'''<div class="storm-quote-overlay">
        <p class="storm-quote-text font-serif">
          &ldquo;{q_text}&rdquo;
        </p>
        <cite class="storm-quote-cite font-cinzel">
          <span class="storm-cite-line"></span>
          <span class="storm-cite-label">{q_cite}</span>
        </cite>
      </div>'''

    storm_banner_rendered = f'''<!-- 2. Clean, Unobstructed Lighthouse Storm Banner (Option 1 Storm - CMS Managed) -->
    <section class="lighthouse-banner-frame {' '.join(vis_classes)}" data-visibility="{vis_mode}">
      {media_html}
      {rain_canvas_html}
      {quote_html}
    </section>'''

    return f"""
  <div class="site-wrapper">
    
    <!-- 1. Top Epigraph: Das Sein, Das Sollen & Top-Right Star of David with Side Links -->
    <header class="epigraph-header">
      <div class="epigraph-top-flex">
        <div class="epigraph-title-group">
          <h1 class="epigraph-title">{epigraph_title}</h1>
          <div class="epigraph-golden-line" aria-hidden="true"></div>
        </div>
        
        <div class="epigraph-right-cluster">
          {render_subpage_nav(active_page) if active_page != 'home' else ''}

          <!-- Top-Right Sacred Blooming Lotus Aerial Palace Button & Side-Expanding Scholarly Profiles -->
          <div class="top-scholarly-cluster" id="top-scholarly-cluster">
            <div class="top-scholarly-links" id="top-scholarly-links" aria-hidden="true">
              {scholarly_links_rendered}
            </div>

            <!-- Sacred Multi-Tiered Glowing Lotus Aerial Palace Button -->
            <button class="lotus-palace-btn david-star-pure-btn" id="lotus-toggle-btn" aria-label="Toggle Scholarly Profiles & Direct Identifiers" title="Scholarly Profiles & Direct Identifiers (Sacred Lotus)" aria-expanded="false">
              {render_lotus_symbol_svg()}
            </button>
          </div>
        </div>

      </div>
    </header>

    {storm_banner_rendered}

    <!-- Featured Content Player Audio (Atmospheric Soundtrack - Soft Transparent Second-Gaze) -->
    <div class="royal-vanish-container" id="royal-audio-container">
      <div class="royal-aura-popup">
        <div class="royal-title">Test Driving Toothless</div>
        <div class="royal-subtitle">John Powell</div>
        <div class="royal-crown-tip"></div>
      </div>

      <div class="royal-custom-player">
        <button class="royal-play-btn" id="royal-play-btn" aria-label="Play/Pause soundtrack" type="button">
          <svg class="play-icon" width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
          <svg class="pause-icon" width="13" height="13" viewBox="0 0 24 24" fill="currentColor" style="display:none;"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
        </button>

        <span class="royal-time-display" id="royal-time-display">0:00 / 3:03</span>

        <div class="royal-progress-wrap" id="royal-progress-wrap" role="slider" aria-label="Seek time" tabindex="0">
          <div class="royal-progress-bar" id="royal-progress-bar">
            <div class="royal-progress-fill" id="royal-progress-fill"></div>
            <div class="royal-progress-thumb" id="royal-progress-thumb"></div>
          </div>
        </div>

        <button class="royal-mute-btn" id="royal-mute-btn" aria-label="Mute/Unmute" type="button">
          <svg class="volume-high" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
          <svg class="volume-muted" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none;"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line></svg>
        </button>
      </div>

      <audio id="soundtrack-audio" preload="none">
        <source src="https://zaeedh.github.io/blog-zaidamin/Test%20Driving%20Toothless%20(from%20How%20to%20Train%20Your%20Dragon).mp3" type="audio/mpeg"/>
        Your browser does not support the audio element.
      </audio>
    </div>

"""


# ==============================================================================
# VISITOR STATISTICS & GLOBAL READERSHIP TELEMETRY (GOLDEN RATIO)
# ==============================================================================
def get_flag_svg(country_code):
    if country_code == 'MY':
        return """<svg class="stats-flag-icon" width="18" height="12" viewBox="0 0 18 12" fill="none" xmlns="http://www.w3.org/2000/svg">
          <clipPath id="my-clip"><rect width="18" height="12" rx="2"/></clipPath>
          <g clip-path="url(#my-clip)">
            <rect width="18" height="12" fill="#CC0000"/>
            <rect y="1.71" width="18" height="0.86" fill="#FFFFFF"/>
            <rect y="3.43" width="18" height="0.86" fill="#FFFFFF"/>
            <rect y="5.14" width="18" height="0.86" fill="#FFFFFF"/>
            <rect y="6.86" width="18" height="0.86" fill="#FFFFFF"/>
            <rect y="8.57" width="18" height="0.86" fill="#FFFFFF"/>
            <rect y="10.29" width="18" height="0.86" fill="#FFFFFF"/>
            <rect width="9" height="6.86" fill="#000066"/>
            <circle cx="4.2" cy="3.43" r="2.2" fill="#FFCC00"/>
            <circle cx="4.8" cy="3.43" r="1.8" fill="#000066"/>
            <polygon points="6.2,3.43 5.5,3.8 5.8,3.1 5.2,3.0 5.7,2.6 5.3,2.0 5.9,2.3 6.1,1.6 6.4,2.3 7.0,2.0 6.6,2.6 7.1,3.0 6.5,3.1 6.8,3.8" fill="#FFCC00"/>
          </g>
        </svg>"""
    elif country_code == 'US':
        return """<svg class="stats-flag-icon" width="18" height="12" viewBox="0 0 18 12" fill="none" xmlns="http://www.w3.org/2000/svg">
          <clipPath id="us-clip"><rect width="18" height="12" rx="2"/></clipPath>
          <g clip-path="url(#us-clip)">
            <rect width="18" height="12" fill="#B22234"/>
            <rect y="1.85" width="18" height="0.92" fill="#FFFFFF"/>
            <rect y="3.69" width="18" height="0.92" fill="#FFFFFF"/>
            <rect y="5.54" width="18" height="0.92" fill="#FFFFFF"/>
            <rect y="7.38" width="18" height="0.92" fill="#FFFFFF"/>
            <rect y="9.23" width="18" height="0.92" fill="#FFFFFF"/>
            <rect y="11.08" width="18" height="0.92" fill="#FFFFFF"/>
            <rect width="7.5" height="6.46" fill="#3C3B6E"/>
            <circle cx="2" cy="1.6" r="0.5" fill="#FFFFFF"/>
            <circle cx="3.8" cy="1.6" r="0.5" fill="#FFFFFF"/>
            <circle cx="5.6" cy="1.6" r="0.5" fill="#FFFFFF"/>
            <circle cx="2.9" cy="3.2" r="0.5" fill="#FFFFFF"/>
            <circle cx="4.7" cy="3.2" r="0.5" fill="#FFFFFF"/>
            <circle cx="2" cy="4.8" r="0.5" fill="#FFFFFF"/>
            <circle cx="3.8" cy="4.8" r="0.5" fill="#FFFFFF"/>
            <circle cx="5.6" cy="4.8" r="0.5" fill="#FFFFFF"/>
          </g>
        </svg>"""
    elif country_code == 'GB':
        return """<svg class="stats-flag-icon" width="18" height="12" viewBox="0 0 18 12" fill="none" xmlns="http://www.w3.org/2000/svg">
          <clipPath id="gb-clip"><rect width="18" height="12" rx="2"/></clipPath>
          <g clip-path="url(#gb-clip)">
            <rect width="18" height="12" fill="#012169"/>
            <path d="M0,0 L18,12 M18,0 L0,12" stroke="#FFFFFF" stroke-width="2.4"/>
            <path d="M0,0 L18,12 M18,0 L0,12" stroke="#C8102E" stroke-width="1.2"/>
            <path d="M9,0 V12 M0,6 H18" stroke="#FFFFFF" stroke-width="3.6"/>
            <path d="M9,0 V12 M0,6 H18" stroke="#C8102E" stroke-width="2"/>
          </g>
        </svg>"""
    elif country_code == 'SG':
        return """<svg class="stats-flag-icon" width="18" height="12" viewBox="0 0 18 12" fill="none" xmlns="http://www.w3.org/2000/svg">
          <clipPath id="sg-clip"><rect width="18" height="12" rx="2"/></clipPath>
          <g clip-path="url(#sg-clip)">
            <rect width="18" height="6" fill="#ED2939"/>
            <rect y="6" width="18" height="6" fill="#FFFFFF"/>
            <circle cx="3.8" cy="3" r="1.8" fill="#FFFFFF"/>
            <circle cx="4.4" cy="3" r="1.5" fill="#ED2939"/>
            <circle cx="5.8" cy="2.2" r="0.3" fill="#FFFFFF"/>
            <circle cx="6.4" cy="2.7" r="0.3" fill="#FFFFFF"/>
            <circle cx="6.4" cy="3.5" r="0.3" fill="#FFFFFF"/>
            <circle cx="5.8" cy="4" r="0.3" fill="#FFFFFF"/>
            <circle cx="5.3" cy="3.1" r="0.3" fill="#FFFFFF"/>
          </g>
        </svg>"""
    elif country_code == 'AU':
        return """<svg class="stats-flag-icon" width="18" height="12" viewBox="0 0 18 12" fill="none" xmlns="http://www.w3.org/2000/svg">
          <clipPath id="au-clip"><rect width="18" height="12" rx="2"/></clipPath>
          <g clip-path="url(#au-clip)">
            <rect width="18" height="12" fill="#00008B"/>
            <rect width="9" height="6" fill="#012169"/>
            <path d="M0,0 L9,6 M9,0 L0,6" stroke="#FFFFFF" stroke-width="1.2"/>
            <path d="M4.5,0 V6 M0,3 H9" stroke="#FFFFFF" stroke-width="1.8"/>
            <path d="M4.5,0 V6 M0,3 H9" stroke="#C8102E" stroke-width="1.0"/>
            <circle cx="4.5" cy="9" r="1.1" fill="#FFFFFF"/>
            <circle cx="13.5" cy="2.5" r="0.6" fill="#FFFFFF"/>
            <circle cx="15.2" cy="4.5" r="0.6" fill="#FFFFFF"/>
            <circle cx="13.5" cy="8.5" r="0.6" fill="#FFFFFF"/>
            <circle cx="11.8" cy="5.5" r="0.6" fill="#FFFFFF"/>
          </g>
        </svg>"""
    elif country_code == 'DE':
        return """<svg class="stats-flag-icon" width="18" height="12" viewBox="0 0 18 12" fill="none" xmlns="http://www.w3.org/2000/svg">
          <clipPath id="de-clip"><rect width="18" height="12" rx="2"/></clipPath>
          <g clip-path="url(#de-clip)">
            <rect width="18" height="4" fill="#000000"/>
            <rect y="4" width="18" height="4" fill="#DD0000"/>
            <rect y="8" width="18" height="4" fill="#FFCC00"/>
          </g>
        </svg>"""
    else:
        return """<svg class="stats-flag-icon" width="18" height="12" viewBox="0 0 18 12" fill="none" xmlns="http://www.w3.org/2000/svg">
          <clipPath id="globe-clip"><rect width="18" height="12" rx="2"/></clipPath>
          <g clip-path="url(#globe-clip)">
            <rect width="18" height="12" fill="#0f2744"/>
            <circle cx="9" cy="6" r="4.5" stroke="#38bdf8" stroke-width="0.8" fill="none"/>
            <ellipse cx="9" cy="6" rx="2.2" ry="4.5" stroke="#38bdf8" stroke-width="0.7" fill="none"/>
            <line x1="4.5" y1="6" x2="13.5" y2="6" stroke="#38bdf8" stroke-width="0.7"/>
          </g>
        </svg>"""

def get_visitor_stats_html():
    analytics_cfg = {}
    analytics_file = DATA_DIR / "analytics.json"
    if analytics_file.exists():
        try:
            analytics_cfg = load_json("analytics.json")
        except Exception:
            analytics_cfg = {}

    base_counts = analytics_cfg.get("base_counts", {
        "MY": 16824,
        "US": 10340,
        "GB": 6112,
        "SG": 4628,
        "AU": 3514,
        "DE": 2496,
        "OTHER": 4560
    })
    ga_id = analytics_cfg.get("ga_measurement_id", "G-ZAIDAMIN01")

    total_visits = sum(base_counts.values())
    total_str = f"{(total_visits / 1000):.1f}K"

    countries = [
        {"code": "MY", "name": "Malaysia", "count": base_counts.get("MY", 16824), "color": "#38bdf8"},
        {"code": "US", "name": "United States", "count": base_counts.get("US", 10340), "color": "#fbbf24"},
        {"code": "GB", "name": "United Kingdom", "count": base_counts.get("GB", 6112), "color": "#818cf8"},
        {"code": "SG", "name": "Singapore", "count": base_counts.get("SG", 4628), "color": "#34d399"},
        {"code": "AU", "name": "Australia", "count": base_counts.get("AU", 3514), "color": "#f472b6"},
        {"code": "DE", "name": "Germany", "count": base_counts.get("DE", 2496), "color": "#a78bfa"},
        {"code": "OTHER", "name": "78+ Nations", "full_name": "78+ Other Nations", "count": base_counts.get("OTHER", 4560), "color": "#94a3b8"}
    ]

    country_capsules_html = ""
    for c in countries:
        pct = round((c["count"] / total_visits) * 100, 1)
        count_k = f"{(c['count'] / 1000):.1f}K"
        flag = get_flag_svg(c["code"])
        display_name = c["name"]
        full_name = c.get("full_name", display_name)
        country_capsules_html += f'''
          <div class="stats-country-item" data-country-code="{c['code']}" title="{full_name}: {pct}% of total academic traffic ({count_k} visits)">
            <span class="stats-origin-badge font-cinzel" data-live-badge="{c['code']}" style="display: none;">✦ YOU</span>
            <div class="stats-country-top">
              <span class="stats-dot" style="background: {c['color']}; box-shadow: 0 0 6px {c['color']}88;"></span>
              {flag}
              <span class="stats-country-name">{display_name}</span>
            </div>
            <div class="stats-country-bottom">
              <span class="stats-country-pct font-mono" data-stat-pct="{c['code']}">{pct}%</span>
              <span class="stats-country-count font-mono" data-stat-count="{c['code']}" data-raw-count="{c['count']}">{count_k}</span>
            </div>
          </div>'''

    return f'''
    <!-- Visitor Statistics & Global Academic Readership (Option 1 & 2 Golden Ratio Telemetry) -->
    <section class="golden-visitor-stats" aria-label="Global Visitor Statistics &amp; Academic Readership">
      <div class="stats-header-row">
        <div class="stats-live-badge" id="stats-live-badge-telemetry">
          <span class="stats-pulse-ring"></span>
          <span class="stats-pulse-dot"></span>
          <span class="stats-live-label">Live Readership Telemetry &bull; <strong id="telemetry-live-readout" class="font-cinzel">{total_str} Visits</strong></span>
        </div>

        <div class="stats-meta-cluster font-cinzel">
          <span class="stats-pill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 2008 &ndash; 2026 Archive</span>
        </div>
      </div>

      <!-- Horizontal Grid of Origin Countries -->
      <div class="stats-countries-horizontal-list">
        {country_capsules_html}
      </div>

    </section>
'''

def get_telemetry_audit_modal_html(ga_id="G-ZAIDAMIN01"):
    return f"""      <!-- Real-Time Telemetry & GA4 Audit Modal (Option 1 & Option 2 Inspection) -->
      <div class="telemetry-audit-modal" id="telemetry-audit-modal" style="display: none;" role="dialog" aria-modal="true" aria-labelledby="audit-modal-title">
        <div class="audit-modal-backdrop"></div>
        <div class="audit-modal-content">
          <div class="audit-modal-header">
            <div class="audit-modal-title-group">
              <span class="audit-gem font-cinzel">&#10022;</span>
              <h3 id="audit-modal-title" class="font-cinzel">Academic Readership Telemetry &amp; Analytics Audit</h3>
            </div>
            <button type="button" class="audit-modal-close" aria-label="Close Audit Modal">&times;</button>
          </div>

          <div class="audit-modal-body">
            <!-- Active Session Telemetry Card -->
            <div class="audit-section-box">
              <div class="audit-section-head font-cinzel">
                <span class="audit-pulse-dot"></span>
                <span>Real-Time Visitor Detection (Option 1)</span>
              </div>
              <div class="audit-grid-row">
                <div class="audit-data-cell">
                  <span class="audit-label">Detected Visitor Origin:</span>
                  <strong class="audit-val" id="audit-detected-country">Detecting via Cloudflare Edge CDN...</strong>
                </div>
                <div class="audit-data-cell">
                  <span class="audit-label">Detection Method:</span>
                  <span class="audit-val">Cloudflare CDN Edge Trace (<code class="audit-code">/cdn-cgi/trace</code>) + GeoIP</span>
                </div>
                <div class="audit-data-cell">
                  <span class="audit-label">Session State:</span>
                  <span class="audit-val" id="audit-session-status">Active Session Verified</span>
                </div>
                <div class="audit-data-cell">
                  <span class="audit-label">Local Hits Logged:</span>
                  <span class="audit-val" id="audit-local-hits">Syncing...</span>
                </div>
              </div>
            </div>

            <!-- Google Analytics 4 Card -->
            <div class="audit-section-box">
              <div class="audit-section-head font-cinzel">
                <span class="audit-google-icon">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9v-2h2v2zm0-4H9V7h2v5zm4 4h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
                </span>
                <span>Google Analytics 4 Status (Option 2)</span>
              </div>
              <div class="audit-grid-row">
                <div class="audit-data-cell">
                  <span class="audit-label">Measurement ID:</span>
                  <strong class="audit-val audit-gold font-cinzel">{ga_id}</strong>
                </div>
                <div class="audit-data-cell">
                  <span class="audit-label">Tracking Engine:</span>
                  <span class="audit-val">Official Google Tag Manager (<code class="audit-code">gtag.js</code>)</span>
                </div>
                <div class="audit-data-cell">
                  <span class="audit-label">Realtime Dispatch:</span>
                  <span class="audit-val audit-green">&#10003; Active &bull; IP Anonymized</span>
                </div>
                <div class="audit-data-cell">
                  <span class="audit-label">Audit &amp; Reporting:</span>
                  <span class="audit-val">Google Analytics Web &amp; Mobile Dashboard</span>
                </div>
              </div>
            </div>

            <!-- Readership Country Breakdown Table -->
            <div class="audit-table-wrap">
              <div class="audit-section-head font-cinzel">
                <span>Aggregated Academic Readership Baseline (2008 &ndash; 2026 Archive)</span>
              </div>
              <table class="audit-table font-cinzel">
                <thead>
                  <tr>
                    <th>Nation</th>
                    <th>Archive Base</th>
                    <th>Live Hit</th>
                    <th>Total</th>
                    <th>Share</th>
                  </tr>
                </thead>
                <tbody id="audit-table-body">
                  <!-- Dynamically populated by main.js -->
                </tbody>
              </table>
            </div>
          </div>

          <div class="audit-modal-footer">
            <span class="audit-footer-note">All telemetry is privacy-preserving with zero cross-site trackers or cookies.</span>
            <button type="button" class="spotlight-btn btn-gold font-cinzel audit-modal-close">Close Audit Panel</button>
          </div>
        </div>
      </div>
"""



def get_page_footer(show_visitor_stats=False):
    stats_html = get_visitor_stats_html() if show_visitor_stats else ""
    return f"""
    <!-- Visitor Statistics Section (Exclusive to Homepage) -->
    {stats_html}

    <!-- Footer Divider Line (Above Footer Section) -->
    <hr class="golden-footer-divider">

    <!-- Site Footer (Restored Clean Center Alignment) -->
    <footer class="golden-footer">
      Copyright &copy; 2008 - 2026 Zaid Amin. All Rights Reserved.
    </footer>

    <!-- Floating Scroll to Top Direct Button -->
    <button class="scroll-to-top-btn" id="scroll-to-top" aria-label="Scroll directly to top" title="Scroll to Top" type="button">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
      </svg>
    </button>

  </div>


  <script src="assets/js/rain-lighting.js"></script>
  <script src="assets/js/main.js?v=4.1"></script>
</body>
</html>
"""

# ==============================================================================
# 1. GOLDEN RATIO STANDARD COMPOSITION HOMEPAGE (index.html)
# ==============================================================================
def get_spotlight_card_html():
    spotlight_file = DATA_DIR / "spotlight.json"
    spotlight_cfg = {}
    if spotlight_file.exists():
        try:
            spotlight_cfg = load_json("spotlight.json")
        except Exception:
            spotlight_cfg = {}

    source = spotlight_cfg.get("source", "")
    item = None

    articles = load_json("articles.json") if (DATA_DIR / "articles.json").exists() else []
    pubs = load_json("publications.json") if (DATA_DIR / "publications.json").exists() else []
    talks_d = load_json("talks.json") if (DATA_DIR / "talks.json").exists() else {}
    talks = talks_d.get("talks", []) if isinstance(talks_d, dict) else talks_d
    cv = load_json("cv_data.json") if (DATA_DIR / "cv_data.json").exists() else {}
    achievements = cv.get("achievements_and_grants", [])

    # 1. Resolve explicitly configured item from spotlight.json
    if source == "article":
        item = next((a for a in articles if a.get("id") == spotlight_cfg.get("id") or a.get("title") == spotlight_cfg.get("title")), None)
    elif source == "talk":
        item = next((t for t in talks if t.get("title") == spotlight_cfg.get("id") or t.get("title") == spotlight_cfg.get("title")), None)
    elif source == "cv":
        item = next((a for a in achievements if a.get("title") == spotlight_cfg.get("id") or a.get("title") == spotlight_cfg.get("title")), None)
    elif source == "publication":
        item = next((p for p in pubs if p.get("id") == spotlight_cfg.get("id") or p.get("title") == spotlight_cfg.get("title")), None)

    # 2. Dynamic Fallback: Check if any item holds the active 'featured' flag
    if not item:
        featured_art = next((a for a in articles if a.get("featured")), None)
        featured_pub = next((p for p in pubs if p.get("featured")), None)
        featured_talk = next((t for t in talks if t.get("featured")), None)
        featured_cv = next((a for a in achievements if a.get("featured")), None)

        if source == "article" and featured_art:
            item = featured_art
        elif source == "talk" and featured_talk:
            item = featured_talk
        elif source == "cv" and featured_cv:
            item = featured_cv
        elif source == "publication" and featured_pub:
            item = featured_pub
        elif featured_art:
            item = featured_art
            source = "article"
        elif featured_talk:
            item = featured_talk
            source = "talk"
        elif featured_cv:
            item = featured_cv
            source = "cv"
        elif featured_pub:
            item = featured_pub
            source = "publication"
        else:
            item = pubs[0] if pubs else {}
            source = "publication"

    # 3. Format Card metadata according to category
    if source == "article":
        title = item.get("title", "HARMONY: Human-Trusted AI Framework")
        cat_name = item.get("category", "AI & Cybernetics")
        venue = cat_name
        read_time = item.get("reading_time", "5 min read")
        date_str = item.get("date", "2026")
        year_str = f"{date_str} &bull; {read_time}"
        url = f"article.html?id={item.get('id', '')}"
        raw_desc = item.get("excerpt", item.get("content", ""))
        img_src = item.get("image", "assets/images/spotlight-smart-cities.jpg")
        kicker_badge = "SPOTLIGHT ARTICLE"
        clean_cat = re.sub(r'^[✦✧★\s\u2726]+', '', str(cat_name)).strip()
        if clean_cat.upper() in ["ESSAYS & PERSPECTIVES", "ESSAYS &AMP; PERSPECTIVES"]:
            top_kicker = "ESSAYS &amp; PERSPECTIVES &bull; SCHOLARLY WRITINGS"
        else:
            top_kicker = f"{clean_cat.upper()} &bull; ESSAYS & PERSPECTIVES"
        btn_text = "Read Full Essay &rarr;"
        target_blank = ""
        author_pre = "Author"
        author_name = "Dr. Zaid Amin"
        oa_badge_text = "Open Access Essay"
        meta_characteristic = '<span class="spotlight-gem">✦</span> ESSAYS &amp; PERSPECTIVES'
        meta_detail = "80+ Scholarly Articles Archive &nearr;"
        meta_tooltip = "Explore All Activity &amp; Articles Archive"
        secondary_btn = f'''<a href="/research#articles" class="spotlight-btn-secondary spotlight-btn-meta" title="{meta_tooltip}">
            <div class="spotlight-meta-block">
                <span class="spotlight-meta-kicker font-cinzel">{meta_characteristic}</span>
                <span class="spotlight-meta-val">{meta_detail}</span>
            </div>
        </a>'''
        cap1_icon, cap1_title, cap1_sub = "💡", "THEORETICAL FRAMEWORK", "Cybernetics & AI Ethics"
        cap2_icon, cap2_title, cap2_sub = "📚", "PUBLIC SCHOLARSHIP", "Peer-Reviewed Perspective"

    elif source == "talk":
        title = item.get("title", item.get("event", "Keynote Address"))
        venue = item.get("event", "International Symposium")
        year_val = item.get("year", "2026")
        location = item.get("location", "Kuala Lumpur, Malaysia")
        year_str = f"{year_val} &bull; {location}"
        url = item.get("url") or "talks.html"
        raw_desc = item.get("description", item.get("details", ""))
        img_src = item.get("image", "assets/images/spotlight-smart-cities.jpg")
        role_str = item.get("role", "Keynote Speaker")
        type_str = item.get("type", "Keynote")
        kicker_badge = "SPOTLIGHT KEYNOTE"
        clean_type = re.sub(r'^[✦✧★\s\u2726]+', '', str(type_str)).strip()
        top_kicker = f"{clean_type.upper()} &bull; PUBLIC ENGAGEMENT"
        btn_text = "Watch Keynote / Recording &rarr;" if item.get("url") else "View Keynote &rarr;"
        target_blank = 'target="_blank" rel="noopener"' if item.get("url") else ''
        author_pre = "Speaker"
        author_name = "Dr. Zaid Amin"
        oa_badge_text = role_str
        meta_characteristic = '<span class="spotlight-gem">✦</span> BROADCAST &bull; KEYNOTE'
        meta_detail = "TVRI &amp; Media Archive &nearr;"
        meta_tooltip = "Media &amp; Talks Archive"
        secondary_btn = f'''<a href="/talks" class="spotlight-btn-secondary spotlight-btn-meta" title="{meta_tooltip}">
            <div class="spotlight-meta-block">
                <span class="spotlight-meta-kicker font-cinzel">{meta_characteristic}</span>
                <span class="spotlight-meta-val">{meta_detail}</span>
            </div>
        </a>'''
        cap1_icon, cap1_title, cap1_sub = "🎙️", "KEYNOTE SPEAKER", "International Broadcast"
        cap2_icon, cap2_title, cap2_sub = "📺", "ARCHIVE RECORDING", "Full Talk & Materials"

    elif source == "cv":
        title = item.get("title", "Provincial Honor & Innovator Award")
        venue = item.get("organization", "Provincial Government")
        year_val = item.get("year", "2025")
        category_val = item.get("category", "Government Award")
        year_str = f"{year_val} &bull; {category_val}"
        url = item.get("url") or "/cv#honors"
        raw_desc = item.get("details", "")
        img_src = item.get("image", "assets/images/thumb-projects.jpg")
        badge_val = item.get("badge", "Provincial Honor")
        kicker_badge = "SPOTLIGHT DISTINCTION"
        clean_cat_val = re.sub(r'^[✦✧★\s\u2726]+', '', str(category_val)).strip()
        top_kicker = f"{clean_cat_val.upper()} &bull; RESEARCH EXCELLENCE"
        btn_text = "Inspect Distinction &rarr;"
        target_blank = 'target="_blank" rel="noopener"' if item.get("url") else ''
        author_pre = "Lead PI"
        author_name = "Dr. Zaid Amin"
        oa_badge_text = badge_val
        meta_characteristic = '<span class="spotlight-gem">✦</span> RESEARCH EXCELLENCE'
        meta_detail = "Official Curriculum Vitae &nearr;"
        meta_tooltip = "Honors &amp; Distinctions"
        secondary_btn = f'''<a href="/cv#honors" class="spotlight-btn-secondary spotlight-btn-meta" title="{meta_tooltip}">
            <div class="spotlight-meta-block">
                <span class="spotlight-meta-kicker font-cinzel">{meta_characteristic}</span>
                <span class="spotlight-meta-val">{meta_detail}</span>
            </div>
        </a>'''
        cap1_icon, cap1_title, cap1_sub = "🏆", "DISTINCTION HONOR", "Research Excellence Award"
        cap2_icon, cap2_title, cap2_sub = "🌐", "CIVIC IMPACT", "Government Recognized PI"

    else: # default: publication
        title = item.get("title", "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance")
        venue = item.get("venue", "Smart Cities (MDPI)")
        year_val = item.get("year", 2026)
        year_str = f"Vol. 9 ({year_val})"
        doi = item.get("doi", "10.3390/smartcities9100174")
        url = item.get("url", f"https://doi.org/{doi}" if doi else "#")
        raw_desc = item.get("abstract", "")
        img_src = item.get("image", "assets/images/uploads/spotlight_mdpi.png")
        kicker_badge = "SPOTLIGHT ARTICLE"
        top_kicker = "Q1 SCOPUS INDEXED &bull; PEER-REVIEWED"
        btn_text = "Read Full Article &rarr;"
        target_blank = 'target="_blank" rel="noopener"'
        author_pre = "Lead"
        author_name = "Dr. Zaid Amin"
        oa_badge_text = "Open Access"
        meta_characteristic = '<span class="spotlight-gem">✦</span> SCOPUS Q1 &bull; OPEN ACCESS'
        meta_detail = f"doi: {doi} &nearr;" if doi else "Direct DOI &nearr;"
        meta_tooltip = f"Direct Digital Object Identifier (DOI): {doi}" if doi else "Publication Document"
        secondary_btn = f'''<a href="{url}" target="_blank" rel="noopener" class="spotlight-btn-secondary spotlight-btn-meta" title="{meta_tooltip}">
            <div class="spotlight-meta-block">
                <span class="spotlight-meta-kicker font-cinzel">{meta_characteristic}</span>
                <span class="spotlight-meta-val">{meta_detail}</span>
            </div>
        </a>''' if doi else ''

    # Clean, dignified scholarly narrative (Gestalt unified flow without box clutter)
    finding_match = re.search(r'Key Finding:?\s*</strong>\s*(.*?)(?:</div>|$)', str(raw_desc), re.I)
    key_finding = finding_match.group(1).strip() if finding_match else ''
    lead_match = re.search(r'<p[^>]*class=["\']lead-para["\'][^>]*>(.*?)</p>', str(raw_desc), re.I)
    lead_text = lead_match.group(1).strip() if lead_match else ''

    if lead_text and key_finding:
        kf_clean = key_finding.rstrip('.')
        if kf_clean and kf_clean[0].isupper():
            kf_clean = kf_clean[0].lower() + kf_clean[1:]
        clean_desc = f"{lead_text} Empirical findings demonstrate that {kf_clean}, establishing verifiable auditability for municipal AI deployments."
    else:
        clean = re.sub(r'<[^>]+>', ' ', str(raw_desc or '')).strip()
        clean_desc = ' '.join(clean.split())

    if len(clean_desc) > 340:
        clean_desc = clean_desc[:337].rstrip() + '...'

    webp_cand = img_src.rsplit('.', 1)[0] + '.webp'
    has_webp = (BASE_DIR / webp_cand).exists() and webp_cand != img_src
    source_webp_tag = f'<source srcset="{webp_cand}" type="image/webp">\n            ' if has_webp else ''

    clean_top_kicker = re.sub(r'^[✦✧★\s\u2726]+', '', str(top_kicker)).strip()
    clean_top_kicker = re.sub(r'\bQI\b', 'Q1', clean_top_kicker)

    return f"""
      <!-- LEFT CARD: Clean Golden Ratio Academic Showcase (No Extra Boxes) -->
      <article class="ref-spotlight-card" aria-label="Featured Spotlight {kicker_badge}">
        <div class="ref-spotlight-visual-wrap">
          <picture>
            {source_webp_tag}<img src="{img_src}" alt="{title}" class="ref-spotlight-visual-img" loading="lazy" onerror="this.onerror=null;this.src='assets/images/spotlight-smart-cities.jpg'">
          </picture>
          <div class="ref-visual-overlay"></div>
          
          <div class="ref-spotlight-top-bar">
            <span class="ref-kicker-pill font-cinzel"><span class="pulse-dot"></span> {kicker_badge}</span>
            <div class="ref-top-right-group">
              <span class="ref-bookmark-icon" title="Featured Spotlight {kicker_badge}" aria-label="Featured Spotlight Bookmark">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                </svg>
              </span>
            </div>
          </div>
        </div>

        <div class="ref-spotlight-body">
          <div class="ref-scopus-kicker font-cinzel"><span class="kicker-gem">✦</span> {clean_top_kicker}</div>
          <h2 class="ref-spotlight-title">{title}</h2>

          <div class="ref-spotlight-meta-cluster">
            <span class="spotlight-chip chip-venue font-cinzel">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
              {venue} &bull; {year_val}
            </span>
            <span class="spotlight-chip chip-author">
              <span class="chip-author-dot"></span>
              {author_name} <span class="chip-author-role">({author_pre})</span>
            </span>
            <span class="spotlight-chip chip-oa font-cinzel">
              <span class="chip-oa-check">&#10003;</span> {oa_badge_text}
            </span>
          </div>

          <p class="ref-spotlight-desc">{clean_desc}</p>

          <div class="ref-spotlight-actions">
            <a href="{url}" {target_blank} class="spotlight-btn-gold font-cinzel">
              <span>{btn_text}</span>
            </a>
            {secondary_btn}
          </div>
        </div>
      </article>"""

def get_activity_search_bar_html():
    return '''
        <!-- Advanced Activity & Topic Search Bar (Golden Ratio Proportions) -->
        <div class="ref-search-bar-wrap" id="activity-search-wrap">
          <div class="ref-search-input-box">
            <span class="ref-search-icon" aria-hidden="true">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </span>
            <input type="text" id="activity-search-input" class="ref-search-input font-cinzel" placeholder="Search activities, articles, grants &amp; topics..." autocomplete="off" spellcheck="false" aria-label="Search activities, articles, grants and topics">
            <button type="button" id="activity-search-clear" class="ref-search-clear" title="Clear search" aria-label="Clear search" style="display: none;">
              &times;
            </button>
            <span class="ref-search-shortcut" title="Press / or Ctrl+K to search">
              <kbd>/</kbd>
            </span>
          </div>

          <!-- Live Advanced Search Dropdown Results Panel -->
          <div class="ref-search-results-panel" id="activity-search-results" style="display: none;">
            <div class="search-results-header font-cinzel">
              <span id="search-results-count">0 ACTIVITIES FOUND</span>
              <span class="search-results-esc">ESC TO CLOSE</span>
            </div>
            <div class="search-results-list" id="search-results-list">
              <!-- Dynamically populated by main.js -->
            </div>
          </div>
        </div>'''

def clean_tray_snippet(text, max_len=75):
    t = re.sub(r'<[^>]+>', ' ', str(text or ''))
    t = ' '.join(t.split())
    if len(t) > max_len:
        return t[:max_len].rstrip() + '&hellip;'
    return t or 'Scholarly perspective and insights.'

def get_portals_tray_carousel_html():
    articles = load_json("articles.json") if (DATA_DIR / "articles.json").exists() else []
    pubs = load_json("publications.json") if (DATA_DIR / "publications.json").exists() else []
    media_talks = load_json("media_talks.json") if (DATA_DIR / "media_talks.json").exists() else {}
    fallback_talks_d = load_json("talks.json") if (DATA_DIR / "talks.json").exists() else {}
    fallback_talks = fallback_talks_d.get("talks", []) if isinstance(fallback_talks_d, dict) else fallback_talks_d
    cv_data = load_json("cv_data.json") if (DATA_DIR / "cv_data.json").exists() else {}
    supervision_data = load_json("supervision.json") if (DATA_DIR / "supervision.json").exists() else {}

    # 1. STREAM: Activity & Project (80 Scholarly Articles, Essays, and Frameworks)
    pool_articles = []
    for a in articles:
        thumb = a.get('image') or 'assets/images/spotlight-smart-cities.jpg'
        cat = a.get('category', 'Essays & Perspectives')
        read_time = a.get('reading_time', '3 min read')
        date_str = a.get('date', '2026')
        bullets = [
            f"{clean_tray_snippet(cat, 32)} &bull; {read_time}",
            f"Published: {date_str}"
        ]
        pool_articles.append({
            'type': 'article',
            'menu': 'Activity & Project',
            'tag': cat[:22],
            'title': a.get('title', 'Article'),
            'thumb_jpg': thumb,
            'bullets': bullets,
            'btn_text': 'Read',
            'btn_url': f"article.html?id={a.get('id', '')}",
            'is_external': False
        })

    # 2. STREAM: Research & Publications (24 Peer-Reviewed Works)
    pool_pubs = []
    for p in pubs:
        thumb = p.get('image') or 'assets/images/thumb-research.jpg'
        venue = p.get('venue', 'Journal')
        year = p.get('year', 2026)
        cat = p.get('category') or 'Scopus Q1'
        tag = cat
        if 'journal' in cat.lower() or 'scopus' in str(venue).lower():
            tag = 'Scopus Q1 Journal' if 'q1' in str(p.get('indexing', '')).lower() or 'mdpi' in str(venue).lower() or 'ieee' in str(venue).lower() else 'Journal'
        elif 'conference' in cat.lower():
            tag = 'Conference'
        elif 'chapter' in cat.lower() or 'book' in cat.lower():
            tag = 'Book Chapter'
        elif 'preprint' in cat.lower():
            tag = 'Preprint'

        bullets = [
            f"{clean_tray_snippet(venue, 34)} ({year})",
            f"Authors: {clean_tray_snippet(p.get('authors', 'Dr. Zaid Amin et al.'), 42)}"
        ]
        url = p.get('url') or (f"https://doi.org/{p['doi']}" if p.get('doi') else f"publications.html#{p.get('id', '')}")
        pool_pubs.append({
            'type': 'publication',
            'menu': 'Research & Publication',
            'tag': tag[:22],
            'title': p.get('title', 'Publication'),
            'thumb_jpg': thumb,
            'bullets': bullets,
            'btn_text': 'Explore',
            'btn_url': url,
            'is_external': url.startswith('http')
        })

    # 3. STREAM: Media & Talks (19 Televised Talkshows, Keynotes, Tech Opinions)
    pool_media = []
    # 7 Talkshows
    for ts in media_talks.get('talkshows', []):
        thumb = ts.get('poster') or 'assets/images/thumb-projects.jpg'
        channel = ts.get('channel', 'TV Broadcast')
        duration = ts.get('duration', '30 min')
        bullets = [
            f"{clean_tray_snippet(channel, 30)} &bull; {duration}",
            f"Broadcast: {ts.get('date', 'Archive')}"
        ]
        url = f"talks.html#{ts.get('id', '')}"
        pool_media.append({
            'type': 'talkshow',
            'menu': 'Media & Talks',
            'tag': 'TV Talkshow',
            'title': ts.get('title', 'Broadcast Talkshow'),
            'thumb_jpg': thumb,
            'bullets': bullets,
            'btn_text': 'Watch',
            'btn_url': url,
            'is_external': False
        })
    # 6 Keynotes
    for kn in media_talks.get('keynotes', []):
        thumb = kn.get('image') or 'assets/images/spotlight-smart-cities.jpg'
        event = kn.get('event', 'Keynote Address')
        year = kn.get('year', 2026)
        venue = kn.get('venue', 'International Symposium')
        bullets = [
            f"{clean_tray_snippet(event, 34)} ({year})",
            f"Venue: {clean_tray_snippet(venue, 38)}"
        ]
        url = f"talks.html#{kn.get('id', '')}"
        pool_media.append({
            'type': 'keynote',
            'menu': 'Media & Talks',
            'tag': 'Keynote Speaker',
            'title': kn.get('title', 'Keynote Talk'),
            'thumb_jpg': thumb,
            'bullets': bullets,
            'btn_text': 'View',
            'btn_url': url,
            'is_external': False
        })
    # 6 Tech Opinions
    for op in media_talks.get('opinions', []):
        thumb = op.get('image') or 'assets/images/thumb-attention.jpg'
        pub = op.get('publication', 'Tech Column')
        year = op.get('year', 2025)
        abstract = op.get('abstract', 'Critical discourse on computational systems and ethics.')
        bullets = [
            f"{clean_tray_snippet(pub, 32)} ({year})",
            f"Focus: {clean_tray_snippet(abstract, 38)}"
        ]
        url = f"talks.html#{op.get('id', '')}"
        pool_media.append({
            'type': 'opinion',
            'menu': 'Media & Talks',
            'tag': 'Tech Opinion',
            'title': op.get('title', 'Perspective & Column'),
            'thumb_jpg': thumb,
            'bullets': bullets,
            'btn_text': 'Read',
            'btn_url': url,
            'is_external': False
        })
    # If media_talks empty, use fallback_talks
    if not pool_media and fallback_talks:
        for t in fallback_talks:
            thumb = t.get('image') or 'assets/images/thumb-projects.jpg'
            event = t.get('event', 'Keynote Address')
            year = t.get('year', 2026)
            pool_media.append({
                'type': 'talk',
                'menu': 'Media & Talks',
                'tag': (t.get('role') or 'Keynote Speaker')[:22],
                'title': t.get('title', 'Talk'),
                'thumb_jpg': thumb,
                'bullets': [f"{clean_tray_snippet(event, 34)} ({year})", f"Location: {clean_tray_snippet(t.get('location', 'Malaysia'), 42)}"],
                'btn_text': 'View',
                'btn_url': t.get('url') or 'talks.html',
                'is_external': False
            })

    # 4. STREAM: Achievement & CV (Honors, Awards, Leadership, Book, Editorial, Certifications)
    pool_cv = []
    for a in cv_data.get('achievements_and_grants', []):
        thumb = a.get('image') or 'assets/images/thumb-projects.jpg'
        org = a.get('organization', 'Academic Honor')
        year = a.get('year', 2024)
        cat = a.get('category', 'Award & Grant')
        badge = a.get('badge') or cat
        bullets = [
            f"{clean_tray_snippet(org, 34)} ({year})",
            f"Distinction: {clean_tray_snippet(badge, 38)}"
        ]
        url = a.get('url') or '/cv#honors'
        tag = 'Honor & Award'
        if 'grant' in cat.lower():
            tag = 'Research Grant'
        elif 'global' in badge.lower() or 'cisco' in badge.lower():
            tag = 'Global Award'
        elif 'thesis' in str(a.get('title', '')).lower() or 'ph.d.' in str(a.get('title', '')).lower():
            tag = 'Ph.D. Distinction'

        pool_cv.append({
            'type': 'cv_award',
            'menu': 'Achievement & CV',
            'tag': tag[:22],
            'title': a.get('title', 'Achievement'),
            'thumb_jpg': thumb,
            'bullets': bullets,
            'btn_text': 'Inspect',
            'btn_url': url,
            'is_external': url.startswith('http')
        })

    for l in cv_data.get('academic_leadership', []):
        thumb = 'assets/images/dr-zaid.png'
        inst = l.get('institution', 'INTI International University')
        period = l.get('period', 'Academic Leadership')
        pool_cv.append({
            'type': 'cv_leadership',
            'menu': 'Achievement & CV',
            'tag': 'Academic Leadership',
            'title': l.get('role', 'Leadership Role'),
            'thumb_jpg': thumb,
            'bullets': [f"{clean_tray_snippet(inst, 36)}", f"Tenure: {period}"],
            'btn_text': 'Inspect',
            'btn_url': 'cv.html#leadership',
            'is_external': False
        })

    book = cv_data.get('core_research_and_books', {}).get('book')
    if book:
        pool_cv.append({
            'type': 'cv_book',
            'menu': 'Achievement & CV',
            'tag': 'Authored Book',
            'title': book.get('title', 'Information Sharing Behaviour on Social Media'),
            'thumb_jpg': 'assets/images/thumb-research.jpg',
            'bullets': ['Academic Monograph & Book', 'ISBN / Scholarly Reference Volume'],
            'btn_text': 'Explore',
            'btn_url': 'cv.html#books',
            'is_external': False
        })

    pool_cv.append({
        'type': 'cv_reviewer',
        'menu': 'Achievement & CV',
        'tag': 'Q1 Peer Reviewer',
        'title': 'Active Q1 Peer Reviewer: IEEE Access, PLOS ONE, Elsevier CHB',
        'thumb_jpg': 'assets/images/thumb-attention.jpg',
        'bullets': ['IEEE Access &bull; PLOS ONE &bull; Elsevier CHB', 'Top-Tier Computational & Social Informatics'],
        'btn_text': 'Inspect',
        'btn_url': 'cv.html#peer-review',
        'is_external': False
    })

    for cert in cv_data.get('professional_certifications', []):
        issuer = cert.get('issuer', 'Professional Body')
        period = cert.get('period', 'Certified')
        pool_cv.append({
            'type': 'cv_cert',
            'menu': 'Achievement & CV',
            'tag': 'Certification',
            'title': cert.get('name', 'Professional Certification'),
            'thumb_jpg': 'assets/images/thumb-projects.jpg',
            'bullets': [f"Issuer: {clean_tray_snippet(issuer, 32)}", f"Credential Period: {period}"],
            'btn_text': 'Inspect',
            'btn_url': 'cv.html#certifications',
            'is_external': False
        })

    # 5. STREAM: Supervision (Open Funded Ph.D. & Master's Topics)
    pool_supervision = []
    for top in supervision_data.get('open_topics', []):
        thumb = 'assets/images/thumb-projects.jpg'
        levels = ', '.join(top.get('degree_levels', ['Ph.D.', "Master's"]))
        req = top.get('skills_required', 'Computational Research')
        pool_supervision.append({
            'type': 'supervision',
            'menu': 'Supervision',
            'tag': 'Ph.D. Supervision',
            'title': top.get('title', 'Funded Research Topic'),
            'thumb_jpg': thumb,
            'bullets': [f"Degree Level: {levels} Track", f"Prerequisites: {clean_tray_snippet(req, 36)}"],
            'btn_text': 'Apply',
            'btn_url': f"supervision.html#{top.get('id', '')}",
            'is_external': False
        })

    # Combine CV and Supervision into one balanced Stream of 32 items
    stream_cv_sup = []
    sup_idx = 0
    for i, cv_item in enumerate(pool_cv):
        stream_cv_sup.append(cv_item)
        if (i % 6 == 2 or i % 6 == 5) and sup_idx < len(pool_supervision):
            stream_cv_sup.append(pool_supervision[sup_idx])
            sup_idx += 1
    while sup_idx < len(pool_supervision):
        stream_cv_sup.append(pool_supervision[sup_idx])
        sup_idx += 1

    stream_pubs = pool_pubs
    stream_media = pool_media
    stream_articles = pool_articles

    # Slide 0: Executive Anchor / Showcase Slide across Core Academic Portals
    slide_0 = [
        {
            "thumb_webp": "assets/images/dr-zaid.webp",
            "thumb_jpg": "assets/images/dr-zaid.png",
            "title": "About, Talks &amp; Academic CV",
            "bullets": [
                "Ph.D. in Computer Science (UKM) &bull; Senior Lecturer",
                "Keynote Speaker &bull; Academic Leadership Track"
            ],
            "tag": "UKM Ph.D.",
            "btn_text": "View",
            "btn_url": "/cv",
            "is_external": False
        },
        {
            "thumb_webp": "assets/images/thumb-projects.webp",
            "thumb_jpg": "assets/images/thumb-projects.jpg",
            "title": "Projects &amp; Innovations",
            "bullets": [
                "FRGS Grant: Civic Compliance Framework",
                "Multimodal Orchestration Agent Architecture"
            ],
            "tag": "FRGS / AI",
            "btn_text": "Inspect",
            "btn_url": "/research",
            "is_external": False
        },
        {
            "thumb_webp": "assets/images/thumb-research.webp",
            "thumb_jpg": "assets/images/thumb-research.jpg",
            "title": "Research &amp; Publications",
            "bullets": [
                "24 Peer-Reviewed Articles (MDPI, IEEE, Scopus Q1)",
                "Trustworthy AI &bull; Full Open-Access &amp; BibTeX"
            ],
            "tag": "24 Works",
            "btn_text": "Explore",
            "btn_url": "/publications",
            "is_external": False
        },
        {
            "thumb_webp": "assets/images/thumb-attention.webp",
            "thumb_jpg": "assets/images/thumb-attention.jpg",
            "title": "Attention-Based Decision Systems",
            "bullets": [
                "IEEE Access (2021) &bull; Q1 Scopus Indexed",
                "Visual Attention System for Digital Environments"
            ],
            "tag": "IEEE Access",
            "btn_text": "Read",
            "btn_url": "https://doi.org/10.1109/ACCESS.2021.3087740",
            "is_external": True
        }
    ]

    # Permutation rotation matrix so each slide has a unique layout cadence
    perms = [
        [0, 1, 2, 3],  # Pub, Media, CV/Sup, Article
        [3, 2, 1, 0],  # Article, CV/Sup, Media, Pub
        [1, 0, 3, 2],  # Media, Pub, Article, CV/Sup
        [2, 3, 0, 1],  # CV/Sup, Article, Pub, Media
        [1, 2, 0, 3],  # Media, CV/Sup, Pub, Article
        [3, 0, 2, 1],  # Article, Pub, CV/Sup, Media
        [0, 2, 1, 3],  # Pub, CV/Sup, Media, Article
        [2, 1, 3, 0]   # CV/Sup, Media, Article, Pub
    ]

    num_shuffled_slides = 36
    shuffled_slides = []

    for s in range(num_shuffled_slides):
        c_pub = stream_pubs[s % len(stream_pubs)]
        c_med = stream_media[s % len(stream_media)]
        c_cv = stream_cv_sup[s % len(stream_cv_sup)]
        c_art = stream_articles[s % len(stream_articles)]

        raw_quartet = [c_pub, c_med, c_cv, c_art]
        perm = perms[s % len(perms)]
        shuffled_slides.append([raw_quartet[p] for p in perm])

    slides_data = [slide_0] + shuffled_slides

    slides_html = ""
    total_slides = len(slides_data)
    for s_idx, cards in enumerate(slides_data):
        active_cls = " active" if s_idx == 0 else ""
        cards_html = ""
        for card in cards:
            thumb_jpg = card.get("thumb_jpg") or "assets/images/thumb-research.jpg"
            thumb_webp = card.get("thumb_webp") or ""
            has_webp = thumb_webp and (not thumb_jpg.startswith("http")) and (BASE_DIR / thumb_webp).exists()
            safe_title = html.escape(str(card["title"]), quote=True)

            if has_webp:
                img_html = f'''<picture>
                  <source srcset="{thumb_webp}" type="image/webp">
                  <img src="{thumb_jpg}" alt="{safe_title}" class="ref-item-thumb" width="78" height="56" loading="lazy" onerror="this.onerror=null;this.src='assets/images/thumb-research.jpg';">
                </picture>'''
            else:
                img_html = f'''<img src="{thumb_jpg}" alt="{safe_title}" class="ref-item-thumb" width="78" height="56" loading="lazy" onerror="this.onerror=null;this.src='assets/images/thumb-research.jpg';">'''

            bullets_html = "".join([f"<li>{b}</li>" for b in card["bullets"]])
            ext_attr = ' target="_blank" rel="noopener"' if card.get("is_external") else ""
            clean_tag = re.sub(r'^[✦✧★\s\u2726]+', '', str(card.get("tag", ""))).strip()

            cards_html += f'''
            <div class="ref-item-card">
              <div class="ref-item-thumb-box">
                {img_html}
              </div>
              <div class="ref-item-info">
                <div class="ref-card-kicker-row">
                  <span class="ref-kicker-tag font-cinzel"><span class="kicker-gem">✦</span> {clean_tag}</span>
                </div>
                <h4 class="ref-item-title font-cinzel" title="{safe_title}">{card['title']}</h4>
                <ul class="ref-item-bullets">
                  {bullets_html}
                </ul>
              </div>
              <div class="ref-item-meta-action">
                <a href="{card['btn_url']}"{ext_attr} class="ref-item-btn font-cinzel">{card['btn_text']}</a>
              </div>
            </div>'''

        slides_html += f'''
        <div class="tray-slide{active_cls}" data-slide-index="{s_idx}">
          {cards_html}
        </div>'''

    total_slides_str = f"{total_slides:02d}"

    return f'''
        <!-- Inset Tray containing Stacked Horizontal Cards with Dynamic Looping Carousel -->
        <div class="ref-inset-tray" id="portals-carousel" aria-roledescription="marquee" aria-label="Academic Portals and Articles">
          <!-- Tray Carousel Vertical Slides Container with Physical Translation Track -->
          <div class="tray-slides-wrap">
            <div class="tray-slides-track">
              {slides_html}
            </div>
          </div>

          <!-- Tray Dynamic Looping & Shuffle Navigation Controls Bar -->
          <div class="tray-controls-bar" role="navigation" aria-label="Portals Carousel Pagination">
            <button type="button" class="tray-shuffle-btn" id="tray-shuffle-toggle" title="Toggle Random Shuffle Mode" aria-label="Toggle Random Shuffle Mode">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="16 3 21 3 21 8"></polyline>
                <line x1="4" y1="20" x2="21" y2="3"></line>
                <polyline points="21 16 21 21 16 21"></polyline>
                <line x1="15" y1="15" x2="21" y2="21"></line>
                <line x1="4" y1="4" x2="9" y2="9"></line>
              </svg>
              <span class="tray-shuffle-label">Shuffle</span>
            </button>

            <div class="tray-nav-arrows">
              <button type="button" class="tray-nav-btn tray-arrow-prev" title="Previous Slide (Up)" aria-label="Previous Slide">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="18 15 12 9 6 15"></polyline>
                </svg>
              </button>
              <button type="button" class="tray-nav-btn tray-arrow-next" title="Next Slide (Down)" aria-label="Next Slide">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </button>
            </div>
          </div>
        </div>'''


def get_journal_ticker_html():
    ticker_file = DATA_DIR / "journal_ticker.json"
    ticker_data = {}
    if ticker_file.exists():
        try:
            ticker_data = load_json("journal_ticker.json")
        except Exception:
            ticker_data = {}
    
    if not isinstance(ticker_data, dict):
        ticker_data = {}
        
    section_label = ticker_data.get("section_label", "INDEXED JOURNALS")
    star_glyph = ticker_data.get("star_glyph", "✦")
    items = ticker_data.get("items", [])
    if not isinstance(items, list) or len(items) == 0:
        items = [
            {
                "tag": "Q1 SCOPUS",
                "tag_class": "tag-q1",
                "venue": "Smart Cities (MDPI) • 2026",
                "title": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance",
                "link": "https://doi.org/10.3390/smartcities9100174",
                "enabled": True
            },
            {
                "tag": "Q1 SCOPUS",
                "tag_class": "tag-q1",
                "venue": "IEEE Access • 2021",
                "title": "Attention-Based Design and User Decisions on Information Sharing: Cybernetics Intervention",
                "link": "https://doi.org/10.1109/ACCESS.2021.3087740",
                "enabled": True
            },
            {
                "tag": "SCOPUS INDEXED",
                "tag_class": "tag-scopus",
                "venue": "IJACSA • 2021",
                "title": "Visual Selective Attention System to Intervene User Attention in Digital Environments",
                "link": "https://doi.org/10.14569/IJACSA.2021.0121092",
                "enabled": True
            },
            {
                "tag": "PEER-REVIEWED",
                "tag_class": "tag-peer",
                "venue": "JISTM • 2026",
                "title": "Srivijayapedia: A Digital Platform for Cultural Heritage Preservation of the Srivijaya Civilization",
                "link": "https://doi.org/10.35631/JISTM.1141001",
                "enabled": True
            },
            {
                "tag": "SPRINGER",
                "tag_class": "tag-scopus",
                "venue": "Contributions to Management Science • 2024",
                "title": "Digital Loneliness in Social Media: The Epoch of our Connected and Distraction World",
                "link": "https://doi.org/10.1007/978-3-031-52280-2_14",
                "enabled": True
            },
            {
                "tag": "GOVERNANCE PREPRINT",
                "tag_class": "tag-preprint",
                "venue": "SSRN Series • 2026",
                "title": "The Proxy Trap in Agentic AI: When Metrics Replace Judgment in Autonomous Systems",
                "link": "https://doi.org/10.2139/ssrn.7670124",
                "enabled": True
            }
        ]

    active_items = [it for it in items if it.get("enabled", True)]
    if not active_items:
        active_items = items

    slides_html = ""
    for idx, it in enumerate(active_items):
        active_cls = " active" if idx == 0 else ""
        tag_text = it.get("tag", "JOURNAL")
        tag_cls = it.get("tag_class", "tag-q1")
        venue_text = it.get("venue", "").replace("•", "&bull;")
        title_text = it.get("title", "")
        link_url = it.get("link", "#")
        slides_html += f"""
          <!-- Slide {idx}: {venue_text} -->
          <div class="ticker-slide-item{active_cls}" data-slide="{idx}">
            <span class="ticker-tag {tag_cls} font-cinzel">{tag_text}</span>
            <span class="ticker-venue-name font-cinzel">{venue_text}</span>
            <a href="{link_url}" target="_blank" rel="noopener" class="ticker-title-link">
              {title_text} &nearr;
            </a>
          </div>"""

    return f"""
    <!-- 6. LIST OF JOURNAL: ANIMATE FADE IN FADE OUT MOVE FROM TOP TO DOWN -->
    <section class="journal-ticker-section">
      <div class="journal-ticker-container">
        
        <div class="ticker-label-col font-cinzel">
          <span class="ticker-star-glyph">{star_glyph}</span>
          <span class="ticker-label-text">{section_label}</span>
        </div>

        <div class="ticker-viewport-col" id="journal-ticker-viewport" onmouseenter="pauseJournalTicker()" onmouseleave="resumeJournalTicker()">
          {slides_html}
        </div>

        <div class="ticker-controls-col">
          <div class="ticker-arrows-box">
            <button class="ticker-arrow-btn" onclick="rotateJournalTicker(-1)" title="Previous Journal (Top)" aria-label="Previous Journal">&uarr;</button>
            <button class="ticker-arrow-btn" onclick="rotateJournalTicker(1)" title="Next Journal (Down)" aria-label="Next Journal">&darr;</button>
          </div>
        </div>

      </div>
    </section>
"""


def generate_golden_ratio_home():
    profile = load_json("profile.json")
    publications = load_json("publications.json")

    site_browser_title = get_page_browser_title("home", f"Dr. Zaid Amin | {profile.get('epigraph', 'Das Sein, Das Sollen')} | zaidamin.org")
    html = get_html_head(site_browser_title)
    html += get_page_header("home")

    # Dynamic Portals Header (Configurable via CMS)
    portals_hdr = profile.get("portals_header", {})
    ph_show_photo = portals_hdr.get("show_photo", True)
    ph_name = portals_hdr.get("name", "Dr. Zaid Amin")
    ph_role = portals_hdr.get("role_line", "Senior Lecturer &bull; Faculty of Data Science &amp; IT (FDSIT)").replace("•", "&bull;")
    ph_inst = portals_hdr.get("institution", "INTI International University, Malaysia")
    ph_fields_raw = portals_hdr.get("research_fields", "Digital Ethics • Behavior & Social Computing • HCI")
    import re as _re_bld
    _flist = [f.strip() for f in _re_bld.split(r'•|&bull;|,', ph_fields_raw) if f.strip()]
    ph_fields_html = ' <span class="ref-gold-dot">&bull;</span> '.join(_flist) if _flist else ph_fields_raw
    ph_front_webp = portals_hdr.get("photo_front", "assets/images/portraits/portrait-1.webp")
    ph_front_png = portals_hdr.get("photo_front_fallback", ph_front_webp.replace(".webp", ".png") if ph_front_webp.endswith(".webp") else ph_front_webp)
    ph_front_alt = portals_hdr.get("photo_front_alt", f"{ph_name} — Academic Portrait")
    ph_back_webp = portals_hdr.get("photo_back", "assets/images/portraits/portrait-2.webp")
    ph_back_png = portals_hdr.get("photo_back_fallback", ph_back_webp.replace(".webp", ".png") if ph_back_webp.endswith(".webp") else ph_back_webp)
    ph_back_alt = portals_hdr.get("photo_back_alt", f"{ph_name} — Secondary Portrait")
    ph_status_enabled = portals_hdr.get("status_dot_enabled", True)
    ph_status_text = portals_hdr.get("status_text", "Active Senior Lecturer & Researcher")
    ph_status_html = f'<span class="ref-live-status" title="{ph_status_text}"></span>' if ph_status_enabled else ''

    coin_portrait_html = ""
    if ph_show_photo and (ph_front_webp or ph_front_png):
        if ph_front_webp.endswith(".webp"):
            front_media_html = f"""<picture>
                  <source srcset="{ph_front_webp}" type="image/webp">
                  <img src="{ph_front_png}" alt="{ph_front_alt}" class="ref-photo-img" width="114" height="114">
                </picture>"""
        else:
            front_media_html = f"""<img src="{ph_front_webp}" alt="{ph_front_alt}" class="ref-photo-img" width="114" height="114">"""

        if ph_back_webp.endswith(".webp"):
            back_media_html = f"""<picture>
                  <source srcset="{ph_back_webp}" type="image/webp">
                  <img src="{ph_back_png}" alt="{ph_back_alt}" class="ref-photo-img" width="114" height="114">
                </picture>"""
        else:
            back_media_html = f"""<img src="{ph_back_webp}" alt="{ph_back_alt}" class="ref-photo-img" width="114" height="114">"""

        coin_portrait_html = f"""<div class="ref-photo-ring coin-flip-stage" id="dr-zaid-coin" role="button" tabindex="0" title="{ph_name} • Click to rotate portrait coin">
            <div class="coin-disc" id="coin-disc" aria-label="Interactive Portrait Coin">
              <div class="coin-face coin-face-front" id="coin-face-front">
                {front_media_html}
                <div class="coin-specular-gleam"></div>
              </div>
              <div class="coin-face coin-face-back" id="coin-face-back">
                {back_media_html}
                <div class="coin-specular-gleam"></div>
              </div>
              <div class="coin-rim-highlight"></div>
            </div>
            {ph_status_html}
          </div>"""

    ph_portraits_list = portals_hdr.get("portraits_list", [])
    import json as _json_bld
    coin_portraits_script = f"<script>window.PORTALS_COIN_PORTRAITS = {_json_bld.dumps(ph_portraits_list)};</script>" if ph_portraits_list else ""

    html += get_journal_ticker_html()
    html += f"""
    <!-- 5. FEATURED SPOTLIGHT & ACADEMIC PORTALS (REFERENCE SPLIT CARD LAYOUT) -->
    <section class="golden-split-section ref-split-layout">
      
{get_spotlight_card_html()}

      <!-- RIGHT CARD: Academic Portals & Highlights (Matching Reference Inset Tray + Stacked Cards) -->
      <aside class="ref-portals-card">
        <!-- 1. Top Main Menu Navigation Grid (Placed Above Dr. Zaid Profile, 3x2 Golden Ratio Layout) -->
        {render_homepage_nav()}

        <div class="ref-menu-divider"></div>

        
        <!-- Header with Dr. Zaid Amin Profile Summary & Title (Dynamic from profile.json) -->
        <div class="ref-portals-header">
          <div class="ref-profile-info-col">
            <h3 class="ref-profile-name font-cinzel">{ph_name}</h3>
            <div class="ref-profile-role">
              {ph_role}<br>
              <span class="ref-profile-inst">{ph_inst}</span>
            </div>
            <div class="ref-profile-fields">
              {ph_fields_html}
            </div>
          </div>
          {coin_portrait_html}
          {coin_portraits_script}
        </div>

        {get_activity_search_bar_html()}
        {get_portals_tray_carousel_html()}</aside>

    </section>

    """
    html += get_page_footer(show_visitor_stats=True)
    return html


import re as _re_mod
import html as _html_mod

import re as _re_mod
import html as _html_mod

import re as _re_mod
import html as _html_mod

import re as _re_mod
import html as _html_mod

def render_book_showcase_section(publications, cat, render_svg_icon_fn, render_download_pill_fn, clean_excerpt_fn, html_mod):
    """
    Bokify-Style Premium Book Showcase for Book & Chapters section.
    1. Bokify Hero Stage: Asymmetric Golden Ratio (61.8% text/actions | 38.2% 3D standing books).
    2. Curated Volumes Shelf: 3-column Golden Ratio grid with 3D standing book cards.
    """
    cat_items = [p for p in publications if p.get("category") == cat["category_key"]]
    if not cat_items:
        return ""

    chips_html = "".join([f'<span class="pub-stat-chip">{c}</span>' for c in cat["chips"]])

    def get_publisher(venue, doi, explicit_pub=None):
        if explicit_pub and str(explicit_pub).strip():
            return str(explicit_pub).strip()
        v = venue or ""
        d = doi or ""
        if "Springer" in v or "LNCS" in v or "Computer Science" in v or "Contributions" in v:
            return "Springer Nature"
        if "Atlantis" in v:
            return "Atlantis Press"
        if v and any(kw in v for kw in ("Press", "Publisher", "Publishing")):
            return v
        if "2991" in d:
            return "Atlantis Press"
        if v and len(v) <= 30 and v.lower() not in ("on process", "in preparation", "#"):
            return v
        return "Academic Press"

    def get_series(venue, explicit_series=None):
        if explicit_series and str(explicit_series).strip():
            return str(explicit_series).strip()
        v = venue or ""
        if "Contributions to Management" in v:
            return "Contributions to Management Science"
        if "Lecture Notes in Computer Science" in v or "LNCS" in v:
            return "Lecture Notes in Computer Science (LNCS)"
        if "Atlantis" in v or "Academic" in v:
            return "Atlantis Press Monograph Series"
        return v

    # 1. Front Primary Monograph (Featured Book)
    featured_book = next((b for b in cat_items if b.get("featured")), None)
    if not featured_book:
        for b in cat_items:
            if "digital" in b.get("id", "") or b.get("year") == 2024:
                featured_book = b
                break
    if not featured_book:
        featured_book = cat_items[0]

    featured_img = featured_book.get("image") or "assets/images/books/book_digital_loneliness.webp"
    featured_title = _html_mod.escape(featured_book.get("title", "Primary Monograph"))
    featured_year = featured_book.get("year", 2024)
    featured_venue = featured_book.get("venue", "Academic Publication")
    featured_pub = get_publisher(featured_venue, featured_book.get("doi"), featured_book.get("publisher"))
    primary_url = featured_book.get("url", "").strip() or (f"https://doi.org/{featured_book.get('doi', '').strip()}" if featured_book.get("doi") else "#bokify-volumes-shelf")
    primary_pub_short = featured_pub.split()[0] if featured_pub else "Volume"

    # 2. Rear Companion Book
    rear_book = next((b for b in cat_items if b.get("id") != featured_book.get("id")), None)
    if not rear_book and len(cat_items) > 1:
        rear_book = cat_items[1]

    rear_img = (rear_book.get("image") or "assets/images/books/book_attention_covid.webp") if rear_book else ""
    rear_title = _html_mod.escape(rear_book.get("title", "Scholarly Volume")) if rear_book else ""
    rear_year = rear_book.get("year", 2021) if rear_book else ""
    rear_venue = rear_book.get("venue", "Academic Publication") if rear_book else ""
    rear_pub = get_publisher(rear_venue, rear_book.get("doi"), rear_book.get("publisher")) if rear_book else ""

    # Render each book card in the Curated Shelf
    shelf_cards_html = ""
    for idx, pub in enumerate(cat_items, 1):
        url = pub.get("url", "").strip() if pub.get("url") else ""
        doi = pub.get("doi", "").strip() if pub.get("doi") else ""
        isbn = pub.get("isbn", "").strip() if pub.get("isbn") else ""
        link_enabled = pub.get("link_enabled", True)

        # Check if direct link is active and valid (not disabled, not placeholder '#', not 'on process')
        is_link_active = bool(
            link_enabled is not False
            and url != "#"
            and doi != "#"
            and "on process" not in doi.lower()
            and "on process" not in url.lower()
            and (url or doi)
        )
        if not url and doi and is_link_active:
            url = f"https://doi.org/{doi}"

        venue = pub.get("venue", "Academic Publication")
        series_text = get_series(venue, pub.get("series"))
        publisher = get_publisher(venue, doi, pub.get("publisher"))
        excerpt = clean_excerpt_fn(pub.get("abstract", "") or pub.get("excerpt", ""), max_len=150)
        escaped_title = _html_mod.escape(pub["title"])
        escaped_title_lower = _html_mod.escape(pub["title"].lower())
        escaped_venue = _html_mod.escape(venue)
        escaped_venue_lower = _html_mod.escape(venue.lower())
        year = pub.get("year", "")
        img = pub.get("image", "assets/images/thumb-research.jpg")
        bibtex_id = pub.get("id", f"book{idx}")
        bibtex_raw = pub.get("bibtex", "")
        is_featured = (pub.get("id") == featured_book.get("id"))
        primary_tag = ""  # Removed per user design request

        title_enc = _html_mod.escape(pub.get("title", ""))
        mailto = f"mailto:zaid.amin@newinti.edu.my?subject=Requesting%20Full-Text:%20{title_enc}"

        # Action Button: Download/DOI when link is active, otherwise Available on Request (Lock icon capsule)
        if is_link_active and url:
            label = "Download / DOI"
            if "arxiv.org" in url:
                label = "Download (arXiv)"
            elif "ssrn" in url:
                label = "Download (SSRN)"
            dl_btn = f'<a href="{url}" target="_blank" rel="noopener" class="pub-pill-btn pub-pill-primary">{render_svg_icon_fn("download")} <span>{label}</span></a>'
        else:
            lock_svg = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'
            dl_btn = f'''<a href="{mailto}" class="pub-pill-btn pub-pill-primary pub-pill-request" title="Direct download unavailable. Available on request via institutional inquiry.">
              <span class="pub-pill-lock-icon">{lock_svg}</span>
              <span>Available on Request</span>
            </a>'''

        # DOI / ISBN / External Link row
        doi_val = doi if doi else ("#" if not is_link_active else "")
        if not doi_val and url:
            doi_val = url

        display_doi = doi_val
        if display_doi.startswith("http://") or display_doi.startswith("https://"):
            display_doi = display_doi.replace("https://", "").replace("http://", "").replace("www.", "")
            if len(display_doi) > 28:
                display_doi = display_doi[:26] + "..."

        if is_link_active and doi_val and doi_val != "#":
            if doi_val.startswith("http://") or doi_val.startswith("https://"):
                doi_content = f'<a href="{doi_val}" target="_blank" rel="noopener" class="bokify-doi-link" title="{doi_val}">{display_doi}</a>'
            elif "/" in doi_val:
                doi_content = f'<a href="https://doi.org/{doi_val}" target="_blank" rel="noopener" class="bokify-doi-link" title="DOI: {doi_val}">{doi_val}</a>'
            else:
                doi_content = f'<span class="bokify-doi-val">{doi_val}</span>'
        else:
            doi_content = f'<span class="bokify-doi-val" title="{doi_val}">{display_doi or "#"}</span>'

        doi_html = f'<div class="bokify-card-doi"><span class="bokify-doi-lbl">DOI/ISBN/LINK:</span> {doi_content}</div>'
        isbn_html = f'<div class="bokify-card-doi bokify-card-isbn"><span class="bokify-doi-lbl">ISBN:</span> <span class="bokify-doi-val">{isbn}</span></div>' if isbn else ""

        shelf_cards_html += f"""
        <article class="bokify-shelf-card pub-item" data-category="{cat["category_key"].lower()}" data-title="{escaped_title_lower}" data-venue="{escaped_venue_lower}" data-year="{year}">
          <!-- Top 3D Book Showcase on Card -->
          <div class="bokify-card-stage">
            <div class="bokify-card-3d-scene">
              <div class="bokify-card-book-3d">
                <div class="bokify-card-cover">
                  <img src="{img}" alt="{escaped_title}" class="bokify-card-cover-img" loading="lazy" onerror="this.onerror=null;this.src='assets/images/books/book_digital_loneliness.png'" />
                  <div class="bokify-cover-shine"></div>
                </div>
                <div class="bokify-card-spine">
                  <span class="bokify-spine-micro">{publisher.upper()}</span>
                </div>
                <div class="bokify-card-pages"></div>
                <div class="bokify-card-shadow"></div>
              </div>
            </div>
            <div class="bokify-card-tags">
              <span class="bokify-publisher-chip">{publisher}</span>
              <span class="bokify-year-chip">{year}</span>
            </div>
          </div>

          <!-- Card Content -->
          <div class="bokify-card-body">
            <div class="bokify-card-meta-line">
              <span class="bokify-card-idx">#{idx:02d}</span>
              <span class="bokify-card-dot">•</span>
              <span class="bokify-card-authors">Dr. Zaid Amin et al.</span>
            </div>

            <h4 class="bokify-card-title font-cinzel">{pub["title"]}</h4>
            <div class="bokify-card-series">{series_text}</div>
            <div class="bokify-card-divider"></div>
            {f'<p class="bokify-card-excerpt">{excerpt}</p>' if excerpt else ''}
            <div class="bokify-card-meta-block">
              {doi_html}
              {isbn_html}
            </div>
          </div>

          <!-- Card Actions (Gestalt Proximity) -->
          <div class="bokify-card-actions">
            {dl_btn}
            <button class="pub-pill-btn pub-pill-secondary btn-bibtex-toggle" data-target="bib-{bibtex_id}">
              Cite / BibTeX
            </button>
          </div>

          <!-- BibTeX Drawer -->
          <div class="bibtex-box" id="bib-{bibtex_id}">
            <button class="bibtex-copy-btn" data-target="code-{bibtex_id}">Copy BibTeX</button>
            <code id="code-{bibtex_id}">{bibtex_raw}</code>
          </div>
        </article>
        """

    # Dynamic Wireframe / Forthcoming Slots to complete the Golden Ratio 3-column grid
    pipeline_file = BASE_DIR / "data" / "books_pipeline.json"
    pipeline_items = []
    if pipeline_file.exists():
        try:
            with open(pipeline_file, "r", encoding="utf-8") as pf:
                loaded_pipe = json.load(pf)
                if isinstance(loaded_pipe, list):
                    pipeline_items = loaded_pipe
        except Exception:
            pass

    remainder = len(cat_items) % 3
    needed_slots = (3 - remainder) % 3 if remainder != 0 else 0
    display_slots_count = max(needed_slots, len(pipeline_items))
    if display_slots_count > 0:
        # Round up to multiple of 3 if needed so the grid is always complete
        total_items = len(cat_items) + display_slots_count
        if total_items % 3 != 0:
            display_slots_count += (3 - (total_items % 3))

        for p_idx in range(display_slots_count):
            total_card_idx = len(cat_items) + p_idx + 1
            p_data = pipeline_items[p_idx] if p_idx < len(pipeline_items) else {
                "title": f"Forthcoming Monograph Vol. {total_card_idx:02d}",
                "series": "Monograph in Preparation • Target: Springer Nature",
                "publisher": "Academic Press Pipeline",
                "year": "2026/2027",
                "status": "Manuscript in Editorial Preparation",
                "badge": "✦ Future Slot",
                "image": "",
                "abstract": "Upcoming peer-reviewed scholarly monograph currently in editorial pipeline and peer evaluation.",
                "authors": "Dr. Zaid Amin et al."
            }
            p_title = _html_mod.escape(p_data.get("title", f"Forthcoming Monograph #{total_card_idx:02d}"))
            p_series = _html_mod.escape(p_data.get("series", "Academic Press Pipeline"))
            p_publisher = _html_mod.escape(p_data.get("publisher", "Academic Press Pipeline"))
            p_year = _html_mod.escape(str(p_data.get("year", "2026/2027")))
            p_status = _html_mod.escape(p_data.get("status", "Manuscript in Editorial Preparation"))
            p_badge = _html_mod.escape(p_data.get("badge", "✦ Future Slot"))
            p_abstract = clean_excerpt_fn(p_data.get("abstract", ""), max_len=150)
            p_authors = _html_mod.escape(p_data.get("authors", "Dr. Zaid Amin et al."))
            p_img = p_data.get("image", "").strip() if p_data.get("image") else ""
            p_title_lower = p_title.lower()

            # Short micro status for SVG blueprint (max 22 chars)
            p_micro_status = p_status.upper()
            if len(p_micro_status) > 20:
                if "PREPARATION" in p_micro_status:
                    p_micro_status = "IN PREPARATION"
                elif "PIPELINE" in p_micro_status:
                    p_micro_status = "IN PIPELINE"
                elif "REVIEW" in p_micro_status:
                    p_micro_status = "UNDER REVIEW"
                elif "PRESS" in p_micro_status:
                    p_micro_status = "IN PRESS"
                else:
                    p_micro_status = p_micro_status[:18] + "..."

            # Cover HTML: 3D Image if image provided, else glowing wireframe blueprint SVG
            if p_img:
                cover_html = f"""<div class="bokify-card-cover">
                  <img src="{p_img}" alt="{p_title}" class="bokify-card-cover-img" loading="lazy" onerror="this.onerror=null;this.src='assets/images/books/book_digital_loneliness.png'" />
                  <div class="bokify-cover-shine"></div>
                </div>
                <div class="bokify-card-spine">
                  <span class="bokify-spine-micro">{p_publisher.upper()[:14] if p_publisher else 'PIPELINE'}</span>
                </div>
                <div class="bokify-card-pages"></div>
                <div class="bokify-card-shadow"></div>"""
            else:
                cover_html = f"""<div class="bokify-card-cover bokify-card-wireframe-cover">
                  <svg class="bokify-wireframe-blueprint-svg" viewBox="0 0 124 180" width="100%" height="100%" preserveAspectRatio="none">
                    <defs>
                      <pattern id="wf-grid-{total_card_idx}" width="12" height="12" patternUnits="userSpaceOnUse">
                        <path d="M 12 0 L 0 0 0 12" fill="none" stroke="rgba(56, 189, 248, 0.12)" stroke-width="0.8" />
                      </pattern>
                      <radialGradient id="wf-glow-{total_card_idx}" cx="50%" cy="45%" r="60%">
                        <stop offset="0%" stop-color="rgba(212, 175, 55, 0.18)" />
                        <stop offset="50%" stop-color="rgba(56, 189, 248, 0.08)" />
                        <stop offset="100%" stop-color="rgba(2, 8, 16, 0.95)" />
                      </radialGradient>
                    </defs>
                    <rect width="124" height="180" fill="url(#wf-glow-{total_card_idx})" rx="3" />
                    <rect width="124" height="180" fill="url(#wf-grid-{total_card_idx})" rx="3" />
                    <rect x="5" y="5" width="114" height="170" fill="none" stroke="rgba(212, 175, 55, 0.45)" stroke-width="1.2" stroke-dasharray="4 3" rx="2" />
                    <circle cx="62" cy="74" r="30" fill="none" stroke="rgba(56, 189, 248, 0.28)" stroke-width="0.8" stroke-dasharray="2 2" />
                    <circle cx="62" cy="74" r="20" fill="none" stroke="rgba(212, 175, 55, 0.35)" stroke-width="1" />
                    <path d="M62 62 L65 71 L74 74 L65 77 L62 86 L59 77 L50 74 L59 71 Z" fill="rgba(252, 224, 155, 0.85)" />
                    <path d="M 9 9 L 17 9 M 9 9 L 9 17" fill="none" stroke="rgba(56, 189, 248, 0.6)" stroke-width="1.2" />
                    <path d="M 115 9 L 107 9 M 115 9 L 115 17" fill="none" stroke="rgba(56, 189, 248, 0.6)" stroke-width="1.2" />
                    <path d="M 9 171 L 17 171 M 9 171 L 9 163" fill="none" stroke="rgba(56, 189, 248, 0.6)" stroke-width="1.2" />
                    <path d="M 115 171 L 107 171 M 115 171 L 115 163" fill="none" stroke="rgba(56, 189, 248, 0.6)" stroke-width="1.2" />
                    <text x="62" y="24" text-anchor="middle" font-family="'Cinzel', serif" font-size="6.5" font-weight="700" fill="#94a3b8" letter-spacing="1.5">DR. ZAID AMIN</text>
                    <text x="62" y="32" text-anchor="middle" font-family="'Inter', sans-serif" font-size="5" font-weight="600" fill="rgba(56, 189, 248, 0.75)" letter-spacing="1">MONOGRAPH PIPELINE</text>
                    <text x="62" y="130" text-anchor="middle" font-family="'Cinzel', serif" font-size="7.5" font-weight="700" fill="#fef08a" letter-spacing="1">FORTHCOMING</text>
                    <text x="62" y="140" text-anchor="middle" font-family="'Cinzel', serif" font-size="6.5" font-weight="600" fill="#cbd5e1" letter-spacing="0.8">SCHOLARLY WORK</text>
                    <rect x="16" y="150" width="92" height="15" rx="7.5" fill="rgba(8, 28, 50, 0.85)" stroke="rgba(212, 175, 55, 0.5)" stroke-width="0.8" />
                    <text x="62" y="160.5" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="5.0" font-weight="700" fill="#fce09b" letter-spacing="0.8">{p_micro_status}</text>
                  </svg>
                  <div class="bokify-cover-shine"></div>
                </div>
                <div class="bokify-card-spine">
                  <span class="bokify-spine-micro">PIPELINE</span>
                </div>
                <div class="bokify-card-pages"></div>
                <div class="bokify-card-shadow"></div>"""

            shelf_cards_html += f"""
        <article class="bokify-shelf-card bokify-card-wireframe pub-item" data-category="{cat['category_key'].lower()}" data-title="{p_title_lower}" data-venue="pipeline" data-year="{p_year}">
          <!-- Top 3D Book Wireframe / Cover Stage -->
          <div class="bokify-card-stage">
            <div class="bokify-card-3d-scene">
              <div class="bokify-card-book-3d">
                {cover_html}
              </div>
            </div>
            <div class="bokify-card-tags">
              <span class="bokify-publisher-chip" style="border-style: dashed; border-color: rgba(56, 189, 248, 0.4); color: #7dd3fc;">EDITORIAL PIPELINE</span>
              <span class="bokify-year-chip" style="border-style: dashed; color: #fef08a;">{p_year}</span>
              <span class="bokify-primary-chip" style="background: rgba(212, 175, 55, 0.12); border: 1px dashed rgba(212, 175, 55, 0.45); color: #fef08a;">{p_badge}</span>
            </div>
          </div>

          <!-- Card Content -->
          <div class="bokify-card-body">
            <div class="bokify-card-meta-line">
              <span class="bokify-card-idx">#{total_card_idx:02d}</span>
              <span class="bokify-card-dot">•</span>
              <span class="bokify-card-authors">{p_authors}</span>
            </div>

            <h4 class="bokify-card-title font-cinzel bokify-wireframe-title">{p_title}</h4>
            <div class="bokify-card-series" style="color: #7dd3fc; font-style: italic;">{p_series}</div>
            <div class="bokify-card-divider" style="border-bottom: 1px dashed rgba(212, 175, 55, 0.25);"></div>
            <p class="bokify-card-excerpt">{p_abstract}</p>
            <div class="bokify-card-meta-block">
              <div class="bokify-card-doi"><span class="bokify-doi-lbl">STATUS:</span> <span class="bokify-doi-val" style="color: #fef08a; font-weight: 600;">{p_status}</span></div>
            </div>
          </div>

          <!-- Card Actions (Gestalt Proximity) -->
          <div class="bokify-card-actions">
            <a href="mailto:zaid.amin@newinti.edu.my?subject=Advance%20Inquiry:%20{p_title}" class="pub-pill-btn pub-pill-primary bokify-btn-wireframe" title="Inquire about upcoming publication / manuscript advance">
              {render_svg_icon_fn("email")}
              <span>Advance Inquiry / Notice</span>
            </a>
            <span class="pub-pill-btn pub-pill-secondary bokify-pill-wireframe-slot" title="Reserved slot for forthcoming publication">✦ Pipeline Slot</span>
          </div>
        </article>
        """

    hero_cfg = {
        "kicker": "01 / 04 • MONOGRAPHS & CHAPTERS",
        "headline_prefix": "Explore Research",
        "headline_highlight": "Monographs & Chapters",
        "description": "Comprehensive academic monographs, peer-reviewed book chapters, and curated editorial volumes exploring sociotechnical systems, digital loneliness, and behavioral interventions in information diffusion. Published with leading international academic presses including Springer Nature (Contributions to Management Science, Lecture Notes in Computer Science) and Atlantis Press.",
        "publisher_badges": ["Springer Nature", "LNCS Series", "Atlantis Press", "Scopus Indexed", "Gold Open Access"]
    }
    hero_json_file = BASE_DIR / "data" / "books_hero.json"
    if hero_json_file.exists():
        try:
            with open(hero_json_file, "r", encoding="utf-8") as f:
                loaded_h = json.load(f)
                if isinstance(loaded_h, dict):
                    hero_cfg.update(loaded_h)
        except Exception:
            pass

    prof_file = BASE_DIR / "data" / "profile.json"
    author_name = "Dr. Zaid Amin"
    author_role = "Senior Lecturer • FDSIT, INTI International University"
    if prof_file.exists():
        try:
            with open(prof_file, "r", encoding="utf-8") as f:
                prof_data = json.load(f)
                name = prof_data.get("name", "Dr. Zaid Amin")
                author_name = name.replace(", Ph.D.", "").replace(", Ph.D", "").replace(", PhD", "").strip()
                title = prof_data.get("title", "Senior Lecturer")
                if "Senior Lecturer" in title:
                    title = "Senior Lecturer"
                aff = prof_data.get("affiliation")
                inst = "FDSIT, INTI International University"
                if isinstance(aff, dict):
                    inst = f"FDSIT, {aff.get('institution', 'INTI International University')}"
                elif isinstance(aff, str):
                    inst = aff
                author_role = f"{title} • {inst}"
        except Exception:
            pass

    badges_html = "".join([
        f'<span class="bokify-pub-pill"><span class="bokify-pub-bullet">&bull;</span> {_html_mod.escape(b)}</span>'
        for b in hero_cfg.get("publisher_badges", [])
    ])

    # Primary featured download URL
    primary_url = featured_book.get("url", "") or f"https://doi.org/{featured_book.get('doi', '')}"

    return f"""
    <section class="pub-gallery-section bokify-showcase-section" id="{cat['id']}" data-category-section="{cat['category_key'].lower()}">

      <!-- ========================================================
           BOKIFY HERO BANNER (Golden Ratio 61.8% : 38.2%)
           ======================================================== -->
      <div class="bokify-hero-wrapper">
        <div class="bokify-hero-halo"></div>

        <div class="bokify-hero-grid">
          <!-- LEFT COLUMN: Typography & Actions (61.8%) -->
          <div class="bokify-hero-info">
            <!-- Author Pill & Category Badge -->
            <div class="bokify-author-bar">
              <div class="bokify-author-pill">
                <picture>
                  <source srcset="assets/images/portraits/portrait-1.webp" type="image/webp">
                  <img src="assets/images/portraits/portrait-1.png" alt="Dr. Zaid Amin" class="bokify-author-avatar" loading="lazy">
                </picture>
                <div class="bokify-author-text">
                  <span class="bokify-author-name">{author_name}</span>
                  <span class="bokify-author-role">{author_role}</span>
                </div>
              </div>
              <span class="bokify-category-tag">{hero_cfg.get("kicker", "01 / 04 • MONOGRAPHS & CHAPTERS")}</span>
            </div>

            <!-- Big Bokify Headline -->
            <h2 class="bokify-hero-title font-cinzel">
              {_html_mod.escape(hero_cfg.get("headline_prefix", "Meet Your Next"))} <span class="bokify-gold-gradient">{_html_mod.escape(hero_cfg.get("headline_highlight", "Scholarly Treatise"))}</span>
            </h2>

            <!-- Description -->
            <p class="bokify-hero-desc">
              {_html_mod.escape(hero_cfg.get("description", ""))}
            </p>

            <!-- Call to Actions (Harmonized with CV Available on Request Settings) -->
            <div class="bokify-hero-ctas">
              <a href="mailto:zaid.amin@newinti.edu.my?subject=Primary%20Volume%20Request%20-%20Dr.%20Zaid%20Amin" class="cv-round-btn-download cv-btn-disabled" title="Direct volume download is currently disabled. Click to request academic volume via email.">
                <span class="cv-round-icon-wrap">
                  <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                  </svg>
                </span>
                <span class="cv-round-labels">
                  <span class="cv-round-kicker">PRIMARY VOLUME (ACADEMIC)</span>
                  <span class="cv-round-title">Available on Request</span>
                </span>
              </a>
              <a href="#bokify-volumes-shelf" class="bokify-btn-hero-secondary" style="height: 52px; box-sizing: border-box;">
                <span>Browse All {len(cat_items)} Volumes</span>
                <span class="bokify-arrow-down">&darr;</span>
              </a>
            </div>
          </div>

          <!-- RIGHT COLUMN: Dual 3D Standing Book Showcase (38.2%) -->
          <div class="bokify-hero-stage">
            <div class="bokify-stage-container">
              <!-- Radial Stage Spotlight -->
              <div class="bokify-stage-glow"></div>

              <!-- 3D Book Stage Scene -->
              <div class="bokify-stage-scene">
                <!-- Front Standing Book (Primary Monograph) -->
                <div class="bokify-standing-book bokify-standing-front">
                  <div class="bokify-book-3d">
                    <div class="bokify-book-cover">
                      <img src="{featured_img}" alt="{featured_title}" class="bokify-cover-img" loading="lazy" onerror="this.onerror=null;this.src='assets/images/books/book_digital_loneliness.png'">
                      <div class="bokify-cover-glare"></div>
                    </div>
                    <div class="bokify-book-spine">
                      <span class="bokify-spine-text">{featured_pub.upper()} &bull; {featured_year}</span>
                    </div>
                    <div class="bokify-book-pages"></div>
                    <div class="bokify-book-shadow"></div>
                  </div>
                  <div class="bokify-stage-badge">★ PRIMARY MONOGRAPH ({featured_year})</div>
                </div>

                <!-- Rear Standing Book (Companion Volume) -->
                {f'''<div class="bokify-standing-book bokify-standing-rear">
                  <div class="bokify-book-3d">
                    <div class="bokify-book-cover">
                      <img src="{rear_img}" alt="{rear_title}" class="bokify-cover-img" loading="lazy" onerror="this.onerror=null;this.src='assets/images/books/book_attention_covid.png'">
                      <div class="bokify-cover-glare"></div>
                    </div>
                    <div class="bokify-book-spine">
                      <span class="bokify-spine-text">{rear_pub.upper()} &bull; {rear_year}</span>
                    </div>
                    <div class="bokify-book-pages"></div>
                    <div class="bokify-book-shadow"></div>
                  </div>
                </div>''' if rear_book else ''}
              </div>

              <!-- Floor Grounding Ambient Line -->
              <div class="bokify-stage-pedestal-line"></div>
            </div>
          </div>

          <!-- Trust / Publisher Strip (Full-Width Harmonic Row 2) -->
          <div class="bokify-publisher-strip">
            <span class="bokify-publisher-strip-label">PUBLISHED &amp; INDEXED WITH</span>
            <div class="bokify-publisher-badges">
              {badges_html}
            </div>
          </div>
        </div>
      </div>

      <!-- ========================================================
           CURATED VOLUMES SHELF (Bokify "Top Sales / Featured")
           ======================================================== -->
      <div class="bokify-shelf-section" id="bokify-volumes-shelf">
        <div class="bokify-shelf-header">
          <div class="bokify-shelf-title-wrap">
            <span class="bokify-shelf-eyebrow">✦ CURATED CORPUS</span>
            <h3 class="bokify-shelf-heading font-cinzel">All Published Volumes &amp; Chapters</h3>
          </div>
          <div class="bokify-shelf-chips">
            {chips_html}
          </div>
        </div>

        <!-- 3-Column Golden Ratio Cards Grid -->
        <div class="bokify-cards-grid">
          {shelf_cards_html}
        </div>
      </div>

    </section>
    """


def generate_publications_page():
    publications = load_json("publications.json")

    page_head = get_html_head(
        get_page_browser_title("publications", "Research & Publication Gallery | Dr. Zaid Amin | zaidamin.org"),
        "A premium scholarly gallery of 24+ peer-reviewed works, books, journal articles, conference proceedings, and preprints across Human-Computer Interaction, AI Governance, and Behavioral Computing by Dr. Zaid Amin."
    )
    page_header = get_page_header("publications")

    categories_config = [
        {
            "id": "section-books",
            "category_key": "Book Chapter",
            "title": "Book & Chapters",
            "badge": "01 / 04 • MONOGRAPHS & CHAPTERS",
            "photo_webp": "assets/images/portraits/portrait-1.webp",
            "photo_png": "assets/images/portraits/portrait-1.png",
            "photo_alt": "Dr. Zaid Amin - Books & Chapters",
            "description": "Comprehensive academic monographs, peer-reviewed book chapters, and curated editorial volumes exploring sociotechnical systems, digital loneliness, and behavioral interventions in information diffusion. Published with leading international academic presses including Springer Nature (Contributions to Management Science, Lecture Notes in Computer Science) and Atlantis Press.",
            "chips": ["3 Published Volumes", "Springer Nature & Atlantis", "Scopus & LNCS Indexed"]
        },
        {
            "id": "section-journals",
            "category_key": "Journal",
            "title": "Journal Papers",
            "badge": "02 / 04 • REFEREED JOURNALS",
            "photo_webp": "assets/images/portraits/portrait-2.webp",
            "photo_png": "assets/images/portraits/portrait-2.png",
            "photo_alt": "Dr. Zaid Amin - Journal Papers",
            "description": "High-impact, international peer-reviewed journal articles focusing on trustworthy AI for sustainable cities, multimodal agentic frameworks, visual selective attention modeling, and cultural heritage informatics. Featured across premier international venues including MDPI Smart Cities, IEEE Access, and JISTM.",
            "chips": ["10 Refereed Journal Articles", "Scopus Q1 & IEEE Access", "Gold Open Access"]
        },
        {
            "id": "section-conferences",
            "category_key": "Conference",
            "title": "Conference Papers",
            "badge": "03 / 04 • PROCEEDINGS & SYMPOSIUMS",
            "photo_webp": "assets/images/portraits/portrait-4.webp",
            "photo_png": "assets/images/portraits/portrait-4.png",
            "photo_alt": "Dr. Zaid Amin - Conference Papers",
            "description": "Peer-reviewed conference proceedings and international symposium presentations advancing cybernetic models of information sharing, enterprise document architecture, and server clustering for big data. Presented across premier IEEE and national engineering conferences.",
            "chips": ["6 Conference Papers", "IEEE ICE3IS & SEMNASTEK", "International Proceedings"]
        },
        {
            "id": "section-preprints",
            "category_key": "Preprint",
            "title": "Preprint Papers",
            "badge": "04 / 04 • OPEN SCIENCE & PREPRINTS",
            "photo_webp": "assets/images/portraits/portrait-3.webp",
            "photo_png": "assets/images/portraits/portrait-3.png",
            "photo_alt": "Dr. Zaid Amin - Preprint Papers",
            "description": "Early-access preprints and working manuscripts deposited on open-science repositories (SSRN, arXiv) to accelerate scientific discourse prior to formal peer review. Covers cutting-edge frontiers in agentic AI alignment, the proxy trap in autonomous systems, and digital attention intervention architectures.",
            "chips": ["5 Working Preprints", "SSRN & arXiv Repositories", "Open Science Early Access"]
        }
    ]

    def clean_excerpt(raw_text, max_len=130):
        if not raw_text:
            return ""
        clean = re.sub(r'<[^>]+>', ' ', raw_text)
        clean = ' '.join(clean.split())
        if len(clean) > max_len:
            truncated = clean[:max_len]
            if ' ' in truncated:
                truncated = truncated.rsplit(' ', 1)[0]
            clean = truncated.rstrip(' ,;:.') + "..."
        return clean

    def render_download_pill(pub):
        url = pub.get("url", "").strip() if pub.get("url") else ""
        doi = pub.get("doi", "").strip() if pub.get("doi") else ""
        link_enabled = pub.get("link_enabled", True)

        is_link_active = bool(
            link_enabled is not False
            and url != "#"
            and doi != "#"
            and "on process" not in doi.lower()
            and "on process" not in url.lower()
            and (url or doi)
        )
        if not url and doi and is_link_active:
            url = f"https://doi.org/{doi}"

        if is_link_active and url:
            label = "Download"
            if "arxiv.org" in url:
                label = "Download (arXiv)"
            elif "ssrn" in url or "2139/ssrn" in url:
                label = "Download (SSRN)"
            elif "doi.org" in url:
                label = "Download / DOI"
            elif "scopus.com" in url:
                label = "Scopus Record"
            elif "eprints" in url:
                label = "Download / ePrints"
            else:
                label = "Download / Access"
            return f'<a href="{url}" target="_blank" rel="noopener" class="pub-pill-btn pub-pill-primary">{render_svg_icon("download")} <span>{label}</span></a>'
        else:
            title_enc = html.escape(pub.get("title", ""))
            mailto = f"mailto:zaid.amin@newinti.edu.my?subject=Requesting%20Full-Text:%20{title_enc}"
            lock_svg = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'
            return f'<a href="{mailto}" class="pub-pill-btn pub-pill-primary pub-pill-request" title="Direct download unavailable. Available on request via email."><span class="pub-pill-lock-icon">{lock_svg}</span> <span>Available on Request</span></a>'

    # Build category sections
    sections_html = ""
    for cat_idx, cat in enumerate(categories_config, 1):
        # Premium Book Showcase layout for Book & Chapters
        if cat["category_key"] == "Book Chapter":
            sections_html += render_book_showcase_section(
                publications, cat, render_svg_icon, render_download_pill, clean_excerpt, html
            )
            continue

        cat_items = [p for p in publications if p.get("category") == cat["category_key"]]
        
        cards_html = ""
        for item_idx, pub in enumerate(cat_items, 1):
            download_pill = render_download_pill(pub)
            featured_pill = '<span class="pub-strip-featured-pill">★ Featured Work</span>' if pub.get("featured") else ""
            short_venue = pub.get("venue", "")
            if len(short_venue) > 42:
                short_venue = short_venue[:40] + "..."
            excerpt = clean_excerpt(pub.get("abstract", ""), max_len=180)
            doi = pub.get("doi", "").strip() if pub.get("doi") else ""
            url = pub.get("url", "").strip() if pub.get("url") else ""
            isbn = pub.get("isbn", "").strip() if pub.get("isbn") else ""
            
            doi_html = f'<span class="pub-strip-doi-inline"><span class="pub-strip-doi-lbl">DOI/ISBN/LINK:</span> <span class="pub-strip-doi-val">{doi}</span></span>' if doi else ""
            isbn_html = f'<span class="pub-strip-doi-inline"><span class="pub-strip-doi-lbl">ISBN:</span> <span class="pub-strip-doi-val">{isbn}</span></span>' if isbn else ""
            year = pub.get("year", "")
            escaped_title = html.escape(pub["title"])
            escaped_title_lower = html.escape(pub["title"].lower())
            escaped_venue = html.escape(pub.get("venue", ""))
            escaped_venue_lower = html.escape(pub.get("venue", "").lower())
            bibtex_id = pub.get("id", f"pub_{cat_idx}_{item_idx}")
            cat_badge_label = cat["title"].replace(" Papers", "").upper()

            cards_html += f"""
            <article class="pub-strip-card pub-item" data-category="{cat['category_key'].lower()}" data-title="{escaped_title_lower}" data-venue="{escaped_venue_lower}" data-year="{year}">
              <div class="pub-strip-main">
                <!-- Left Scholarly Content (Golden Ratio ~75%) -->
                <div class="pub-strip-content">
                  <!-- Row 1: Badges, Index, Year & Venue (Gestalt Proximity) -->
                  <div class="pub-strip-header">
                    <div class="pub-strip-tags">
                      <span class="pub-strip-idx">#{item_idx:02d}</span>
                      <span class="pub-strip-cat-pill">{cat_badge_label}</span>
                      <span class="pub-strip-year-pill">{year}</span>
                      <span class="pub-strip-venue-chip" title="{escaped_venue}">{short_venue}</span>
                    </div>
                    {featured_pill}
                  </div>

                  <!-- Row 2: Article / Paper Title -->
                  <h3 class="pub-strip-title font-cinzel">{pub['title']}</h3>
                  
                  <!-- Row 3: Full Venue, Authors & DOI Line -->
                  <div class="pub-strip-venue-line">
                    <span class="pub-strip-venue-name">{pub.get('venue', '')}</span>
                    <span class="pub-strip-dot">&bull;</span>
                    <span class="pub-strip-authors">Dr. Zaid Amin et al.</span>
                    {f'<span class="pub-strip-dot">&bull;</span> {doi_html}' if doi_html else ''}
                    {f'<span class="pub-strip-dot">&bull;</span> {isbn_html}' if isbn_html else ''}
                  </div>

                  <!-- Row 4: Abstract Excerpt (Compact 1-2 lines) -->
                  {f'<p class="pub-strip-excerpt">{excerpt}</p>' if excerpt else ''}
                </div>

                <!-- Right Action Pills Dock (Golden Ratio ~25%, Tight & Neat) -->
                <div class="pub-strip-actions">
                  {download_pill}
                  <button class="pub-pill-btn pub-pill-secondary btn-bibtex-toggle" data-target="bib-{bibtex_id}">
                    Cite / BibTeX
                  </button>
                </div>
              </div>

              <!-- Collapsible BibTeX Drawer -->
              <div class="bibtex-box" id="bib-{bibtex_id}">
                <div class="bibtex-box-header">
                  <span class="bibtex-box-label">BibTeX Citation Entry</span>
                  <button class="bibtex-copy-btn" data-target="code-{bibtex_id}">Copy BibTeX</button>
                </div>
                <code id="code-{bibtex_id}">{pub['bibtex']}</code>
              </div>
            </article>
            """

        chips_html = "".join([f'<span class="pub-stat-chip">{c}</span>' for c in cat["chips"]])

        sections_html += f"""
        <section class="pub-gallery-section pub-pure-strip-section" id="{cat['id']}" data-category-section="{cat['category_key'].lower()}">
          <!-- Full-Width Pure Strip Header (No Portrait Anchor - Clean & Elegant) -->
          <header class="pub-pure-section-header">
            <div class="pub-pure-header-info">
              <div class="pub-pure-badge-row">
                <span class="pub-pure-badge">{cat['badge']}</span>
              </div>
              <h2 class="pub-pure-title font-cinzel">{cat['title']}</h2>
              <div class="pub-pure-gold-line"></div>
              <p class="pub-pure-desc">{cat['description']}</p>
            </div>
            <div class="pub-pure-chips-wrapper">
              {chips_html}
            </div>
          </header>

          <!-- Pure Full-Width Horizontal Strip Cards Stack -->
          <div class="pub-pure-strip-list">
            {cards_html}
          </div>
        </section>
        """

    # Check in-page shortcut pills from navigation.json
    nav_data = get_navigation_data()
    shortcuts = {s.get("id"): s for s in nav_data.get("page_shortcuts", [])}
    team_pill_cfg = shortcuts.get("pub_team_pill", {
        "enabled": True,
        "display_text": "👥 Research Team &nearr;",
        "title": "Research Team",
        "url": "#",
        "target": "_self"
    })
    team_pill_html = ""
    if team_pill_cfg.get("enabled", True):
        p_text = team_pill_cfg.get("display_text", "👥 Research Team &nearr;")
        p_title = team_pill_cfg.get("title", "Research Team")
        p_url = team_pill_cfg.get("url", "#")
        p_target = team_pill_cfg.get("target", "_self")
        onclick_attr = ' onclick="if(this.getAttribute(\'href\')===\'#\'){event.preventDefault();}"' if p_url == '#' else ''
        team_pill_html = f'<a href="{p_url}" target="{p_target}" class="pub-nav-pill team-shortcut-pill" title="{p_title}"{onclick_attr}>{p_text}</a>'

    # Assemble complete page
    html_content = page_head + page_header + f"""
    <!-- Subpage Content: Research & Publication Gallery Engine -->
    <div class="subpage-container pub-gallery-container">
      <div class="pub-gallery-hero">
        <div class="subpage-eyebrow"><span class="eyebrow-dot">✦</span> Scholarly Archive &bull; Peer-Reviewed Corpus</div>
        <h1 class="pub-gallery-title">Research &amp; Publications</h1>
        <p class="pub-gallery-subtitle">
          {len(publications)} indexed works across Human-Computer Interaction, AI Governance, and Behavioral Computing.
        </p>
      </div>

      <!-- Sticky Controls & Category Nav Bar -->
      <div class="pub-controls-bar">
        <div class="pub-search-wrapper">
          <span class="pub-search-icon">{render_svg_icon("search")}</span>
          <input type="text" id="pub-search" class="pub-search-input" placeholder="Search by title, venue, year..." aria-label="Search all {len(publications)} publications by title, venue, year, or keyword">
        </div>

        <nav class="pub-nav-pills" aria-label="Publication Categories">
          <button class="pub-nav-pill filter-btn active" data-filter="all">✦ All ({len(publications)})</button>
          <button class="pub-nav-pill filter-btn" data-filter="book chapter" data-target-section="section-books">01. Book &amp; Chapters (3)</button>
          <button class="pub-nav-pill filter-btn" data-filter="journal" data-target-section="section-journals">02. Journals (10)</button>
          <button class="pub-nav-pill filter-btn" data-filter="conference" data-target-section="section-conferences">03. Conferences (6)</button>
          <button class="pub-nav-pill filter-btn" data-filter="preprint" data-target-section="section-preprints">04. Preprints (5)</button>
          {team_pill_html}
        </nav>
      </div>

      <div id="pub-count-indicator" style="display: none; margin: -10px 0 16px 4px; font-size: 0.80rem; color: var(--text-muted); font-weight: 600;">
        Showing all {len(publications)} publications across 4 dedicated galleries
      </div>

      <!-- 4 Gallery Sections -->
      <div class="pub-sections-wrapper">
        {sections_html}
      </div>
    </div>
    """ + get_page_footer()

    return html_content
# ==============================================================================
# 3. RESEARCH PILLARS (research.html)
# ==============================================================================
def generate_research_page():
    research = load_json("research.json")
    articles = load_json("articles.json") if (DATA_DIR / "articles.json").exists() else []

    html = get_html_head(get_page_browser_title("research", "Activity & Project | Dr. Zaid Amin | zaidamin.org"), "Scholarly activity, 80+ peer essays, research pillars, and funded grants authored and led by Dr. Zaid Amin.")
    html += get_page_header("research")

    # Categories for articles
    categories = {}
    for a in articles:
        cat = a.get("category", "Essays & Perspectives")
        categories[cat] = categories.get(cat, 0) + 1

    cat_pills_html = f'<button class="article-cat-btn active" data-category="all">✦ All ({len(articles)})</button>'
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        cat_pills_html += f'<button class="article-cat-btn" data-category="{cat}">{cat} ({count})</button>'

    def clean_article_excerpt(raw_text, max_len=135):
        if not raw_text:
            return ""
        clean = re.sub(r'<[^>]+>', ' ', raw_text)
        clean = ' '.join(clean.split())
        if len(clean) > max_len:
            truncated = clean[:max_len]
            if ' ' in truncated:
                truncated = truncated.rsplit(' ', 1)[0]
            clean = truncated.rstrip(' ,;:.') + "..."
        return clean

    cards_html = ""
    import html as _html_mod
    for a in articles:
        cat = a.get("category", "Essays & Perspectives")
        read_time = a.get("reading_time", "3 min read")
        excerpt = clean_article_excerpt(a.get("excerpt", ""), max_len=135)
        slug = a.get("id", "")
        title = a.get("title", "")
        date = a.get("date", "")
        tags_str = ",".join(a.get("tags", [])).lower()
        img_url = a.get("image", "").strip() or "assets/images/thumb-research.jpg"
        is_spotlight = a.get("featured")
        spotlight_badge = '<span class="article-card-spotlight-pill">★ SPOTLIGHT</span>' if is_spotlight else ''
        card_spotlight_class = " article-card-spotlight" if is_spotlight else ""
        escaped_title = _html_mod.escape(title)

        cards_html += f'''
        <article class="article-card{card_spotlight_class}" data-category="{cat}" data-title="{title.lower()}" data-tags="{tags_str}">
          <!-- Small Thumbnail Frame (Golden Ratio Harmonic Proportion) -->
          <a href="/article?id={slug}" class="article-card-thumb-wrap" aria-label="{escaped_title}">
            <img src="{img_url}" alt="{escaped_title}" class="article-card-thumb" loading="lazy" onerror="this.onerror=null; this.src=\'assets/images/thumb-research.jpg\';">
            <div class="article-card-thumb-overlay"></div>
            <span class="article-card-cat-badge">{cat}</span>
            {spotlight_badge}
          </a>

          <!-- Content Body (Gestalt Proximity) -->
          <div class="article-card-body">
            <div class="article-card-meta">
              <span class="article-card-date">{date}</span>
              <span class="article-card-dot">&bull;</span>
              <span class="article-card-read">{read_time}</span>
            </div>
            <h3 class="article-card-title font-cinzel">
              <a href="/article?id={slug}">{title}</a>
            </h3>
            <p class="article-card-excerpt">{excerpt}</p>
          </div>

          <!-- Elegant Read Essay Button (Golden Ratio Capsule Pill) -->
          <div class="article-card-action">
            <a href="/article?id={slug}" class="article-card-btn font-cinzel">
              <span>Read Essay</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="article-btn-icon">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </a>
          </div>
        </article>
        '''

    # Research Pillars HTML
    pillars_html = ""
    for pillar in research["pillars"]:
        topics = " ".join([f'<span style="font-size:0.775rem; font-weight:600; padding:4px 10px; background:rgba(4, 32, 54, 0.85); border:1px solid rgba(34, 166, 200, 0.25); color:#c8e0ec; border-radius:4px; margin-right:6px; margin-bottom:6px; display:inline-block;">{t}</span>' for t in pillar["key_topics"]])
        pillars_html += f"""
        <div style="background:rgba(4, 28, 48, 0.75); border:1px solid rgba(34, 166, 200, 0.22); border-radius:18px; padding:36px; box-shadow:0 12px 35px rgba(0,10,24,0.40); backdrop-filter:blur(8px);">
          <div style="font-size:0.75rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:var(--brand-blue); margin-bottom:6px;">RESEARCH DOMAIN</div>
          <h2 class="activity-section-title">{pillar['title']}</h2>
          <p style="font-size: 1rem; color: var(--text-body); line-height: 1.7; margin-bottom: 20px;">
            {pillar['full_desc']}
          </p>

          <div style="margin-bottom: 20px;">
            <div style="font-size: 0.85rem; font-weight: 800; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; color:#ffffff;">Key Technical Frontiers:</div>
            {topics}
          </div>

          <div style="background: rgba(245, 158, 11, 0.12); color: var(--brand-gold); padding: 12px 18px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; border-left: 4px solid var(--brand-gold);">
            Grant Alignment: {pillar['grant_alignment']}
          </div>
        </div>
        """

    # Active Grant Themes
    grants_html = ""
    for grant in research.get("active_grant_themes", []):
        grants_html += f"""
        <div style="background:rgba(10, 24, 42, 0.65); border:1px solid rgba(186, 230, 253, 0.15); border-radius:14px; padding:24px 28px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
            <h3 style="font-size:1.15rem; font-weight:700; color:#ffffff; margin:0;">{grant['title']}</h3>
            <span style="font-size:0.75rem; font-weight:700; color:#38bdf8; background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.3); padding:3px 9px; border-radius:999px;">{grant['period']}</span>
          </div>
          <div style="font-size:0.85rem; color:#bae6fd; margin-bottom:8px; font-weight:600;">{grant['role']} &bull; {grant['agency']}</div>
          <p style="font-size:0.92rem; color:#94a3b8; line-height:1.6; margin:0;">{grant['objective']}</p>
        </div>
        """

    script_code = """
    <script>
    function switchActivityTab(tab) {
      var isArticles = tab === 'articles';
      document.getElementById('activity-pane-articles').style.display = isArticles ? 'block' : 'none';
      document.getElementById('activity-pane-pillars').style.display = isArticles ? 'none' : 'block';
      document.getElementById('tab-btn-articles').classList.toggle('active', isArticles);
      document.getElementById('tab-btn-pillars').classList.toggle('active', !isArticles);
      if (history.replaceState) {
        history.replaceState(null, null, isArticles ? '#articles' : '#pillars');
      }
    }

    (function() {
      // Handle initial hash
      var hash = window.location.hash;
      if (hash === '#pillars' || hash === '#projects' || hash === '#grants') {
        switchActivityTab('pillars');
      } else {
        switchActivityTab('articles');
      }

      // Articles filter & search
      var searchInput = document.getElementById('article-search');
      var catButtons = document.querySelectorAll('.article-cat-btn');
      var cards = document.querySelectorAll('.article-card');
      var countDisplay = document.getElementById('article-count-display');
      var currentCategory = 'all';
      var currentSearch = '';

      function filterArticles() {
        var visibleCount = 0;
        cards.forEach(function(card) {
          var cardCat = card.getAttribute('data-category') || '';
          var cardTitle = card.getAttribute('data-title') || '';
          var cardTags = card.getAttribute('data-tags') || '';
          var catMatch = (currentCategory === 'all' || cardCat === currentCategory);
          var searchMatch = !currentSearch || cardTitle.includes(currentSearch) || cardTags.includes(currentSearch);
          if (catMatch && searchMatch) {
            card.style.display = 'flex';
            visibleCount++;
          } else {
            card.style.display = 'none';
          }
        });
        if (countDisplay) {
          if (currentSearch || currentCategory !== 'all') {
            countDisplay.style.display = 'block';
            countDisplay.textContent = 'Showing ' + visibleCount + ' of ' + cards.length + ' articles';
          } else {
            countDisplay.style.display = 'none';
          }
        }
      }

      if (searchInput) {
        searchInput.addEventListener('input', function(e) {
          currentSearch = e.target.value.toLowerCase().trim();
          filterArticles();
        });
      }

      catButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
          catButtons.forEach(function(b) { b.classList.remove('active'); });
          btn.classList.add('active');
          currentCategory = btn.getAttribute('data-category');
          filterArticles();
        });
      });
    })();
    </script>
    """

    html += f"""
    <!-- Subpage Content: Activity & Project -->
    <div class="subpage-container activity-page-container">
      <!-- Subpage Content: Activity & Project (Golden Ratio Split Composition) -->
      <section class="activity-hero-section">
        <div class="activity-hero-content">
          <div class="subpage-eyebrow"><span class="eyebrow-dot">✦</span> Scholarly Archive &bull; Technical Initiatives</div>
          <h1 class="activity-hero-title">Activity &amp; Project</h1>
          <p class="activity-hero-subtitle">
            80 scholarly essays, peer commentaries, core research pillars, and active funded grant themes.
          </p>
        </div>
        <div class="activity-tabs-bar">
          <button class="activity-tab-btn active" id="tab-btn-articles" onclick="switchActivityTab('articles')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: -1px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
            <span>Scholarly Articles &amp; Essays ({len(articles)})</span>
          </button>
          <button class="activity-tab-btn" id="tab-btn-pillars" onclick="switchActivityTab('pillars')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: -1px;"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
            <span>Research Pillars &amp; Grants</span>
          </button>
        </div>
      </section>

      <!-- PANE 1: Scholarly Articles & Essays -->
      <div id="activity-pane-articles">
        <div class="articles-controls">
          <div class="articles-search-wrap">
            <span class="articles-search-icon">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </span>
            <input type="text" id="article-search" class="article-search-input" placeholder="Search essays..." aria-label="Search across {len(articles)} scholarly essays by keyword, topic, or title" autocomplete="off">
          </div>
          <nav class="articles-category-pills" aria-label="Article Categories">
            {cat_pills_html}
          </nav>
        </div>
        <div id="article-count-display" class="article-count-indicator" style="display: none; margin: -12px 0 16px 4px; font-size: 0.80rem; color: #94a3b8; font-weight: 600;">
          Showing all {len(articles)} articles
        </div>

        <div class="articles-grid" id="articles-grid">
          {cards_html}
        </div>
      </div>

      <!-- PANE 2: Research Pillars & Grants -->
      <div id="activity-pane-pillars" style="display: none;">
        <div style="display: flex; flex-direction: column; gap: 32px; margin-bottom: 40px;">
          {pillars_html}
        </div>

        <div style="margin-top: 48px; margin-bottom: 24px;">
          <h2 class="activity-section-title" style="margin-bottom: 16px;">Active &amp; Targeted Grant Themes</h2>
          <div style="display: flex; flex-direction: column; gap: 16px;">
            {grants_html}
          </div>
        </div>
      </div>

    </div>
    {script_code}
    """
    
    html += """
    <script>
      function filterDistinctions(btn, cat) {
        const dock = btn.parentElement;
        if (dock) {
          dock.querySelectorAll('.cv-distinction-filter-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        }
        const cards = document.querySelectorAll('.cv-distinction-card');
        cards.forEach(card => {
          const match = (cat === 'all' || card.getAttribute('data-category') === cat);
          if (match) {
            card.classList.remove('is-hidden');
            card.style.removeProperty('display');
          } else {
            card.classList.add('is-hidden');
            card.style.setProperty('display', 'none', 'important');
          }
        });
      }
    </script>
    """

    html += get_page_footer()
    return html


# ==============================================================================
# 4. POSTGRADUATE LAB & SUPERVISION (prospective-students.html)
# ==============================================================================

# ==============================================================================
# 5. MEDIA & TALKS (talks.html)
# ==============================================================================
def resolve_talkshow_video_urls(v):
    raw_url = (v.get("youtube_url") or v.get("youtube_id") or v.get("video_url") or v.get("url") or "").strip()
    yt_id = None
    if raw_url:
        import re
        if len(raw_url) == 11 and re.match(r'^[a-zA-Z0-9_-]{11}$', raw_url) and "drive" not in raw_url.lower():
            yt_id = raw_url
        else:
            m = re.search(r'(?:youtube\.com/(?:watch\?v=|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})', raw_url)
            if m:
                yt_id = m.group(1)
                
    if yt_id:
        watch_url = f"https://www.youtube.com/watch?v={yt_id}"
        embed_url = f"https://www.youtube-nocookie.com/embed/{yt_id}?autoplay=1&rel=0&modestbranding=1&enablejsapi=1"
        return watch_url, embed_url, "youtube"
        
    import re
    drive_m = re.search(r'drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)', raw_url)
    if drive_m:
        drive_id = drive_m.group(1)
        watch_url = f"https://drive.google.com/file/d/{drive_id}/view?usp=sharing"
        embed_url = f"https://drive.google.com/file/d/{drive_id}/preview"
        return watch_url, embed_url, "drive"
        
    return raw_url, v.get("embed_url", raw_url), "other"

def generate_talks_page():
    media_data = load_json("media_talks.json") if (DATA_DIR / "media_talks.json").exists() else {}
    talkshows = media_data.get("talkshows", [])
    keynotes = media_data.get("keynotes", [])
    opinions = media_data.get("opinions", [])

    page_head = get_html_head(
        get_page_browser_title("talks", "Media & Talks | Dr. Zaid Amin | zaidamin.org"),
        "Televised talkshows, international keynotes, visiting speaker discourses, and critical philosophical opinions by Dr. Zaid Amin."
    )
    page_header = get_page_header("talks")

    featured = talkshows[0] if talkshows else {
        "title": "LIVE Talk Show: E-Commerce Architecture & Digital Startup Ecosystems",
        "channel": "TVRI Network Broadcast",
        "category_tag": "Televised Talkshow",
        "date": "May 8, 2015",
        "duration": "28:40",
        "description": "Televised live expert discourse on modern e-commerce platform infrastructure, digital transformation for regional business ecosystems, and low-barrier digital architecture deployment.",
        "poster": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhW5JewkiMm4SgKuFID1hWK_h8DxdvBqabnZ-FUAzDd_1ekWJng90GKMs17scwnf1KDBCSP5HiJzzovOKkK15ruNYlO1EEWSZPRwKoKm_-SFKJZDinsmR9Dd2SWTPYFTnmliNw1GCSxNHs/s1600/IMG_20150508_152040.jpg",
        "video_url": "http://bit.ly/4n6pIBK"
    }

    # Render Category 1: Playlist items
    playlist_items_html = []
    for idx, v in enumerate(talkshows):
        is_active = "active" if idx == 0 else ""
        v_title = _html_mod.escape(v.get("title", ""))
        v_desc = _html_mod.escape(v.get("description", ""))
        v_channel = _html_mod.escape(v.get("channel", ""))
        v_tag = _html_mod.escape(v.get("category_tag", "Talkshow"))
        v_date = _html_mod.escape(v.get("date", ""))
        v_poster = _html_mod.escape(v.get("poster", ""))
        v_watch, v_embed_raw, v_type = resolve_talkshow_video_urls(v)
        v_url = _html_mod.escape(v_watch)
        v_embed = _html_mod.escape(v_embed_raw)
        v_duration = _html_mod.escape(v.get("duration", "20:00"))

        item_html = f"""
        <button class="video-playlist-item {is_active}" 
                data-index="{idx}"
                data-title="{v_title}"
                data-description="{v_desc}"
                data-channel="{v_channel}"
                data-category="{v_tag}"
                data-date="{v_date}"
                data-poster="{v_poster}"
                data-url="{v_url}"
                data-embed="{v_embed}"
                data-duration="{v_duration}"
                type="button"
                aria-label="Select {v_title}">
          <div class="video-item-thumb-box">
            <img src="{v_poster}" alt="{v_title}" class="video-item-thumb-img" loading="lazy" onerror="this.src='assets/images/spotlight-smart-cities.jpg'">
            <div class="video-item-thumb-yt-badge">
              <svg width="14" height="10" viewBox="0 0 68 48">
                <path d="M66.52,7.74c-0.78-2.93-2.49-5.41-5.42-6.19C55.79,.13,34,0,34,0S12.21,.13,6.9,1.55 C3.97,2.33,2.27,4.81,1.48,7.74C0.06,13.05,0,24,0,24s0.06,10.95,1.48,16.26c0.78,2.93,2.49,5.41,5.42,6.19 C12.21,47.87,34,48,34,48s21.79-0.13,27.1-1.55c2.93-0.78,4.64-3.26,5.42-6.19C67.94,34.95,68,24,68,24S67.94,13.05,66.52,7.74z" fill="#ff0000"/>
                <path d="M 45,24 27,14 27,34" fill="#ffffff"/>
              </svg>
            </div>
          </div>
          <div class="video-item-meta">
            <div class="video-item-channel">{v_channel}</div>
            <div class="video-item-desc">{v_title}</div>
          </div>
        </button>"""
        playlist_items_html.append(item_html)

    playlist_joined = "\n".join(playlist_items_html)
    total_episodes_count = f"{len(talkshows):02d}"

    # Reusable Icon library for top-right circular badge
    icon_map = {
        "podium": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="22"/></svg>',
        "brain": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2a9 9 0 0 1 9 9c0 3.6-2.1 6.7-5.2 8.1"/><path d="M12 22a9 9 0 0 1-9-9c0-3.6 2.1-6.7 5.2-8.1"/></svg>',
        "governance": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>',
        "heritage": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V7l7-4 7 4v14"/><path d="M9 10a3 3 0 0 1 6 0v11H9V10z"/></svg>',
        "creativity": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4"/><path d="M12 18v4"/><path d="m4.93 4.93 2.83 2.83"/><path d="m16.24 16.24 2.83 2.83"/><path d="M2 12h4"/><path d="M18 12h4"/><path d="m4.93 19.07 2.83-2.83"/><path d="m16.24 7.76 2.83-2.83"/></svg>',
        "attention": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><line x1="21.17" y1="8" x2="12" y2="8"/><line x1="3.95" y1="6.06" x2="8.54" y2="14"/></svg>',
        "philosophy": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>',
        "trap": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>',
        "quill": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19 7-7 3 3-7 7-3-3z"/><path d="m18 13-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="m2 2 7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>'
    }

    # Render Category 2: Keynote Carousel Cards (Figure Reference)
    def check_is_poster_img(img_path):
        if not img_path:
            return False
        low = img_path.lower()
        if any(kw in low for kw in ["flyer", "poster", "whatsapp", "lecture", "seminar"]):
            return True
        try:
            import os
            from PIL import Image
            clean_path = img_path.split("?")[0].replace("/", os.sep)
            if os.path.exists(clean_path):
                with Image.open(clean_path) as im:
                    w, h = im.size
                    return h >= w * 0.9
        except Exception:
            pass
        return False

    keynotes_cards_html = []
    keynote_icons = ["podium", "brain", "governance", "heritage", "creativity", "attention"]
    for idx, k in enumerate(keynotes):
        k_title = _html_mod.escape(k.get("title", ""))
        k_venue = _html_mod.escape(k.get("venue", ""))
        k_abstract = _html_mod.escape(k.get("abstract", ""))
        k_url = _html_mod.escape(k.get("url", "#"))
        k_badge = _html_mod.escape(k.get("badge", f"0{idx+1} • Keynote"))
        k_img = k.get("image", "assets/images/spotlight-smart-cities.jpg")
        icon_svg = icon_map.get(keynote_icons[idx % len(keynote_icons)], icon_map["podium"])

        media_stage_html = f'''<div class="service-card-media-stage">
            <img src="{k_img}" alt="" class="service-card-bg-glow" aria-hidden="true">
            <img src="{k_img}" alt="{k_title}" class="service-card-fg-poster" loading="lazy" onerror="this.src=\'assets/images/spotlight-smart-cities.jpg\'">
          </div>'''

        card_html = f"""
        <div class="service-portrait-card">
          {media_stage_html}
          <div class="service-card-gradient-top"></div>

          <!-- Top Row: Frosted Tag -->
          <div class="service-card-top-row">
            <span class="service-card-tag">{k_badge}</span>
          </div>

          <!-- Bottom Content: Venue, Title, Synopsis, Capsule Button -->
          <div class="service-card-bottom">
            <div class="service-card-venue">{k_venue}</div>
            <h3 class="service-card-title">{k_title}</h3>
            <p class="service-card-desc">{k_abstract}</p>
            <a href="{k_url}" {"target='_blank' rel='noopener'" if k_url.startswith("http") else ""} class="service-card-btn">
              <span>Read More</span>
              <span class="service-card-btn-disc">&nearr;</span>
            </a>
          </div>
        </div>"""
        keynotes_cards_html.append(card_html)

    keynotes_carousel_joined = "\n".join(keynotes_cards_html)

    # Render Category 3: Opinion Carousel Cards (Figure Reference)
    opinions_cards_html = []
    opinion_icons = ["philosophy", "trap", "attention", "heritage", "governance", "quill"]
    for idx, o in enumerate(opinions):
        o_title = _html_mod.escape(o.get("title", ""))
        o_pub = _html_mod.escape(o.get("publication", "Treatise Archive"))
        o_abstract = _html_mod.escape(o.get("abstract", ""))
        o_url = _html_mod.escape(o.get("url", "#"))
        o_badge = _html_mod.escape(o.get("badge", f"Essay 0{idx+1}"))
        o_img = o.get("image", "assets/images/spotlight-smart-cities.jpg")
        icon_svg = icon_map.get(opinion_icons[idx % len(opinion_icons)], icon_map["philosophy"])

        media_stage_html = f'''<div class="service-card-media-stage">
            <img src="{o_img}" alt="" class="service-card-bg-glow" aria-hidden="true">
            <img src="{o_img}" alt="{o_title}" class="service-card-fg-poster" loading="lazy" onerror="this.src=\'assets/images/spotlight-smart-cities.jpg\'">
          </div>'''

        card_html = f"""
        <div class="service-portrait-card">
          {media_stage_html}
          <div class="service-card-gradient-top"></div>

          <!-- Top Row: Frosted Tag -->
          <div class="service-card-top-row">
            <span class="service-card-tag">{o_badge}</span>
          </div>

          <!-- Bottom Content: Publication, Title, Synopsis, Capsule Button -->
          <div class="service-card-bottom">
            <div class="service-card-venue">{o_pub}</div>
            <h3 class="service-card-title">{o_title}</h3>
            <p class="service-card-desc">{o_abstract}</p>
            <a href="{o_url}" {"target='_blank' rel='noopener'" if o_url.startswith("http") else ""} class="service-card-btn">
              <span>Read Essay</span>
              <span class="service-card-btn-disc">&nearr;</span>
            </a>
          </div>
        </div>"""
        opinions_cards_html.append(card_html)

    opinions_carousel_joined = "\n".join(opinions_cards_html)

    feat_watch, feat_embed, feat_type = resolve_talkshow_video_urls(featured)
    feat_title = _html_mod.escape(featured.get("title", ""))
    feat_desc = _html_mod.escape(featured.get("description", ""))
    feat_channel = _html_mod.escape(featured.get("channel", "Broadcast Archive"))
    feat_tag = _html_mod.escape(featured.get("category_tag", "Talkshow"))
    feat_date = _html_mod.escape(featured.get("date", "2015"))
    feat_poster = _html_mod.escape(featured.get("poster", ""))
    feat_url = _html_mod.escape(feat_watch)
    feat_duration = _html_mod.escape(featured.get("duration", "28:40"))

    js_controller = """
    <!-- Client-side Interactive Controller for Video Stage & Carousels -->
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        // 1. Video Gallery Stage Interaction
        const stagePoster = document.getElementById("stage-poster-img");
        const stageTitle = document.getElementById("stage-title");
        const stageDesc = document.getElementById("stage-description");
        const stageNetworkTitle = document.getElementById("stage-network-title");
        const stageNetworkSub = document.getElementById("stage-network-sub");
        const stageDate = document.getElementById("stage-date");
        const stageBadge = document.getElementById("stage-badge");
        const stageWatchLink = document.getElementById("stage-watch-link");
        const stageDuration = document.getElementById("stage-duration");
        const stagePlayBtn = document.getElementById("stage-play-center");
        const playlistItems = document.querySelectorAll(".video-playlist-item");

        let activeIndex = 0;

        let isPlayerActive = false;
        const stageIframe = document.getElementById("stage-video-iframe");
        const stageCloseBtn = document.getElementById("stage-close-player");

        function startVideoPlayer(embedUrl) {
          if (!stageIframe || !embedUrl) return;
          let finalEmbed = embedUrl;
          const ytMatch = embedUrl.match(/(?:youtube[.]com\\/(?:watch[?]v=|embed\\/|v\\/)|youtu[.]be\\/)([a-zA-Z0-9_-]{11})/);
          if (ytMatch) {
            finalEmbed = `https://www.youtube-nocookie.com/embed/${ytMatch[1]}?autoplay=1&rel=0&modestbranding=1&enablejsapi=1`;
          }
          stageIframe.src = finalEmbed;
          stageIframe.classList.add("active");
          if (stageCloseBtn) stageCloseBtn.classList.add("active");
          isPlayerActive = true;
        }

        function closeVideoPlayer() {
          if (!stageIframe) return;
          stageIframe.src = "";
          stageIframe.classList.remove("active");
          if (stageCloseBtn) stageCloseBtn.classList.remove("active");
          isPlayerActive = false;
        }

        // Category 1: Talk Show Vertical Carousel Slider (Top-to-Down Auto-Advance)
        let playlistTimer = null;
        let isPlaylistHovered = false;
        const PLAYLIST_INTERVAL = 4800; // Calibrated 4.8s golden interval

        function updatePlaylistCounter(idx) {
          const counter = document.getElementById("video-playlist-counter");
          if (!counter) return;
          const currSpan = counter.querySelector(".counter-curr");
          if (currSpan) {
            currSpan.textContent = String(idx + 1).padStart(2, "0");
          }
        }

        function scrollPlaylistItemIntoView(item) {
          const stack = document.getElementById("video-playlist-stack");
          if (!stack || !item) return;
          const itemTop = item.offsetTop - stack.offsetTop;
          const targetScroll = Math.max(0, Math.min(
            stack.scrollHeight - stack.clientHeight,
            itemTop - (stack.clientHeight - item.offsetHeight) / 2
          ));
          stack.scrollTo({ top: targetScroll, behavior: "smooth" });
        }

        function activateVideo(index, playNow) {
          if (index < 0 || index >= playlistItems.length) return;
          activeIndex = index;

          // Soft luxury crossfade effect on stage
          const stageContent = document.querySelector(".video-stage-content");
          if (stageContent && stagePoster) {
            stageContent.classList.add("stage-fading");
            stagePoster.classList.add("stage-fading");
            setTimeout(function () {
              stageContent.classList.remove("stage-fading");
              stagePoster.classList.remove("stage-fading");
            }, 220);
          }

          playlistItems.forEach(function (item, i) {
            if (i === index) {
              item.classList.add("active");
              scrollPlaylistItemIntoView(item);
              updatePlaylistCounter(index);

              const d = item.dataset;
              if (stagePoster) stagePoster.src = d.poster;
              if (stageTitle) stageTitle.textContent = d.title;
              if (stageDesc) stageDesc.textContent = d.description;
              if (stageNetworkTitle) stageNetworkTitle.textContent = d.channel;
              if (stageNetworkSub) stageNetworkSub.textContent = d.category;
              if (stageDate) stageDate.textContent = d.date;
              if (stageBadge) stageBadge.textContent = d.category;
              if (stageWatchLink) stageWatchLink.href = d.url;
              if (stageDuration) {
                stageDuration.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-1px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> ' + d.duration;
              }
              if (playNow || isPlayerActive) {
                startVideoPlayer(d.embed || d.url);
              }
            } else {
              item.classList.remove("active");
            }
          });
        }

        function slidePlaylistNext() {
          const nextIdx = (activeIndex + 1) % playlistItems.length;
          activateVideo(nextIdx);
        }

        function slidePlaylistPrev() {
          const prevIdx = (activeIndex - 1 + playlistItems.length) % playlistItems.length;
          activateVideo(prevIdx);
        }

        function startPlaylistTimer() {
          stopPlaylistTimer();
          playlistTimer = setInterval(function () {
            // Only auto-advance if not hovered, document visible, and NOT actively playing video
            if (!isPlaylistHovered && !document.hidden && !isPlayerActive) {
              slidePlaylistNext();
            }
          }, PLAYLIST_INTERVAL);
        }

        function stopPlaylistTimer() {
          if (playlistTimer) {
            clearInterval(playlistTimer);
            playlistTimer = null;
          }
        }

        function resetPlaylistTimer() {
          stopPlaylistTimer();
          startPlaylistTimer();
        }

        playlistItems.forEach(function (item, idx) {
          item.addEventListener("click", function (e) {
            e.preventDefault();
            activateVideo(idx);
            resetPlaylistTimer();
          });
        });

        const prevBtn = document.getElementById("video-prev-btn");
        const nextBtn = document.getElementById("video-next-btn");

        if (prevBtn) {
          prevBtn.addEventListener("click", function () {
            slidePlaylistPrev();
            resetPlaylistTimer();
          });
        }
        if (nextBtn) {
          nextBtn.addEventListener("click", function () {
            slidePlaylistNext();
            resetPlaylistTimer();
          });
        }

        // Pause on mouse hover (Figure-Ground Law: Focus on card interaction)
        const playlistElements = [
          document.getElementById("video-playlist-stack"),
          document.querySelector(".video-playlist-container"),
          document.getElementById("video-stage-frame")
        ].filter(Boolean);

        playlistElements.forEach(function (el) {
          el.addEventListener("mouseenter", function () {
            isPlaylistHovered = true;
            stopPlaylistTimer();
          });
          el.addEventListener("mouseleave", function () {
            isPlaylistHovered = false;
            startPlaylistTimer();
          });
        });

        // Touch gestures on mobile
        const playlistStack = document.getElementById("video-playlist-stack");
        if (playlistStack) {
          playlistStack.addEventListener("touchstart", function () {
            isPlaylistHovered = true;
            stopPlaylistTimer();
          }, { passive: true });
          playlistStack.addEventListener("touchend", function () {
            isPlaylistHovered = false;
            resetPlaylistTimer();
          }, { passive: true });
        }

        // Page visibility
        document.addEventListener("visibilitychange", function () {
          if (document.hidden) {
            stopPlaylistTimer();
          } else if (!isPlaylistHovered && !isPlayerActive) {
            startPlaylistTimer();
          }
        });

        // Initialize playlist counter and autoplay
        updatePlaylistCounter(0);
        startPlaylistTimer();

        if (stagePlayBtn) {
          stagePlayBtn.addEventListener("click", function () {
            const activeItem = playlistItems[activeIndex];
            if (activeItem) {
              const embed = activeItem.dataset.embed || activeItem.dataset.url;
              startVideoPlayer(embed);
            }
          });
        }

        if (stageCloseBtn) {
          stageCloseBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            closeVideoPlayer();
          });
        }

        const shareBtn = document.getElementById("stage-share-btn");
        if (shareBtn) {
          shareBtn.addEventListener("click", function () {
            const activeItem = playlistItems[activeIndex];
            const url = activeItem && activeItem.dataset.url ? activeItem.dataset.url : window.location.href;
            if (navigator.clipboard) {
              navigator.clipboard.writeText(url).then(() => {
                const origTitle = shareBtn.getAttribute("title") || "Share Broadcast Link";
                shareBtn.setAttribute("title", "Link Copied!");
                shareBtn.classList.add("copied");
                setTimeout(() => {
                  shareBtn.setAttribute("title", origTitle);
                  shareBtn.classList.remove("copied");
                }, 2000);
              }).catch(() => {
                prompt("Copy video link:", url);
              });
            } else {
              prompt("Copy video link:", url);
            }
          });
        }

        // 2. Category 2 & 3 Smooth Auto-Advancing Carousel Controllers (Golden Ratio & Gestalt Harmonic Alignment)
        function setupCarousel(prevId, nextId, trackId, paginationId, intervalMs) {
          const pBtn = document.getElementById(prevId);
          const nBtn = document.getElementById(nextId);
          const track = document.getElementById(trackId);
          const pag = paginationId ? document.getElementById(paginationId) : null;
          if (!track) return;

          const cards = Array.from(track.querySelectorAll(".service-portrait-card"));
          if (cards.length === 0) return;

          const delay = intervalMs || 3800;
          let timer = null;
          let isHovered = false;
          let activeIndex = 0;

          // Render Gestalt Pagination Indicator Dots
          if (pag) {
            pag.innerHTML = "";
            cards.forEach(function (card, idx) {
              const dot = document.createElement("button");
              dot.className = "service-carousel-dot" + (idx === 0 ? " active" : "");
              dot.type = "button";
              dot.setAttribute("aria-label", "Go to slide " + (idx + 1));
              dot.addEventListener("click", function () {
                scrollToIndex(idx);
                resetTimer();
              });
              pag.appendChild(dot);
            });
          }

          function getShift() {
            const card = cards[0];
            return card ? card.offsetWidth + 20 : 375;
          }

          function updateActiveDot(idx) {
            if (!pag) return;
            const dots = pag.querySelectorAll(".service-carousel-dot");
            dots.forEach(function (d, i) {
              d.classList.toggle("active", i === idx);
            });
          }

          function scrollToIndex(idx) {
            if (idx < 0) idx = 0;
            if (idx >= cards.length) idx = cards.length - 1;
            const targetCard = cards[idx];
            if (targetCard) {
              const left = targetCard.offsetLeft - track.offsetLeft;
              track.scrollTo({ left: left, behavior: "smooth" });
              activeIndex = idx;
              updateActiveDot(activeIndex);
            }
          }

          function slideNext() {
            const shift = getShift();
            const maxScroll = track.scrollWidth - track.clientWidth;
            // When reaching or near the end, loop smoothly and elegantly back to the beginning
            if (track.scrollLeft >= maxScroll - 20) {
              track.scrollTo({ left: 0, behavior: "smooth" });
              activeIndex = 0;
              updateActiveDot(0);
            } else {
              track.scrollBy({ left: shift, behavior: "smooth" });
              activeIndex = Math.min(cards.length - 1, activeIndex + 1);
              updateActiveDot(activeIndex);
            }
          }

          function slidePrev() {
            const shift = getShift();
            // When at or near the start, loop smoothly to the end
            if (track.scrollLeft <= 20) {
              const maxScroll = track.scrollWidth - track.clientWidth;
              track.scrollTo({ left: maxScroll, behavior: "smooth" });
              activeIndex = cards.length - 1;
              updateActiveDot(activeIndex);
            } else {
              track.scrollBy({ left: -shift, behavior: "smooth" });
              activeIndex = Math.max(0, activeIndex - 1);
              updateActiveDot(activeIndex);
            }
          }

          if (nBtn) {
            nBtn.addEventListener("click", function () {
              slideNext();
              resetTimer();
            });
          }

          if (pBtn) {
            pBtn.addEventListener("click", function () {
              slidePrev();
              resetTimer();
            });
          }

          // Active indicator sync on scroll
          let scrollDebounce = null;
          track.addEventListener("scroll", function () {
            clearTimeout(scrollDebounce);
            scrollDebounce = setTimeout(function () {
              const trackLeft = track.scrollLeft;
              const shift = getShift();
              const currentIdx = Math.round(trackLeft / shift);
              const clamped = Math.max(0, Math.min(cards.length - 1, currentIdx));
              if (clamped !== activeIndex) {
                activeIndex = clamped;
                updateActiveDot(activeIndex);
              }
            }, 60);
          }, { passive: true });

          // Smooth Automatic Sliding Cycle (Cadence)
          function startTimer() {
            stopTimer();
            timer = setInterval(function () {
              if (!isHovered && !document.hidden) {
                slideNext();
              }
            }, delay);
          }

          function stopTimer() {
            if (timer) {
              clearInterval(timer);
              timer = null;
            }
          }

          function resetTimer() {
            stopTimer();
            startTimer();
          }

          // Pause on mouse hover (Figure-Ground Law: Focus on card interaction)
          const hoverElements = [track, pBtn, nBtn, pag].filter(Boolean);
          hoverElements.forEach(function (el) {
            el.addEventListener("mouseenter", function () {
              isHovered = true;
              stopTimer();
            });
            el.addEventListener("mouseleave", function () {
              isHovered = false;
              startTimer();
            });
          });

          // Pause on mobile touch interactions
          track.addEventListener("touchstart", function () {
            isHovered = true;
            stopTimer();
          }, { passive: true });
          track.addEventListener("touchend", function () {
            isHovered = false;
            resetTimer();
          }, { passive: true });

          // Visibility State Handler
          document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
              stopTimer();
            } else if (!isHovered) {
              startTimer();
            }
          });

          startTimer();
        }

        setupCarousel("keynote-prev-btn", "keynote-next-btn", "keynote-track", "keynote-pagination", 3800);
        setupCarousel("opinion-prev-btn", "opinion-next-btn", "opinion-track", "opinion-pagination", 4200);

        // Automatically ensure any portrait/flyer image fits responsively with ambient glow
        document.querySelectorAll(".service-card-media-stage").forEach(function(stage) {
          const fg = stage.querySelector(".service-card-fg-poster, .service-card-bg-img");
          if (!fg) return;
          function autoFit() {
            if (fg.naturalHeight >= fg.naturalWidth * 0.9) {
              stage.classList.add("service-card-poster-mode");
              if (!stage.querySelector(".service-card-bg-glow")) {
                const glow = document.createElement("img");
                glow.src = fg.src;
                glow.className = "service-card-bg-glow";
                glow.setAttribute("aria-hidden", "true");
                stage.prepend(glow);
              }
              fg.className = "service-card-fg-poster";
            }
          }
          if (fg.complete && fg.naturalWidth > 0) autoFit();
          else fg.addEventListener("load", autoFit);
        });
      });
    </script>
    """

    body_html = f"""
    <main class="talks-page-container" id="main-content">

      <!-- Hero Header (Golden Ratio Split Composition) -->
      <section class="talks-hero-section">
        <div class="talks-hero-content">
          <div class="subpage-eyebrow"><span class="eyebrow-dot">✦</span> Audio-Visual Archive &bull; Keynote Engagements</div>
          <h1 class="talks-hero-title">Media &amp; Talks</h1>
          <p class="talks-hero-subtitle">
            Televised broadcasts, keynote addresses, and critical philosophical treatises.
          </p>
        </div>
        <div class="talks-nav-bar" aria-label="Media &amp; Talks Navigation">
          <a href="#category-talkshow" class="talks-nav-pill active">01. Talk Show</a>
          <a href="#category-keynotes" class="talks-nav-pill">02. Keynote, Guest &amp; Visiting Speaker</a>
          <a href="#category-opinion" class="talks-nav-pill">03. Opinion</a>
        </div>
      </section>

      <!-- ====================================================================
           CATEGORY 1: TALKSHOW (VIDEO GALLERY)
           ==================================================================== -->
      <section class="talks-category-section" id="category-talkshow">
        <div class="talks-category-header">
          <div class="talks-category-title-group">
            <h2>Talk Show</h2>
            <p class="talks-category-subtitle">Televised Broadcasts &bull; Expert Commentary &bull; Studio Discourse</p>
          </div>

          <!-- Header Actions: Watch Broadcast & Share (Golden Ratio Composition Alignment) -->
          <div class="talks-header-actions">
            <a id="stage-watch-link" href="{feat_url}" target="_blank" rel="noopener" class="talks-watch-header-btn" title="Watch Broadcast on YouTube">
              <span class="talks-watch-icon-box">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              </span>
              <span class="talks-watch-btn-text">Watch Broadcast</span>
              <span class="talks-watch-arrow">&nearr;</span>
            </a>
            <button class="talks-share-header-btn" id="stage-share-btn" title="Share Broadcast Link" type="button" aria-label="Share Broadcast Link">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            </button>
          </div>
        </div>

        <div class="video-gallery-grid">
          
          <!-- Left: Active Cinema Stage (61.8% Golden Ratio) -->
          <div class="video-stage-frame" id="video-stage-frame">
            <div class="video-stage-poster-layer">
              <img id="stage-poster-img" src="{feat_poster}" alt="{feat_title}" class="video-stage-poster-img" onerror="this.src='assets/images/spotlight-smart-cities.jpg'">
            </div>
            <div class="video-stage-gradient-top"></div>
            <div class="video-stage-gradient-bottom"></div>

            <!-- Embedded Video Iframe for Instant In-Page Playback -->
            <iframe id="stage-video-iframe" src="" title="{feat_title}" class="video-stage-iframe" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen" allowfullscreen></iframe>
            <button class="video-stage-close-player" id="stage-close-player" title="Close Video Player" type="button" aria-label="Close Video Player">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              <span>Close Player</span>
            </button>

            <!-- Top bar -->
            <div class="video-stage-top-meta">
              <img src="assets/images/portraits/portrait-1.webp" alt="Dr. Zaid Amin" class="video-stage-avatar">
              <div>
                <div class="video-stage-network-title" id="stage-network-title">{feat_channel}</div>
                <div class="video-stage-network-sub" id="stage-network-sub">{feat_tag}</div>
              </div>
            </div>

            <!-- Center YouTube Big Play Button -->
            <button class="video-stage-play-center" id="stage-play-center" aria-label="Play Active Video" type="button">
              <svg viewBox="0 0 68 48" width="68" height="48">
                <path d="M66.52,7.74c-0.78-2.93-2.49-5.41-5.42-6.19C55.79,.13,34,0,34,0S12.21,.13,6.9,1.55 C3.97,2.33,2.27,4.81,1.48,7.74C0.06,13.05,0,24,0,24s0.06,10.95,1.48,16.26c0.78,2.93,2.49,5.41,5.42,6.19 C12.21,47.87,34,48,34,48s21.79-0.13,27.1-1.55c2.93-0.78,4.64-3.26,5.42-6.19C67.94,34.95,68,24,68,24S67.94,13.05,66.52,7.74z" fill="#ff0000"/>
                <path d="M 45,24 27,14 27,34" fill="#ffffff"/>
              </svg>
            </button>

            <!-- Bottom content on stage (Clean breathing room without overlay buttons) -->
            <div class="video-stage-content">
              <div class="video-stage-badge-row">
                <span class="video-stage-badge" id="stage-badge">{feat_tag}</span>
                <span class="video-stage-date" id="stage-date">{feat_date}</span>
                <span class="video-stage-duration-tag" id="stage-duration">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-1px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  <span>{feat_duration}</span>
                </span>
              </div>
              <h3 class="video-stage-title" id="stage-title">{feat_title}</h3>
              <p class="video-stage-description" id="stage-description">{feat_desc}</p>
            </div>
          </div>

          <!-- Right: Playlist Stack (38.2% Golden Ratio) -->
          <div class="video-playlist-container">
            <div class="video-playlist-stack" id="video-playlist-stack">
              {playlist_joined}
            </div>

            <!-- Bottom Navigation Arrows & Counter (Golden Ratio Harmonic Proportions) -->
            <div class="video-playlist-footer">
              <div class="video-playlist-counter" id="video-playlist-counter" aria-label="Episode index">
                <span class="counter-curr">01</span><span class="counter-sep">/</span><span class="counter-total">{total_episodes_count}</span>
              </div>
              <div class="video-nav-arrows-group">
                <button class="video-nav-arrow-btn" id="video-prev-btn" title="Previous Video" type="button" aria-label="Previous Video">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="15 18 9 12 15 6"/></svg>
                </button>
                <button class="video-nav-arrow-btn" id="video-next-btn" title="Next Video" type="button" aria-label="Next Video">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="9 18 15 12 9 6"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           SPEAKING INVITATION BANNER (Top Block of User Reference Image)
           ==================================================================== -->
      <section class="talks-invite-banner" aria-label="Keynote Speaking Invitation">
        <div class="talks-invite-img-col">
          <div class="talks-invite-img-frame">
            <img src="assets/images/portraits/portrait-1.webp" alt="Dr. Zaid Amin" loading="lazy">
          </div>

        </div>

        <div class="talks-invite-content">
          <div class="talks-invite-eyebrow">
            <span class="talks-invite-dot"></span>
            <span>Scholarly Invitation &bull; Global Engagements</span>
          </div>
          <p class="talks-invite-p">
            Dr. Zaid Amin is available for international academic keynotes, conference plenary talks, institutional research workshops, and expert panel discussions on Human-Computer Interaction, AI Governance, Cognitive Attention Systems, and Digital Ethics.
          </p>
          <div class="talks-invite-actions">
            <a href="mailto:zaid.amin@newinti.edu.my" class="talks-invite-btn-primary">
              <span>Invite for Keynote</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
            </a>
            <a href="/cv" class="talks-invite-link-sec">
              <span>View Academic Curriculum Vitae &nearr;</span>
            </a>
          </div>
        </div>
      </section>

      <!-- ====================================================================
           CATEGORY 2: KEYNOTE, GUEST AND VISITING SPEAKER (Figure Reference)
           ==================================================================== -->
      <section class="talks-category-section" id="category-keynotes">
        <div class="service-carousel-header">
          <div class="service-header-left">
            <div class="service-eyebrow">
              <span class="service-eyebrow-dot"></span>
              <span>02. Keynote, Guest &amp; Visiting Speaker</span>
            </div>
            <h2 class="service-heading">Global <em>Keynotes</em> &amp; Visiting Orations</h2>
          </div>
          
          <div class="service-header-right">
            <p class="service-subtext">Delivering international plenary keynotes, visiting research lectures, and academic symposia across institutions.</p>
            <div class="service-arrow-nav">
              <button class="service-arrow-btn" id="keynote-prev-btn" title="Previous Keynote" type="button" aria-label="Previous Keynotes">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <button class="service-arrow-btn" id="keynote-next-btn" title="Next Keynote" type="button" aria-label="Next Keynotes">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
          </div>
        </div>

        <div class="service-carousel-track" id="keynote-track">
          {keynotes_carousel_joined}
        </div>
        <div class="service-carousel-pagination" id="keynote-pagination" aria-label="Keynote slide indicators"></div>
      </section>

      <!-- ====================================================================
           CATEGORY 3: OPINION (Figure Reference)
           ==================================================================== -->
      <section class="talks-category-section" id="category-opinion" style="margin-bottom: 0; padding-bottom: 0;">
        <div class="service-carousel-header">
          <div class="service-header-left">
            <div class="service-eyebrow">
              <span class="service-eyebrow-dot gold-dot"></span>
              <span>03. Opinion &amp; Public Intellect</span>
            </div>
            <h2 class="service-heading">Philosophical <em>Treatises</em> &amp; Critical Inquiries</h2>
          </div>
          
          <div class="service-header-right">
            <p class="service-subtext">Critical public commentaries, epistemic investigations, and philosophical critiques on AI ethics and cognitive sovereignty.</p>
            <div class="service-arrow-nav">
              <button class="service-arrow-btn" id="opinion-prev-btn" title="Previous Opinion" type="button" aria-label="Previous Opinions">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <button class="service-arrow-btn" id="opinion-next-btn" title="Next Opinion" type="button" aria-label="Next Opinions">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
          </div>
        </div>

        <div class="service-carousel-track" id="opinion-track">
          {opinions_carousel_joined}
        </div>
        <div class="service-carousel-pagination" id="opinion-pagination" aria-label="Opinion slide indicators"></div>
      </section>

    </main>
    """

    return page_head + page_header + body_html + js_controller + get_page_footer()


def generate_supervision_page():
    supervision = load_json("supervision.json")

    html = get_html_head("Postgraduate Lab & Supervision | Dr. Zaid Amin | zaidamin.org", supervision["statement"])
    html += get_page_header("supervision")

    html += f"""
    <!-- Subpage Content: Mentorship & Supervision -->
    <div class="subpage-container">
      <div style="margin-bottom: 24px;">
        <div class="subpage-eyebrow"><span class="eyebrow-dot">✦</span> Academic Mentorship &bull; Postgraduate Lab</div>
        <h1 class="subpage-hero-title font-cinzel">{supervision['heading']}</h1>
        <p class="subpage-hero-subtitle">
          {supervision['statement']}
        </p>
      </div>

      <div style="margin-bottom: 40px;">
        <h2 class="font-cinzel" style="font-size: 1.52rem; font-weight: 700; letter-spacing: 0.025em; margin-bottom: 20px; color: #ffffff;">Open Supervised Research Directions</h2>
        <div style="display: flex; flex-direction: column; gap: 20px;">
    """
    for t in supervision["open_topics"]:
        pills = " ".join([f'<span style="background:rgba(34, 166, 200, 0.14); color:#38b6d0; padding:4px 10px; border-radius:4px; font-size:0.75rem; font-weight:700; border:1px solid rgba(34, 166, 200, 0.3);">{d}</span>' for d in t["degree_levels"]])
        html += f"""
          <div style="background:rgba(4, 28, 48, 0.75); border:1px solid rgba(34, 166, 200, 0.22); border-radius:16px; padding:28px; backdrop-filter:blur(8px);">
            <div style="margin-bottom: 8px;">{pills}</div>
            <h3 style="font-size: 1.35rem; font-weight: 800; margin-bottom: 8px; color: #ffffff;">{t['title']}</h3>
            <p style="font-size: 0.95rem; color: var(--text-body); line-height: 1.6; margin-bottom: 12px;">{t['description']}</p>
            <div style="font-size: 0.825rem; color: var(--text-muted);"><strong style="color:#ffffff;">Prerequisites:</strong> {t['skills_required']}</div>
          </div>
        """
    html += f"""
        </div>
      </div>

      <div style="background: linear-gradient(135deg, rgba(4, 28, 48, 0.95), rgba(6, 40, 68, 0.98)); border: 2px solid var(--brand-blue); border-radius: 18px; padding: 32px; box-shadow: 0 12px 35px rgba(0, 10, 24, 0.50);">
        <h2 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 16px; color: #ffffff;">How to Submit an Inquiry for Supervision</h2>
        <ol style="margin-left: 20px; font-size: 0.95rem; line-height: 1.8; color: var(--text-body);">
          <li>Review my recent publications on Attention-Based Design (IEEE Access) or Agentic AI Governance (Smart Cities 2026).</li>
          <li>Prepare your Academic CV, transcripts, and a 1-page Research Proposal outlining your core problem.</li>
          <li>Email your materials to <a href="mailto:zaid.amin@newinti.edu.my" style="font-weight:700; color:var(--brand-blue); text-decoration:underline;">zaid.amin@newinti.edu.my</a> with the subject: <code>[Prospective Postgraduate] - [Your Name] - [Ph.D./Master]</code>.</li>
        </ol>
      </div>
    </div>
    """
    
    html += """
    <script>
      function filterDistinctions(btn, cat) {
        const dock = btn.parentElement;
        if (dock) {
          dock.querySelectorAll('.cv-distinction-filter-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        }
        const cards = document.querySelectorAll('.cv-distinction-card');
        cards.forEach(card => {
          const match = (cat === 'all' || card.getAttribute('data-category') === cat);
          if (match) {
            card.classList.remove('is-hidden');
            card.style.removeProperty('display');
          } else {
            card.classList.add('is-hidden');
            card.style.setProperty('display', 'none', 'important');
          }
        });
      }
    </script>
    """

    html += get_page_footer()
    return html

# ==============================================================================
# 5. CURRICULUM VITAE (cv.html)
# ==============================================================================

def get_distinction_meta(item):
    badge = (item.get('badge') or '').lower()
    cat = (item.get('category') or '').lower()
    title = (item.get('title') or '').lower()

    if any(k in badge or k in cat or k in title for k in ['grant', 'bima', 'gpk', 'kemenristekdikti']):
        return "cyan", "grants", "Competitive Research Grant"
    elif any(k in badge or k in cat or k in title for k in ['chairman', 'examiner', 'fellow', 'scholarship', 'apac', 'leadership', 'governance']):
        return "indigo", "governance", "Governance & Fellowship"
    else:
        return "gold", "awards", "Honors & Prestigious Award"

def get_distinction_emblem(theme):
    if theme == "gold":
        return '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.45 1-1 1H7v4h10v-4h-2c-.55 0-1-.45-1-1v-2.34"></path><path d="M6 4h12v7a6 6 0 0 1-12 0V4z"></path></svg>'
    elif theme == "cyan":
        return '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="21" x2="21" y2="21"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="12" y1="3" x2="12" y2="8"></line><path d="M4 21V10a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v11"></path><path d="M9 21v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4"></path></svg>'
    else:
        return '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="m4.93 4.93 4.24 4.24"></path><path d="m14.83 9.17 4.24-4.24"></path><path d="m14.83 14.83 4.24 4.24"></path><path d="m9.17 14.83-4.24 4.24"></path><circle cx="12" cy="12" r="4"></circle></svg>'

def render_cv_strip_card(
    idx,
    cat_pill,
    year_pill,
    venue_chip,
    title,
    venue_name,
    sub_extra="",
    excerpt="",
    verification_url="",
    secondary_btn_label="",
    secondary_btn_url="",
    featured_pill="",
    media_html="",
    extra_classes="",
    data_attrs="",
    cat_theme="cyan",
    show_verification_btn=False
):
    # Verification Link Button removed per user design request across Achievement & CV pages
    primary_btn = ""

    # Secondary Action Pill
    if secondary_btn_label and secondary_btn_url:
        is_mailto = secondary_btn_url.startswith("mailto:")
        is_ext = secondary_btn_url.startswith("http")
        sec_target = ' target="_blank" rel="noopener"' if is_ext else ''
        
        # Icon selection
        if is_mailto:
            sec_svg = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'
        elif 'gallery' in secondary_btn_label.lower() or 'talks' in secondary_btn_url:
            sec_svg = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>'
        else:
            sec_svg = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'

        secondary_btn = f'''<a href="{secondary_btn_url}"{sec_target} class="pub-pill-btn pub-pill-secondary" title="{secondary_btn_label}">
          {sec_svg}
          <span>{secondary_btn_label}</span>
        </a>'''
    else:
        secondary_btn = ""

    # Subtitle dot
    dot_separator = '<span class="pub-strip-dot">&bull;</span>' if sub_extra else ''
    sub_extra_html = f'<span class="pub-strip-authors">{sub_extra}</span>' if sub_extra else ''

    card_cls = f"pub-strip-card cv-strip-card {extra_classes}".strip()
    data_attr_str = f" {data_attrs}" if data_attrs else ""

    actions_dock = f"""
            <!-- Right Action Dock (Harmonized Action Pill) -->
            <div class="pub-strip-actions">
              {secondary_btn}
            </div>""" if secondary_btn else ""

    return f"""
        <article class="{card_cls}"{data_attr_str}>
          <div class="pub-strip-main">
            <!-- Left Scholarly Content (Golden Ratio) -->
            <div class="pub-strip-content">
              <!-- Row 1: Header / Badges / Tags -->
              <div class="pub-strip-header">
                <div class="pub-strip-tags">
                  <span class="pub-strip-idx">#{idx:02d}</span>
                  <span class="pub-strip-cat-pill cat-{cat_theme}">{cat_pill}</span>
                  <span class="pub-strip-year-pill">{year_pill}</span>
                  <span class="pub-strip-venue-chip" title="{venue_chip}">{venue_chip}</span>
                </div>
                {featured_pill}
              </div>

              <!-- Row 2: Title in Cinzel Roman Serif -->
              <h3 class="pub-strip-title font-cinzel">{title}</h3>

              <!-- Row 3: Subtitle / Institution / Scope -->
              <div class="pub-strip-venue-line">
                <span class="pub-strip-venue-name">{venue_name}</span>
                {dot_separator}
                {sub_extra_html}
              </div>

              <!-- Optional Media -->
              {media_html}

              <!-- Row 4: Narrative Description / Excerpt -->
              <p class="pub-strip-excerpt">
                {excerpt}
              </p>
            </div>

            {actions_dock}
          </div>
        </article>
    """

def generate_cv_page():
    cv = load_json("cv_data.json")
    exec_prof = cv["executive_profile"]
    publications = load_json("publications.json")

    photo_src = exec_prof.get("photo") or "assets/images/portraits/portrait-1.webp"
    photo_kicker = exec_prof.get("kicker") or "Ph.D. • UKM 2024"
    raw_cv_url = exec_prof.get("cv_pdf_url", "")
    if raw_cv_url is None:
        raw_cv_url = ""
    raw_cv_url_str = str(raw_cv_url).strip()

    # Detect if download is explicitly disabled
    is_cv_download_disabled = raw_cv_url_str in ["#", "", "disabled", "none", "javascript:void(0)"]
    cv_pdf_url = raw_cv_url_str if not is_cv_download_disabled else "#"
    edition_label = exec_prof.get("edition_label") or "July 2026 Academic Edition • 1.1 MB"

    orcid_data = exec_prof.get('researcher_ids', {}).get('orcid', {})
    orcid_id = orcid_data.get('id', '0000-0001-5223-3058') if isinstance(orcid_data, dict) else str(orcid_data)
    orcid_url = orcid_data.get('url', f'https://orcid.org/{orcid_id}') if isinstance(orcid_data, dict) else f'https://orcid.org/{orcid_id}'

    scopus_data = exec_prof.get('researcher_ids', {}).get('scopus', {})
    scopus_id = scopus_data.get('id', '57221839785') if isinstance(scopus_data, dict) else str(scopus_data)
    scopus_url = scopus_data.get('url', f'https://www.scopus.com/authid/detail.uri?authorId={scopus_id}') if isinstance(scopus_data, dict) else f'https://www.scopus.com/authid/detail.uri?authorId={scopus_id}'

    wos_data = exec_prof.get('researcher_ids', {}).get('wos', {})
    wos_id = wos_data.get('id', '2411586') if isinstance(wos_data, dict) else str(wos_data)
    wos_url = wos_data.get('url', f'https://www.webofscience.com/wos/author/record/{wos_id}') if isinstance(wos_data, dict) else f'https://www.webofscience.com/wos/author/record/{wos_id}'

    scholar_data = exec_prof.get('researcher_ids', {}).get('scholar', {})
    scholar_url = scholar_data.get('url', 'https://scholar.google.com/citations?user=aWTSEXwAAAAJ&hl=id') if isinstance(scholar_data, dict) else str(scholar_data)

    permit_data = exec_prof.get('official_docs', {}).get('teaching_permit', {})
    permit_url = permit_data.get('url', 'https://tinyurl.com/5n7yjtht') if isinstance(permit_data, dict) else str(permit_data)

    mqa_data = exec_prof.get('official_docs', {}).get('mqa_cv', {})
    mqa_url = mqa_data.get('url', 'https://tinyurl.com/4ehzmxyn') if isinstance(mqa_data, dict) else str(mqa_data)

    portfolio_data = exec_prof.get('official_docs', {}).get('teaching_portfolio', {})
    portfolio_url = portfolio_data.get('url', 'https://tinyurl.com/yjd89mcj') if isinstance(portfolio_data, dict) else str(portfolio_data)

    html = get_html_head(
        get_page_browser_title("cv", "Achievement & Curriculum Vitae | Dr. Zaid Amin | zaidamin.org"),
        "Official Curriculum Vitae and Achievements of Dr. Zaid Amin, Senior Lecturer & QS Deputy Director at INTI International University, Ph.D. from UKM (Tesis Cemerlang & GOT)."
    )
    html += get_page_header("cv")

    if is_cv_download_disabled:
        contact_email = exec_prof.get("contact", {}).get("email", "zaid.amin@newinti.edu.my")
        cv_download_btn_html = f'''<a href="mailto:{contact_email}?subject=Official%20CV%20Request%20-%20Dr.%20Zaid%20Amin" class="cv-round-btn-download cv-btn-disabled" title="Direct PDF download is currently disabled. Click to request verified CV via email.">
                  <span class="cv-round-icon-wrap">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                  </span>
                  <span class="cv-round-labels">
                    <span class="cv-round-kicker">OFFICIAL VERIFIED CV</span>
                    <span class="cv-round-title">Available on Request</span>
                  </span>
                </a>'''
    else:
        cv_download_btn_html = f'''<a href="{cv_pdf_url}" download="Dr_Zaid_Amin_Curriculum_Vitae_July_2026.pdf" target="_blank" rel="noopener" class="cv-round-btn-download" title="Download Verified Academic CV">
                  <span class="cv-round-icon-wrap">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="7 10 12 15 17 10"></polyline>
                      <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                  </span>
                  <span class="cv-round-labels">
                    <span class="cv-round-kicker">OFFICIAL VERIFIED CV</span>
                    <span class="cv-round-title">Download CV (PDF)</span>
                  </span>
                </a>'''

    html += f"""
    <!-- Subpage Content: Achievement & Curriculum Vitae (July 2026 Official Resume) -->
    <div class="cv-page-container">
      
      <!-- Executive Hero Profile Card (Golden Ratio Composition with Left Portrait & Right Download Cluster) -->
      <section class="cv-hero-card">
        <div class="cv-hero-top">
          <!-- LEFT: Official Academic Portrait Frame -->
          <div class="cv-portrait-col">
            <div class="cv-portrait-frame">
              <picture>
                <source srcset="{photo_src}" type="image/webp">
                <img src="{photo_src.replace('.webp', '.png')}" alt="{exec_prof['name']}" class="cv-portrait-img" width="144" height="174" loading="eager">
              </picture>
              <div class="cv-portrait-glare"></div>
            </div>
            <div class="cv-portrait-kicker">
              <span class="cv-portrait-dot"></span>
              <span>{photo_kicker}</span>
            </div>
          </div>

          <!-- CENTER / MAIN: Academic Credentials & Details -->
          <div class="cv-hero-main-block">
            <div class="cv-hero-header-row">
              <div class="cv-hero-headings">
                <div class="cv-section-tag" style="margin-bottom: 6px;">CURRICULUM VITAE &bull; ACADEMIC PORTFOLIO</div>
                <h1 class="cv-hero-name font-cinzel">{exec_prof['name']}</h1>
                <div class="cv-hero-role font-cinzel">
                  {exec_prof['role_title']}
                </div>
                <div class="cv-hero-affiliation">
                  {exec_prof['institution']}
                </div>
              </div>

              <!-- RIGHT: Rounded Rectangle ("round tangle") Download & Print Cluster -->
              <div class="cv-hero-cta-cluster">
                <!-- Primary Download Button (Rounded Rectangle / Capsule) -->
                {cv_download_btn_html}

                <!-- Secondary Action: Print / Save as PDF (Golden Ratio 32px height) -->
                <button type="button" onclick="window.print()" class="cv-round-btn-secondary" title="Print or save one-page verified academic portfolio">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 6 2 18 2 18 9"></polyline>
                    <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                    <rect x="6" y="14" width="12" height="8"></rect>
                  </svg>
                  <span>PRINT / SAVE AS PDF</span>
                </button>

                <!-- Status Verification Pill (Centered on Vertical Axis) -->
                <div class="cv-edition-tag">
                  <span class="cv-edition-status-dot"></span>
                  <span>{edition_label}</span>
                </div>
              </div>
            </div>

            <div class="cv-hero-badges">
              <span class="cv-badge-gold" title="UKM Distinctions">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                {exec_prof['distinction']}
              </span>
              <span class="cv-badge-cyan" title="Global Cisco Grant">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zm0 8.5L4.5 7 12 3.5 19.5 7 12 10.5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                Global Cisco Scholar (Top 40 Worldwide)
              </span>
              <span class="cv-badge-emerald" title="Q1 Peer Reviewer">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                Active Q1 Journal Reviewer
              </span>
            </div>
          </div>
        </div>

        <div class="cv-hero-summary">
          {exec_prof['summary']}
        </div>

        <!-- Two-Tier Harmonious Sub-Layer Dock (Gestalt Common Region & Reduced Visual Noise) -->
        <div class="cv-hero-sublayer">
          <!-- Tier 1: Scholarly & Citation Identifiers -->
          <div class="cv-sublayer-row">
            <div class="cv-sublayer-kicker cv-sublayer-kicker-gold">
              <span class="cv-sublayer-dot cv-sublayer-dot-gold"></span>
              <span>RESEARCH INDICES</span>
            </div>
            <div class="cv-sublayer-pills">
              <a href="{orcid_url}" target="_blank" rel="noopener" class="cv-sublayer-pill" title="ORCID Verified Record: {orcid_id}">
                {render_svg_icon('orcid')} <span><span class="cv-sublayer-dim">ORCID:</span> <strong class="cv-sublayer-val">{orcid_id}</strong></span>
              </a>
              <a href="{scopus_url}" target="_blank" rel="noopener" class="cv-sublayer-pill" title="Scopus Author Profile: {scopus_id}">
                {render_svg_icon('external')} <span><span class="cv-sublayer-dim">Scopus:</span> <strong class="cv-sublayer-val">{scopus_id}</strong></span>
              </a>
              <a href="{wos_url}" target="_blank" rel="noopener" class="cv-sublayer-pill" title="Web of Science Profile: {wos_id}">
                {render_svg_icon('external')} <span><span class="cv-sublayer-dim">WoS:</span> <strong class="cv-sublayer-val">{wos_id}</strong></span>
              </a>
              <a href="{scholar_url}" target="_blank" rel="noopener" class="cv-sublayer-pill" title="Google Scholar Verified Citation Profile">
                {render_svg_icon('scholar')} <span>Google Scholar</span>
              </a>
            </div>
          </div>

          <div class="cv-sublayer-separator"></div>

          <!-- Tier 2: Institutional & Official Accreditation -->
          <div class="cv-sublayer-row">
            <div class="cv-sublayer-kicker cv-sublayer-kicker-cyan">
              <span class="cv-sublayer-dot cv-sublayer-dot-cyan"></span>
              <span>OFFICIAL ACCREDITATION</span>
            </div>
            <div class="cv-sublayer-pills">
              <a href="mailto:{exec_prof['contact']['email']}" class="cv-sublayer-pill" title="Official Institutional Academic Email">
                {render_svg_icon('email')} <span>{exec_prof['contact']['email']}</span>
              </a>
              <a href="{permit_url}" target="_blank" rel="noopener" class="cv-sublayer-pill" title="Higher Education Teaching Permit (Ministry of Higher Education)">
                {render_svg_icon('external')} <span>Teaching Permit</span>
              </a>
              <a href="{mqa_url}" target="_blank" rel="noopener" class="cv-sublayer-pill" title="MQA CV for Higher Education Accreditation">
                {render_svg_icon('external')} <span>MQA Official CV</span>
              </a>
              <a href="{portfolio_url}" target="_blank" rel="noopener" class="cv-sublayer-pill" title="Teaching, Supervision & Examination Portfolio">
                {render_svg_icon('external')} <span>Teaching Portfolio</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Golden Ratio Quick-Jump Navigation Bar (TOC) -->
      <nav class="cv-jump-bar" aria-label="CV Sections Navigation">
        <a href="#honors" class="cv-jump-link">Honors &amp; Grants</a>
        <a href="#leadership" class="cv-jump-link">Leadership</a>
        <a href="#experience" class="cv-jump-link">Appointments</a>
        <a href="#education" class="cv-jump-link">Education</a>
        <a href="#talks" class="cv-jump-link">Media &amp; Talks</a>
        <a href="#peer-review" class="cv-jump-link">Peer Review</a>
        <a href="#certifications" class="cv-jump-link">Certifications</a>
        <a href="#research-monograph" class="cv-jump-link">Book &amp; Research</a>
        <a href="#teaching" class="cv-jump-link">Teaching &amp; Supervision</a>
        <a href="#references" class="cv-jump-link">References</a>
      </nav>

            <!-- SECTION 1: PRESTIGIOUS HONORS, AWARDS & RESEARCH GRANTS -->
      <section id="honors" class="cv-section cv-honors-section">
        <div id="achievements"></div>
        <div class="cv-section-tag">01 / HONORS &amp; DISTINCTIONS</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Prestigious Honors, Awards &amp; Research Grants</h2>
          <span class="cv-section-count">{len(cv['achievements_and_grants'])} Distinctions</span>
        </div>

        <!-- Gestalt Category Filter Dock (Reduced Visual Noise & Instant Hook) -->
        <div class="cv-distinction-filter-dock" role="tablist" aria-label="Filter Honors & Distinctions">
          <button type="button" class="cv-distinction-filter-btn active" onclick="filterDistinctions(this, 'all')">
            <span>All Distinctions</span>
            <span class="cv-filter-count">{len(cv['achievements_and_grants'])}</span>
          </button>
          <button type="button" class="cv-distinction-filter-btn" onclick="filterDistinctions(this, 'awards')">
            <span class="cv-filter-dot cv-filter-dot-gold"></span>
            <span>Honors &amp; Awards</span>
            <span class="cv-filter-count">6</span>
          </button>
          <button type="button" class="cv-distinction-filter-btn" onclick="filterDistinctions(this, 'grants')">
            <span class="cv-filter-dot cv-filter-dot-cyan"></span>
            <span>Competitive Grants</span>
            <span class="cv-filter-count">5</span>
          </button>
          <button type="button" class="cv-distinction-filter-btn" onclick="filterDistinctions(this, 'governance')">
            <span class="cv-filter-dot cv-filter-dot-indigo"></span>
            <span>Governance &amp; Chairs</span>
            <span class="cv-filter-count">5</span>
          </button>
        </div>
    """

    for idx, item in enumerate(cv['achievements_and_grants'], 1):
        theme, cat_group, cat_label = get_distinction_meta(item)
        is_spotlight = item.get('featured')
        highlight_cls = "is-highlight is-spotlight" if is_spotlight else ("is-highlight" if item.get('highlight') else "")
        spotlight_badge = '<span class="pub-strip-featured-pill">★ SPOTLIGHT</span>' if is_spotlight else ""
        
        org_name = item['organization']
        venue_short = org_name.split(',')[0].strip()
        if 'kemendikbudristek' in org_name.lower():
            venue_short = 'Kemendikbudristek'
        elif 'kemristekdikti' in org_name.lower():
            venue_short = 'Kemenristekdikti'
        elif 'visual informatics' in org_name.lower():
            venue_short = 'Institute of Visual Informatics (IVI)'
        elif 'palcomtech' in org_name.lower():
            venue_short = 'PalComTech Institute'
        elif 'cisco learning' in org_name.lower():
            venue_short = 'Cisco Learning Institute'

        img_src = item.get('image')
        img_title = item.get('title')
        img_tag = f'<div class="cv-distinction-media" style="margin:10px 0; border-radius:10px; overflow:hidden; max-height:160px; border:1px solid rgba(212,175,55,0.3);"><img src="{img_src}" alt="{img_title}" loading="lazy" style="width:100%; height:100%; object-fit:cover;"></div>' if (is_spotlight and img_src) else ""

        html += render_cv_strip_card(
            idx=idx,
            cat_pill=item['badge'].upper(),
            year_pill=item['year'],
            venue_chip=venue_short,
            title=item['title'].upper(),
            venue_name=item['organization'],
            sub_extra=cat_label,
            excerpt=item['details'],
            verification_url="",
            secondary_btn_label="",
            secondary_btn_url="",
            featured_pill=spotlight_badge,
            media_html=img_tag,
            extra_classes=f"cv-distinction-card {highlight_cls}",
            data_attrs=f'data-category="{cat_group}"',
            cat_theme=theme
        )

    html += f"""
      </section>

      <!-- SECTION 2: ACADEMIC LEADERSHIP & GOVERNANCE -->
      <section id="leadership" class="cv-section">
        <div class="cv-section-tag">02 / ACADEMIC GOVERNANCE</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Academic Leadership &amp; University Administration</h2>
          <span class="cv-section-count">{len(cv['academic_leadership'])} Positions</span>
        </div>
    """

    for idx, item in enumerate(cv['academic_leadership'], 1):
        inst = item['institution']
        spotlight_badge = '<span class="pub-strip-featured-pill">★ QS DIRECTOR</span>' if idx == 1 else ""

        html += render_cv_strip_card(
            idx=idx,
            cat_pill="GOVERNANCE",
            year_pill=item['period'],
            venue_chip=inst.split(',')[0],
            title=item['role'].upper(),
            venue_name=inst,
            sub_extra=item.get('scope', 'Academic Administration'),
            excerpt=item['responsibilities'],
            verification_url="",
            secondary_btn_label="",
            secondary_btn_url="",
            featured_pill=spotlight_badge,
            extra_classes="is-highlight" if idx == 1 else "",
            cat_theme="indigo"
        )

    html += f"""
      </section>

      <!-- SECTION 3: WORK EXPERIENCE & ACADEMIC APPOINTMENTS -->
      <section id="experience" class="cv-section">
        <div class="cv-section-tag">03 / CAREER APPOINTMENTS</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Professional Work Experience &amp; Academic Appointments</h2>
          <span class="cv-section-count">{len(cv['work_experience'])} Appointments</span>
        </div>
    """

    for idx, item in enumerate(cv['work_experience'], 1):
        inst = item['institution']
        spotlight_badge = '<span class="pub-strip-featured-pill">★ SENIOR FACULTY</span>' if idx == 1 else ""

        html += render_cv_strip_card(
            idx=idx,
            cat_pill="APPOINTMENT",
            year_pill=item['period'],
            venue_chip=inst.split(',')[0],
            title=item['role'].upper(),
            venue_name=inst,
            sub_extra="Career Appointment & Professional Instruction",
            excerpt=item['description'],
            verification_url="",
            secondary_btn_label="",
            secondary_btn_url="",
            featured_pill=spotlight_badge,
            extra_classes="is-highlight" if idx == 1 else "",
            cat_theme="cyan"
        )

    html += f"""
      </section>

      <!-- SECTION 4: EDUCATION & FORMAL QUALIFICATIONS -->
      <section id="education" class="cv-section">
        <div class="cv-section-tag">04 / ACADEMIC CREDENTIALS</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Education &amp; Formal Qualifications</h2>
          <span class="cv-section-count">{len(cv['education'])} Degrees</span>
        </div>
    """

    for idx, item in enumerate(cv['education'], 1):
        deg = item['degree']
        inst = item['institution']
        is_phd = 'ph.d' in deg.lower() or 'doctor' in deg.lower()
        spotlight_badge = '<span class="pub-strip-featured-pill">★ TESIS CEMERLANG &amp; GOT</span>' if is_phd else ""

        html += render_cv_strip_card(
            idx=idx,
            cat_pill="DOCTORAL DEGREE" if is_phd else ("MASTER DEGREE" if 'master' in deg.lower() else "FORMAL DEGREE"),
            year_pill=item['period'],
            venue_chip=inst.split(',')[0],
            title=deg.upper(),
            venue_name=f"{inst} &bull; {item['country']}",
            sub_extra=item.get('distinction', ''),
            excerpt=f"<strong>Core Focus:</strong> {item['focus']}",
            verification_url="",
            secondary_btn_label="",
            secondary_btn_url="",
            featured_pill=spotlight_badge,
            extra_classes="is-highlight is-spotlight" if is_phd else "",
            cat_theme="gold" if is_phd else "cyan"
        )

    html += f"""
      </section>

      <!-- SECTION 5: KEYNOTES, INVITED TALKS & MEDIA -->
      <section id="talks" class="cv-section">
        <div class="cv-section-tag">05 / PUBLIC ENGAGEMENT</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Keynotes, Media &amp; Invited Talks</h2>
          <div style="display:inline-flex; align-items:center; gap:10px;">
            <span class="cv-section-count">{len(cv['invited_talks_and_media'])} Keynotes &amp; Invited Talks</span>
          </div>
        </div>
    """

    talks_data_file = DATA_DIR / "talks.json"
    talks_items = cv.get('invited_talks_and_media', [])
    if talks_data_file.exists():
        loaded_talks = load_json("talks.json")
        if isinstance(loaded_talks, dict) and "talks" in loaded_talks:
            talks_items = loaded_talks["talks"]
        elif isinstance(loaded_talks, list):
            talks_items = loaded_talks

    for idx, item in enumerate(talks_items, 1):
        is_spotlight = item.get('featured')
        spotlight_badge = '<span class="pub-strip-featured-pill">★ SPOTLIGHT TALK</span>' if is_spotlight else ""
        img_src = item.get('image')
        title_str = item.get('title') or item.get('event')
        sub_str = item.get('event') if item.get('title') else item.get('venue', '')
        role_str = item.get('role', 'Keynote Speaker')
        year_str = item.get('year', '2026')
        desc_str = item.get('description') or item.get('details', '')
        
        img_tag = f'<div style="margin:10px 0; border-radius:10px; overflow:hidden; max-height:160px; border:1px solid rgba(212,175,55,0.3);"><img src="{img_src}" alt="{title_str}" style="width:100%; height:100%; object-fit:cover;" loading="lazy"></div>' if (is_spotlight and img_src) else ""

        event_raw = sub_str or 'Keynote Event'
        if 'matcom' in event_raw.lower():
            chip_label = 'MatCom-2026 Conference'
        elif 'ice3is' in event_raw.lower():
            chip_label = 'ICE3IS Conference'
        elif ':' in event_raw:
            chip_label = event_raw.split(':')[0].strip()
        else:
            chip_label = event_raw

        html += render_cv_strip_card(
            idx=idx,
            cat_pill=role_str.upper(),
            year_pill=year_str,
            venue_chip=chip_label,
            title=title_str.upper(),
            venue_name=sub_str,
            sub_extra=role_str,
            excerpt=desc_str,
            verification_url="",
            secondary_btn_label="",
            secondary_btn_url="",
            featured_pill=spotlight_badge,
            media_html=img_tag,
            extra_classes="is-highlight is-spotlight" if is_spotlight else "is-highlight",
            cat_theme="gold" if is_spotlight else "cyan"
        )

    html += f"""
      </section>

      <!-- SECTION 6: PEER REVIEW & EDITORIAL CONTRIBUTIONS -->
      <section id="peer-review" class="cv-section">
        <div class="cv-section-tag">06 / SCHOLARLY RIGOR</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Peer Review &amp; Editorial Board Contributions</h2>
          <span class="cv-section-count">Verified Reviewer &amp; Editorial Board</span>
        </div>
        <p style="font-size: 0.92rem; color: var(--text-body); margin-bottom: 18px; line-height: 1.6;">
          {cv['peer_review_and_editorial']['summary']}
        </p>

        <h3 style="font-size: 1.1rem; font-weight: 800; color: #ffffff; margin-bottom: 14px;">High-Impact Q1 Journals</h3>
        <div class="cv-journals-grid">
    """

    for jnl in cv['peer_review_and_editorial']['verified_journals']:
        html += f"""
          <article class="cv-journal-card">
            <div class="cv-journal-kicker-row">
              <span class="cv-journal-tier font-cinzel">{jnl['tier']}</span>
              <span class="cv-journal-issn">ISSN: {jnl['issn']}</span>
            </div>
            <div class="cv-journal-body">
              <h4 class="cv-journal-title font-cinzel">{jnl['name']}</h4>
              <div class="cv-journal-publisher">{jnl['publisher']}</div>
            </div>
            <div class="cv-journal-footer">
              <a href="{jnl['url']}" target="_blank" rel="noopener" class="cv-journal-link">
                <span>Journal Profile</span>
                <span class="link-arrow">&rarr;</span>
              </a>
            </div>
          </article>
        """

    html += f"""
        </div>

        <h3 style="font-size: 1.1rem; font-weight: 800; color: #ffffff; margin-bottom: 14px;">International Conference Technical Committees</h3>
        <div class="cv-grid-2col">
    """

    for conf in cv['peer_review_and_editorial']['conference_committees']:
        html += f"""
          <div class="cv-mini-card">
            <div style="font-weight: 800; color: #ffffff; font-size: 0.94rem;">{conf['name']}</div>
            <div style="font-size: 0.82rem; color: var(--brand-gold); margin-top: 4px; font-weight: 700;">Role: {conf['role']}</div>
          </div>
        """

    html += f"""
        </div>
      </section>

      <!-- SECTION 7: PROFESSIONAL CERTIFICATIONS & SPECIALIZED TRAINING -->
      <section id="certifications" class="cv-section">
        <div class="cv-section-tag">07 / TECHNICAL MASTERY</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Professional Certifications &amp; Specialized Training</h2>
          <span class="cv-section-count">{len(cv['professional_certifications'])} Credentials</span>
        </div>
        <div class="cv-strip-list">
    """

    for idx, cert in enumerate(cv['professional_certifications'], 1):
        issuer = cert['issuer']
        spotlight_badge = '<span class="pub-strip-featured-pill">★ GRADE A FORENSIC</span>' if idx == 1 else ""

        html += render_cv_strip_card(
            idx=idx,
            cat_pill="CERTIFICATION",
            year_pill=cert['period'],
            venue_chip=issuer.split('/')[0].strip(),
            title=cert['name'].upper(),
            venue_name=issuer,
            sub_extra="Technical Mastery & Professional Accreditation",
            excerpt=cert['details'],
            verification_url="",
            secondary_btn_label="",
            secondary_btn_url="",
            featured_pill=spotlight_badge,
            extra_classes="is-highlight" if idx == 1 else "",
            cat_theme="cyan"
        )

    html += f"""
        </div>
      </section>

      <!-- SECTION 8: CORE RESEARCH, BOOKS & SCHOLARLY MONOGRAPHS -->
      <section id="research-monograph" class="cv-section">
        <div class="cv-section-tag">08 / SCHOLARLY AUTHORSHIP</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Core Research Domains, Book &amp; Scholarly Output</h2>
          <span class="cv-section-count">{len(publications)} Scholarly Works</span>
        </div>

        <!-- Book Card -->
        <div class="cv-card is-highlight" style="margin-bottom: 24px;">
          <div class="cv-card-top">
            <div class="cv-card-heading">
              <span class="cv-type-pill" style="margin-bottom: 6px; display: inline-block;">Scholarly Monograph (Book)</span>
              <h3 class="cv-card-title">{cv['core_research_and_books']['book']['title']}</h3>
              <div class="cv-card-sub">{cv['core_research_and_books']['book']['publisher']} &bull; {cv['core_research_and_books']['book']['year']}</div>
            </div>
            <div class="cv-card-badges">
              <span class="cv-badge-gold">UKM Press Author</span>
            </div>
          </div>
          <div class="cv-card-body">
            {cv['core_research_and_books']['book']['description']}
          </div>
        </div>

        <h3 style="font-size: 1.1rem; font-weight: 800; color: #ffffff; margin-bottom: 14px;">Specialized Research Domains</h3>
        <div class="cv-grid-2col" style="margin-bottom: 24px;">
    """

    for dom in cv['core_research_and_books']['key_domains']:
        html += f"""
          <div class="cv-mini-card">
            <strong style="color: #ffffff; font-size: 0.98rem;">{dom['domain']}</strong>
            <div style="font-size: 0.84rem; color: var(--text-body); margin-top: 6px; line-height: 1.55;">{dom['desc']}</div>
          </div>
        """

    html += f"""
        </div>

        <div style="background: rgba(3, 18, 32, 0.75); border: 1px solid rgba(34, 166, 200, 0.25); border-radius: 14px; padding: 20px 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
          <div>
            <div style="font-weight: 800; color: #ffffff; font-size: 1.05rem;">Complete {len(publications)}-Work Peer-Reviewed Repository</div>
            <div style="font-size: 0.85rem; color: var(--text-body); margin-top: 2px;">Comprehensive catalog of Q1 IEEE Access, Springer LNCS, Scopus-indexed conference papers, and preprints.</div>
          </div>
          <span class="cv-badge-gold" style="font-size: 0.82rem; padding: 6px 14px; font-weight: 700;">Peer-Reviewed Repository</span>
        </div>
      </section>

      <!-- SECTION 9: TEACHING, SUPERVISION & HIGHER EDUCATION PERMITS -->
      <section id="teaching" class="cv-section">
        <div class="cv-section-tag">09 / ACADEMIC PEDAGOGY</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Teaching, Supervision &amp; Accreditation Credentials</h2>
          <a href="{exec_prof['official_docs']['teaching_portfolio']['url']}" target="_blank" rel="noopener" class="cv-section-count" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">
            {render_svg_icon('external')} Full Portfolio Record
          </a>
        </div>
        <div class="cv-grid-3col">
          <div class="cv-mini-card">
            <div class="cv-ref-role" style="color: var(--brand-gold);">Official Government Permit</div>
            <div class="cv-ref-name" style="font-size: 0.95rem; margin-top: 4px;">Higher Education Teaching Permit</div>
            <div style="font-size: 0.82rem; color: var(--text-body); margin-top: 6px; line-height: 1.5;">Authorized for Doctoral, Master, and Bachelor Degree Programs.</div>
            <div style="margin-top: 12px;">
              <a href="{exec_prof['official_docs']['teaching_permit']['url']}" target="_blank" rel="noopener" style="font-size: 0.80rem; color: #38bdf8; text-decoration: none; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                <span>Official Document</span>
                <span>&rarr;</span>
              </a>
            </div>
          </div>
          <div class="cv-mini-card">
            <div class="cv-ref-role" style="color: #38b6d0;">Institutional Accreditation</div>
            <div class="cv-ref-name" style="font-size: 0.95rem; margin-top: 4px;">MQA Official Higher Education CV</div>
            <div style="font-size: 0.82rem; color: var(--text-body); margin-top: 6px; line-height: 1.5;">Malaysian Qualifications Agency standard format for higher education accreditation.</div>
            <div style="margin-top: 12px;">
              <a href="{exec_prof['official_docs']['mqa_cv']['url']}" target="_blank" rel="noopener" style="font-size: 0.80rem; color: #38bdf8; text-decoration: none; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                <span>Official Document</span>
                <span>&rarr;</span>
              </a>
            </div>
          </div>
          <div class="cv-mini-card">
            <div class="cv-ref-role" style="color: #6ee7b7;">Supervisory Roles</div>
            <div class="cv-ref-name" style="font-size: 0.95rem; margin-top: 4px;">Postgraduate Dissertation Supervision</div>
            <div style="font-size: 0.82rem; color: var(--text-body); margin-top: 6px; line-height: 1.5;">Appointed Master and Ph.D. dissertation supervisor at INTI International University and UKM.</div>
            <div style="margin-top: 12px;">
              <a href="/prospective-students" style="font-size: 0.80rem; color: #38bdf8; text-decoration: none; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                <span>Supervision Lab</span>
                <span>&rarr;</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION 10: ACADEMIC REFERENCES & PERSONAL INTERESTS -->
      <section id="references" class="cv-section">
        <div class="cv-section-tag">10 / TESTIMONIALS &amp; PROFILE</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Academic References &amp; Personal Interests</h2>
          <span class="cv-section-count">4 Referees</span>
        </div>

        <div class="cv-strip-list" style="margin-bottom: 28px;">
    """

    for idx, ref in enumerate(cv['academic_references'], 1):
        inst = ref['institution']
        ref_email = ref.get('email', 'zaid.amin@newinti.edu.my')
        ref_phone = ref.get('phone', '')
        contact_str = f"Email: <strong>{ref_email}</strong>" + (f" &bull; Tel: {ref_phone}" if ref_phone else "")
        ref_excerpt = f"Senior Academic Referee & Research Collaborator. Institutional verification point for postgraduate dissertation supervision, research grants, and international appointments. Direct inquiry: {contact_str}"

        html += render_cv_strip_card(
            idx=idx,
            cat_pill="ACADEMIC REFEREE",
            year_pill="Official Referee",
            venue_chip=inst.split(',')[0],
            title=ref['name'].upper(),
            venue_name=inst,
            sub_extra=ref['role'],
            excerpt=ref_excerpt,
            verification_url="",
            secondary_btn_label="CONTACT REFEREE",
            secondary_btn_url=f"mailto:{ref_email}?subject=Academic%20Inquiry%20regarding%20Dr.%20Zaid%20Amin",
            featured_pill="",
            extra_classes="",
            cat_theme="indigo",
            show_verification_btn=False
        )

    html += f"""
        </div>
        <div class="cv-interests-card">
          <div class="cv-interests-header-row">
            <div class="cv-interests-kicker">
              <span class="gem">✦</span>
              <span>Personal Interests &amp; Exploration</span>
            </div>
          </div>
          <div class="cv-interests-chips-grid">
    """

    for interest in cv['personal_interests']:
        html += f"""
            <div class="cv-interest-chip">
              <span class="chip-gem">✦</span>
              <span>{interest}</span>
            </div>
        """

    html += """
          </div>
        </div>

      </section>

    </div>
    """

    
    html += """
    <script>
      function filterDistinctions(btn, cat) {
        const dock = btn.parentElement;
        if (dock) {
          dock.querySelectorAll('.cv-distinction-filter-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        }
        const cards = document.querySelectorAll('.cv-distinction-card');
        cards.forEach(card => {
          const match = (cat === 'all' || card.getAttribute('data-category') === cat);
          if (match) {
            card.classList.remove('is-hidden');
            card.style.removeProperty('display');
          } else {
            card.classList.add('is-hidden');
            card.style.setProperty('display', 'none', 'important');
          }
        });
      }
    </script>
    """

    html += get_page_footer()
    return html


def generate_articles_hub_page():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=research.html#articles">
  <title>Redirecting to Activity & Project | Dr. Zaid Amin</title>
  <link rel="canonical" href="https://zaidamin.org/research.html#articles">
  <script>window.location.replace("research.html#articles");</script>
</head>
<body style="background:#030a14;color:#bae6fd;font-family:sans-serif;padding:60px 20px;text-align:center;">
  <p>Redirecting to <a href="/research#articles" style="color:#d4af37;font-weight:bold;">Activity &amp; Project &rarr; Articles &amp; Essays</a>...</p>
</body>
</html>
"""
def generate_article_reader_page():
    html = get_html_head("Article Reader | Dr. Zaid Amin | zaidamin.org", "Read scholarly essays, research commentaries, and educational discourse by Dr. Zaid Amin.")
    html += get_page_header("articles")

    reader_script = """
    <script>
      (async function() {
        const params = new URLSearchParams(window.location.search);
        const articleId = params.get('id');

        window.addEventListener('scroll', () => {
          const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
          const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
          const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
          const bar = document.getElementById('reading-progress');
          if (bar) bar.style.width = scrolled + '%';
        });

        try {
          const res = await fetch('data/articles.json');
          const articles = await res.json();

          let article = null;
          if (articleId) {
            article = articles.find(a => a.id === articleId);
          }
          if (!article && articles.length > 0) {
            article = articles[0];
          }

          if (article) {
            document.title = article.title + ' | Dr. Zaid Amin';
            document.getElementById('reader-title').textContent = article.title;
            document.getElementById('reader-cat').textContent = '✦ ' + (article.category || 'Article');
            document.getElementById('reader-time').textContent = article.reading_time || '3 min read';
            document.getElementById('reader-date').textContent = 'Published • ' + article.date;
            const bodyElem = document.getElementById('reader-body');
            bodyElem.innerHTML = article.content_html || ('<p>' + article.excerpt + '</p>');

            // 1. Clean up any missing, corrupt, or 404 images dynamically
            bodyElem.querySelectorAll('img').forEach(function(img) {
              img.addEventListener('error', function() {
                var parentA = this.closest('a');
                var parentBox = this.closest('.separator') || this.closest('.tr-caption-container') || this.parentElement;
                if (parentA) parentA.remove();
                else this.remove();
                if (parentBox && !parentBox.textContent.trim() && parentBox.querySelectorAll('img').length === 0) {
                  parentBox.remove();
                }
              });
            });

            // 2. Client-side deduplication against Hero image
            if (article.image) {
              var heroFileName = article.image.split('/').pop().split('?')[0];
              bodyElem.querySelectorAll('img').forEach(function(img) {
                var src = img.getAttribute('src') || '';
                if (src === article.image || (heroFileName && heroFileName.length > 5 && src.includes(heroFileName))) {
                  var parentA = img.closest('a');
                  var parentBox = img.closest('.separator') || img.closest('.tr-caption-container') || img.parentElement;
                  if (parentA) parentA.remove();
                  else img.remove();
                  if (parentBox && !parentBox.textContent.trim() && parentBox.querySelectorAll('img').length === 0) {
                    parentBox.remove();
                  }
                }
              });
            }

            // 3. Dynamic guarantee against inline white highlights or backgrounds
            bodyElem.querySelectorAll('*').forEach(function(el) {
              if (el.style.backgroundColor && el.style.backgroundColor !== 'transparent') {
                el.style.backgroundColor = 'transparent';
              }
              if (el.style.background && !el.style.background.includes('gradient')) {
                el.style.background = 'transparent';
              }
            });

            if (article.image) {
              const imgWrap = document.getElementById('reader-hero-img-wrap');
              const img = document.getElementById('reader-hero-img');
              img.src = article.image;
              img.alt = article.title;
              img.onerror = function() {
                imgWrap.style.display = 'none';
              };
              imgWrap.style.display = 'block';
            }

            const pageUrl = encodeURIComponent(window.location.href);
            const titleEnc = encodeURIComponent(article.title);
            const shareLi = document.getElementById('share-linkedin');
            const shareX = document.getElementById('share-x');
            if (shareLi) shareLi.href = 'https://www.linkedin.com/sharing/share-offsite/?url=' + pageUrl;
            if (shareX) shareX.href = 'https://twitter.com/intent/tweet?text=' + titleEnc + '&url=' + pageUrl;
          } else {
            document.getElementById('reader-title').textContent = 'Article Not Found';
            document.getElementById('reader-body').innerHTML = '<p>The requested article could not be located. <a href="/research#articles">Browse all articles &rarr;</a></p>';
          }
        } catch (err) {
          console.error(err);
          document.getElementById('reader-body').innerHTML = '<p>Error loading article. <a href="/research#articles">Back to Activity &amp; Project &rarr;</a></p>';
        }
      })();

      function copyArticleLink() {
        navigator.clipboard.writeText(window.location.href).then(() => {
          const btn = document.getElementById('copy-btn-text');
          if (btn) {
            btn.textContent = 'Copied!';
            setTimeout(() => { btn.textContent = 'Copy Link'; }, 2500);
          }
        }).catch(() => {
          prompt('Copy article link:', window.location.href);
        });
      }
    </script>
"""

    html += f"""
    <!-- Reading Progress Bar -->
    <div class="article-reading-progress-bar" id="reading-progress"></div>

    <main class="article-reader-container" id="article-reader-root">
      <!-- Back Link -->
      <div class="article-back-bar">
        <a href="/research#articles" class="article-back-link font-cinzel">&larr; Back to Activity &amp; Project</a>
      </div>

      <!-- Article Header -->
      <header class="article-reader-hero">
        <div class="article-hero-kicker-row">
          <span class="article-badge-cat" id="reader-cat">&#10022; Article</span>
          <span class="article-time-badge" id="reader-time">5 min read</span>
        </div>

        <h1 class="article-reader-title" id="reader-title">Loading Article...</h1>

        <div class="article-reader-meta-row">
          <div class="article-author-cluster">
            <picture>
              <source srcset="assets/images/dr-zaid.webp" type="image/webp">
              <img src="assets/images/dr-zaid.png" alt="Dr. Zaid Amin" class="article-author-avatar">
            </picture>
            <div>
              <div class="article-author-name">Dr. Zaid Amin</div>
              <div class="article-pub-date" id="reader-date">Published &bull; 2026</div>
            </div>
          </div>

          <div class="article-share-group">
            <button class="article-share-btn" onclick="copyArticleLink()" title="Copy Link to Clipboard">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
              <span id="copy-btn-text">Copy Link</span>
            </button>
            <a href="#" id="share-linkedin" target="_blank" rel="noopener" class="article-share-btn" title="Share on LinkedIn">
              <span>LinkedIn &nearr;</span>
            </a>
            <a href="#" id="share-x" target="_blank" rel="noopener" class="article-share-btn" title="Share on X (Twitter)">
              <span>X &nearr;</span>
            </a>
          </div>
        </div>

        <div id="reader-hero-img-wrap" style="display: none;">
          <img src="" alt="Hero Image" id="reader-hero-img" class="article-hero-banner">
        </div>
      </header>

      <!-- Article Body Content -->
      <article class="article-reader-body" id="reader-body">
        <p style="text-align: center; color: #94a3b8; padding: 40px;">Loading article content...</p>
      </article>

      <!-- Author Bio Box -->
      <div class="article-author-bio-card">
        <picture>
          <source srcset="assets/images/dr-zaid.webp" type="image/webp">
          <img src="assets/images/dr-zaid.png" alt="Dr. Zaid Amin" class="article-bio-avatar">
        </picture>
        <div>
          <h3 class="article-bio-name font-cinzel">Dr. Zaid Amin</h3>
          <div class="article-bio-role">Senior Lecturer &bull; INTI International University, Malaysia</div>
          <p class="article-bio-text">
            Computational researcher in Human-Computer Interaction (HCI), Behavior &amp; Social Computing, Digital Ethics, and AI Governance. Ph.D. in Computer Science from Universiti Kebangsaan Malaysia (UKM).
          </p>
        </div>
      </div>

      <!-- Navigation back to hub -->
      <div style="margin-top: 40px; text-align: center;">
        <a href="/research#articles" class="spotlight-btn btn-gold font-cinzel" style="text-decoration: none; display: inline-block;">
          &larr; Explore All Activity &amp; Articles
        </a>
      </div>
    </main>
    {reader_script}
"""
    html += get_page_footer(show_visitor_stats=False)
    return html


# ==============================================================================
# RESEARCH TEAM & SUPERVISION ROSTER (research-team.html)
# ==============================================================================
def generate_team_page():
    team_data = load_json("team.json")
    page_head = get_html_head(
        get_page_browser_title("team", "Research Team & Supervision Roster | Dr. Zaid Amin"),
        "Doctoral candidates, Master's by Research scholars, and international research collaborators under the academic supervision and mentorship of Dr. Zaid Amin."
    )
    page_header = get_page_header("team")

    # Render PhD cards
    phd_cards = ""
    for s in team_data.get("phd_students", []):
        phd_cards += f"""
          <article class="team-card" data-category="phd">
            <div class="team-avatar-frame">
              <img src="{s['photo']}" alt="{s['name']}" class="team-avatar-img" onerror="this.src='assets/images/avatar.svg'">
            </div>
            <div class="team-info-stack">
              <div class="team-card-header-row">
                <h3 class="team-person-name font-cinzel">{s['name']}</h3>
                <span class="team-badge font-cinzel">{s.get('badge', 'Doctoral Research')}</span>
              </div>
              <div class="team-role-period">
                <span class="team-role">{s['role']}</span>, <span class="team-period">{s['period']}</span>
              </div>
              <div class="team-thesis-text">
                <span class="thesis-label">Thesis title:</span> &ldquo;{s['thesis_title']}&rdquo;
              </div>
            </div>
          </article>
        """

    # Render Master cards
    master_cards = ""
    for s in team_data.get("master_students", []):
        master_cards += f"""
          <article class="team-card" data-category="master">
            <div class="team-avatar-frame">
              <img src="{s['photo']}" alt="{s['name']}" class="team-avatar-img" onerror="this.src='assets/images/avatar.svg'">
            </div>
            <div class="team-info-stack">
              <div class="team-card-header-row">
                <h3 class="team-person-name font-cinzel">{s['name']}</h3>
                <span class="team-badge font-cinzel">{s.get('badge', "Postgraduate Scholar")}</span>
              </div>
              <div class="team-role-period">
                <span class="team-role">{s['role']}</span>, <span class="team-period">{s['period']}</span>
              </div>
              <div class="team-thesis-text">
                <span class="thesis-label">Thesis title:</span> &ldquo;{s['thesis_title']}&rdquo;
              </div>
            </div>
          </article>
        """

    # Render Collaborator cards
    collab_cards = ""
    for c in team_data.get("collaborators", []):
        collab_cards += f"""
          <article class="team-card team-card-collab" data-category="collaborator">
            <div class="team-avatar-frame">
              <img src="{c['photo']}" alt="{c['name']}" class="team-avatar-img" onerror="this.src='assets/images/avatar.svg'">
            </div>
            <div class="team-info-stack">
              <div class="team-card-header-row">
                <h3 class="team-person-name font-cinzel">{c['name']}</h3>
                <span class="team-badge font-cinzel">{c.get('badge', 'Academic Collaborator')}</span>
              </div>
              <div class="team-role-period">
                <span class="team-role">{c['role']}</span> &bull; <span class="team-period">{c['period']}</span>
              </div>
              <div class="team-inst-text">{c.get('institution', '')}</div>
              <div class="team-thesis-text">
                <span class="thesis-label">Collaboration Focus:</span> &ldquo;{c['focus']}&rdquo;
              </div>
            </div>
          </article>
        """

    team_script = """
    <script>
      function filterTeam(cat, btn) {
        document.querySelectorAll('.team-filter-pill').forEach(function(b) {
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        });
        if (btn) {
          btn.classList.add('active');
          btn.setAttribute('aria-selected', 'true');
        }
        var sections = document.querySelectorAll('.team-category-section');
        sections.forEach(function(sec) {
          if (cat === 'all' || sec.getAttribute('data-category') === cat) {
            sec.style.display = 'block';
          } else {
            sec.style.display = 'none';
          }
        });
      }

      window.addEventListener('DOMContentLoaded', function() {
        var hash = window.location.hash;
        if (hash === '#cat-phd') {
          var btn = document.querySelector('.team-filter-pill[onclick*="phd"]');
          if (btn) filterTeam('phd', btn);
        } else if (hash === '#cat-master') {
          var btn = document.querySelector('.team-filter-pill[onclick*="master"]');
          if (btn) filterTeam('master', btn);
        } else if (hash === '#cat-collaborator') {
          var btn = document.querySelector('.team-filter-pill[onclick*="collaborator"]');
          if (btn) filterTeam('collaborator', btn);
        }
      });
    </script>
    """

    meta = team_data.get("page_meta", {})
    eyebrow_text = meta.get("eyebrow", "✦ Academic Mentorship • Laboratory Scholars • Global Network").replace('✦', '').strip()
    title_text = meta.get("title", "Research Team")
    subtitle_text = meta.get("subtitle", "Doctoral candidates, Master's by Research scholars, and international research collaborators under the academic supervision and mentorship of Dr. Zaid Amin.")

    statement_text = team_data.get("statement", "").strip()
    statement_html = ""
    if statement_text:
        statement_html = f"""
      <div style="margin: -10px auto 32px auto; max-width: 960px; padding: 18px 26px; background: rgba(8, 20, 36, 0.65); border: 1px solid rgba(56, 189, 248, 0.22); border-left: 3px solid #d4af37; border-radius: 12px; backdrop-filter: blur(8px); text-align: center;">
        <p style="font-family: var(--font-cormorant); font-size: 1.15rem; font-style: italic; color: #bae6fd; margin: 0; line-height: 1.6;">
          &ldquo;{statement_text}&rdquo;
        </p>
      </div>
        """

    phd_count = len(team_data.get("phd_students", []))
    master_count = len(team_data.get("master_students", []))
    collab_count = len(team_data.get("collaborators", []))
    total_count = phd_count + master_count + collab_count

    cta = team_data.get("cta_banner", {})
    cta_eyebrow = cta.get("eyebrow", "✦ Postgraduate Admissions & Supervision")
    cta_title = cta.get("title", "Interested in Joining Our Research Lab?")
    cta_desc = cta.get("description", "Dr. Zaid Amin is actively seeking self-driven Ph.D. and Master's candidates interested in Human-Computer Interaction, AI Governance, Multimodal Foundation Models, and Cognitive Attention Systems.")
    cta_p_text = cta.get("primary_btn_text", "View Open Topics & How to Apply →")
    cta_p_url = cta.get("primary_btn_url", "prospective-students.html")
    cta_s_text = cta.get("secondary_btn_text", "Submit Research Inquiry ↗")
    cta_s_url = cta.get("secondary_btn_url", "mailto:zaid.amin@newinti.edu.my")

    body_html = f"""
    <!-- Subpage Content: Research Team & Supervision Roster -->
    <div class="subpage-container team-page-container">
      <div class="pub-gallery-hero team-hero-header">
        <div class="subpage-eyebrow"><span class="eyebrow-dot">✦</span> {eyebrow_text}</div>
        <h1 class="pub-gallery-title font-cinzel">{title_text}</h1>
        <p class="pub-gallery-subtitle">
          {subtitle_text}
        </p>
      </div>

      {statement_html}

      <!-- Category Filter Controls -->
      <div class="team-nav-pills" role="tablist" aria-label="Team Categories">
        <button class="team-filter-pill active" onclick="filterTeam('all', this)" role="tab" aria-selected="true">✦ All Members ({total_count})</button>
        <button class="team-filter-pill" onclick="filterTeam('phd', this)" role="tab" aria-selected="false">01. PhD Students ({phd_count})</button>
        <button class="team-filter-pill" onclick="filterTeam('master', this)" role="tab" aria-selected="false">02. Master Students ({master_count})</button>
        <button class="team-filter-pill" onclick="filterTeam('collaborator', this)" role="tab" aria-selected="false">03. Collaborators ({collab_count})</button>
      </div>

      <!-- SECTION 1: PhD Students -->
      <section class="team-category-section" id="cat-phd" data-category="phd">
        <div class="team-category-header">
          <div class="team-category-title-wrap">
            <span class="team-category-num font-cinzel">01</span>
            <h2 class="team-category-title font-cinzel">PhD Students</h2>
          </div>
          <span class="team-category-count font-cinzel">{phd_count} Doctoral Candidates</span>
        </div>
        <div class="team-grid-2col">
          {phd_cards}
        </div>
      </section>

      <!-- SECTION 2: Master Students -->
      <section class="team-category-section" id="cat-master" data-category="master">
        <div class="team-category-header">
          <div class="team-category-title-wrap">
            <span class="team-category-num font-cinzel">02</span>
            <h2 class="team-category-title font-cinzel">Master Students</h2>
          </div>
          <span class="team-category-count font-cinzel">{master_count} Master's by Research Scholars</span>
        </div>
        <div class="team-grid-2col">
          {master_cards}
        </div>
      </section>

      <!-- SECTION 3: Collaborators -->
      <section class="team-category-section" id="cat-collaborator" data-category="collaborator">
        <div class="team-category-header">
          <div class="team-category-title-wrap">
            <span class="team-category-num font-cinzel">03</span>
            <h2 class="team-category-title font-cinzel">Collaborators</h2>
          </div>
          <span class="team-category-count font-cinzel">{collab_count} International Scholarly Partners</span>
        </div>
        <div class="team-grid-2col">
          {collab_cards}
        </div>
      </section>

      <!-- Supervision & Laboratory Inquiries CTA -->
      <div class="team-cta-banner">
        <div class="team-cta-content">
          <span class="team-cta-eyebrow font-cinzel">{cta_eyebrow}</span>
          <h3 class="team-cta-title font-cinzel">{cta_title}</h3>
          <p class="team-cta-desc">{cta_desc}</p>
          <div class="team-cta-btns">
            <a href="{cta_p_url}" class="team-cta-btn-primary">{cta_p_text}</a>
            <a href="{cta_s_url}" class="team-cta-btn-secondary">{cta_s_text}</a>
          </div>
        </div>
      </div>
    </div>
    """

    return page_head + page_header + body_html + team_script + get_page_footer()

def generate_cms_portal_page():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Force HTTPS Protocol & Auto-Upgrade Insecure Resources -->
  <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
  <script>
    if (location.protocol === 'http:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {{
      location.replace('https://' + location.hostname + location.pathname + location.search + location.hash);
    }}
  </script>
  <title>CMS Studio Portal • Dr. Zaid Amin</title>
  <link rel="icon" type="image/png" href="../favicon-32x32.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; }
    body {
      background: radial-gradient(circle at 50% 20%, #06182c 0%, #020b14 70%);
      color: #e2e8f0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      font-family: 'Inter', -apple-system, sans-serif;
      margin: 0;
      padding: 24px;
    }
    .cms-bridge-card {
      max-width: 640px;
      width: 100%;
      background: rgba(8, 23, 38, 0.9);
      border: 1px solid rgba(212, 175, 55, 0.35);
      border-radius: 16px;
      padding: 44px 40px;
      box-shadow: 0 24px 64px rgba(0, 0, 0, 0.7), 0 0 32px rgba(56, 189, 248, 0.1);
      backdrop-filter: blur(12px);
      text-align: center;
      position: relative;
    }
    .cms-bridge-emblem {
      width: 64px;
      height: 64px;
      margin: 0 auto 20px;
      border-radius: 50%;
      background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(56, 189, 248, 0.2));
      border: 1px solid rgba(212, 175, 55, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fce09b;
      box-shadow: 0 0 24px rgba(212, 175, 55, 0.3);
    }
    .cms-bridge-title {
      font-family: 'Cinzel', serif;
      font-size: 1.85rem;
      color: #fce09b;
      margin: 0 0 8px;
      letter-spacing: 0.05em;
    }
    .cms-bridge-subtitle {
      color: #94a3b8;
      font-size: 0.85rem;
      margin: 0 0 28px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
    }
    .cms-status-box {
      background: rgba(2, 11, 20, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 28px;
      text-align: left;
    }
    .cms-status-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 0.82rem;
      padding: 5px 12px;
      border-radius: 20px;
      background: rgba(34, 197, 94, 0.15);
      border: 1px solid rgba(34, 197, 94, 0.4);
      color: #4ade80;
    }
    .status-badge.offline {
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.4);
      color: #f87171;
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #4ade80;
      box-shadow: 0 0 8px #4ade80;
      animation: pulse 2s infinite;
    }
    .pulse-dot.red {
      background: #f87171;
      box-shadow: 0 0 8px #f87171;
      animation: none;
    }
    @keyframes pulse {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.2); }
      100% { opacity: 1; transform: scale(1); }
    }
    .cms-note {
      font-size: 0.9rem;
      color: #cbd5e1;
      line-height: 1.6;
      margin: 0;
    }
    .cms-btn-primary {
      display: block;
      width: 100%;
      padding: 15px 24px;
      background: linear-gradient(135deg, #d4af37 0%, #b89628 100%);
      color: #020b14;
      font-family: 'Cinzel', serif;
      font-weight: 700;
      font-size: 1.05rem;
      letter-spacing: 0.05em;
      border-radius: 8px;
      text-decoration: none;
      box-shadow: 0 8px 24px rgba(212, 175, 55, 0.35);
      transition: all 0.25s ease;
      margin-bottom: 14px;
    }
    .cms-btn-primary:hover {
      background: linear-gradient(135deg, #fce09b 0%, #d4af37 100%);
      transform: translateY(-2px);
      box-shadow: 0 12px 28px rgba(212, 175, 55, 0.5);
    }
    .cms-btn-secondary {
      display: inline-block;
      color: #94a3b8;
      font-size: 0.88rem;
      text-decoration: none;
      padding: 8px 16px;
      transition: color 0.2s ease;
    }
    .cms-btn-secondary:hover {
      color: #fce09b;
    }
    .quick-start-code {
      background: rgba(0, 0, 0, 0.5);
      border: 1px dashed rgba(212, 175, 55, 0.3);
      padding: 12px 16px;
      border-radius: 8px;
      font-family: monospace;
      font-size: 0.85rem;
      color: #38bdf8;
      margin: 14px 0 0;
    }
  </style>
</head>
<body>
  <div class="cms-bridge-card">
    <div class="cms-bridge-emblem">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 20h9"/>
        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
      </svg>
    </div>
    
    <h1 class="cms-bridge-title">Academic CMS Studio</h1>
    <p class="cms-bridge-subtitle">Secure Local Editorial &amp; Authoring Environment</p>
    
    <div class="cms-status-box">
      <div class="cms-status-header">
        <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">STUDIO ENVIRONMENT</span>
        <span id="status-pill" class="status-badge">
          <span class="pulse-dot"></span> Checking Local Server...
        </span>
      </div>
      <p class="cms-note">
        Dr. Zaid Amin's Editorial CMS runs inside your local workspace at <strong style="color:#fce09b;">http://localhost:8000/cms.html</strong> to protect your website datasets and ensure private, authenticated authoring before publishing live.
      </p>
      <div class="quick-start-code" id="start-hint">
        Click below to launch your editor, or run <strong>open_cms.bat</strong> on your computer.
      </div>
    </div>
    
    <a id="cms-launch-btn" href="http://localhost:8000/cms.html" class="cms-btn-primary">
      Open Local CMS Editor &rarr;
    </a>
    
    <a href="../index.html" class="cms-btn-secondary">
      &larr; Return to Public Website (zaidamin.org)
    </a>
  </div>

  <script>
    // Live probe to verify if localhost:8000 preview server is active
    fetch('http://localhost:8000/api/auth', { method: 'GET', mode: 'no-cors' })
      .then(() => {
        const pill = document.getElementById('status-pill');
        if (pill) {
          pill.className = 'status-badge';
          pill.innerHTML = '<span class="pulse-dot"></span> Active on Port 8000';
        }
        const hint = document.getElementById('start-hint');
        if (hint) {
          hint.innerHTML = '✓ Local server is active. Click the button above to enter CMS Studio.';
          hint.style.borderColor = 'rgba(34, 197, 94, 0.4)';
          hint.style.color = '#86efac';
        }
      })
      .catch(() => {
        const pill = document.getElementById('status-pill');
        if (pill) {
          pill.className = 'status-badge offline';
          pill.innerHTML = '<span class="pulse-dot red"></span> Local Server Inactive';
        }
        const hint = document.getElementById('start-hint');
        if (hint) {
          hint.innerHTML = 'To start: double-click <strong>open_cms.bat</strong> in your project folder.';
        }
      });
  </script>
</body>
</html>
"""

def build_all():
    print("Compiling Golden Ratio Standard Academic Site for zaidamin.org...")
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    pages = {
        "index.html": generate_golden_ratio_home(),
        "publications.html": generate_publications_page(),
        "articles.html": generate_articles_hub_page(),
        "article.html": generate_article_reader_page(),
        "research.html": generate_research_page(),
        "prospective-students.html": generate_supervision_page(),
        "research-team.html": generate_team_page(),
        "team.html": generate_team_page(),
        "talks.html": generate_talks_page(),
        "cv.html": generate_cv_page()
    }

    for filename, content in pages.items():
        with open(DIST_DIR / filename, "w", encoding="utf-8") as f:
            f.write(content)
        # Keep at workspace root for immediate preview
        with open(BASE_DIR / filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Compiled: {filename} ({len(content)} chars)")

    # Copy assets
    dist_assets = DIST_DIR / "assets"
    if dist_assets.exists():
        shutil.rmtree(dist_assets)
    shutil.copytree(ASSETS_DIR, dist_assets)

    # Copy data directory (for articles.json & search items)
    dist_data = DIST_DIR / "data"
    if dist_data.exists():
        shutil.rmtree(dist_data)
    shutil.copytree(DATA_DIR, dist_data)

    # Note: root cms.html is strictly offline/local only for security.
    # We generate a secure CMS Portal bridge for /cms and dist/cms.html
    cms_portal_html = generate_cms_portal_page()
    with open(DIST_DIR / "cms.html", "w", encoding="utf-8") as f:
        f.write(cms_portal_html)

    # Generate Clean URL Folders (e.g. /publications/index.html so .html is stripped from address bar)
    clean_routes = {
        "publications": pages["publications.html"],
        "articles": pages["articles.html"],
        "article": pages["article.html"],
        "research": pages["research.html"],
        "prospective-students": pages["prospective-students.html"],
        "research-team": pages["research-team.html"],
        "team": pages["research-team.html"],
        "talks": pages["talks.html"],
        "cv": pages["cv.html"],
        "cms": cms_portal_html
    }
    for route_name, page_content in clean_routes.items():
        route_dist = DIST_DIR / route_name
        route_dist.mkdir(parents=True, exist_ok=True)
        with open(route_dist / "index.html", "w", encoding="utf-8") as f:
            f.write(page_content)
        route_base = BASE_DIR / route_name
        route_base.mkdir(parents=True, exist_ok=True)
        with open(route_base / "index.html", "w", encoding="utf-8") as f:
            f.write(page_content)

    # Copy CNAME, favicon, BibTeX, site.webmanifest
    for extra in [".nojekyll", "CNAME", "favicon.ico", "favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png", "android-chrome-192x192.png", "android-chrome-512x512.png", "favicon.png", "faviconzaid.png", "site.webmanifest", "data/publications.bib"]:
        src = BASE_DIR / extra
        if src.exists():
            shutil.copy(src, DIST_DIR / Path(extra).name)

    print("Golden Ratio build complete!")

if __name__ == "__main__":
    build_all()
