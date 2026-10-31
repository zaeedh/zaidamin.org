"""
Academic Royal Blue Storm Static Site Generator - zaidamin.org
Atmospheric Animated Storm Canvas • Centered Portrait • Simple Portfolio & Links
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
        "arrow-up-right": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"></line><polyline points="7 7 17 7 17 17"></polyline></svg>',
        "arrow-left": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>',
        "shield": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
        "eye": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>',
        "globe": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line></svg>',
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
<html lang="en">
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

def get_subpage_nav(active_page=""):
    return f"""
  <header class="subpage-nav">
    <a href="index.html" class="back-home-link">
      {render_svg_icon('arrow-left')}
      Home Storm
    </a>

    <div style="display: flex; gap: 16px; align-items: center;">
      <a href="publications.html" style="font-size: 0.825rem; font-weight: 700; text-transform: uppercase; color: {'var(--electric-cyan)' if active_page == 'publications' else 'var(--text-sub)'};">Publications</a>
      <a href="research.html" style="font-size: 0.825rem; font-weight: 700; text-transform: uppercase; color: {'var(--electric-cyan)' if active_page == 'research' else 'var(--text-sub)'};">Research</a>
      <a href="prospective-students.html" style="font-size: 0.825rem; font-weight: 700; text-transform: uppercase; color: {'var(--electric-cyan)' if active_page == 'lab' else 'var(--text-sub)'};">Join Lab</a>
      <a href="cv.html" style="font-size: 0.825rem; font-weight: 700; text-transform: uppercase; color: {'var(--electric-cyan)' if active_page == 'cv' else 'var(--text-sub)'};">CV</a>

      <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle theme">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      </button>
    </div>
  </header>
