"""
Academic Golden Ratio Static Site Generator - zaidamin.org
Epigraph (Qur'an 31:27) • Option 1 Storm Banner Across All Pages • Wardiere Showcase Layout
Author: Antigravity AI & Dr. Zaid Amin
"""

import json
import os
import shutil
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
        "external": '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'
    }
    return icons.get(name, "")

def get_html_head(title="Dr. Zaid Amin | Academic & Computational Researcher | zaidamin.org", description=""):
    profile = load_json("profile.json")
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
  <link rel="stylesheet" href="assets/css/style.css?v=3.5">
  <link rel="icon" href="favicon.ico">
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
            <a href="cv.html#talks" class="main-menu-link {'active' if active_page == 'talks' else ''}">Recent Media &amp; Talks</a>
            <a href="research.html" class="main-menu-link {'active' if active_page == 'research' else ''}">Activity &amp; Project</a>
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
    countries = [
        {"code": "MY", "name": "Malaysia", "pct": 34.8, "count": "16.8K", "color": "#38bdf8"},
        {"code": "US", "name": "United States", "pct": 21.4, "count": "10.3K", "color": "#fbbf24"},
        {"code": "GB", "name": "United Kingdom", "pct": 12.6, "count": "6.1K", "color": "#818cf8"},
        {"code": "SG", "name": "Singapore", "pct": 9.5, "count": "4.6K", "color": "#34d399"},
        {"code": "AU", "name": "Australia", "pct": 7.2, "count": "3.5K", "color": "#f472b6"},
        {"code": "DE", "name": "Germany", "pct": 5.1, "count": "2.5K", "color": "#a78bfa"},
        {"code": "OTHER", "name": "78+ Other Nations", "pct": 9.4, "count": "4.5K", "color": "#94a3b8"}
    ]
    country_capsules_html = ""
    for c in countries:
        flag = get_flag_svg(c["code"])
        country_capsules_html += f"""
          <div class="stats-country-item" title="{c['name']}: {c['pct']}% of total academic traffic ({c['count']} visits)">
            <div class="stats-country-top">
              <span class="stats-dot" style="background: {c['color']}; box-shadow: 0 0 6px {c['color']}88;"></span>
              {flag}
              <span class="stats-country-name">{c['name']}</span>
            </div>
            <div class="stats-country-bottom">
              <span class="stats-country-pct">{c['pct']}%</span>
              <span class="stats-country-count">{c['count']}</span>
            </div>
          </div>"""

    return f"""
    <!-- Visitor Statistics & Global Academic Readership (Golden Ratio Telemetry) -->
    <section class="golden-visitor-stats" aria-label="Global Visitor Statistics &amp; Academic Readership">
      <div class="stats-header-row">
        <div class="stats-live-badge">
          <span class="stats-pulse-ring"></span>
          <span class="stats-pulse-dot"></span>
          <span class="stats-live-label">Live Readership Telemetry</span>
        </div>


        <div class="stats-meta-cluster font-cinzel">
          <span class="stats-pill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 2008 &ndash; 2026 Archive</span>
        </div>
      </div>

      <!-- 3. Horizontal List of Origin Countries -->
      <div class="stats-countries-horizontal-list">
        {country_capsules_html}
      </div>
    </section>
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
        Copyright &copy; 2008 - 2026 Dr. Zaid Amin. All Rights Reserved.
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
  <script src="assets/js/main.js"></script>
</body>
</html>
"""

