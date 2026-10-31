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
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="icon" href="favicon.ico">
</head>
<body>
"""

def get_page_header(active_page="home"):
    return f"""
  <div class="site-wrapper">
    
    <!-- 1. Top Epigraph -->
    <header class="epigraph-header">
      <h1 class="epigraph-title">Das Sein, Das Sollen.</h1>
      <p class="epigraph-quote font-serif">
        &ldquo;If all the trees on earth were pens and the ocean were ink, refilled by seven other oceans, the Words of Allah would not be exhausted. Surely Allah is Almighty, All-Wise.&rdquo; &mdash; Qur&rsquo;an 31:27
      </p>
    </header>

    <!-- 2. Clean, Unobstructed Lighthouse Storm Banner (Option 1 Storm - Active on Every Page) -->
    <section class="lighthouse-banner-frame">
      <picture>
        <source srcset="assets/images/lighthouse-banner.webp" type="image/webp">
        <img src="assets/images/lighthouse-banner.jpg" class="lighthouse-bg-img" alt="Lighthouse Storm over Ocean" width="2048" height="790">
      </picture>
      <canvas id="rain-canvas"></canvas>
    </section>

    <!-- 3. Top Academic Navigation Bar (Brand + Menu + Photo Avatar + Actions) -->
    <header class="ocean-top-bar">
      <a href="index.html" class="ocean-brand">
        <div class="ocean-logo-badge">ZA</div>
        <div class="ocean-brand-text">
          <span class="ocean-brand-name">Dr. Zaid Amin</span>
          <span class="ocean-brand-title">Ph.D. &bull; Senior Lecturer</span>
        </div>
      </a>
      
      <nav class="ocean-nav-links">
        <a href="index.html" class="ocean-nav-link {'active' if active_page == 'home' else ''}">HOME</a>
        <a href="publications.html" class="ocean-nav-link {'active' if active_page == 'publications' else ''}">PUBLICATIONS</a>
        <a href="research.html" class="ocean-nav-link {'active' if active_page == 'research' else ''}">RESEARCH</a>
        <a href="prospective-students.html" class="ocean-nav-link {'active' if active_page == 'supervision' else ''}">SUPERVISION</a>
        <a href="cv.html" class="ocean-nav-link {'active' if active_page == 'cv' else ''}">ABOUT &amp; CV</a>
      </nav>
      
      <div class="ocean-profile-actions">
        <a href="cv.html" class="ocean-avatar-link" title="Dr. Zaid Amin Profile">
          <picture>
            <source srcset="assets/images/dr-zaid.webp" type="image/webp">
            <img src="assets/images/dr-zaid.png" alt="Dr. Zaid Amin" class="ocean-nav-avatar">
          </picture>
          <span class="avatar-status-dot"></span>
        </a>
        <a href="mailto:zaid.amin@newinti.edu.my" class="ocean-action-dots" title="Quick Contact">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>
        </a>
      </div>
    </header>
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
    research = load_json("research.json")
    supervision = load_json("supervision.json")

    html = get_html_head("Dr. Zaid Amin | Das Sein, Das Sollen | zaidamin.org")
    html += get_page_header("home")

    html += f"""
    <!-- 3. GOLDEN RATIO MODERN ACADEMIC SHOWCASE (Wardiere Reference Layout) -->
    <section class="golden-ocean-showcase">

      <!-- Golden Ratio Split: Left Major Hero (~61.8%) & Right Minor Floating Panel (~38.2%) -->
      <div class="ocean-hero-grid">
        
        <!-- LEFT: Major Column (Headline + Bio + 3D Focus Carousel Showcase) -->
        <div class="ocean-major-hero">
          <div class="ocean-tagline-badge">
            <span class="pulse-dot"></span>
            INTI INTERNATIONAL UNIVERSITY &bull; FDSIT &bull; PH.D. UKM
          </div>

          <h2 class="ocean-headline">
            ADVANCING TRUSTWORTHY AI, COGNITIVE COMPUTING &amp; ETHICAL GOVERNANCE
          </h2>

          <p class="ocean-mission-text">
            Bridging human-centered computing, behavioral analytics, and agentic AI alignment. Former Head of Informatics Master&rsquo;s Program, driving empirical research in civic compliance, attention-based systems, and digital cultural preservation.
          </p>

          <div class="ocean-metadata-row">
            <span class="meta-date">Term 2026</span>
            <span class="meta-divider">&bull;</span>
            <span class="meta-loc">Nilai, Malaysia</span>
            <span class="meta-divider">&bull;</span>
            <a href="https://orcid.org/0000-0001-5223-3058" target="_blank" rel="noopener" class="meta-orcid">ORCID: 0000-0001-5223-3058</a>
          </div>

          <!-- 3D Research Focus Carousel Showcase -->
          <div class="ocean-carousel-showcase" id="research-carousel">
            <div class="carousel-cards-track">
              
              <!-- Card 0: Left Preview -->
              <div class="carousel-preview-card card-prev" id="carousel-card-0" onclick="setCarouselCard(0)">
                <div class="carousel-card-inner card-gradient-1">
                  <div class="carousel-card-icon">🏛️</div>
                  <div class="carousel-card-title">Digital Heritage &amp; XR</div>
                  <div class="carousel-card-sub">Srivijayapedia VR</div>
                </div>
              </div>

              <!-- Card 1: Center Active Focal Card -->
              <div class="carousel-preview-card card-active" id="carousel-card-1">
                <div class="carousel-card-inner card-gradient-2">
                  <div class="carousel-badge-live">FLAGSHIP FOCUS</div>
                  <div class="carousel-card-icon">🤖</div>
                  <div class="carousel-card-title">Trustworthy AI &amp; Governance</div>
                  <div class="carousel-card-desc">Multi-agent orchestration for sustainable smart cities, civic compliance &amp; algorithmic auditing.</div>
                  <a href="research.html" class="carousel-explore-link">Explore Theme &rarr;</a>
                </div>
                <!-- Arrow Controls -->
                <button class="carousel-arrow arrow-left" onclick="rotateCarousel(-1)" aria-label="Previous Theme">&#8249;</button>
                <button class="carousel-arrow arrow-right" onclick="rotateCarousel(1)" aria-label="Next Theme">&#8250;</button>
              </div>

              <!-- Card 2: Right Preview -->
              <div class="carousel-preview-card card-next" id="carousel-card-2" onclick="setCarouselCard(2)">
                <div class="carousel-card-inner card-gradient-3">
                  <div class="carousel-card-icon">🧠</div>
                  <div class="carousel-card-title">HCI &amp; Attention Systems</div>
                  <div class="carousel-card-sub">Cognitive Decisions</div>
                </div>
              </div>

            </div>

            <!-- Dot Indicators -->
            <div class="carousel-dots">
              <span class="dot" onclick="setCarouselCard(0)"></span>
              <span class="dot active" onclick="setCarouselCard(1)"></span>
              <span class="dot" onclick="setCarouselCard(2)"></span>
            </div>
          </div>
        </div>

        <!-- RIGHT: Minor Column (Floating Modern White/Glass Academic Card Panel) -->
        <div class="ocean-minor-panel">
          <div class="floating-packages-card">
            
            <!-- Search & Filter Bar (Matching reference explore header) -->
            <div class="card-search-header">
              <div class="search-input-box">
                <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                <input type="text" id="home-quick-filter" placeholder="Explore publications, grants, themes..." oninput="filterHomePackages(this.value)">
              </div>
              <button class="filter-settings-btn" title="Filter Categories" onclick="location.href='publications.html'">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>
              </button>
            </div>

            <div class="card-panel-heading-row">
              <h3 class="card-panel-title">Academic Packages &amp; Works</h3>
              <span class="card-panel-subtitle">Selected High-Impact Contributions</span>
            </div>

            <!-- 3 Rich Package Cards (Bromo, Lampung, Lombok style) -->
            <div class="packages-list" id="home-packages-list">
              
              <!-- Package 1: Smart Cities AI -->
              <div class="package-item-card">
                <div class="package-thumb-box thumb-ai">
                  <span class="bookmark-icon">★</span>
                  <div class="thumb-label">MDPI</div>
                </div>
                <div class="package-info-col">
                  <h4 class="package-item-title">Trustworthy AI for Sustainable Cities</h4>
                  <ul class="package-bullets">
                    <li>Multimodal Orchestration Agent Framework</li>
                    <li>MDPI Smart Cities Journal (Scopus Indexed)</li>
                    <li>Civic Compliance &amp; Ethical Systems</li>
                  </ul>
                </div>
                <div class="package-action-col">
                  <div class="package-price-metric">
                    <span class="metric-big">Q1</span>
                    <span class="metric-sub">Scopus</span>
                  </div>
                  <a href="https://doi.org/10.3390/smartcities9100174" target="_blank" rel="noopener" class="package-book-btn">Read Paper</a>
                </div>
              </div>

              <!-- Package 2: The Proxy Trap in Agentic AI -->
              <div class="package-item-card">
                <div class="package-thumb-box thumb-ethics">
                  <span class="bookmark-icon">★</span>
                  <div class="thumb-label">SSRN</div>
                </div>
                <div class="package-info-col">
                  <h4 class="package-item-title">The Proxy Trap in Agentic AI</h4>
                  <ul class="package-bullets">
                    <li>When Metrics Replace Human Judgment</li>
                    <li>High-Impact AI Governance Preprint</li>
                    <li>Behavioral Decision Theory</li>
                  </ul>
                </div>
                <div class="package-action-col">
                  <div class="package-price-metric">
                    <span class="metric-big">2026</span>
                    <span class="metric-sub">Preprint</span>
                  </div>
                  <a href="https://doi.org/10.2139/ssrn.7670124" target="_blank" rel="noopener" class="package-book-btn">Explore</a>
                </div>
              </div>

              <!-- Package 3: Attention-Based Design (IEEE Access) -->
              <div class="package-item-card">
                <div class="package-thumb-box thumb-heritage">
                  <span class="bookmark-icon">★</span>
                  <div class="thumb-label">IEEE</div>
                </div>
                <div class="package-info-col">
                  <h4 class="package-item-title">Attention-Based Design &amp; Decisions</h4>
                  <ul class="package-bullets">
                    <li>Information Sharing in Cognitive Computing</li>
                    <li>IEEE Access Flagship Review</li>
                    <li>Ph.D. UKM Foundation Research</li>
                  </ul>
                </div>
                <div class="package-action-col">
                  <div class="package-price-metric">
                    <span class="metric-big">IEEE</span>
                    <span class="metric-sub">Q1 Ranked</span>
                  </div>
                  <a href="https://doi.org/10.1109/ACCESS.2021.3087740" target="_blank" rel="noopener" class="package-book-btn">View Paper</a>
                </div>
              </div>

            </div>

            <!-- Floating Yellow Expand / Scroll-Down Button (Matching reference circular chevron) -->
            <a href="#full-academic-content" class="floating-expand-btn" title="Explore Detailed Research Agenda">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
            </a>

          </div>
        </div>

      </div>

    </section>

    <!-- 4. DETAILED ACADEMIC FOUNDATIONS & RESEARCH AGENDA -->
    <section id="full-academic-content" class="golden-academic-details">
      
      <div class="details-section-header">
        <h3 class="details-heading">Comprehensive Research Agenda &amp; Academic Leadership</h3>
        <p class="details-sub">Investigating the intersections of empirical software engineering, cognitive computing, and algorithmic integrity.</p>
      </div>

      <div class="details-grid-3col">
"""
    # Add research pillars
    for pillar in research["pillars"]:
        html += f"""
        <div class="pillar-item-card">
          <div class="pillar-badge">RESEARCH PILLAR</div>
          <h4 class="pillar-title">{pillar['title']}</h4>
          <p class="pillar-desc">{pillar['full_desc']}</p>
          <span class="pillar-grant-tag">Grant Target: {pillar['grant_alignment']}</span>
        </div>
        """

    html += f"""
      </div>

      <!-- Action & Portal Connect Strip -->
      <div class="academic-connect-strip">
        <div class="strip-left">
          <h4 class="strip-title">Join the Research Lab &bull; Prospective Postgraduate Candidates</h4>
          <p class="strip-desc">Actively recruiting Ph.D. and Master&rsquo;s researchers in Human-Computer Interaction, AI Alignment, and Digital Heritage.</p>
        </div>
        <div class="strip-right">
          <a href="prospective-students.html" class="golden-btn golden-btn-primary">Supervision Information {render_svg_icon('arrow-right')}</a>
          <a href="cv.html" class="golden-btn golden-btn-outline">Curriculum Vitae {render_svg_icon('arrow-right')}</a>
        </div>
      </div>

      <!-- Scholarly Network Cluster -->
      <div class="scholarly-network-bar">
        <span class="network-label">Scholarly Profiles &amp; Direct Identifiers:</span>
        <div class="network-links">
          <a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" class="network-pill">{render_svg_icon('scholar')} Google Scholar</a>
          <a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" class="network-pill">{render_svg_icon('orcid')} ORCID</a>
          <a href="{profile['social_links']['github']}" target="_blank" rel="noopener" class="network-pill">{render_svg_icon('github')} GitHub</a>
          <a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="network-pill">{render_svg_icon('linkedin')} LinkedIn</a>
          <a href="mailto:{profile['social_links']['email']}" class="network-pill">{render_svg_icon('email')} Institutional Email</a>
        </div>
      </div>

    </section>
"""
    html += get_page_footer()
    return html

# ==============================================================================
# 2. PUBLICATIONS ARCHIVE (publications.html)
# ==============================================================================
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
        <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid rgba(34, 166, 200, 0.25); padding-bottom: 6px; margin-bottom: 16px; color: #ffffff;">2. Academic Leadership History</h2>
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

      <div style="margin-bottom: 32px;">
        <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid rgba(34, 166, 200, 0.25); padding-bottom: 6px; margin-bottom: 16px; color: #ffffff;">3. Complete Publication Record ({len(publications)} Works)</h2>
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