"""

# ==============================================================================
# 1. THE ROYAL BLUE STORM BANNER HOMEPAGE (index.html)
# ==============================================================================
def generate_storm_home():
    profile = load_json("profile.json")
    publications = load_json("publications.json")
    research = load_json("research.json")
    supervision = load_json("supervision.json")

    html = get_html_head("Dr. Zaid Amin | Academic & Computational Researcher | zaidamin.org")

    # Big Animated Storm Banner at the Top
    html += f"""
  <header class="storm-hero-wrapper">
    <canvas id="storm-canvas"></canvas>

    <div class="storm-hero-content">
      <!-- Eyebrow Tag -->
      <div class="storm-eyebrow">
        <span>INTI INTERNATIONAL UNIVERSITY</span> &bull;
        <span>SENIOR LECTURER</span> &bull;
        <span>UKM PH.D.</span>
      </div>

      <!-- Photo Hub in the Middle -->
      <div class="photo-hub-container">
        <div class="photo-halo-ring">
          <img src="assets/images/photo.jpg" onerror="this.onerror=null; this.src='assets/images/avatar.svg';" class="hero-portrait-img" alt="{profile['name']}">
        </div>
        <div class="photo-status-badge">Accepting Ph.D. Scholars</div>
      </div>

      <!-- Title & Credentials -->
      <h1 class="storm-title">{profile['name']}<span style="color:var(--accent-amber); font-size:2.4rem;">, Ph.D.</span></h1>
      <div class="storm-creds">Human-Computer Interaction &bull; AI Governance &bull; Behavioral Computing</div>

      <p class="storm-motto">
        &ldquo;<strong>Das Sein, das Sollen</strong> &mdash; Bridging empirical computational intelligence with human ethical purpose.&rdquo;
      </p>

      <!-- Key Buttons Cluster -->
      <div class="storm-buttons-cluster">
        <a href="publications.html" class="btn-royal-solid">
          Publications ({len(publications)})
          {render_svg_icon('arrow-up-right')}
        </a>

        <a href="research.html" class="btn-royal-glass">
          Research Pillars & Grants
          {render_svg_icon('arrow-up-right')}
        </a>

        <a href="prospective-students.html" class="btn-royal-accent">
          Join Research Lab (Ph.D./Master)
          {render_svg_icon('arrow-up-right')}
        </a>

        <a href="cv.html" class="btn-royal-glass">
          Curriculum Vitae (PDF)
          {render_svg_icon('arrow-up-right')}
        </a>
      </div>

      <!-- Scholarly Orbit Icons -->
      <div class="storm-icons-row">
        <a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" class="storm-icon-pill" title="Google Scholar">
          {render_svg_icon('scholar')}
        </a>
        <a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" class="storm-icon-pill" title="ORCID ({profile['metrics']['orcid_id']})">
          {render_svg_icon('orcid')}
        </a>
        <a href="{profile['social_links']['github']}" target="_blank" rel="noopener" class="storm-icon-pill" title="GitHub (@zaeedh)">
          {render_svg_icon('github')}
        </a>
        <a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="storm-icon-pill" title="LinkedIn">
          {render_svg_icon('linkedin')}
        </a>
        <a href="mailto:{profile['social_links']['email']}" class="storm-icon-pill" title="Email Dr. Amin">
          {render_svg_icon('email')}
        </a>
      </div>
    </div>
  </header>

  <!-- Simple Portfolio Showcase Directly Below Banner -->
  <main class="portfolio-showcase">
    <div class="showcase-header">
      <div class="showcase-tag">Academic Dossier & Agenda</div>
      <h2 class="showcase-title">Research Vision & Leadership</h2>
      <p style="color:var(--text-muted); font-size:1.05rem; max-width:680px; margin:8px auto 0 auto;">
        {research['vision']}
      </p>
    </div>

    <!-- 3 Core Research Pillars Cards -->
    <div class="royal-cards-grid">
      <div class="royal-card">
        <div class="royal-card-icon">
          {render_svg_icon('shield')}
        </div>
        <h3 class="royal-card-title">AI Governance & The Proxy Trap</h3>
        <p class="royal-card-desc">
          Mitigating metric substitution and proxy reward hacking when autonomous multi-agent AI systems make civic and organizational decisions.
        </p>
        <a href="research.html" class="royal-card-link">Explore Pillar {render_svg_icon('arrow-up-right')}</a>
      </div>

      <div class="royal-card">
        <div class="royal-card-icon">
          {render_svg_icon('eye')}
        </div>
        <h3 class="royal-card-title">HCI & Cognitive Attention</h3>
        <p class="royal-card-desc">
          Building upon the doctoral <strong>Tune-Attention Model</strong> at UKM to develop humane interface micro-frictions against viral distraction and misinformation.
        </p>
        <a href="research.html" class="royal-card-link">Explore Pillar {render_svg_icon('arrow-up-right')}</a>
      </div>

      <div class="royal-card">
        <div class="royal-card-icon">
          {render_svg_icon('globe')}
        </div>
        <h3 class="royal-card-title">Digital Heritage Preservation</h3>
        <p class="royal-card-desc">
          Synthesizing social computing and immersive VR through <strong>Srivijayapedia</strong> to preserve ancient maritime civilizational archives.
        </p>
        <a href="research.html" class="royal-card-link">Explore Pillar {render_svg_icon('arrow-up-right')}</a>
      </div>
    </div>

    <!-- Royal Metrics Strip -->
    <div class="royal-metrics-strip">
      <div>
        <div class="metric-num">24+</div>
        <div class="metric-lbl">Indexed Publications</div>
      </div>
      <div>
        <div class="metric-num">Q1</div>
        <div class="metric-lbl">IEEE Access & MDPI</div>
      </div>
      <div>
        <div class="metric-num">10+</div>
        <div class="metric-lbl">Years Leadership</div>
      </div>
      <div>
        <div class="metric-num">Ph.D.</div>
        <div class="metric-lbl">Universiti Kebangsaan Malaysia</div>
      </div>
    </div>

    <!-- Featured Flagship Publications (Top 3) -->
    <div class="featured-pubs-wrap">
      <div class="featured-header-row">
        <div>
          <span style="font-size:0.75rem; font-weight:800; color:var(--electric-cyan); text-transform:uppercase; letter-spacing:0.1em;">Flagship Works</span>
          <h3 style="font-size:1.6rem; font-weight:800; margin-top:4px;">Selected Recent Scholarship</h3>
        </div>
        <a href="publications.html" class="btn-royal-glass" style="font-size:0.8rem; padding:8px 18px;">
          View All 24 Publications
          {render_svg_icon('arrow-up-right')}
        </a>
      </div>

      <div class="featured-pub-row">
        <div style="font-size:0.75rem; font-weight:800; color:var(--accent-amber); text-transform:uppercase; margin-bottom:4px;">★ Journal Article &bull; 2026 &bull; MDPI Smart Cities</div>
        <div style="font-size:1.15rem; font-weight:800; color:var(--text-main); margin-bottom:4px;">Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance</div>
        <div style="font-size:0.85rem; color:var(--text-muted); font-style:italic;">Smart Cities (MDPI) &bull; DOI: 10.3390/smartcities9100174</div>
      </div>

      <div class="featured-pub-row">
        <div style="font-size:0.75rem; font-weight:800; color:var(--accent-amber); text-transform:uppercase; margin-bottom:4px;">★ SSRN Preprint &bull; 2026</div>
        <div style="font-size:1.15rem; font-weight:800; color:var(--text-main); margin-bottom:4px;">The Proxy Trap in Agentic AI: When Metrics Replace Judgment</div>
        <div style="font-size:0.85rem; color:var(--text-muted); font-style:italic;">Social Science Research Network &bull; DOI: 10.2139/ssrn.7670124</div>
      </div>

      <div class="featured-pub-row">
        <div style="font-size:0.75rem; font-weight:800; color:var(--accent-amber); text-transform:uppercase; margin-bottom:4px;">★ Q1 Publication &bull; 2021 &bull; IEEE Access</div>
        <div style="font-size:1.15rem; font-weight:800; color:var(--text-main); margin-bottom:4px;">Attention-Based Design and User Decisions on Information Sharing: A Thematic Literature Review</div>
        <div style="font-size:0.85rem; color:var(--text-muted); font-style:italic;">IEEE Access &bull; DOI: 10.1109/ACCESS.2021.3087740</div>
      </div>
    </div>

    <!-- Postgraduate Lab Direct Callout -->
    <div style="background:linear-gradient(135deg, var(--royal-navy) 0%, var(--royal-card) 100%); border:1px solid var(--royal-border); border-radius:20px; padding:36px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
      <div>
        <div style="font-size:0.75rem; font-weight:800; color:var(--accent-amber); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">Postgraduate Supervision</div>
        <h3 style="font-size:1.6rem; font-weight:800; color:#ffffff; margin-bottom:8px;">Join My Research Group (Ph.D. & Master's)</h3>
        <p style="font-size:0.95rem; color:var(--text-sub); max-width:620px;">
          Actively recruiting self-motivated scholars in AI Governance, The Proxy Trap, and Attention Cybernetics at INTI International University.
        </p>
      </div>
      <a href="prospective-students.html" class="btn-royal-accent">
        View Open Topics & Apply
        {render_svg_icon('arrow-up-right')}
      </a>
    </div>
  </main>

  <!-- Royal Footer -->
  <footer class="royal-footer">
    <div style="margin-bottom:12px; font-weight:700; color:var(--text-main);">
      Dr. Zaid Amin, Ph.D. &bull; Faculty of Data Science and Information Technology, INTI International University
    </div>
    <div style="margin-bottom:16px; color:var(--text-muted);">
      Email: <a href="mailto:{profile['social_links']['email']}" style="color:var(--electric-cyan); text-decoration:underline;">zaid.amin@newinti.edu.my</a> &bull; Domain: <strong>zaidamin.org</strong>
    </div>
    <div style="display:flex; justify-content:center; align-items:center; gap:16px;">
      <span>&copy; 2026 Dr. Zaid Amin</span>
      <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle theme">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      </button>
    </div>
  </footer>

  <script src="assets/js/storm.js"></script>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""
    return html

# ==============================================================================
# 2. PUBLICATIONS ARCHIVE (publications.html)
# ==============================================================================
def generate_publications_page():
    publications = load_json("publications.json")

    html = get_html_head("Publications (24+) | Dr. Zaid Amin | zaidamin.org")
    html += get_subpage_nav("publications")

    html += f"""
  <div class="subpage-container">
    <div style="margin-bottom: 32px;">
      <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--electric-cyan);">Scholarly Index</span>
      <h1 style="font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; margin: 6px 0 10px 0;">Publications & Citations ({len(publications)})</h1>
      <p style="font-size: 1rem; color: var(--text-sub); max-width: 760px;">
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
          <span style="font-size:0.75rem; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--electric-cyan);">{pub['category']} &bull; {pub['year']}</span>
          {f'<span style="font-size:0.75rem; color:var(--accent-amber); font-weight:800;">★ Featured</span>' if pub.get('featured') else ''}
        </div>

        <h3 style="font-size:1.25rem; font-weight:800; margin-bottom:6px; line-height:1.35; color:var(--text-main);">{pub['title']}</h3>
        <div style="font-size:0.9rem; color:var(--text-sub); margin-bottom:6px;"><strong>Dr. Zaid Amin</strong> and collaborators</div>
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
  <script src="assets/js/main.js"></script>
</body>
</html>
"""
    return html

# ==============================================================================
# 3. RESEARCH PILLARS (research.html)
# ==============================================================================
def generate_research_page():
    research = load_json("research.json")

    html = get_html_head("Research Pillars & Grants | Dr. Zaid Amin | zaidamin.org")
    html += get_subpage_nav("research")

    html += f"""
  <div class="subpage-container">
    <div style="margin-bottom: 40px;">
      <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--electric-cyan);">Scholarly Agenda</span>
      <h1 style="font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; margin: 6px 0 10px 0;">Research Pillars & Grants</h1>
      <p style="font-size: 1.05rem; color: var(--text-sub); max-width: 820px; line-height: 1.6;">
        {research['vision']}
      </p>
    </div>

    <div style="display: flex; flex-direction: column; gap: 32px;">
    """
    for pillar in research["pillars"]:
        topics = " ".join([f'<span style="font-size:0.775rem; font-weight:600; padding:4px 10px; background:var(--royal-surface); border:1px solid var(--royal-border); border-radius:4px; margin-right:6px; margin-bottom:6px; display:inline-block; color:var(--text-sub);">{t}</span>' for t in pillar["key_topics"]])
        html += f"""
      <div style="background:var(--royal-card); border:1px solid var(--royal-border); border-radius:18px; padding:36px; box-shadow:0 8px 24px -10px rgba(0,0,0,0.4);">
        <h2 style="font-size: 1.7rem; font-weight: 800; margin-bottom: 12px; color:var(--text-main);">{pillar['title']}</h2>
        <p style="font-size: 1rem; color: var(--text-sub); line-height: 1.7; margin-bottom: 20px;">
          {pillar['full_desc']}
        </p>

        <div style="margin-bottom: 20px;">
          <div style="font-size: 0.85rem; font-weight: 800; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; color:var(--text-main);">Key Technical Frontiers:</div>
          {topics}
        </div>

        <div style="background: var(--accent-amber-light); color: var(--accent-amber); padding: 12px 18px; border-radius: 6px; font-size: 0.85rem; font-weight: 700; border-left: 4px solid var(--accent-amber);">
          Grant Alignment: {pillar['grant_alignment']}
        </div>
      </div>
        """
    html += """
    </div>
  </div>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""
    return html

# ==============================================================================
# 4. POSTGRADUATE LAB & SUPERVISION (prospective-students.html)
# ==============================================================================
def generate_supervision_page():
    supervision = load_json("supervision.json")

    html = get_html_head("Postgraduate Lab & Supervision | Dr. Zaid Amin | zaidamin.org")
    html += get_subpage_nav("lab")

    html += f"""
  <div class="subpage-container">
    <div style="margin-bottom: 36px;">
      <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--electric-cyan);">Academic Mentorship</span>
      <h1 style="font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; margin: 6px 0 10px 0;">{supervision['heading']}</h1>
      <p style="font-size: 1.05rem; color: var(--text-sub); line-height: 1.7; max-width: 820px;">
        {supervision['statement']}
      </p>
    </div>

    <div style="margin-bottom: 40px;">
      <h2 style="font-size: 1.6rem; font-weight: 800; margin-bottom: 20px;">Open Supervised Research Directions</h2>
      <div style="display: flex; flex-direction: column; gap: 20px;">
    """
    for t in supervision["open_topics"]:
        pills = " ".join([f'<span style="background:rgba(56,189,248,0.15); color:var(--electric-cyan); padding:3px 10px; border-radius:4px; font-size:0.75rem; font-weight:700;">{d}</span>' for d in t["degree_levels"]])
        html += f"""
        <div style="background:var(--royal-card); border:1px solid var(--royal-border); border-radius:14px; padding:28px;">
          <div style="margin-bottom: 8px;">{pills}</div>
          <h3 style="font-size: 1.35rem; font-weight: 800; margin-bottom: 8px; color:var(--text-main);">{t['title']}</h3>
          <p style="font-size: 0.95rem; color: var(--text-sub); line-height: 1.6; margin-bottom: 12px;">{t['description']}</p>
          <div style="font-size: 0.825rem; color: var(--text-muted);"><strong>Prerequisites:</strong> {t['skills_required']}</div>
        </div>
        """
    html += f"""
      </div>
    </div>

    <div style="background: var(--royal-card); border: 2px solid var(--electric-blue); border-radius: 16px; padding: 32px;">
      <h2 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 16px; color:var(--text-main);">How to Submit an Inquiry for Supervision</h2>
      <ol style="margin-left: 20px; font-size: 0.95rem; line-height: 1.8; color: var(--text-sub);">
        <li>Review my recent publications on Attention-Based Design (IEEE Access) or Agentic AI Governance (Smart Cities 2026).</li>
        <li>Prepare your Academic CV, transcripts, and a 1-page Research Proposal outlining your core problem.</li>
        <li>Email your materials to <a href="mailto:zaid.amin@newinti.edu.my" style="font-weight:700; color:var(--electric-cyan); text-decoration:underline;">zaid.amin@newinti.edu.my</a> with the subject: <code>[Prospective Postgraduate] - [Your Name] - [Ph.D./Master]</code>.</li>
      </ol>
    </div>
  </div>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""
    return html