# ==============================================================================
# 1. GOLDEN RATIO STANDARD COMPOSITION HOMEPAGE (index.html)
# ==============================================================================
def get_spotlight_card_html():
    return '''
      <!-- LEFT CARD: Chosen Featured Spotlight Article (Clean Editorial Display) -->
      <article class="ref-spotlight-card" aria-label="Featured Spotlight Publication">
        <div class="ref-spotlight-visual-wrap">
          <picture>
            <source srcset="assets/images/spotlight-smart-cities.webp" type="image/webp">
            <img src="assets/images/spotlight-smart-cities.jpg" alt="Trustworthy AI for Sustainable Cities" class="ref-spotlight-visual-img" loading="lazy">
          </picture>
          <div class="ref-visual-overlay"></div>
          
          <div class="ref-spotlight-top-bar">
            <span class="ref-kicker-pill font-cinzel"><span class="pulse-dot"></span> SPOTLIGHT ARTICLE</span>
            <div class="ref-top-right-group">
              <span class="ref-bookmark-icon" title="Featured Spotlight Publication" aria-label="Featured Publication Bookmark">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                </svg>
              </span>
            </div>
          </div>
        </div>

        <div class="ref-spotlight-body">
          <div class="ref-scopus-kicker font-cinzel"><span class="kicker-gem">✦</span> Q1 SCOPUS INDEXED</div>
          <h2 class="ref-spotlight-title">Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance</h2>

          <div class="ref-spotlight-meta">
            <div class="meta-row-pub">
              <span class="spotlight-venue font-cinzel">Smart Cities (MDPI)</span>
              <span class="spotlight-divider">&bull;</span>
              <span class="spotlight-year">Vol. 9 (2026)</span>
              <span class="spotlight-oa-pill font-cinzel"><span class="oa-check">&#10003;</span> Open Access</span>
            </div>
            <div class="meta-row-author">
              <span class="author-pre">Lead Author:</span> <strong class="author-name">Zaid Amin, Ph.D.</strong>
            </div>
          </div>

          <p class="ref-spotlight-desc">Addresses critical systemic vulnerabilities in urban autonomous deployments where metric-driven proxies diverge from authentic civic welfare. Introduces an audited multimodal orchestration agent architecture enforcing real-time cybernetic feedback loops, cognitive transparency, and verifiable alignment for municipal governance.</p>

          <div class="ref-spotlight-actions">
            <a href="https://doi.org/10.3390/smartcities9100174" target="_blank" rel="noopener" class="spotlight-btn btn-gold font-cinzel">
              Read Full Article &rarr;
            </a>
            <a href="https://doi.org/10.3390/smartcities9100174" target="_blank" rel="noopener" class="spotlight-doi-pill font-cinzel" title="Direct Digital Object Identifier (DOI)">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
              DOI: 10.3390/sc9100174 &nearr;
            </a>
          </div>
        </div>
      </article>'''

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

