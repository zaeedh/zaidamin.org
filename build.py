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
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DIST_DIR = BASE_DIR / "dist"
ASSETS_DIR = BASE_DIR / "assets"

def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)

def render_svg_icon(name):
    icons = {
        "scholar": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 24a7 7 0 1 1 0-14 7 7 0 0 1 0 14zm0-24L0 9.5l4.8 3.8v6.7L12 24l7.2-4v-6.7l4.8-3.8L12 0zm0 3.7l7.1 5.8-7.1 5.8-7.1-5.8 7.1-5.8z"/></svg>',
        "orcid": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.306v7.444h2.297c2.359 0 3.8-1.381 3.8-3.722 0-2.203-1.406-3.722-3.8-3.722h-2.297z"/></svg>',
        "github": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>',
        "linkedin": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>',
        "email": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>',
        "arrow-right": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>',
        "arrow-left": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>',
        "external": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>',
        "download": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>',
        "search": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'
    }
    return icons.get(name, "")

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
  <link rel="stylesheet" href="assets/css/style.css?v=3.8">
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

def get_page_header(active_page="home"):
    profile = load_json("profile.json")
    star_svg = '''<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" class="david-star-svg">
      <polygon points="12,2 20.66,17 3.34,17" />
      <polygon points="12,22 3.34,7 20.66,7" />
    </svg>'''
    return f"""
  <div class="site-wrapper">
    
    <!-- 1. Top Epigraph: Das Sein, Das Sollen & Top-Right Star of David with Side Links -->
    <header class="epigraph-header">
      <div class="epigraph-top-flex">
        <div class="epigraph-title-group">
          <h1 class="epigraph-title">Das Sein, Das Sollen.</h1>
          <div class="epigraph-golden-line" aria-hidden="true"></div>
        </div>
        
        <div class="epigraph-right-cluster">
          {f'''<nav class="top-epigraph-menu" id="top-main-nav" aria-label="Main Navigation">
            <a href="index.html" class="main-menu-link {'active' if active_page == 'home' else ''}" title="Home" aria-label="Home">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px;" aria-hidden="true">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
            </a>
            <a href="publications.html" class="main-menu-link {'active' if active_page == 'publications' else ''}">Research &amp; Publication</a>
            <a href="research.html" class="main-menu-link {'active' if active_page in ['research', 'articles'] else ''}">Activity &amp; Project</a>
            <a href="talks.html" class="main-menu-link {'active' if active_page == 'talks' else ''}">Media &amp; Talks</a>
            <a href="cv.html" class="main-menu-link {'active' if active_page in ['cv', 'achievements'] else ''}">Achievement &amp; CV</a>
          </nav>''' if active_page != 'home' else ''}

          <!-- Top-Right Star of David Button & Side-Expanding Scholarly Profiles -->
          <div class="top-scholarly-cluster">
            <div class="top-scholarly-links" id="top-scholarly-links" aria-hidden="true">
              <a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" class="top-link-pill" title="Google Scholar">{render_svg_icon('scholar')} <span>Google Scholar</span></a>
              <a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" class="top-link-pill" title="ORCID">{render_svg_icon('orcid')} <span>ORCID</span></a>
              <a href="{profile['social_links']['github']}" target="_blank" rel="noopener" class="top-link-pill" title="GitHub">{render_svg_icon('github')} <span>GitHub</span></a>
              <a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="top-link-pill" title="LinkedIn">{render_svg_icon('linkedin')} <span>LinkedIn</span></a>
              <a href="mailto:{profile['social_links']['email']}" class="top-link-pill" title="Institutional Email">{render_svg_icon('email')} <span>Institutional Email</span></a>
            </div>

            <!-- Pure Rotating Star of David Button (No circle boundary!) -->
            <button class="david-star-pure-btn" id="star-toggle-btn" aria-label="Toggle Scholarly Profiles" title="Scholarly Profiles & Direct Identifiers" aria-expanded="false">
              <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" class="david-star-svg">
                <polygon points="12,2 20.66,17 3.34,17" />
                <polygon points="12,22 3.34,7 20.66,7" />
              </svg>
            </button>
          </div>
        </div>

      </div>
    </header>

<!-- 2. Clean, Unobstructed Lighthouse Storm Banner (Option 1 Storm - Active on Every Page) -->
    <section class="lighthouse-banner-frame">
      <picture>
        <source srcset="assets/images/lighthouse-banner.webp" type="image/webp">
        <img src="assets/images/lighthouse-banner.jpg" class="lighthouse-bg-img" alt="Lighthouse Storm over Ocean" width="2048" height="790">
      </picture>
      <canvas id="rain-canvas"></canvas>

      <!-- Qur'an Quotation Overlay (Followed Red Arrow: Blended, Soft, Elegant & Premium over the Ocean) -->
      <div class="storm-quote-overlay">
        <p class="storm-quote-text font-serif">
          &ldquo;If all the trees on earth were pens and the ocean were ink, refilled by seven other oceans, the Words of Allah would not be exhausted. Surely Allah is Almighty, All-Wise.&rdquo;
        </p>
        <cite class="storm-quote-cite font-cinzel">
          <span class="storm-cite-line"></span>
          <span class="storm-cite-label">Qur&rsquo;an 31:27</span>
        </cite>
      </div>
    </section>

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

    <!-- Site Footer -->
    <footer class="golden-footer">
      <div class="footer-left">
        Copyright &copy; 2008 - 2026 Zaid Amin. All Rights Reserved.
      </div>
    </footer>

    <!-- Floating Scroll to Top Direct Button -->
    <button class="scroll-to-top-btn" id="scroll-to-top" aria-label="Scroll directly to top" title="Scroll to Top" type="button">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
      </svg>
    </button>

  </div>


  <script src="assets/js/rain-lighting.js"></script>
  <script src="assets/js/main.js?v=3.6"></script>
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
        desc = item.get("excerpt", "")
        img_src = item.get("image", "assets/images/spotlight-smart-cities.jpg")
        kicker_badge = "SPOTLIGHT ARTICLE"
        clean_cat = re.sub(r'^[✦✧★\s\u2726]+', '', str(cat_name)).strip()
        top_kicker = f"{clean_cat.upper()} &bull; ESSAYS & PERSPECTIVES"
        btn_text = "Read Full Essay &rarr;"
        target_blank = ""
        meta_oa = f'<span class="spotlight-oa-pill font-cinzel"><span class="oa-check">&#10003;</span> Open Access Essay</span>'
        author_pre = "Author"
        author_name = "Dr. Zaid Amin, Ph.D."
        secondary_pill = '<a href="research.html#articles" class="spotlight-doi-pill font-cinzel" title="Explore All Activity &amp; Articles"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg> All Activity &nearr;</a>'

    elif source == "talk":
        title = item.get("title", item.get("event", "Keynote Address"))
        venue = item.get("event", "International Symposium")
        year_val = item.get("year", "2026")
        location = item.get("location", "Kuala Lumpur, Malaysia")
        year_str = f"{year_val} &bull; {location}"
        url = item.get("url") or "talks.html"
        desc = item.get("description", item.get("details", ""))
        img_src = item.get("image", "assets/images/spotlight-smart-cities.jpg")
        role_str = item.get("role", "Keynote Speaker")
        type_str = item.get("type", "Keynote")
        kicker_badge = "SPOTLIGHT KEYNOTE"
        clean_type = re.sub(r'^[✦✧★\s\u2726]+', '', str(type_str)).strip()
        top_kicker = f"{clean_type.upper()} &bull; PUBLIC ENGAGEMENT"
        btn_text = "Watch Keynote / Recording &rarr;" if item.get("url") else "View Keynote &rarr;"
        target_blank = 'target="_blank" rel="noopener"' if item.get("url") else ''
        meta_oa = f'<span class="spotlight-oa-pill font-cinzel" style="color:#d8b4fe; border-color:rgba(168,85,247,0.3);"><span class="oa-check">&#10003;</span> {role_str}</span>'
        author_pre = "Speaker"
        author_name = "Dr. Zaid Amin, Ph.D."
        secondary_pill = '<a href="talks.html" class="spotlight-doi-pill font-cinzel" title="Media &amp; Talks Archive"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg> Media &amp; Talks &nearr;</a>'

    elif source == "cv":
        title = item.get("title", "Provincial Honor & Innovator Award")
        venue = item.get("organization", "Provincial Government")
        year_val = item.get("year", "2025")
        category_val = item.get("category", "Government Award")
        year_str = f"{year_val} &bull; {category_val}"
        url = item.get("url") or "cv.html#honors"
        desc = item.get("details", "")
        img_src = item.get("image", "assets/images/thumb-projects.jpg")
        badge_val = item.get("badge", "Provincial Honor")
        kicker_badge = "SPOTLIGHT DISTINCTION"
        clean_cat_val = re.sub(r'^[✦✧★\s\u2726]+', '', str(category_val)).strip()
        top_kicker = f"{clean_cat_val.upper()} &bull; RESEARCH EXCELLENCE"
        btn_text = "Inspect Distinction &rarr;"
        target_blank = 'target="_blank" rel="noopener"' if item.get("url") else ''
        meta_oa = f'<span class="spotlight-oa-pill font-cinzel" style="color:#86efac; border-color:rgba(34,197,94,0.3);"><span class="oa-check">&#10003;</span> {badge_val}</span>'
        author_pre = "Recipient / Lead PI"
        author_name = "Dr. Zaid Amin, Ph.D."
        secondary_pill = '<a href="cv.html#honors" class="spotlight-doi-pill font-cinzel" title="Honors &amp; Distinctions"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg> Honors &amp; CV &nearr;</a>'

    else: # default: publication
        title = item.get("title", "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance")
        venue = item.get("venue", "Smart Cities (MDPI)")
        year_val = item.get("year", 2026)
        year_str = f"Vol. 9 ({year_val})"
        doi = item.get("doi", "10.3390/smartcities9100174")
        url = item.get("url", f"https://doi.org/{doi}" if doi else "#")
        desc = item.get("abstract", "")
        img_src = item.get("image", "assets/images/spotlight-smart-cities.jpg")
        kicker_badge = "SPOTLIGHT ARTICLE"
        top_kicker = "Q1 SCOPUS INDEXED &bull; PEER-REVIEWED"
        btn_text = "Read Full Article &rarr;"
        target_blank = 'target="_blank" rel="noopener"'
        meta_oa = f'<span class="spotlight-oa-pill font-cinzel"><span class="oa-check">&#10003;</span> Open Access</span>'
        author_pre = "Lead Author"
        author_name = "Zaid Amin, Ph.D."
        secondary_pill = f'<a href="{url}" target="_blank" rel="noopener" class="spotlight-doi-pill font-cinzel" title="Direct Digital Object Identifier (DOI)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg> DOI: {doi} &nearr;</a>' if doi else ''

    img_webp = img_src.replace(".jpg", ".webp") if img_src.endswith(".jpg") else img_src

    clean_desc = re.sub(r'<[^>]+>', ' ', str(desc or ''))
    clean_desc = ' '.join(clean_desc.split())
    if len(clean_desc) > 360:
        clean_desc = clean_desc[:357] + '...'

    return f"""
      <!-- LEFT CARD: Chosen Featured Spotlight Article (Clean Editorial Display) -->
      <article class="ref-spotlight-card" aria-label="Featured Spotlight {kicker_badge}">
        <div class="ref-spotlight-visual-wrap">
          <picture>
            <source srcset="{img_webp}" type="image/webp">
            <img src="{img_src}" alt="{title}" class="ref-spotlight-visual-img" loading="lazy">
          </picture>
          <div class="ref-visual-overlay"></div>
          
          <div class="ref-spotlight-top-bar">
            <span class="ref-kicker-pill font-cinzel"><span class="pulse-dot"></span> {kicker_badge}</span>
            <div class="ref-top-right-group">
              <span class="ref-bookmark-icon" title="Featured Spotlight {kicker_badge}" aria-label="Featured Spotlight Bookmark">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                </svg>
              </span>
            </div>
          </div>
        </div>

        <div class="ref-spotlight-body">
          <div class="ref-scopus-kicker font-cinzel"><span class="kicker-gem">✦</span> {re.sub(r'^[✦✧★\s\u2726]+', '', str(top_kicker)).strip()}</div>
          <h2 class="ref-spotlight-title">{title}</h2>

          <div class="ref-spotlight-meta">
            <div class="meta-row-pub">
              <span class="spotlight-venue font-cinzel">{venue}</span>
              <span class="spotlight-divider">&bull;</span>
              <span class="spotlight-year">{year_str}</span>
              {meta_oa}
            </div>
            <div class="meta-row-author">
              <span class="author-pre">{author_pre}:</span> <strong class="author-name">{author_name}</strong>
            </div>
          </div>

          <div class="ref-spotlight-desc">{clean_desc}</div>

          <div class="ref-spotlight-actions">
            <a href="{url}" {target_blank} class="spotlight-btn btn-gold font-cinzel">
              {btn_text}
            </a>
            {secondary_pill}
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
    talks_d = load_json("talks.json") if (DATA_DIR / "talks.json").exists() else {}
    talks = talks_d.get("talks", []) if isinstance(talks_d, dict) else talks_d
    cv_d = load_json("cv_data.json") if (DATA_DIR / "cv_data.json").exists() else {}
    achievements = cv_d.get("achievements_and_grants", [])

    pool_articles = []
    for a in articles:
        thumb = a.get('image') or 'assets/images/spotlight-smart-cities.jpg'
        cat = a.get('category', 'Essays & Perspectives')
        bullets = [
            f"{clean_tray_snippet(cat, 32)} &bull; {a.get('reading_time', '3 min read')}",
            f"Published: {a.get('date', '2026')}"
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

    pool_pubs = []
    for p in pubs:
        thumb = p.get('image') or 'assets/images/thumb-research.jpg'
        venue = p.get('venue', 'Journal')
        year = p.get('year', 2026)
        bullets = [
            f"{clean_tray_snippet(venue, 34)} ({year})",
            f"Authors: {clean_tray_snippet(p.get('authors', 'Dr. Zaid Amin'), 42)}"
        ]
        url = p.get('url') or (f"https://doi.org/{p['doi']}" if p.get('doi') else f"publications.html#{p.get('id', '')}")
        pool_pubs.append({
            'type': 'publication',
            'menu': 'Research & Publication',
            'tag': (p.get('category') or 'Scopus Q1')[:22],
            'title': p.get('title', 'Publication'),
            'thumb_jpg': thumb,
            'bullets': bullets,
            'btn_text': 'Explore',
            'btn_url': url,
            'is_external': url.startswith('http')
        })

    pool_talks = []
    for t in talks:
        thumb = t.get('image') or 'assets/images/thumb-projects.jpg'
        event = t.get('event', 'Keynote Address')
        year = t.get('year', 2026)
        bullets = [
            f"{clean_tray_snippet(event, 34)} ({year})",
            f"Location: {clean_tray_snippet(t.get('location', 'Malaysia'), 42)}"
        ]
        url = t.get('url') or 'talks.html'
        pool_talks.append({
            'type': 'talk',
            'menu': 'Media & Talks',
            'tag': (t.get('role') or 'Keynote Speaker')[:22],
            'title': t.get('title', 'Talk'),
            'thumb_jpg': thumb,
            'bullets': bullets,
            'btn_text': 'View Talk',
            'btn_url': url,
            'is_external': url.startswith('http')
        })

    pool_cv = []
    for c in achievements:
        thumb = c.get('image') or 'assets/images/thumb-projects.jpg'
        org = c.get('organization', 'Academic Honor')
        year = c.get('year', 2025)
        bullets = [
            f"{clean_tray_snippet(org, 34)} ({year})",
            f"Category: {clean_tray_snippet(c.get('category', 'Award & Grant'), 42)}"
        ]
        url = c.get('url') or 'cv.html#honors'
        pool_cv.append({
            'type': 'cv',
            'menu': 'Achievement & CV',
            'tag': (c.get('badge') or c.get('category') or 'Distinction')[:22],
            'title': c.get('title', 'Achievement'),
            'thumb_jpg': thumb,
            'bullets': bullets,
            'btn_text': 'Inspect',
            'btn_url': url,
            'is_external': url.startswith('http')
        })

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
            "btn_text": "View CV",
            "btn_url": "cv.html",
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
            "btn_url": "research.html",
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
            "btn_url": "publications.html",
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

    slides_data = [slide_0]

    art_idx = 0
    pub_idx = 0
    talk_idx = 0
    cv_idx = 0

    while art_idx < len(pool_articles) or pub_idx < len(pool_pubs) or talk_idx < len(pool_talks) or cv_idx < len(pool_cv):
        current_slide = []

        # Slot 1: Article (if available)
        if art_idx < len(pool_articles):
            current_slide.append(pool_articles[art_idx])
            art_idx += 1
        elif pub_idx < len(pool_pubs):
            current_slide.append(pool_pubs[pub_idx])
            pub_idx += 1

        # Slot 2: Publication (if available) or Article
        if pub_idx < len(pool_pubs):
            current_slide.append(pool_pubs[pub_idx])
            pub_idx += 1
        elif art_idx < len(pool_articles):
            current_slide.append(pool_articles[art_idx])
            art_idx += 1

        # Slot 3: Talk (if available), else CV (if available), else Article
        if talk_idx < len(pool_talks):
            current_slide.append(pool_talks[talk_idx])
            talk_idx += 1
        elif cv_idx < len(pool_cv):
            current_slide.append(pool_cv[cv_idx])
            cv_idx += 1
        elif art_idx < len(pool_articles):
            current_slide.append(pool_articles[art_idx])
            art_idx += 1
        elif pub_idx < len(pool_pubs):
            current_slide.append(pool_pubs[pub_idx])
            pub_idx += 1

        # Slot 4: CV (if available), else Pub, else Article
        if cv_idx < len(pool_cv):
            current_slide.append(pool_cv[cv_idx])
            cv_idx += 1
        elif pub_idx < len(pool_pubs):
            current_slide.append(pool_pubs[pub_idx])
            pub_idx += 1
        elif art_idx < len(pool_articles):
            current_slide.append(pool_articles[art_idx])
            art_idx += 1

        if current_slide:
            while len(current_slide) < 4:
                current_slide.append(pool_articles[len(current_slide) % len(pool_articles)])
            slides_data.append(current_slide)

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


def generate_golden_ratio_home():
    profile = load_json("profile.json")
    publications = load_json("publications.json")

    html = get_html_head("Dr. Zaid Amin | Das Sein, Das Sollen | zaidamin.org")
    html += get_page_header("home")

    html += f"""
    <!-- 6. LIST OF JOURNAL: ANIMATE FADE IN FADE OUT MOVE FROM TOP TO DOWN -->
    <section class="journal-ticker-section">
      <div class="journal-ticker-container">
        
        <div class="ticker-label-col font-cinzel">
          <span class="ticker-star-glyph">✦</span>
          <span class="ticker-label-text">INDEXED JOURNALS</span>
        </div>

        <div class="ticker-viewport-col" id="journal-ticker-viewport" onmouseenter="pauseJournalTicker()" onmouseleave="resumeJournalTicker()">
          
          <!-- Slide 0: MDPI Smart Cities -->
          <div class="ticker-slide-item active" data-slide="0">
            <span class="ticker-tag tag-q1 font-cinzel">Q1 SCOPUS</span>
            <span class="ticker-venue-name font-cinzel">Smart Cities (MDPI) &bull; 2026</span>
            <a href="https://doi.org/10.3390/smartcities9100174" target="_blank" rel="noopener" class="ticker-title-link">
              Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance &nearr;
            </a>
          </div>

          <!-- Slide 1: IEEE Access -->
          <div class="ticker-slide-item" data-slide="1">
            <span class="ticker-tag tag-q1 font-cinzel">Q1 SCOPUS</span>
            <span class="ticker-venue-name font-cinzel">IEEE Access &bull; 2021</span>
            <a href="https://doi.org/10.1109/ACCESS.2021.3087740" target="_blank" rel="noopener" class="ticker-title-link">
              Attention-Based Design and User Decisions on Information Sharing: Cybernetics Intervention &nearr;
            </a>
          </div>

          <!-- Slide 2: IJACSA -->
          <div class="ticker-slide-item" data-slide="2">
            <span class="ticker-tag tag-scopus font-cinzel">SCOPUS INDEXED</span>
            <span class="ticker-venue-name font-cinzel">IJACSA &bull; 2021</span>
            <a href="https://doi.org/10.14569/IJACSA.2021.0121092" target="_blank" rel="noopener" class="ticker-title-link">
              Visual Selective Attention System to Intervene User Attention in Digital Environments &nearr;
            </a>
          </div>

          <!-- Slide 3: JISTM -->
          <div class="ticker-slide-item" data-slide="3">
            <span class="ticker-tag tag-peer font-cinzel">PEER-REVIEWED</span>
            <span class="ticker-venue-name font-cinzel">JISTM &bull; 2026</span>
            <a href="https://doi.org/10.35631/JISTM.1141001" target="_blank" rel="noopener" class="ticker-title-link">
              Srivijayapedia: A Digital Platform for Cultural Heritage Preservation of the Srivijaya Civilization &nearr;
            </a>
          </div>

          <!-- Slide 4: Springer Contributions to Management Science -->
          <div class="ticker-slide-item" data-slide="4">
            <span class="ticker-tag tag-scopus font-cinzel">SPRINGER</span>
            <span class="ticker-venue-name font-cinzel">Contributions to Management Science &bull; 2024</span>
            <a href="https://doi.org/10.1007/978-3-031-52280-2_14" target="_blank" rel="noopener" class="ticker-title-link">
              Digital Loneliness in Social Media: The Epoch of our Connected and Distraction World &nearr;
            </a>
          </div>

          <!-- Slide 5: SSRN AI Governance Series -->
          <div class="ticker-slide-item" data-slide="5">
            <span class="ticker-tag tag-preprint font-cinzel">GOVERNANCE PREPRINT</span>
            <span class="ticker-venue-name font-cinzel">SSRN Series &bull; 2026</span>
            <a href="https://doi.org/10.2139/ssrn.7670124" target="_blank" rel="noopener" class="ticker-title-link">
              The Proxy Trap in Agentic AI: When Metrics Replace Judgment in Autonomous Systems &nearr;
            </a>
          </div>

        </div>

        <div class="ticker-controls-col">
          <div class="ticker-arrows-box">
            <button class="ticker-arrow-btn" onclick="rotateJournalTicker(-1)" title="Previous Journal (Top)" aria-label="Previous Journal">&uarr;</button>
            <button class="ticker-arrow-btn" onclick="rotateJournalTicker(1)" title="Next Journal (Down)" aria-label="Next Journal">&darr;</button>
          </div>
        </div>

      </div>
    </section>

    <!-- 5. FEATURED SPOTLIGHT & ACADEMIC PORTALS (REFERENCE SPLIT CARD LAYOUT) -->
    <section class="golden-split-section ref-split-layout">
      
{get_spotlight_card_html()}

      <!-- RIGHT CARD: Academic Portals & Highlights (Matching Reference Inset Tray + Stacked Cards) -->
      <aside class="ref-portals-card">
        <!-- 1. Top Main Menu Navigation Grid (Placed Above Dr. Zaid Profile, 3x2 Golden Ratio Layout) -->
        <nav class="ref-top-menu-bar" aria-label="Main Navigation">
          <a href="index.html" class="ref-menu-tab tab-home active" title="Home" aria-label="Home">
            <svg class="tab-icon-home" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </a>
          <a href="publications.html" class="ref-menu-tab" title="Research &amp; Publications">
            <span class="tab-txt-full">Research &amp; Pubs</span><span class="tab-txt-compact">Research</span>
          </a>
          <a href="research.html" class="ref-menu-tab" title="Activities &amp; Funded Projects">
            <span class="tab-txt-full">Activity &amp; Project</span><span class="tab-txt-compact">Activity</span>
          </a>
          <a href="talks.html" class="ref-menu-tab" title="Recent Media &amp; Invited Talks">
            <span class="tab-txt-full">Media &amp; Talks</span><span class="tab-txt-compact">Media</span>
          </a>
          <a href="cv.html" class="ref-menu-tab" title="Achievements, Honors &amp; Curriculum Vitae">
            <span class="tab-txt-full">Achievement &amp; CV</span><span class="tab-txt-compact">CV</span>
          </a>
        </nav>

        <div class="ref-menu-divider"></div>

        
        <!-- Header with Dr. Zaid Amin Profile Summary & Title -->
        <div class="ref-portals-header">
          <div class="ref-profile-info-col">
            <h3 class="ref-profile-name font-cinzel">Zaid Amin, Ph.D.</h3>
            <div class="ref-profile-role">
              Senior Lecturer &bull; Faculty of Data Science &amp; IT (FDSIT)<br>
              <span class="ref-profile-inst">INTI International University, Malaysia</span>
            </div>
            <div class="ref-profile-fields">
              Digital Ethics <span class="ref-gold-dot">&bull;</span> Behavior &amp; Social Computing <span class="ref-gold-dot">&bull;</span> HCI
            </div>
          </div>
          <div class="ref-photo-ring coin-flip-stage" id="dr-zaid-coin" role="button" tabindex="0" title="Dr. Zaid Amin, Ph.D. • Click to rotate portrait coin">
            <div class="coin-disc" id="coin-disc" aria-label="Interactive Portrait Coin">
              <div class="coin-face coin-face-front" id="coin-face-front">
                <picture>
                  <source srcset="assets/images/portraits/portrait-1.webp" type="image/webp">
                  <img src="assets/images/portraits/portrait-1.png" alt="Dr. Zaid Amin, Ph.D. — Academic Portrait" class="ref-photo-img" width="114" height="114">
                </picture>
                <div class="coin-specular-gleam"></div>
              </div>
              <div class="coin-face coin-face-back" id="coin-face-back">
                <picture>
                  <source srcset="assets/images/portraits/portrait-2.webp" type="image/webp">
                  <img src="assets/images/portraits/portrait-2.png" alt="Dr. Zaid Amin, Ph.D. — Singapore" class="ref-photo-img" width="114" height="114">
                </picture>
                <div class="coin-specular-gleam"></div>
              </div>
              <div class="coin-rim-highlight"></div>
            </div>
            <span class="ref-live-status" title="Active Senior Lecturer &amp; Researcher"></span>
          </div>
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

    def get_publisher(venue, doi):
        v = venue or ""
        d = doi or ""
        if "Springer" in v or "LNCS" in v or "Computer Science" in v or "Contributions" in v:
            return "Springer Nature"
        if "Atlantis" in v or "2991" in d:
            return "Atlantis Press"
        return "Academic Press"

    def get_series(venue):
        v = venue or ""
        if "Contributions to Management" in v:
            return "Contributions to Management Science"
        if "Lecture Notes in Computer Science" in v or "LNCS" in v:
            return "Lecture Notes in Computer Science (LNCS)"
        if "Atlantis" in v or "Academic" in v:
            return "Atlantis Press Monograph Series"
        return v

    # Front featured book (2024 Springer Digital Loneliness)
    featured_book = None
    for b in cat_items:
        if "digital" in b.get("id", "") or b.get("year") == 2024:
            featured_book = b
            break
    if not featured_book:
        featured_book = cat_items[0]

    # Rear book (2021 LNCS Attention-Based)
    rear_book = None
    for b in cat_items:
        if "covid" in b.get("id", "") or "attention" in b.get("id", "") or b.get("year") == 2021:
            rear_book = b
            break
    if not rear_book and len(cat_items) > 1:
        rear_book = cat_items[1]

    # Render each book card in the Curated Shelf
    shelf_cards_html = ""
    for idx, pub in enumerate(cat_items, 1):
        url = pub.get("url", "").strip()
        doi = pub.get("doi", "").strip()
        if not url and doi:
            url = f"https://doi.org/{doi}"
        venue = pub.get("venue", "Academic Publication")
        series_text = get_series(venue)
        publisher = get_publisher(venue, doi)
        excerpt = clean_excerpt_fn(pub.get("abstract", ""), max_len=140)
        escaped_title = _html_mod.escape(pub["title"])
        escaped_title_lower = _html_mod.escape(pub["title"].lower())
        escaped_venue = _html_mod.escape(venue)
        escaped_venue_lower = _html_mod.escape(venue.lower())
        year = pub.get("year", "")
        img = pub.get("image", "assets/images/thumb-research.jpg")
        bibtex_id = pub.get("id", f"book{idx}")
        bibtex_raw = pub.get("bibtex", "")
        is_featured = pub.get("featured", False) or ("digital" in pub.get("id", ""))
        primary_tag = '<span class="bokify-primary-chip">★ Primary Volume</span>' if is_featured else ""

        # Download pill
        if url:
            label = "Download / DOI"
            if "arxiv.org" in url:
                label = "Download (arXiv)"
            elif "ssrn" in url:
                label = "Download (SSRN)"
            dl_btn = f'<a href="{url}" target="_blank" rel="noopener" class="pub-pill-btn pub-pill-primary">{render_svg_icon_fn("download")} <span>{label}</span></a>'
        else:
            title_enc = _html_mod.escape(pub.get("title", ""))
            mailto = f"mailto:zaid.amin@newinti.edu.my?subject=Requesting%20Full-Text:%20{title_enc}"
            dl_btn = f'<a href="{mailto}" class="pub-pill-btn pub-pill-primary">{render_svg_icon_fn("email")} <span>Request Full-Text</span></a>'

        doi_html = f'<div class="bokify-card-doi"><span class="bokify-doi-lbl">DOI:</span> <a href="{url}" target="_blank" rel="noopener" class="bokify-doi-link">{doi}</a></div>' if doi else ""

        shelf_cards_html += f"""
        <article class="bokify-shelf-card pub-item" data-category="{cat["category_key"].lower()}" data-title="{escaped_title_lower}" data-venue="{escaped_venue_lower}" data-year="{year}">
          <!-- Top 3D Book Showcase on Card -->
          <div class="bokify-card-stage">
            <div class="bokify-card-3d-scene">
              <div class="bokify-card-book-3d">
                <div class="bokify-card-cover">
                  <img src="{img}" alt="{escaped_title}" class="bokify-card-cover-img" loading="lazy" />
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
              {primary_tag}
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
            {doi_html}
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
                  <span class="bokify-author-name">Dr. Zaid Amin, Ph.D.</span>
                  <span class="bokify-author-role">Senior Lecturer &bull; FDSIT, INTI International University</span>
                </div>
              </div>
              <span class="bokify-category-tag">01 / 04 &bull; MONOGRAPHS &amp; CHAPTERS</span>
            </div>

            <!-- Big Bokify Headline -->
            <h2 class="bokify-hero-title font-cinzel">
              Meet Your Next <span class="bokify-gold-gradient">Scholarly Treatise</span>
            </h2>

            <!-- Description -->
            <p class="bokify-hero-desc">
              Comprehensive academic monographs, peer-reviewed book chapters, and curated editorial treatises exploring sociotechnical systems, digital loneliness, and behavioral interventions in information diffusion. Published with leading international academic presses including Springer Nature (Contributions to Management Science, Lecture Notes in Computer Science) and Atlantis Press.
            </p>

            <!-- Call to Actions -->
            <div class="bokify-hero-ctas">
              <a href="{primary_url}" target="_blank" rel="noopener" class="bokify-btn-hero-primary">
                {render_svg_icon_fn("download")}
                <span>Download Primary Volume (Springer)</span>
              </a>
              <a href="#bokify-volumes-shelf" class="bokify-btn-hero-secondary">
                <span>Browse All 3 Volumes</span>
                <span class="bokify-arrow-down">&darr;</span>
              </a>
            </div>

            <!-- Trust / Publisher Strip (Bokify Audible/Amazon/Google Books style) -->
            <div class="bokify-publisher-strip">
              <span class="bokify-publisher-strip-label">PUBLISHED &amp; INDEXED WITH</span>
              <div class="bokify-publisher-badges">
                <span class="bokify-pub-pill"><span class="bokify-pub-bullet">&bull;</span> Springer Nature</span>
                <span class="bokify-pub-pill"><span class="bokify-pub-bullet">&bull;</span> LNCS Series</span>
                <span class="bokify-pub-pill"><span class="bokify-pub-bullet">&bull;</span> Atlantis Press</span>
                <span class="bokify-pub-pill"><span class="bokify-pub-bullet">&bull;</span> Scopus Indexed</span>
                <span class="bokify-pub-pill"><span class="bokify-pub-bullet">&bull;</span> Gold Open Access</span>
              </div>
            </div>
          </div>

          <!-- RIGHT COLUMN: Dual 3D Standing Book Showcase (38.2%) -->
          <div class="bokify-hero-stage">
            <div class="bokify-stage-container">
              <!-- Radial Stage Spotlight -->
              <div class="bokify-stage-glow"></div>

              <!-- 3D Book Stage Scene -->
              <div class="bokify-stage-scene">
                <!-- Front Standing Book (Digital Loneliness - 2024) -->
                <div class="bokify-standing-book bokify-standing-front">
                  <div class="bokify-book-3d">
                    <div class="bokify-book-cover">
                      <img src="assets/images/books/book_digital_loneliness.webp" alt="Digital Loneliness in Social Media" class="bokify-cover-img" loading="lazy">
                      <div class="bokify-cover-glare"></div>
                    </div>
                    <div class="bokify-book-spine">
                      <span class="bokify-spine-text">SPRINGER NATURE &bull; 2024</span>
                    </div>
                    <div class="bokify-book-pages"></div>
                    <div class="bokify-book-shadow"></div>
                  </div>
                  <div class="bokify-stage-badge">★ PRIMARY MONOGRAPH (2024)</div>
                </div>

                <!-- Rear Standing Book (Attention-Based Design - 2021) -->
                <div class="bokify-standing-book bokify-standing-rear">
                  <div class="bokify-book-3d">
                    <div class="bokify-book-cover">
                      <img src="assets/images/books/book_attention_covid.webp" alt="Attention-Based Design" class="bokify-cover-img" loading="lazy">
                      <div class="bokify-cover-glare"></div>
                    </div>
                    <div class="bokify-book-spine">
                      <span class="bokify-spine-text">LNCS &bull; 2021</span>
                    </div>
                    <div class="bokify-book-pages"></div>
                    <div class="bokify-book-shadow"></div>
                  </div>
                </div>
              </div>

              <!-- Floor Grounding Ambient Line -->
              <div class="bokify-stage-pedestal-line"></div>
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
        "Research & Publication Gallery | Dr. Zaid Amin | zaidamin.org",
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
            "description": "Comprehensive academic monographs, peer-reviewed book chapters, and curated editorial treatises exploring sociotechnical systems, digital loneliness, and behavioral interventions in information diffusion. Published with leading international academic presses including Springer Nature (Contributions to Management Science, Lecture Notes in Computer Science) and Atlantis Press.",
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
            clean = clean[:max_len].rstrip() + "..."
        return clean

    def render_download_pill(pub):
        url = pub.get("url", "").strip()
        doi = pub.get("doi", "").strip()
        if not url and doi:
            url = f"https://doi.org/{doi}"

        if url:
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
            return f'<a href="{mailto}" class="pub-pill-btn pub-pill-primary">{render_svg_icon("email")} <span>Request Full-Text</span></a>'

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
            doi = pub.get("doi", "").strip()
            url = pub.get("url", "").strip()
            if not url and doi:
                url = f"https://doi.org/{doi}"
            doi_html = f'<span class="pub-strip-doi-inline"><span class="pub-strip-doi-lbl">DOI:</span> <a href="{url}" target="_blank" rel="noopener" class="pub-strip-doi-link">{doi}</a></span>' if doi else ""
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
          <input type="text" id="pub-search" class="pub-search-input" placeholder="Search across all 24 publications by title, venue, year, or keyword..." aria-label="Search publications">
        </div>

        <nav class="pub-nav-pills" aria-label="Publication Categories">
          <button class="pub-nav-pill filter-btn active" data-filter="all">✦ All ({len(publications)})</button>
          <button class="pub-nav-pill filter-btn" data-filter="book chapter" data-target-section="section-books">01. Book &amp; Chapters (3)</button>
          <button class="pub-nav-pill filter-btn" data-filter="journal" data-target-section="section-journals">02. Journals (10)</button>
          <button class="pub-nav-pill filter-btn" data-filter="conference" data-target-section="section-conferences">03. Conferences (6)</button>
          <button class="pub-nav-pill filter-btn" data-filter="preprint" data-target-section="section-preprints">04. Preprints (5)</button>
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

    html = get_html_head("Activity & Project | Dr. Zaid Amin | zaidamin.org", "Scholarly activity, 80+ peer essays, research pillars, and funded grants authored and led by Dr. Zaid Amin.")
    html += get_page_header("research")

    # Categories for articles
    categories = {}
    for a in articles:
        cat = a.get("category", "Essays & Perspectives")
        categories[cat] = categories.get(cat, 0) + 1

    cat_pills_html = f'<button class="article-cat-btn active" data-category="all">All ({len(articles)})</button>'
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        cat_pills_html += f'<button class="article-cat-btn" data-category="{cat}">{cat} ({count})</button>'

    def clean_article_excerpt(raw_text, max_len=135):
        if not raw_text:
            return ""
        clean = re.sub(r'<[^>]+>', ' ', raw_text)
        clean = ' '.join(clean.split())
        if len(clean) > max_len:
            clean = clean[:max_len].rstrip() + "..."
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
          <a href="article.html?id={slug}" class="article-card-thumb-wrap" aria-label="{escaped_title}">
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
              <a href="article.html?id={slug}">{title}</a>
            </h3>
            <p class="article-card-excerpt">{excerpt}</p>
          </div>

          <!-- Elegant Read Essay Button (Golden Ratio Capsule Pill) -->
          <div class="article-card-action">
            <a href="article.html?id={slug}" class="article-card-btn font-cinzel">
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
          countDisplay.textContent = visibleCount + ' articles found';
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
      <section class="activity-hero-section">
        <div class="subpage-eyebrow"><span class="eyebrow-dot">✦</span> Scholarly Archive &bull; Technical Initiatives</div>
        <h1 class="activity-hero-title">Activity &amp; Project</h1>
        <p class="activity-hero-subtitle">
          80 scholarly essays, peer commentaries, core research pillars, and active funded grant themes.
        </p>
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
          <div class="articles-search-row">
            <div class="articles-search-wrap">
              <span class="articles-search-icon">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              </span>
              <input type="text" id="article-search" class="article-search-input" placeholder="Search across {len(articles)} scholarly essays by keyword, topic, or title..." autocomplete="off">
            </div>
            <div id="article-count-display" class="article-count-badge">
              {len(articles)} articles
            </div>
          </div>
          <div class="articles-category-pills">
            {cat_pills_html}
          </div>
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
    html += get_page_footer()
    return html


# ==============================================================================
# 4. POSTGRADUATE LAB & SUPERVISION (prospective-students.html)
# ==============================================================================

# ==============================================================================
# 5. MEDIA & TALKS (talks.html)
# ==============================================================================
def generate_talks_page():
    media_data = load_json("media_talks.json") if (DATA_DIR / "media_talks.json").exists() else {}
    talkshows = media_data.get("talkshows", [])
    keynotes = media_data.get("keynotes", [])
    opinions = media_data.get("opinions", [])

    page_head = get_html_head(
        "Media & Talks | Dr. Zaid Amin | zaidamin.org",
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
        v_url = _html_mod.escape(v.get("video_url", "https://youtube.com"))
        v_duration = _html_mod.escape(v.get("duration", "20:00"))

        v_embed = _html_mod.escape(v.get("embed_url", v_url))

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

        card_html = f"""
        <div class="service-portrait-card">
          <img src="{k_img}" alt="{k_title}" class="service-card-bg-img" loading="lazy" onerror="this.src='assets/images/spotlight-smart-cities.jpg'">
          <div class="service-card-gradient-top"></div>
          <div class="service-card-gradient-bottom"></div>

          <!-- Top Row: Frosted Tag & Icon Badge -->
          <div class="service-card-top-row">
            <span class="service-card-tag">{k_badge}</span>
            <div class="service-card-icon-badge" aria-hidden="true">
              {icon_svg}
            </div>
          </div>

          <!-- Bottom Content: Venue, Title, Synopsis, Capsule Button -->
          <div class="service-card-bottom">
            <div class="service-card-venue">{k_venue}</div>
            <h3 class="service-card-title">{k_title}</h3>
            <p class="service-card-desc">{k_abstract}</p>
            <a href="{k_url}" {"target='_blank' rel='noopener'" if k_url.startswith("http") else ""} class="service-card-btn">
              <span>Learn More</span>
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

        card_html = f"""
        <div class="service-portrait-card">
          <img src="{o_img}" alt="{o_title}" class="service-card-bg-img" loading="lazy" onerror="this.src='assets/images/spotlight-smart-cities.jpg'">
          <div class="service-card-gradient-top"></div>
          <div class="service-card-gradient-bottom"></div>

          <!-- Top Row: Frosted Tag & Icon Badge -->
          <div class="service-card-top-row">
            <span class="service-card-tag">{o_badge}</span>
            <div class="service-card-icon-badge" aria-hidden="true">
              {icon_svg}
            </div>
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

    feat_title = _html_mod.escape(featured.get("title", ""))
    feat_desc = _html_mod.escape(featured.get("description", ""))
    feat_channel = _html_mod.escape(featured.get("channel", "Broadcast Archive"))
    feat_tag = _html_mod.escape(featured.get("category_tag", "Talkshow"))
    feat_date = _html_mod.escape(featured.get("date", "2015"))
    feat_poster = _html_mod.escape(featured.get("poster", ""))
    feat_url = _html_mod.escape(featured.get("video_url", "https://youtube.com"))
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
          stageIframe.src = embedUrl;
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

        function activateVideo(index, playNow) {
          if (index < 0 || index >= playlistItems.length) return;
          activeIndex = index;

          playlistItems.forEach((item, i) => {
            if (i === index) {
              item.classList.add("active");
              try { item.scrollIntoView({ behavior: "smooth", block: "nearest" }); } catch(err){}
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

        playlistItems.forEach((item, idx) => {
          item.addEventListener("click", function (e) {
            e.preventDefault();
            activateVideo(idx);
          });
        });

        const prevBtn = document.getElementById("video-prev-btn");
        const nextBtn = document.getElementById("video-next-btn");

        if (prevBtn) {
          prevBtn.addEventListener("click", function () {
            const nextIdx = (activeIndex - 1 + playlistItems.length) % playlistItems.length;
            activateVideo(nextIdx);
          });
        }
        if (nextBtn) {
          nextBtn.addEventListener("click", function () {
            const nextIdx = (activeIndex + 1) % playlistItems.length;
            activateVideo(nextIdx);
          });
        }

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
                alert("Video link copied to clipboard!");
              }).catch(() => {
                prompt("Copy video link:", url);
              });
            } else {
              prompt("Copy video link:", url);
            }
          });
        }

        // 2. Category 2 & 3 Carousel Track Controllers
        function setupCarousel(prevId, nextId, trackId) {
          const pBtn = document.getElementById(prevId);
          const nBtn = document.getElementById(nextId);
          const track = document.getElementById(trackId);
          if (!track || !pBtn || !nBtn) return;

          nBtn.addEventListener("click", function () {
            const card = track.querySelector(".service-portrait-card");
            const shift = card ? card.offsetWidth + 20 : 320;
            track.scrollBy({ left: shift, behavior: "smooth" });
          });

          pBtn.addEventListener("click", function () {
            const card = track.querySelector(".service-portrait-card");
            const shift = card ? card.offsetWidth + 20 : 320;
            track.scrollBy({ left: -shift, behavior: "smooth" });
          });
        }

        setupCarousel("keynote-prev-btn", "keynote-next-btn", "keynote-track");
        setupCarousel("opinion-prev-btn", "opinion-next-btn", "opinion-track");
      });
    </script>
    """

    body_html = f"""
    <main class="talks-page-container" id="main-content">

      <!-- Hero Header -->
      <section class="talks-hero-section">
        <div class="subpage-eyebrow"><span class="eyebrow-dot">✦</span> Audio-Visual Archive &bull; Keynote Engagements</div>
        <h1 class="talks-hero-title">Media &amp; Talks</h1>
        <p class="talks-hero-subtitle">
          Televised broadcasts, keynote addresses, and critical philosophical treatises.
        </p>
        <div class="talks-nav-bar" aria-label="Media &amp; Talks Navigation">
          <a href="#category-talkshow" class="talks-nav-pill active">01. Talkshow (Video Gallery)</a>
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
            <h2>01. Talkshow (Video Gallery)</h2>
            <p class="talks-category-subtitle">Televised Broadcasts &bull; Expert Commentary &bull; Studio Discourse</p>
          </div>
          <a href="https://drive.google.com/drive/folders/1KB6A1C3cubX5q3CwWNZDAOYdjIwtkqzm" target="_blank" rel="noopener" class="yt-header-pill" title="Full Google Drive Video Repository">
            <svg width="15" height="11" viewBox="0 0 68 48" style="vertical-align: -1px;">
              <path d="M66.52,7.74c-0.78-2.93-2.49-5.41-5.42-6.19C55.79,.13,34,0,34,0S12.21,.13,6.9,1.55 C3.97,2.33,2.27,4.81,1.48,7.74C0.06,13.05,0,24,0,24s0.06,10.95,1.48,16.26c0.78,2.93,2.49,5.41,5.42,6.19 C12.21,47.87,34,48,34,48s21.79-0.13,27.1-1.55c2.93-0.78,4.64-3.26,5.42-6.19C67.94,34.95,68,24,68,24S67.94,13.05,66.52,7.74z" fill="#ffffff"/>
              <path d="M 45,24 27,14 27,34" fill="#cc0000"/>
            </svg>
            <span>SUBSCRIBE</span>
          </a>
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
            <iframe id="stage-video-iframe" src="" title="{feat_title}" class="video-stage-iframe" allow="autoplay; fullscreen" allowfullscreen></iframe>
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

            <!-- Bottom content & controls -->
            <div class="video-stage-content">
              <div class="video-stage-badge-row">
                <span class="video-stage-badge" id="stage-badge">{feat_tag}</span>
                <span class="video-stage-date" id="stage-date">{feat_date}</span>
              </div>
              <h3 class="video-stage-title" id="stage-title">{feat_title}</h3>
              <p class="video-stage-description" id="stage-description">{feat_desc}</p>
              
              <div class="video-stage-action-bar">
                <a id="stage-watch-link" href="{feat_url}" target="_blank" rel="noopener" class="video-stage-watch-link">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  <span>WATCH BROADCAST</span>
                </a>
                <button class="video-stage-btn-icon" id="stage-share-btn" title="Share Video Link" type="button" aria-label="Share Video">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
                </button>
                <div class="video-stage-duration" id="stage-duration">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:-1px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  <span>{feat_duration}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Playlist Stack (38.2% Golden Ratio) -->
          <div class="video-playlist-container">
            <div class="video-playlist-stack" id="video-playlist-stack">
              {playlist_joined}
            </div>

            <!-- Bottom Navigation Arrows -->
            <div class="video-playlist-footer">
              <button class="video-nav-arrow-btn" id="video-prev-btn" title="Previous Video" type="button" aria-label="Previous Video">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <button class="video-nav-arrow-btn" id="video-next-btn" title="Next Video" type="button" aria-label="Next Video">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
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
          <div class="talks-invite-social-row">
            <a href="https://scholar.google.com/citations?user=k37uIeQAAAAJ" target="_blank" rel="noopener" title="Google Scholar">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            </a>
            <a href="https://orcid.org/0000-0002-3686-2489" target="_blank" rel="noopener" title="ORCID">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9 8v8M12 8v8M15 8v8"/></svg>
            </a>
            <a href="https://github.com/zaeedh" target="_blank" rel="noopener" title="GitHub">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            </a>
            <a href="https://linkedin.com" target="_blank" rel="noopener" title="LinkedIn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
            </a>
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
            <a href="cv.html" class="talks-invite-link-sec">
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
    html += get_page_footer()
    return html