# ==============================================================================
# 5. CURRICULUM VITAE (cv.html)
# ==============================================================================
def generate_cv_page():
    profile = load_json("profile.json")
    publications = load_json("publications.json")

    html = get_html_head("Curriculum Vitae | Dr. Zaid Amin, Ph.D. | zaidamin.org")
    html += get_subpage_nav("cv")

    html += f"""
  <div class="subpage-container" style="max-width: 900px;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; border-bottom: 2px solid var(--royal-border); padding-bottom: 24px;">
      <div>
        <h1 style="font-size: 2.6rem; font-weight: 900; margin-bottom: 4px; color:var(--text-main);">Dr. Zaid Amin</h1>
        <div style="font-size: 1.15rem; color: var(--electric-cyan); font-weight: 700;">Curriculum Vitae</div>
        <div style="font-size: 0.9rem; color: var(--text-sub); margin-top: 4px;">
          Senior Lecturer &bull; Faculty of Data Science and Information Technology, INTI International University<br>
          Email: zaid.amin@newinti.edu.my &bull; Website: zaidamin.org &bull; ORCID: 0000-0001-5223-3058
        </div>
      </div>
      <div>
        <button onclick="window.print()" class="pub-btn" style="padding: 10px 20px; font-size: 0.85rem;">
          Print / Save as PDF
        </button>
      </div>
    </div>

    <div style="margin-bottom: 32px;">
      <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid var(--royal-border); padding-bottom: 6px; margin-bottom: 16px; color:var(--text-main);">1. Education</h2>
    """
    for edu in profile["education"]:
        html += f"""
      <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between;">
          <strong style="color:var(--text-main);">{edu['degree']}</strong>
          <span style="color: var(--text-muted);">{edu['country']}</span>
        </div>
        <div style="color: var(--electric-cyan); font-size: 0.95rem;">{edu['institution']}</div>
        <div style="font-size: 0.85rem; color: var(--text-muted);">{edu['focus']}</div>
      </div>
        """

    html += f"""
    </div>

    <div style="margin-bottom: 32px;">
      <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid var(--royal-border); padding-bottom: 6px; margin-bottom: 16px; color:var(--text-main);">2. Academic Leadership History</h2>
    """
    for role in profile["leadership_roles"]:
        html += f"""
      <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between;">
          <strong style="color:var(--text-main);">{role['role']}</strong>
          <span style="color: var(--text-muted); font-size: 0.85rem;">{role['period']}</span>
        </div>
        <div style="color: var(--electric-cyan);">{role['institution']}</div>
        <div style="font-size: 0.85rem; color: var(--text-sub);">{role['description']}</div>
      </div>
        """

    html += f"""
    </div>

    <div style="margin-bottom: 32px;">
      <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid var(--royal-border); padding-bottom: 6px; margin-bottom: 16px; color:var(--text-main);">3. Complete Publication Record ({len(publications)} Works)</h2>
      <ol style="margin-left: 20px; font-size: 0.9rem; line-height: 1.7; color:var(--text-sub);">
    """
    for pub in publications:
        doi_str = f' DOI: <a href="{pub["url"]}" target="_blank" style="color:var(--electric-cyan);">{pub["doi"]}</a>' if pub.get("doi") else ""
        html += f"""
        <li style="margin-bottom: 10px;">
          <strong style="color:var(--text-main);">Zaid Amin</strong> et al. ({pub['year']}). "{pub['title']}". <em>{pub['venue']}</em>.{doi_str}
        </li>
        """

    html += """
      </ol>
    </div>
  </div>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""
    return html

# ==============================================================================
# MAIN COMPILER BUILD
# ==============================================================================
def build_all():
    print("Compiling Royal Blue Storm Academic Site for zaidamin.org...")
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    pages = {
        "index.html": generate_storm_home(),
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

    print("Royal Storm build complete!")

if __name__ == "__main__":
    build_all()