def get_portals_tray_carousel_html():
    slides_data = [
        # Slide 0: Core Portals & Top Academic Highlights (4 items)
        [
            {
                "thumb_webp": "assets/images/dr-zaid.webp",
                "thumb_jpg": "assets/images/dr-zaid.png",
                "title": "About, Talks &amp; Academic CV",
                "bullets": [
                    "Ph.D. in Computer Science (UKM)",
                    "Keynote Speaker, Media Interviews &amp; Panels",
                    "Academic Honors &amp; Leadership Track"
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
                    "Multimodal Orchestration Agent Architecture",
                    "Municipal Autonomous Auditing Prototypes"
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
                    "Trustworthy AI &amp; Civic Autonomous Systems",
                    "Full Open-Access Preprints &amp; BibTeX Citations"
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
                    "Visual Attention System for Digital Environments",
                    "Empirical Intervention &amp; Cognitive Feedback Loops"
                ],
                "tag": "IEEE Access",
                "btn_text": "Read",
                "btn_url": "https://doi.org/10.1109/ACCESS.2021.3087740",
                "is_external": True
            }
        ],
        # Slide 1: Blogger: AI, Pedagogy, Cognition & Cybernetics (4 items)
        [
            {
                "thumb_webp": "",
                "thumb_jpg": "assets/images/blogger/post_1.png",
                "title": "HARMONY: Human-Trusted AI Framework",
                "bullets": [
                    "Multi-agent normative alignment framework",
                    "Grounded ethical orchestration &amp; cybernetics",
                    "Civic trust modeling in urban autonomous systems"
                ],
                "tag": "AI / 2026",
                "btn_text": "Read",
                "btn_url": "https://www.zaidamin.org/2026/02/harmony-human-trusted-ai-and-resilient.html",
                "is_external": True
            },
            {
                "thumb_webp": "",
                "thumb_jpg": "assets/images/blogger/post_2.jpg",
                "title": "Kehidupan Pendidik Teladan Rasulullah",
                "bullets": [
                    "Pedagogical philosophy &amp; exemplary mentorship",
                    "Nurturing ethical intellect and civic empathy",
                    "Scholarly reflections on holistic education"
                ],
                "tag": "Pedagogy",
                "btn_text": "Read",
                "btn_url": "https://www.zaidamin.org/2021/05/kehidupan-pendidik-yang-diteladankan.html",
                "is_external": True
            },
            {
                "thumb_webp": "",
                "thumb_jpg": "assets/images/blogger/post_3.jpg",
                "title": "Mengenal Tipe-Tipe Bias Kognitif",
                "bullets": [
                    "Cognitive heuristics &amp; systemic decision errors",
                    "Algorithmic and human bias systemic parallels",
                    "De-biasing methodologies for critical judgment"
                ],
                "tag": "Cognition",
                "btn_text": "Read",
                "btn_url": "https://www.zaidamin.org/2020/07/mengenal-tipe-tipe-bias-dalam.html",
                "is_external": True
            },
            {
                "thumb_webp": "",
                "thumb_jpg": "assets/images/blogger/post_4.jpg",
                "title": "Cyberspace &amp; Perubahan Perilaku",
                "bullets": [
                    "Digital sociology &amp; psychological transformations",
                    "Hyper-connected environments &amp; attention economy",
                    "Human-computer behavioral paradigm shifts"
                ],
                "tag": "Cybernetics",
                "btn_text": "Read",
                "btn_url": "https://www.zaidamin.org/2019/08/cyberspace-dan-perubahan-perilaku.html",
                "is_external": True
            }
        ],
        # Slide 2: Epistemic Vigilance, Governance & Doctoral Path (4 items)
        [
            {
                "thumb_webp": "",
                "thumb_jpg": "assets/images/blogger/post_5.jpg",
                "title": "Tackling Disinformation: Fake News",
                "bullets": [
                    "Cognitive resistance against online disinformation",
                    "Epistemic vigilance in algorithm-curated media",
                    "Information literacy &amp; truth verification models"
                ],
                "tag": "Media AI",
                "btn_text": "Read",
                "btn_url": "https://www.zaidamin.org/2019/06/tackling-disinformation-fake-news-and.html",
                "is_external": True
            },
            {
                "thumb_webp": "assets/images/thumb-governance.webp",
                "thumb_jpg": "assets/images/thumb-governance.jpg",
                "title": "The Proxy Trap in Agentic AI",
                "bullets": [
                    "AI Governance Series &bull; SSRN Preprint 2026",
                    "When Metrics Replace Judgment in Autonomous Nodes",
                    "Preserving Civic Human Oversight in Admin Protocols"
                ],
                "tag": "Governance",
                "btn_text": "Examine",
                "btn_url": "https://doi.org/10.2139/ssrn.7670124",
                "is_external": True
            },
            {
                "thumb_webp": "",
                "thumb_jpg": "assets/images/blogger/post_7.jpg",
                "title": "Hal yang Tidak Kuketahui Sebelum UKM",
                "bullets": [
                    "Doctoral milestones &amp; postgraduate research life",
                    "Research rigor, perseverance &amp; publication path",
                    "Academic mentorship &amp; community building"
                ],
                "tag": "Academic",
                "btn_text": "Read",
                "btn_url": "https://www.zaidamin.org/2018/09/hal-hal-yang-tidak-kuketahui-sebelum.html",
                "is_external": True
            },
            {
                "thumb_webp": "",
                "thumb_jpg": "assets/images/blogger/post_6.jpg",
                "title": "Dimuliakan Melalui Makan &amp; Minum",
                "bullets": [
                    "Philosophical reflections on gratitude and mindfulness",
                    "Everyday rituals as avenues for dignified living",
                    "Moral cultivation in contemporary society"
                ],
                "tag": "Philosophy",
                "btn_text": "Read",
                "btn_url": "https://www.zaidamin.org/2019/06/dimuliakan-melalui-makan-dan-minum.html",
                "is_external": True
            }
        ],
        # Slide 3: Startups, Cultural Heritage & Digital Society (4 items)
        [
            {
                "thumb_webp": "",
                "thumb_jpg": "assets/images/blogger/post_8.jpg",
                "title": "E-Commerce &amp; Startup Ecosystem",
                "bullets": [
                    "Digital economy trends &amp; startup ecosystem",
                    "Empowering student innovation in commerce tech",
                    "Technology-driven enterprise development"
                ],
                "tag": "Industry",
                "btn_text": "Read",
                "btn_url": "https://www.zaidamin.org/2015/09/talk-show-e-commerce-entrepreneurship.html",
                "is_external": True
            },
            {
                "thumb_webp": "assets/images/thumb-research.webp",
                "thumb_jpg": "assets/images/thumb-research.jpg",
                "title": "Srivijayapedia Heritage Platform",
                "bullets": [
                    "JISTM (2026) &bull; Cultural Heritage Preservation",
                    "Srivijaya Civilization Semantic Digital Archive",
                    "Human-Centered Cultural Informatics Mapping"
                ],
                "tag": "JISTM 2026",
                "btn_text": "Read",
                "btn_url": "https://doi.org/10.35631/JISTM.1141001",
                "is_external": True
            },
            {
                "thumb_webp": "assets/images/thumb-attention.webp",
                "thumb_jpg": "assets/images/thumb-attention.jpg",
                "title": "Digital Loneliness &amp; Screen Epoch",
                "bullets": [
                    "Contributions to Management Science (Springer 2024)",
                    "Cognitive Distraction in Social Media Ecosystems",
                    "Algorithmic Attention Capture &amp; Behavioral Health"
                ],
                "tag": "Springer",
                "btn_text": "Read",
                "btn_url": "https://doi.org/10.1007/978-3-031-52280-2_14",
                "is_external": True
            },
            {
                "thumb_webp": "assets/images/spotlight-smart-cities.webp",
                "thumb_jpg": "assets/images/spotlight-smart-cities.jpg",
                "title": "Municipal Autonomous Auditing",
                "bullets": [
                    "MDPI Smart Cities (2026) &bull; Multi-Agent Governance",
                    "Real-Time Cybernetic Civic Feedback Loops",
                    "Mitigating Metric Divergence in Urban Systems"
                ],
                "tag": "Smart Cities",
                "btn_text": "Inspect",
                "btn_url": "https://doi.org/10.3390/smartcities9100174",
                "is_external": True
            }
        ]
    ]

    slides_html = ""
    total_slides = len(slides_data)
    for s_idx, cards in enumerate(slides_data):
        active_cls = " active" if s_idx == 0 else ""
        cards_html = ""
        for card in cards:
            if card.get("thumb_webp"):
                img_html = f'''<picture>
                  <source srcset="{card['thumb_webp']}" type="image/webp">
                  <img src="{card['thumb_jpg']}" alt="{card['title']}" class="ref-item-thumb" width="78" height="56" loading="lazy">
                </picture>'''
            else:
                img_html = f'''<img src="{card['thumb_jpg']}" alt="{card['title']}" class="ref-item-thumb" width="78" height="56" loading="lazy">'''

            bullets_html = "".join([f"<li>{b}</li>" for b in card["bullets"]])
            ext_attr = ' target="_blank" rel="noopener"' if card.get("is_external") else ""

            cards_html += f'''
            <div class="ref-item-card">
              <div class="ref-item-thumb-box">
                {img_html}
              </div>
              <div class="ref-item-info">
                <div class="ref-card-kicker-row">
                  <span class="ref-kicker-tag font-cinzel">&#10022; {card['tag']}</span>
                </div>
                <h4 class="ref-item-title font-cinzel">{card['title']}</h4>
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

    dots_html = ""
    for d_idx in range(total_slides):
        active_cls = " active" if d_idx == 0 else ""
        dots_html += f'<button class="spotlight-dot{active_cls}" data-slide-target="{d_idx}" aria-label="Slide {d_idx+1}" type="button"></button>'

    return f'''
        <!-- Inset Tray containing 4 Stacked Horizontal Cards with Vertical Sliding Ticker -->
        <div class="ref-inset-tray" id="portals-carousel" aria-roledescription="marquee" aria-label="Academic Portals and Articles">
          <!-- Tray Carousel Vertical Slides Container -->
          <div class="tray-slides-wrap">
            {slides_html}
          </div>

          <!-- Tray Indicator Dots -->
          <div class="tray-dots-bar">
            {dots_html}
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
          <span class="ticker-slide-counter font-cinzel" id="ticker-counter">1 / 6</span>
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
          <a href="cv.html#talks" class="ref-menu-tab" title="Recent Media &amp; Invited Talks">
            <span class="tab-txt-full">Media &amp; Talks</span><span class="tab-txt-compact">Media</span>
          </a>
          <a href="research.html" class="ref-menu-tab" title="Activities &amp; Funded Projects">
            <span class="tab-txt-full">Activity &amp; Project</span><span class="tab-txt-compact">Activity</span>
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
          <div class="ref-photo-ring">
            <picture>
              <source srcset="assets/images/dr-zaid.webp" type="image/webp">
              <img src="assets/images/dr-zaid.png" alt="Zaid Amin, Ph.D." class="ref-photo-img" width="114" height="114">
            </picture>
            <span class="ref-live-status" title="Active Senior Lecturer &amp; Researcher"></span>
          </div>
        </div>

        {get_activity_search_bar_html()}
        {get_portals_tray_carousel_html()}</aside>

    </section>

    """
    html += get_page_footer(show_visitor_stats=True)
    return html

def generate_publications_page():
    publications = load_json("publications.json")

    html = get_html_head("Publications (24+) | Dr. Zaid Amin | zaidamin.org", "Complete indexed research publications by Dr. Zaid Amin across Human-Computer Interaction, AI Governance, and Behavioral Computing.")
    html += get_page_header("publications")

    html += f"""
    <!-- Subpage Content: Publications Engine -->
    <div class="subpage-container">
      <div style="margin-bottom: 32px;">
        <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--brand-blue);">Scholarly Archive</span>
        <h1 style="font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; margin: 6px 0 10px 0; color: #ffffff;">Publications &amp; Citations ({len(publications)})</h1>
        <p style="font-size: 1rem; color: var(--text-muted); max-width: 760px;">
          Complete indexed works across Human-Computer Interaction, AI Governance, Behavioral Computing, and Information Systems. Search in real-time or filter by category.
        </p>
      </div>

      <div class="publications-controls">
        <input type="text" id="pub-search" class="search-input" placeholder="Search by paper title, venue, year, or keyword...">

        <div class="filter-pills">
          <button class="filter-btn active" data-filter="all">All ({len(publications)})</button>
          <button class="filter-btn" data-filter="journal">Journals</button>
          <button class="filter-btn" data-filter="conference">Conferences</button>
          <button class="filter-btn" data-filter="book chapter">Book Chapters</button>
          <button class="filter-btn" data-filter="preprint">Preprints</button>
        </div>
      </div>

      <div id="pub-count-indicator" style="margin-bottom: 16px; font-size: 0.85rem; color: var(--text-muted); font-weight: 700;">
        Showing all {len(publications)} publications
      </div>

      <div class="publications-list">
    """
    for pub in publications:
        doi_link = f'<a href="{pub["url"]}" target="_blank" rel="noopener" class="pub-btn">DOI: {pub["doi"]} {render_svg_icon("external")}</a>' if pub.get("doi") else ""

        html += f"""
        <article class="pub-item" data-category="{pub['category'].lower()}">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.75rem; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--brand-blue);">{pub['category']} &bull; {pub['year']}</span>
            {f'<span style="font-size:0.75rem; color:var(--brand-gold); font-weight:800;">★ Featured</span>' if pub.get('featured') else ''}
          </div>

          <h3 style="font-size:1.25rem; font-weight:800; margin-bottom:6px; line-height:1.35; color:#ffffff;">{pub['title']}</h3>
          <div style="font-size:0.9rem; color:var(--text-body); margin-bottom:6px;"><strong>Dr. Zaid Amin</strong> and collaborators</div>
          <div style="font-size:0.875rem; color:var(--text-muted); font-style:italic; font-family:var(--font-serif); margin-bottom:14px;">{pub['venue']}</div>

          <div style="display:flex; gap:10px; align-items:center;">
            {doi_link}
            <button class="pub-btn btn-bibtex-toggle" data-target="bib-{pub['id']}">Cite / BibTeX</button>
          </div>

          <div class="bibtex-box" id="bib-{pub['id']}">
            <button class="bibtex-copy-btn" data-target="code-{pub['id']}">Copy BibTeX</button>
            <code id="code-{pub['id']}">{pub['bibtex']}</code>
          </div>
        </article>
        """

    html += """
      </div>
    </div>
    """
    html += get_page_footer()
    return html

# ==============================================================================
# 3. RESEARCH PILLARS (research.html)
# ==============================================================================
def generate_research_page():
    research = load_json("research.json")

    html = get_html_head("Research Pillars & Grants | Dr. Zaid Amin | zaidamin.org", research["vision"])
    html += get_page_header("research")

    html += f"""
    <!-- Subpage Content: Research Pillars -->
    <div class="subpage-container">
      <div style="margin-bottom: 40px;">
        <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--brand-blue);">Scholarly Agenda</span>
        <h1 style="font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; margin: 6px 0 10px 0; color: #ffffff;">Research Pillars &amp; Grants</h1>
        <p style="font-size: 1.05rem; color: var(--text-muted); max-width: 820px; line-height: 1.6;">
          {research['vision']}
        </p>
      </div>

      <div style="display: flex; flex-direction: column; gap: 32px;">
    """
    for pillar in research["pillars"]:
        topics = " ".join([f'<span style="font-size:0.775rem; font-weight:600; padding:4px 10px; background:rgba(4, 32, 54, 0.85); border:1px solid rgba(34, 166, 200, 0.25); color:#c8e0ec; border-radius:4px; margin-right:6px; margin-bottom:6px; display:inline-block;">{t}</span>' for t in pillar["key_topics"]])
        html += f"""
        <div style="background:rgba(4, 28, 48, 0.75); border:1px solid rgba(34, 166, 200, 0.22); border-radius:18px; padding:36px; box-shadow:0 12px 35px rgba(0,10,24,0.40); backdrop-filter:blur(8px);">
          <div style="font-size:0.75rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:var(--brand-blue); margin-bottom:6px;">RESEARCH DOMAIN</div>
          <h2 style="font-size: 1.7rem; font-weight: 800; margin-bottom: 12px; color:#ffffff;">{pillar['title']}</h2>
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
    html += """
      </div>
    </div>
    """
    html += get_page_footer()
    return html