# ==============================================================================
# 5. CURRICULUM VITAE (cv.html)
# ==============================================================================
def generate_cv_page():
    cv = load_json("cv_data.json")
    exec_prof = cv["executive_profile"]
    publications = load_json("publications.json")

    html = get_html_head(
        "Achievement & Curriculum Vitae | Dr. Zaid Amin, Ph.D. | zaidamin.org",
        "Official Curriculum Vitae and Achievements of Dr. Zaid Amin, Senior Lecturer & QS Deputy Director at INTI International University, Ph.D. from UKM (Tesis Cemerlang & GOT)."
    )
    html += get_page_header("cv")

    html += f"""
    <!-- Subpage Content: Achievement & Curriculum Vitae (July 2026 Official Resume) -->
    <div class="cv-page-container">
      
      <!-- Executive Hero Profile Card -->
      <section class="cv-hero-card">
        <div class="cv-hero-top">
          <div style="flex: 1 1 540px;">
            <div class="cv-section-tag" style="margin-bottom: 6px;">CURRICULUM VITAE &bull; ACADEMIC PORTFOLIO</div>
            <h1 class="cv-hero-name font-cinzel">{exec_prof['name']}</h1>
            <div class="cv-hero-role font-cinzel">
              {exec_prof['role_title']}
            </div>
            <div class="cv-hero-affiliation">
              {exec_prof['institution']}
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

          <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 10px;">
            <button onclick="window.print()" class="cv-action-pill cv-action-pill-primary" title="Print or save verified PDF copy">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
              Print / Save as PDF
            </button>
            <span style="font-size: 0.76rem; color: var(--text-muted); font-family: monospace;">July 2026 Academic Edition</span>
          </div>
        </div>

        <div class="cv-hero-summary">
          {exec_prof['summary']}
        </div>

        <div class="cv-hero-actions">
          <a href="{exec_prof['researcher_ids']['orcid']['url']}" target="_blank" rel="noopener" class="cv-action-pill" title="ORCID Verified Record">
            {render_svg_icon('orcid')} <span>ORCID: {exec_prof['researcher_ids']['orcid']['id']}</span>
          </a>
          <a href="{exec_prof['researcher_ids']['scopus']['url']}" target="_blank" rel="noopener" class="cv-action-pill" title="Scopus Author Profile">
            {render_svg_icon('external')} <span>Scopus ID: {exec_prof['researcher_ids']['scopus']['id']}</span>
          </a>
          <a href="{exec_prof['researcher_ids']['wos']['url']}" target="_blank" rel="noopener" class="cv-action-pill" title="Web of Science Profile">
            {render_svg_icon('external')} <span>WoS ResearcherID: {exec_prof['researcher_ids']['wos']['id']}</span>
          </a>
          <a href="{exec_prof['researcher_ids']['scholar']['url']}" target="_blank" rel="noopener" class="cv-action-pill" title="Google Scholar Profile">
            {render_svg_icon('scholar')} <span>Google Scholar</span>
          </a>
          <a href="mailto:{exec_prof['contact']['email']}" class="cv-action-pill" title="Institutional Email">
            {render_svg_icon('email')} <span>{exec_prof['contact']['email']}</span>
          </a>
          <a href="{exec_prof['official_docs']['teaching_permit']['url']}" target="_blank" rel="noopener" class="cv-action-pill" title="Higher Education Teaching Permit">
            {render_svg_icon('external')} <span>Teaching Permit</span>
          </a>
          <a href="{exec_prof['official_docs']['mqa_cv']['url']}" target="_blank" rel="noopener" class="cv-action-pill" title="MQA CV Accreditation Document">
            {render_svg_icon('external')} <span>MQA Official CV</span>
          </a>
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
      <section id="honors" class="cv-section">
        <div id="achievements"></div>
        <div class="cv-section-tag">01 / HONORS &amp; DISTINCTIONS</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Prestigious Honors, Awards &amp; Research Grants</h2>
          <span class="cv-section-count">{len(cv['achievements_and_grants'])} Distinctions</span>
        </div>
    """

    for item in cv['achievements_and_grants']:
        is_spotlight = item.get('featured')
        highlight_cls = "is-highlight is-spotlight" if is_spotlight else ("is-highlight" if item.get('highlight') else "")
        spotlight_badge = '<span class="cv-type-pill" style="background:rgba(212,175,55,0.22); color:#fef08a; border:1px solid #d4af37; font-weight:800; letter-spacing:0.04em;">★ SPOTLIGHT</span>' if is_spotlight else ""
        url_link = f'<a href="{item["url"]}" target="_blank" rel="noopener" class="cv-type-pill" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">{render_svg_icon("external")} Verification Link</a>' if item.get('url') else ''
        img_tag = f'<div style="margin:12px 0; border-radius:10px; overflow:hidden; max-height:160px; border:1px solid rgba(212,175,55,0.3);"><img src="{item["image"]}" alt="{item["title"]}" style="width:100%; height:100%; object-fit:cover;"></div>' if (is_spotlight and item.get('image')) else ""
        html += f"""
        <div class="cv-card {highlight_cls}">
          <div class="cv-card-top">
            <div class="cv-card-heading">
              <h3 class="cv-card-title">{item['title']}</h3>
              <div class="cv-card-sub">{item['organization']}</div>
            </div>
            <div class="cv-card-badges">
              {spotlight_badge}
              <span class="cv-year-pill">{item['year']}</span>
              <span class="cv-type-pill">{item['badge']}</span>
              {url_link}
            </div>
          </div>
          {img_tag}
          <div class="cv-card-body">
            {item['details']}
          </div>
        </div>
        """

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

    for item in cv['academic_leadership']:
        html += f"""
        <div class="cv-card is-highlight">
          <div class="cv-card-top">
            <div class="cv-card-heading">
              <h3 class="cv-card-title">{item['role']}</h3>
              <div class="cv-card-sub">{item['institution']}</div>
            </div>
            <div class="cv-card-badges">
              <span class="cv-year-pill">{item['period']}</span>
              <span class="cv-type-pill">{item['scope']}</span>
            </div>
          </div>
          <div class="cv-card-body">
            {item['responsibilities']}
          </div>
        </div>
        """

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

    for item in cv['work_experience']:
        html += f"""
        <div class="cv-card">
          <div class="cv-card-top">
            <div class="cv-card-heading">
              <h3 class="cv-card-title">{item['role']}</h3>
              <div class="cv-card-sub">{item['institution']}</div>
            </div>
            <div class="cv-card-badges">
              <span class="cv-year-pill">{item['period']}</span>
            </div>
          </div>
          <div class="cv-card-body">
            {item['description']}
          </div>
        </div>
        """

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

    for item in cv['education']:
        html += f"""
        <div class="cv-card">
          <div class="cv-card-top">
            <div class="cv-card-heading">
              <h3 class="cv-card-title">{item['degree']}</h3>
              <div class="cv-card-sub">{item['institution']} &bull; {item['country']}</div>
            </div>
            <div class="cv-card-badges">
              <span class="cv-year-pill">{item['period']}</span>
              <span class="cv-type-pill">{item['distinction']}</span>
            </div>
          </div>
          <div class="cv-card-body">
            <strong>Core Focus:</strong> {item['focus']}
          </div>
        </div>
        """

    html += f"""
      </section>

      <!-- SECTION 5: KEYNOTES, INVITED TALKS & MEDIA -->
      <section id="talks" class="cv-section">
        <div class="cv-section-tag">05 / PUBLIC ENGAGEMENT</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Keynotes, Media &amp; Invited Talks</h2>
          <span class="cv-section-count">{len(cv['invited_talks_and_media'])} Keynotes</span> <a href="talks.html" class="pub-pill-btn primary" style="font-size:0.72rem; padding:4px 12px; margin-left:12px; text-decoration:none; display:inline-flex; align-items:center; gap:4px;">Full Interactive Gallery &nearr;</a>
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

    for item in talks_items:
        is_spotlight = item.get('featured')
        highlight_cls = "is-highlight is-spotlight" if is_spotlight else "is-highlight"
        spotlight_badge = '<span class="cv-type-pill" style="background:rgba(212,175,55,0.22); color:#fef08a; border:1px solid #d4af37; font-weight:800; letter-spacing:0.04em;">★ SPOTLIGHT</span>' if is_spotlight else ""
        url_link = f'<a href="{item["url"]}" target="_blank" rel="noopener" class="cv-type-pill" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">{render_svg_icon("external")} Verification Link</a>' if item.get('url') else ''
        img_tag = f'<div style="margin:12px 0; border-radius:10px; overflow:hidden; max-height:160px; border:1px solid rgba(212,175,55,0.3);"><img src="{item["image"]}" alt="{item.get("title", item.get("event", ""))}" style="width:100%; height:100%; object-fit:cover;"></div>' if (is_spotlight and item.get('image')) else ""
        title_str = item.get('title') or item.get('event')
        sub_str = item.get('event') if item.get('title') else item.get('venue', '')
        role_str = item.get('role', 'Keynote Speaker')
        year_str = item.get('year', '2026')
        desc_str = item.get('description') or item.get('details', '')

        html += f"""
        <div class="cv-card {highlight_cls}">
          <div class="cv-card-top">
            <div class="cv-card-heading">
              <h3 class="cv-card-title">{title_str}</h3>
              <div class="cv-card-sub">{sub_str}</div>
            </div>
            <div class="cv-card-badges">
              {spotlight_badge}
              <span class="cv-year-pill">{year_str}</span>
              <span class="cv-type-pill">{role_str}</span>
              {url_link}
            </div>
          </div>
          {img_tag}
          <div class="cv-card-body">
            {desc_str}
          </div>
        </div>
        """

    html += f"""
      </section>

      <!-- SECTION 6: PEER REVIEW & EDITORIAL CONTRIBUTIONS -->
      <section id="peer-review" class="cv-section">
        <div class="cv-section-tag">06 / SCHOLARLY RIGOR</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Peer Review &amp; Editorial Board Contributions</h2>
          <a href="{cv['peer_review_and_editorial']['comprehensive_link']}" target="_blank" rel="noopener" class="cv-section-count" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">
            {render_svg_icon('external')} Publons / WoS Record
          </a>
        </div>
        <p style="font-size: 0.92rem; color: var(--text-body); margin-bottom: 18px; line-height: 1.6;">
          {cv['peer_review_and_editorial']['summary']}
        </p>

        <h3 style="font-size: 1.1rem; font-weight: 800; color: #ffffff; margin-bottom: 14px;">Verified High-Impact Q1 Journals</h3>
        <div class="cv-grid-2col" style="margin-bottom: 24px;">
    """

    for jnl in cv['peer_review_and_editorial']['verified_journals']:
        html += f"""
          <div class="cv-mini-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
              <strong style="color: #ffffff; font-size: 0.98rem;">{jnl['name']}</strong>
              <span class="cv-type-pill">{jnl['tier']}</span>
            </div>
            <div style="font-size: 0.85rem; color: var(--brand-blue); margin-top: 4px;">{jnl['publisher']}</div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; font-size: 0.78rem; color: var(--text-muted);">
              <span>ISSN: {jnl['issn']}</span>
              <a href="{jnl['url']}" target="_blank" rel="noopener" style="color: var(--brand-gold); text-decoration: underline; font-weight: 700;">Verified Record &rarr;</a>
            </div>
          </div>
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
        <div class="cv-grid-2col">
    """

    for cert in cv['professional_certifications']:
        html += f"""
          <div class="cv-mini-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
              <strong style="color: #ffffff; font-size: 0.98rem; line-height: 1.35;">{cert['name']}</strong>
              <span class="cv-year-pill">{cert['period']}</span>
            </div>
            <div style="font-size: 0.85rem; color: var(--brand-blue); margin-top: 4px; font-weight: 600;">{cert['issuer']}</div>
            <div style="font-size: 0.82rem; color: var(--text-body); margin-top: 8px; line-height: 1.55;">{cert['details']}</div>
          </div>
        """

    html += f"""
        </div>
      </section>

      <!-- SECTION 8: CORE RESEARCH, BOOKS & SCHOLARLY MONOGRAPHS -->
      <section id="research-monograph" class="cv-section">
        <div class="cv-section-tag">08 / SCHOLARLY AUTHORSHIP</div>
        <div class="cv-section-title-wrap">
          <h2 class="cv-section-title">Core Research Domains, Book &amp; Scholarly Output</h2>
          <a href="publications.html" class="cv-section-count" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">
            View All {len(publications)} Works &rarr;
          </a>
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
            <div style="font-weight: 800; color: #ffffff; font-size: 1.05rem;">Complete 24-Work Peer-Reviewed Repository</div>
            <div style="font-size: 0.85rem; color: var(--text-body); margin-top: 2px;">Comprehensive catalog of Q1 IEEE Access, Springer LNCS, Scopus-indexed conference papers, and preprints.</div>
          </div>
          <a href="publications.html" class="pub-btn" style="text-decoration:none; padding: 9px 18px; font-size: 0.82rem; font-weight: 800; background: var(--brand-blue); color: #021220; border-radius: 999px;">
            Explore Publications &rarr;
          </a>
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
            <div style="margin-top: 10px;">
              <a href="{exec_prof['official_docs']['teaching_permit']['url']}" target="_blank" rel="noopener" style="font-size: 0.78rem; color: var(--brand-blue); text-decoration: underline; font-weight: 700;">Verified Document &rarr;</a>
            </div>
          </div>
          <div class="cv-mini-card">
            <div class="cv-ref-role" style="color: #38b6d0;">Institutional Accreditation</div>
            <div class="cv-ref-name" style="font-size: 0.95rem; margin-top: 4px;">MQA Official Higher Education CV</div>
            <div style="font-size: 0.82rem; color: var(--text-body); margin-top: 6px; line-height: 1.5;">Malaysian Qualifications Agency standard format for higher education accreditation.</div>
            <div style="margin-top: 10px;">
              <a href="{exec_prof['official_docs']['mqa_cv']['url']}" target="_blank" rel="noopener" style="font-size: 0.78rem; color: var(--brand-blue); text-decoration: underline; font-weight: 700;">Verified Document &rarr;</a>
            </div>
          </div>
          <div class="cv-mini-card">
            <div class="cv-ref-role" style="color: #6ee7b7;">Supervisory Roles</div>
            <div class="cv-ref-name" style="font-size: 0.95rem; margin-top: 4px;">Postgraduate Dissertation Supervision</div>
            <div style="font-size: 0.82rem; color: var(--text-body); margin-top: 6px; line-height: 1.5;">Appointed Master and Ph.D. dissertation supervisor at INTI International University and UKM.</div>
            <div style="margin-top: 10px;">
              <a href="prospective-students.html" style="font-size: 0.78rem; color: var(--brand-blue); text-decoration: underline; font-weight: 700;">Supervision Lab &rarr;</a>
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

        <div class="cv-grid-referees" style="margin-bottom: 28px;">
    """

    for ref in cv['academic_references']:
        html += f"""
          <div class="cv-mini-card">
            <div class="cv-ref-name">{ref['name']}</div>
            <div class="cv-ref-role">{ref['role']}</div>
            <div class="cv-ref-inst">{ref['institution']}</div>
            <div class="cv-ref-contact">
              <div>Phone: <a href="tel:{ref['phone']}" style="color: var(--brand-blue);">{ref['phone']}</a></div>
              <div>Email: <a href="mailto:{ref['email']}" style="color: var(--brand-blue);">{ref['email']}</a></div>
            </div>
          </div>
        """

    html += f"""
        </div>

        <div class="cv-mini-card" style="padding: 20px 24px;">
          <div class="cv-section-tag" style="margin-bottom: 8px;">PERSONAL INTERESTS &amp; EXPLORATION</div>
          <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """

    for interest in cv['personal_interests']:
        html += f"""
            <span class="cv-badge-cyan" style="font-size: 0.82rem; padding: 5px 14px;">{interest}</span>
        """

    html += """
          </div>
        </div>

      </section>

    </div>
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
  <p>Redirecting to <a href="research.html#articles" style="color:#d4af37;font-weight:bold;">Activity &amp; Project &rarr; Articles &amp; Essays</a>...</p>
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
            document.getElementById('reader-body').innerHTML = article.content_html || ('<p>' + article.excerpt + '</p>');

            if (article.image) {
              const imgWrap = document.getElementById('reader-hero-img-wrap');
              const img = document.getElementById('reader-hero-img');
              img.src = article.image;
              img.alt = article.title;
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
            document.getElementById('reader-body').innerHTML = '<p>The requested article could not be located. <a href="research.html#articles">Browse all articles &rarr;</a></p>';
          }
        } catch (err) {
          console.error(err);
          document.getElementById('reader-body').innerHTML = '<p>Error loading article. <a href="research.html#articles">Back to Activity &amp; Project &rarr;</a></p>';
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
        <a href="research.html#articles" class="article-back-link font-cinzel">&larr; Back to Activity &amp; Project</a>
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
              <div class="article-author-name">Dr. Zaid Amin, Ph.D.</div>
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
          <img src="assets/images/dr-zaid.png" alt="Dr. Zaid Amin, Ph.D." class="article-bio-avatar">
        </picture>
        <div>
          <h3 class="article-bio-name font-cinzel">Zaid Amin, Ph.D.</h3>
          <div class="article-bio-role">Senior Lecturer &bull; INTI International University, Malaysia</div>
          <p class="article-bio-text">
            Computational researcher in Human-Computer Interaction (HCI), Behavior &amp; Social Computing, Digital Ethics, and AI Governance. Ph.D. in Computer Science from Universiti Kebangsaan Malaysia (UKM).
          </p>
        </div>
      </div>

      <!-- Navigation back to hub -->
      <div style="margin-top: 40px; text-align: center;">
        <a href="research.html#articles" class="spotlight-btn btn-gold font-cinzel" style="text-decoration: none; display: inline-block;">
          &larr; Explore All Activity &amp; Articles
        </a>
      </div>
    </main>
    {reader_script}
"""
    html += get_page_footer(show_visitor_stats=False)
    return html

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

    # Note: cms.html is strictly offline/local only for security.
    # It is never copied to dist/ to guarantee 100% cyber threat immunity on public GitHub Pages.

    # Generate Clean URL Folders (e.g. /publications/index.html so .html is stripped from address bar)
    clean_routes = {
        "publications": pages["publications.html"],
        "articles": pages["articles.html"],
        "article": pages["article.html"],
        "research": pages["research.html"],
        "prospective-students": pages["prospective-students.html"],
        "talks": pages["talks.html"],
        "cv": pages["cv.html"]
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
