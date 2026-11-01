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
    star_svg = '''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" class="david-star-svg">
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
          <!-- Main Menu: Positioned on top row (Justify Right, Borderless, Hides on Star Hover/Click) -->
          <nav class="top-epigraph-menu" id="top-main-nav" aria-label="Main Navigation">
            <a href="index.html" class="main-menu-link {'active' if active_page == 'home' else ''}">Home</a>
            <a href="publications.html" class="main-menu-link {'active' if active_page == 'publications' else ''}">Research &amp; Publication</a>
            <a href="cv.html#talks" class="main-menu-link {'active' if active_page == 'talks' else ''}">Recent Media &amp; Talks</a>
            <a href="research.html" class="main-menu-link {'active' if active_page == 'research' else ''}">Project</a>
            <a href="cv.html#achievements" class="main-menu-link {'active' if active_page == 'achievements' else ''}">Achievement</a>
            <a href="cv.html" class="main-menu-link {'active' if active_page == 'cv' else ''}">About &amp; CV</a>
          </nav>

          <!-- Top-Right Star of David Button & Side-Expanding Scholarly Profiles -->
          <div class="top-scholarly-cluster">
            <div class="top-scholarly-links" id="top-scholarly-links" aria-hidden="true">
              <span class="top-scholarly-label">Scholarly Profiles &amp; Direct Identifiers:</span>
              <a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" class="top-link-pill" title="Google Scholar">{render_svg_icon('scholar')} <span>Google Scholar</span></a>
              <a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" class="top-link-pill" title="ORCID">{render_svg_icon('orcid')} <span>ORCID</span></a>
              <a href="{profile['social_links']['github']}" target="_blank" rel="noopener" class="top-link-pill" title="GitHub">{render_svg_icon('github')} <span>GitHub</span></a>
              <a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="top-link-pill" title="LinkedIn">{render_svg_icon('linkedin')} <span>LinkedIn</span></a>
              <a href="mailto:{profile['social_links']['email']}" class="top-link-pill" title="Institutional Email">{render_svg_icon('email')} <span>Institutional Email</span></a>
            </div>

            <!-- Pure Rotating Star of David Button (No circle boundary!) -->
            <button class="david-star-pure-btn" id="star-toggle-btn" aria-label="Toggle Scholarly Profiles" title="Scholarly Profiles & Direct Identifiers" aria-expanded="false">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" class="david-star-svg">
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
    </section>

    <!-- 3. Sub-Section Below Storm: Full Fit Second-Gaze Quotation (Qur'an 31:27) -->
    <section class="ocean-quote-subsection">
      <div class="ocean-quote-full-frame">
        <p class="golden-quotation-text font-serif">
          &ldquo;If all the trees on earth were pens and the ocean were ink, refilled by seven other oceans, the Words of Allah would not be exhausted. Surely Allah is Almighty, All-Wise.&rdquo;
        </p>
        <cite class="golden-quotation-cite">
          <span class="golden-cite-line"></span>
          <span class="golden-cite-label font-cinzel">Qur&rsquo;an 31:27</span>
          <span class="golden-cite-line"></span>
        </cite>
      </div>
    </section>
"""

def get_page_footer():
    return """
    <!-- Site Footer -->
    <footer class="golden-footer">
      <div class="footer-left">
        &copy; 2026 Dr. Zaid Amin &bull; Faculty of Data Science and Information Technology, INTI International University.
      </div>
      <div class="footer-right">
        <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle theme">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 24a7 7 0 1 1 0-14 7 7 0 0 1 0 14zm0-24L0 9.5l4.8 3.8v6.7L12 24l7.2-4v-6.7l4.8-3.8L12 0zm0 3.7l7.1 5.8-7.1 5.8-7.1-5.8 7.1-5.8z"/></svg>
        </button>
      </div>
    </footer>

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
    <!-- 5. GOLDEN RATIO SPLIT SECTION: SPOTLIGHT ARTICLE (~61.8%) & PROFILE CARD (~38.2%) -->
    <section class="golden-split-section">
      
      <!-- LEFT: Major Spotlight Article (61.8% Golden Ratio Proportion) -->
      <article class="spotlight-article-card">
        <div class="spotlight-header-row">
          <span class="spotlight-kicker font-cinzel"><span class="pulse-dot"></span> SPOTLIGHT ARTICLE</span>
          <span class="spotlight-badge-q1 font-cinzel">Q1 SCOPUS INDEXED</span>
        </div>

        <h2 class="spotlight-article-title">
          Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance
        </h2>

        <div class="spotlight-meta-line">
          <span class="spotlight-venue font-cinzel">Smart Cities (MDPI)</span>
          <span class="spotlight-divider">&bull;</span>
          <span class="spotlight-year">2026 Volume 9</span>
          <span class="spotlight-divider">&bull;</span>
          <span class="spotlight-author">Lead Author: Dr. Zaid Amin, Ph.D.</span>
          <span class="spotlight-divider">&bull;</span>
          <span class="spotlight-open-access">Open Access</span>
        </div>

        <p class="spotlight-summary">
          Addresses critical systemic vulnerabilities in urban autonomous deployments where metric-driven proxies diverge from authentic civic welfare. Introduces an audited multimodal orchestration agent architecture enforcing real-time cybernetic feedback loops, cognitive transparency, and verifiable alignment for municipal governance.
        </p>

        <div class="spotlight-highlights-grid">
          <div class="spotlight-highlight-item">
            <span class="highlight-num font-cinzel">01</span>
            <div class="highlight-body">
              <strong>Multi-Agent Governance:</strong> Formal auditing protocols mitigating reward hacking and metric substitution across decentralized municipal nodes.
            </div>
          </div>
          <div class="spotlight-highlight-item">
            <span class="highlight-num font-cinzel">02</span>
            <div class="highlight-body">
              <strong>Civic Behavioral Cybernetics:</strong> Preserving human ethical discretion and attention-driven oversight within automated administrative decisions.
            </div>
          </div>
        </div>

        <div class="spotlight-actions-bar">
          <a href="https://doi.org/10.3390/smartcities9100174" target="_blank" rel="noopener" class="spotlight-btn btn-gold font-cinzel">
            Read Paper (DOI) &nearr;
          </a>
          <a href="https://doi.org/10.3390/smartcities9100174" target="_blank" rel="noopener" class="spotlight-btn btn-outline">
            PDF Preprint
          </a>
          <button onclick="copyBibtex('amin2026trustworthy')" class="spotlight-btn btn-ghost" title="Copy BibTeX Citation">
            Copy BibTeX
          </button>
          <a href="publications.html" class="spotlight-btn btn-more">
            Explore All 24 Publications &rarr;
          </a>
        </div>
      </article>

      <!-- RIGHT: Profile Card with Circular Photo, Bio & 4 Stacked Rectangular Buttons (~38.2%) -->
      <aside class="profile-feature-card">
        <div class="profile-feature-content">
          
          <!-- Circular Photo -->
          <div class="profile-photo-col">
            <div class="profile-photo-ring">
              <picture>
                <source srcset="assets/images/dr-zaid.webp" type="image/webp">
                <img src="assets/images/dr-zaid.png" alt="Dr. Zaid Amin" class="profile-circular-avatar" width="110" height="110">
              </picture>
              <span class="profile-live-status" title="Active Senior Lecturer &amp; Researcher"></span>
            </div>
          </div>

          <!-- Middle Bio Details -->
          <div class="profile-info-col">
            <h3 class="profile-person-name">Dr. Zaid Amin</h3>
            <div class="profile-person-title">Senior Lecturer in Data Science &amp; IT</div>
            <div class="profile-person-dept">Faculty of Data Science &amp; IT (FDSIT)<br>INTI International University, Malaysia</div>
            <div class="profile-person-degree font-cinzel">Ph.D. Computer Science &bull; UKM</div>
            <p class="profile-person-bio">
              Trustworthy AI &bull; Human-Centered Computing &bull; Civic Cybernetics
            </p>
          </div>

          <!-- Right Stack: 4 Rectangular Action Buttons (Matching Wireframe [ ] [ ] [ ] [ ]) -->
          <div class="profile-actions-stack">
            <a href="cv.html" class="profile-rect-btn" title="View Full Curriculum Vitae">
              <span class="rect-btn-icon">📄</span>
              <span class="rect-btn-text">Full CV</span>
            </a>
            <a href="mailto:{profile['social_links']['email']}" class="profile-rect-btn" title="Institutional Email Contact">
              <span class="rect-btn-icon">✉</span>
              <span class="rect-btn-text">Email</span>
            </a>
            <a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" class="profile-rect-btn" title="ORCID Profile">
              <span class="rect-btn-icon">🆔</span>
              <span class="rect-btn-text">ORCID</span>
            </a>
            <a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" class="profile-rect-btn" title="Google Scholar Profile">
              <span class="rect-btn-icon">🎓</span>
              <span class="rect-btn-text">Scholar</span>
            </a>
          </div>

        </div>
      </aside>

    </section>

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

    <!-- 7. FOOTER DIVIDER LINE (Matching Wireframe) -->
    <hr class="golden-footer-divider">
    """
    html += get_page_footer()
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