# ==============================================================================
# 4. POSTGRADUATE LAB & SUPERVISION (prospective-students.html)
# ==============================================================================
def generate_supervision_page():
    supervision = load_json("supervision.json")

    html = get_html_head("Postgraduate Lab & Supervision | Dr. Zaid Amin | zaidamin.org", supervision["statement"])
    html += get_page_header("supervision")

    html += f"""
    <!-- Subpage Content: Mentorship & Supervision -->
    <div class="subpage-container">
      <div style="margin-bottom: 36px;">
        <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--brand-blue);">Academic Mentorship</span>
        <h1 style="font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; margin: 6px 0 10px 0; color: #ffffff;">{supervision['heading']}</h1>
        <p style="font-size: 1.05rem; color: var(--text-body); line-height: 1.7; max-width: 820px;">
          {supervision['statement']}
        </p>
      </div>

      <div style="margin-bottom: 40px;">
        <h2 style="font-size: 1.6rem; font-weight: 800; margin-bottom: 20px; color: #ffffff;">Open Supervised Research Directions</h2>
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
            <h1 class="cv-hero-name">{exec_prof['name']}</h1>
            <div style="font-size: 1.12rem; font-weight: 700; color: var(--brand-blue); margin-bottom: 6px;">
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
        highlight_cls = "is-highlight" if item.get('highlight') else ""
        html += f"""
        <div class="cv-card {highlight_cls}">
          <div class="cv-card-top">
            <div class="cv-card-heading">
              <h3 class="cv-card-title">{item['title']}</h3>
              <div class="cv-card-sub">{item['organization']}</div>
            </div>
            <div class="cv-card-badges">
              <span class="cv-year-pill">{item['year']}</span>
              <span class="cv-type-pill">{item['badge']}</span>
            </div>
          </div>
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
          <span class="cv-section-count">{len(cv['invited_talks_and_media'])} Keynotes</span>
        </div>
    """

    for item in cv['invited_talks_and_media']:
        url_link = f'<a href="{item["url"]}" target="_blank" rel="noopener" class="cv-type-pill" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">{render_svg_icon("external")} Verification Link</a>' if item.get('url') else ''
        html += f"""
        <div class="cv-card is-highlight">
          <div class="cv-card-top">
            <div class="cv-card-heading">
              <h3 class="cv-card-title">{item['event']}</h3>
              <div class="cv-card-sub">{item['venue']}</div>
            </div>
            <div class="cv-card-badges">
              <span class="cv-year-pill">{item['year']}</span>
              <span class="cv-type-pill">{item['role']}</span>
              {url_link}
            </div>
          </div>
          <div class="cv-card-body">
            {item['details']}
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

def build_all():
    print("Compiling Golden Ratio Standard Academic Site for zaidamin.org...")
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    pages = {
        "index.html": generate_golden_ratio_home(),
        "publications.html": generate_publications_page(),
        "research.html": generate_research_page(),
        "prospective-students.html": generate_supervision_page(),
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

    # Copy CNAME, favicon, BibTeX
    for extra in ["CNAME", "favicon.ico", "data/publications.bib"]:
        src = BASE_DIR / extra
        if src.exists():
            shutil.copy(src, DIST_DIR / Path(extra).name)

    print("Golden Ratio build complete!")

if __name__ == "__main__":
    build_all()
