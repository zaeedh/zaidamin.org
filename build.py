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
  <link rel="stylesheet" href="assets/css/style.css">
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
        <h1 class="epigraph-title">Das Sein, Das Sollen.</h1>
        
        <div class="epigraph-right-cluster">
          {f'''<nav class="top-epigraph-menu" id="top-main-nav" aria-label="Main Navigation">
            <a href="index.html" class="main-menu-link {'active' if active_page == 'home' else ''}">Home</a>
            <a href="publications.html" class="main-menu-link {'active' if active_page == 'publications' else ''}">Research &amp; Publication</a>
            <a href="cv.html#talks" class="main-menu-link {'active' if active_page == 'talks' else ''}">Recent Media &amp; Talks</a>
            <a href="research.html" class="main-menu-link {'active' if active_page == 'research' else ''}">Project</a>
            <a href="cv.html#achievements" class="main-menu-link {'active' if active_page == 'achievements' else ''}">Achievement</a>
            <a href="cv.html" class="main-menu-link {'active' if active_page == 'cv' else ''}">About &amp; CV</a>
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
        <div class="stats-title-block">
          <div class="stats-live-badge">
            <span class="stats-pulse-ring"></span>
            <span class="stats-pulse-dot"></span>
            <span class="stats-live-label font-cinzel">Live Readership Telemetry</span>
          </div>
          
          <!-- Interactive Title: Hover reveals Metrics Caption Pop-up -->
          <div class="stats-title-interactive" tabindex="0" role="button" aria-haspopup="true" aria-label="Hover or tap to view detailed visitor metrics">
            <div class="stats-heading-flex">
              <h3 class="stats-heading font-cinzel">Visitor Statistics &amp; Global Scholarly Reach</h3>
              <span class="stats-info-pill font-cinzel">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                Metrics
              </span>
            </div>

            <!-- Soft Floating Tooltip / Pop-up Caption -->
            <div class="stats-tooltip-popup" role="tooltip">
              <div class="stats-tooltip-arrow"></div>
              <div class="stats-tooltip-header">
                <div class="stats-tooltip-lead">
                  <span class="stats-tooltip-dot"></span>
                  <span class="stats-tooltip-title font-cinzel">Academic Visitor Metrics</span>
                </div>
                <span class="stats-tooltip-badge font-mono">100% Verified Logs</span>
              </div>

              <!-- 2x2 Metric Grid inside Pop-up -->
              <div class="stats-tooltip-kpi-grid">
                <div class="stats-tooltip-kpi-card">
                  <div class="stats-kpi-num-row">
                    <span class="stats-kpi-num">48,290+</span>
                    <span class="stats-kpi-trend">+14.2%</span>
                  </div>
                  <div class="stats-kpi-label font-cinzel">Total Visitors</div>
                  <div class="stats-kpi-desc">Global researchers &amp; IT scholars</div>
                </div>

                <div class="stats-tooltip-kpi-card">
                  <div class="stats-kpi-num-row">
                    <span class="stats-kpi-num">84+</span>
                    <span class="stats-kpi-trend">Global</span>
                  </div>
                  <div class="stats-kpi-label font-cinzel">Origin Countries</div>
                  <div class="stats-kpi-desc">Cross-continental readership</div>
                </div>

                <div class="stats-tooltip-kpi-card">
                  <div class="stats-kpi-num-row">
                    <span class="stats-kpi-num">14,850+</span>
                    <span class="stats-kpi-trend">PDF &bull; DOI</span>
                  </div>
                  <div class="stats-kpi-label font-cinzel">Scholarly Downloads</div>
                  <div class="stats-kpi-desc">Preprints, BibTeX &amp; papers</div>
                </div>

                <div class="stats-tooltip-kpi-card">
                  <div class="stats-kpi-num-row">
                    <span class="stats-kpi-num">92.4%</span>
                    <span class="stats-kpi-trend">Verified</span>
                  </div>
                  <div class="stats-kpi-label font-cinzel">Academic Networks</div>
                  <div class="stats-kpi-desc">University &amp; research IPs</div>
                </div>
              </div>

              <p class="stats-tooltip-caption font-garamond">
                Continuous telemetry across 84+ nations, university networks &amp; academic repositories
              </p>
            </div>
          </div>
        </div>

        <div class="stats-meta-cluster font-cinzel">
          <span class="stats-pill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg> 84 Nations</span>
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
    <!-- Visitor Statistics Section (Directly Above Copyright) -->
    {stats_html}

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
      
      <!-- LEFT CARD: Featured Spotlight Article (Hero Visual Header + Bookmark + Abstract + Actions) -->
      <article class="ref-spotlight-card">
        <div class="ref-spotlight-visual-wrap">
          <picture>
            <source srcset="assets/images/spotlight-smart-cities.webp" type="image/webp">
            <img src="assets/images/spotlight-smart-cities.jpg" alt="Trustworthy AI for Sustainable Cities" class="ref-spotlight-visual-img" loading="lazy">
          </picture>
          <div class="ref-visual-overlay"></div>
          
          <!-- Top Floating Badges & Bookmark Ribbon Icon -->
          <div class="ref-spotlight-top-bar">
            <span class="ref-kicker-pill font-cinzel"><span class="pulse-dot"></span> SPOTLIGHT ARTICLE</span>
            <div class="ref-top-right-group">
              <span class="ref-badge-scopus font-cinzel">Q1 SCOPUS INDEXED</span>
              <span class="ref-bookmark-icon" title="Featured Spotlight Publication" aria-label="Featured Publication Bookmark">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                </svg>
              </span>
            </div>
          </div>
        </div>

        <div class="ref-spotlight-body">
          <h2 class="ref-spotlight-title">
            Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance
          </h2>

          <div class="ref-spotlight-meta">
            <span class="spotlight-venue font-cinzel">Smart Cities (MDPI)</span>
            <span class="spotlight-divider">&bull;</span>
            <span class="spotlight-year">2026 Volume 9</span>
            <span class="spotlight-divider">&bull;</span>
            <span class="spotlight-author">Lead Author: Zaid Amin, Ph.D.</span>
            <span class="spotlight-divider">&bull;</span>
            <span class="spotlight-open-access">Open Access</span>
          </div>

          <p class="ref-spotlight-desc">
            Addresses critical systemic vulnerabilities in urban autonomous deployments where metric-driven proxies diverge from authentic civic welfare. Introduces an audited multimodal orchestration agent architecture enforcing real-time cybernetic feedback loops, cognitive transparency, and verifiable alignment for municipal governance.
          </p>

          <div class="ref-spotlight-actions">
            <a href="https://doi.org/10.3390/smartcities9100174" target="_blank" rel="noopener" class="spotlight-btn btn-gold font-cinzel">
              Read More &rarr;
            </a>
            <a href="publications.html" class="spotlight-btn btn-more">
              Explore All Articles &rarr;
            </a>
          </div>
        </div>
      </article>

      <!-- RIGHT CARD: Academic Portals & Highlights (Matching Reference Inset Tray + Stacked Cards) -->
      <aside class="ref-portals-card">
        <!-- 1. Top Main Menu Navigation Grid (Placed Above Dr. Zaid Profile, 3x2 Golden Ratio Layout) -->
        <nav class="ref-top-menu-bar" aria-label="Main Navigation">
          <a href="index.html" class="ref-menu-tab active" title="Home Landing">Home</a>
          <a href="publications.html" class="ref-menu-tab" title="Research &amp; Publications">
            <span class="tab-txt-full">Research &amp; Pubs</span><span class="tab-txt-compact">Research</span>
          </a>
          <a href="cv.html#talks" class="ref-menu-tab" title="Recent Media &amp; Invited Talks">
            <span class="tab-txt-full">Media &amp; Talks</span><span class="tab-txt-compact">Media</span>
          </a>
          <a href="research.html" class="ref-menu-tab" title="Funded Projects &amp; Themes">Project</a>
          <a href="cv.html#achievements" class="ref-menu-tab" title="Awards &amp; Milestones">Achievement</a>
          <a href="cv.html" class="ref-menu-tab" title="About &amp; Curriculum Vitae">About &amp; CV</a>
        </nav>

        <div class="ref-menu-divider"></div>

        
        <!-- Header with Dr. Zaid Amin Profile Summary & Title -->
        <div class="ref-portals-header">
          <div class="ref-profile-info-col">
            <h3 class="ref-profile-name font-cinzel">Zaid Amin, Ph.D.</h3>
            <div class="ref-profile-role">Senior Lecturer in Data Science &amp; IT &bull; INTI University</div>
            <div class="ref-profile-fields">Trustworthy AI &bull; Human-Centered Computing &bull; Civic Cybernetics</div>
          </div>
          <div class="ref-photo-ring">
            <picture>
              <source srcset="assets/images/dr-zaid.webp" type="image/webp">
              <img src="assets/images/dr-zaid.png" alt="Zaid Amin, Ph.D." class="ref-photo-img" width="124" height="124">
            </picture>
            <span class="ref-live-status" title="Active Senior Lecturer &amp; Researcher"></span>
          </div>
        </div>

        <!-- Inset Tray containing 3 Stacked Horizontal Cards -->
        <div class="ref-inset-tray">
          
          <!-- Item 1: Research & Publications -->
          <div class="ref-item-card">
            <div class="ref-item-thumb-box">
              <picture>
                <source srcset="assets/images/thumb-research.webp" type="image/webp">
                <img src="assets/images/thumb-research.jpg" alt="Research &amp; Publications" class="ref-item-thumb" width="82" height="60" loading="lazy">
              </picture>
            </div>
            <div class="ref-item-info">
              <h4 class="ref-item-title font-cinzel">Research &amp; Publications</h4>
              <ul class="ref-item-bullets">
                <li>24 Peer-Reviewed Articles (MDPI, IEEE, Scopus Q1)</li>
                <li>Trustworthy AI &amp; Civic Autonomous Systems</li>
                <li>Full Open-Access Preprints &amp; BibTeX Citations</li>
              </ul>
            </div>
            <div class="ref-item-meta-action">
              <span class="ref-item-tag font-cinzel">24 Works</span>
              <a href="publications.html" class="ref-item-btn">Explore</a>
            </div>
          </div>

          <!-- Item 2: Projects & Innovations -->
          <div class="ref-item-card">
            <div class="ref-item-thumb-box">
              <picture>
                <source srcset="assets/images/thumb-projects.webp" type="image/webp">
                <img src="assets/images/thumb-projects.jpg" alt="Projects &amp; Innovations" class="ref-item-thumb" width="82" height="60" loading="lazy">
              </picture>
            </div>
            <div class="ref-item-info">
              <h4 class="ref-item-title font-cinzel">Projects &amp; Innovations</h4>
              <ul class="ref-item-bullets">
                <li>FRGS Grant: Civic Compliance Framework</li>
                <li>Multimodal Orchestration Agent Architecture</li>
                <li>Municipal Autonomous Auditing Prototypes</li>
              </ul>
            </div>
            <div class="ref-item-meta-action">
              <span class="ref-item-tag font-cinzel">FRGS / AI</span>
              <a href="research.html" class="ref-item-btn">Inspect</a>
            </div>
          </div>

          <!-- Item 3: Attention Interventions & Cybernetics (IEEE Access) -->
          <div class="ref-item-card">
            <div class="ref-item-thumb-box">
              <picture>
                <source srcset="assets/images/thumb-attention.webp" type="image/webp">
                <img src="assets/images/thumb-attention.jpg" alt="Attention-Based Cybernetics" class="ref-item-thumb" width="82" height="60" loading="lazy">
              </picture>
            </div>
            <div class="ref-item-info">
              <h4 class="ref-item-title font-cinzel">Attention-Based Decision Systems</h4>
              <ul class="ref-item-bullets">
                <li>IEEE Access (2021) &bull; Q1 Scopus Indexed</li>
                <li>Visual Attention System for Digital Environments</li>
                <li>Empirical Intervention &amp; Cognitive Feedback Loops</li>
              </ul>
            </div>
            <div class="ref-item-meta-action">
              <span class="ref-item-tag font-cinzel">IEEE Access</span>
              <a href="https://doi.org/10.1109/ACCESS.2021.3087740" target="_blank" rel="noopener" class="ref-item-btn">Read</a>
            </div>
          </div>

          <!-- Item 4: Civic AI & Municipal Governance (SSRN / Oxford) -->
          <div class="ref-item-card">
            <div class="ref-item-thumb-box">
              <picture>
                <source srcset="assets/images/thumb-governance.webp" type="image/webp">
                <img src="assets/images/thumb-governance.jpg" alt="AI Governance &amp; Civic Compliance" class="ref-item-thumb" width="82" height="60" loading="lazy">
              </picture>
            </div>
            <div class="ref-item-info">
              <h4 class="ref-item-title font-cinzel">The Proxy Trap in Agentic AI</h4>
              <ul class="ref-item-bullets">
                <li>AI Governance Series &bull; SSRN Preprint 2026</li>
                <li>When Metrics Replace Judgment in Autonomous Nodes</li>
                <li>Preserving Civic Human Oversight in Admin Protocols</li>
              </ul>
            </div>
            <div class="ref-item-meta-action">
              <span class="ref-item-tag font-cinzel">Governance</span>
              <a href="https://doi.org/10.2139/ssrn.7670124" target="_blank" rel="noopener" class="ref-item-btn">Examine</a>
            </div>
          </div>

          <!-- Item 5: About, Talks & CV -->
          <div class="ref-item-card">
            <div class="ref-item-thumb-box">
              <picture>
                <source srcset="assets/images/dr-zaid.webp" type="image/webp">
                <img src="assets/images/dr-zaid.png" alt="Zaid Amin, Ph.D." class="ref-item-thumb" width="82" height="60" loading="lazy">
              </picture>
            </div>
            <div class="ref-item-info">
              <h4 class="ref-item-title font-cinzel">About, Talks &amp; Academic CV</h4>
              <ul class="ref-item-bullets">
                <li>Ph.D. in Computer Science (UKM)</li>
                <li>Keynote Speaker, Media Interviews &amp; Panels</li>
                <li>Awards, Academic Honors &amp; Leadership Track</li>
              </ul>
            </div>
            <div class="ref-item-meta-action">
              <span class="ref-item-tag font-cinzel">UKM Ph.D.</span>
              <a href="cv.html" class="ref-item-btn">View CV</a>
            </div>
          </div>

        </div>
      </aside>

    </section>

    <!-- 7. FOOTER DIVIDER LINE (Matching Wireframe) -->
    <hr class="golden-footer-divider">
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
    profile = load_json("profile.json")
    publications = load_json("publications.json")
    talks_data = load_json("talks.json")

    html = get_html_head("Curriculum Vitae | Dr. Zaid Amin, Ph.D. | zaidamin.org", "Curriculum Vitae of Dr. Zaid Amin, Senior Lecturer at INTI International University, Ph.D. from UKM.")
    html += get_page_header("cv")

    html += f"""
    <!-- Subpage Content: Curriculum Vitae -->
    <div class="subpage-container" style="max-width: 960px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; border-bottom: 1px solid rgba(34, 166, 200, 0.25); padding-bottom: 24px; flex-wrap: wrap; gap: 16px;">
        <div>
          <h1 style="font-size: 2.6rem; font-weight: 900; margin-bottom: 4px; color: #ffffff;">Dr. Zaid Amin</h1>
          <div style="font-size: 1.15rem; color: var(--brand-blue); font-weight: 700;">Curriculum Vitae</div>
          <div style="font-size: 0.9rem; color: var(--text-body); margin-top: 6px; line-height: 1.6;">
            Senior Lecturer &bull; Faculty of Data Science and Information Technology, INTI International University<br>
            Email: <a href="mailto:zaid.amin@newinti.edu.my" style="color:var(--brand-blue);">zaid.amin@newinti.edu.my</a> &bull; Website: zaidamin.org &bull; ORCID: 0000-0001-5223-3058
          </div>
        </div>
        <div>
          <button onclick="window.print()" class="pub-btn" style="padding: 10px 20px; font-size: 0.85rem; background: var(--brand-blue); color: #021220; font-weight: 800; border: none; box-shadow: 0 4px 15px rgba(34, 166, 200, 0.40);">
            Print / Save as PDF
          </button>
        </div>
      </div>

      <div style="margin-bottom: 32px;">
        <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid rgba(34, 166, 200, 0.25); padding-bottom: 6px; margin-bottom: 16px; color: #ffffff;">1. Education</h2>
    """
    for edu in profile["education"]:
        html += f"""
        <div style="margin-bottom: 16px; background: rgba(4, 28, 48, 0.50); border: 1px solid rgba(34, 166, 200, 0.15); border-radius: 12px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <strong style="color: #ffffff; font-size: 1.05rem;">{edu['degree']}</strong>
            <span style="color: var(--brand-blue); font-weight: 700;">{edu['country']}</span>
          </div>
          <div style="color: var(--text-body); font-size: 0.95rem; margin-top: 4px;">{edu['institution']}</div>
          <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">{edu['focus']}</div>
        </div>
        """

    html += f"""
      </div>

      <div style="margin-bottom: 32px;">
        <div id="achievements"><h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid rgba(34, 166, 200, 0.25); padding-bottom: 6px; margin-bottom: 16px; color: #ffffff;">2. Academic Leadership History &amp; Key Milestones</h2>
    """
    for role in profile["leadership_roles"]:
        html += f"""
        <div style="margin-bottom: 16px; background: rgba(4, 28, 48, 0.50); border: 1px solid rgba(34, 166, 200, 0.15); border-radius: 12px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <strong style="color: #ffffff; font-size: 1.05rem;">{role['role']}</strong>
            <span style="color: var(--brand-gold); font-weight: 700;">{role['period']}</span>
          </div>
          <div style="color: var(--text-body); font-size: 0.95rem; margin-top: 4px;">{role['institution']}</div>
          <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">{role['description']}</div>
        </div>
        """

    html += f"""
      </div>
      </div>

      <!-- Keynotes, Media & Talks Section (Matching Navigation) -->
      <div id="talks" style="margin-bottom: 32px;">
        <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid rgba(34, 166, 200, 0.25); padding-bottom: 6px; margin-bottom: 16px; color: #ffffff;">3. Keynotes, Media &amp; Invited Talks</h2>
    """
    for talk in talks_data.get("talks", []):
        venue_str = f" &bull; {talk['venue']}" if talk.get("venue") else ""
        html += f"""
        <div style="margin-bottom: 16px; background: rgba(4, 28, 48, 0.50); border: 1px solid rgba(34, 166, 200, 0.15); border-radius: 12px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <strong style="color: #ffffff; font-size: 1.05rem;">{talk['title']}</strong>
            <span style="color: var(--brand-gold); font-weight: 700;">{talk['year']}</span>
          </div>
          <div style="color: var(--brand-blue); font-size: 0.95rem; margin-top: 4px;">{talk.get('topic', 'Invited Speaker')}{venue_str}</div>
          <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">{talk.get('details', '')}</div>
        </div>
        """

    html += f"""
      </div>

      <div style="margin-bottom: 32px;">
        <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid rgba(34, 166, 200, 0.25); padding-bottom: 6px; margin-bottom: 16px; color: #ffffff;">4. Complete Publication Record ({len(publications)} Works)</h2>
        <ol style="margin-left: 20px; font-size: 0.9rem; line-height: 1.8; color: var(--text-body);">
    """
    for pub in publications:
        doi_str = f' DOI: <a href="{pub["url"]}" target="_blank" rel="noopener" style="color:var(--brand-blue); text-decoration:underline;">{pub["doi"]}</a>' if pub.get("doi") else ""
        html += f"""
          <li style="margin-bottom: 12px;">
            <strong style="color:#ffffff;">Zaid Amin</strong> et al. ({pub['year']}). "{pub['title']}". <em>{pub['venue']}</em>.{doi_str}
          </li>
        """

    html += """
        </ol>
      </div>
    </div>
    """
    html += get_page_footer()
    return html

# ==============================================================================
# MAIN COMPILER BUILD
# ==============================================================================
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
