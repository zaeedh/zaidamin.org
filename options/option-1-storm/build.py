"""
Academic Golden Ratio Static Site Generator - zaidamin.org
Epigraph (Qur'an 31:27) • Clean Lighthouse Storm Banner • Golden Ratio (1.618 : 1) Composition
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

def get_subpage_nav(active_page=""):
    return f"""
  <header class="subpage-nav">
    <a href="index.html" class="back-home-link">
      {render_svg_icon('arrow-left')}
      Home
    </a>

    <div style="display: flex; gap: 18px; align-items: center;">
      <a href="publications.html" style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; color: {'var(--brand-blue)' if active_page == 'publications' else 'var(--text-body)'};">Publications</a>
      <a href="research.html" style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; color: {'var(--brand-blue)' if active_page == 'research' else 'var(--text-body)'};">Research</a>
      <a href="prospective-students.html" style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; color: {'var(--brand-blue)' if active_page == 'lab' else 'var(--text-body)'};">Join Lab</a>
      <a href="cv.html" style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; color: {'var(--brand-blue)' if active_page == 'cv' else 'var(--text-body)'};">CV</a>
    </div>
  </header>
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

    html += f"""
  <div class="site-wrapper">
    
    <!-- 1. Top Epigraph -->
    <header class="epigraph-header">
      <h1 class="epigraph-title">Das Sein, Das Sollen.</h1>
      <p class="epigraph-quote font-serif">
        &ldquo;If all the trees on earth were pens and the ocean were ink, refilled by seven other oceans, the Words of Allah would not be exhausted. Surely Allah is Almighty, All-Wise.&rdquo; &mdash; Qur&rsquo;an 31:27
      </p>
    </header>

    <!-- 2. Clean, Unobstructed Lighthouse Storm Banner -->
    <section class="lighthouse-banner-frame">
      <picture>
        <source srcset="assets/images/lighthouse-banner.webp" type="image/webp">
        <img src="assets/images/lighthouse-banner.jpg" class="lighthouse-bg-img" alt="Lighthouse Storm over Ocean" width="2048" height="790">
      </picture>
      <canvas id="rain-canvas"></canvas>
    </section>

    <!-- 3. Golden Ratio Standard Composition (61.8% Major : 38.2% Minor) -->
    <main class="golden-composition-grid">
      
      <!-- Major Column (61.8% / 1.618fr) -->
      <section class="golden-major-col">
        <!-- Scholar Hero Block -->
        <div class="scholar-hero-block">
          <div class="scholar-hero-inner">
            <div class="royal-avatar-box">
              <picture>
                <source srcset="assets/images/dr-zaid.webp" type="image/webp">
                <img src="assets/images/dr-zaid.png" alt="Dr. Zaid Amin" class="royal-avatar-img">
              </picture>
            </div>
            <div style="flex: 1;">
              <div class="scholar-tagline-pill">
                INTI INTERNATIONAL UNIVERSITY &bull; SENIOR LECTURER &bull; UKM PH.D.
              </div>
              <h2 class="scholar-name-large">{profile['name']}<span class="royal-degree-gold">, Ph.D.</span></h2>
              <div class="scholar-subheading">Human-Computer Interaction &bull; AI Governance &bull; Behavioral Computing</div>

              <p class="royal-motto">
                <span class="motto-gold">&ldquo;Das Sein, das Sollen</span> &ndash; The guiding beacon of human reason and digital ethics amidst the turbulent storm of algorithmic complexity.&rdquo;
              </p>

              <p class="scholar-mission-text">
                {profile['short_bio']}
              </p>
            </div>
          </div>
        </div>

        <!-- 3 Core Research Pillars -->
        <div>
          <h3 class="pillars-heading">Research Pillars & Agenda</h3>
    """

    for pillar in research["pillars"]:
        html += f"""
          <div class="pillar-item-card">
            <h4 class="pillar-title">{pillar['title']}</h4>
            <p class="pillar-desc">{pillar['full_desc']}</p>
            <span class="pillar-grant-tag">Grant Alignment: {pillar['grant_alignment']}</span>
          </div>
        """

    html += f"""
        </div>

        <!-- Flagship Publications Highlights -->
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 class="pillars-heading" style="margin-bottom:0;">Featured Publications</h3>
            <a href="publications.html" style="font-size:0.85rem; font-weight:700; color:var(--brand-blue);">View All 24 Works {render_svg_icon('arrow-right')}</a>
          </div>

          <div class="flagship-pub-card">
            <div class="flagship-badge">★ Journal Article &bull; 2026 &bull; MDPI Smart Cities</div>
            <div class="flagship-title">Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance</div>
            <div class="flagship-venue">Smart Cities &bull; DOI: 10.3390/smartcities9100174</div>
          </div>

          <div class="flagship-pub-card">
            <div class="flagship-badge">★ SSRN Working Paper &bull; 2026</div>
            <div class="flagship-title">The Proxy Trap in Agentic AI: When Metrics Replace Judgment</div>
            <div class="flagship-venue">Social Science Research Network &bull; DOI: 10.2139/ssrn.7670124</div>
          </div>

          <div class="flagship-pub-card">
            <div class="flagship-badge">★ Q1 Flagship &bull; 2021 &bull; IEEE Access</div>
            <div class="flagship-title">Attention-Based Design and User Decisions on Information Sharing: A Thematic Literature Review</div>
            <div class="flagship-venue">IEEE Access &bull; DOI: 10.1109/ACCESS.2021.3087740</div>
          </div>
        </div>
      </section>

      <!-- Minor Column (38.2% / 1fr) -->
      <aside class="golden-minor-col">
        <!-- Action Buttons Card -->
        <div class="action-buttons-card">
          <div class="action-card-title">Academic Portal & Actions</div>
          
          <div class="action-buttons-list">
            <a href="publications.html" class="golden-btn golden-btn-primary">
              <span>Publications ({len(publications)})</span>
              {render_svg_icon('arrow-right')}
            </a>
            <a href="research.html" class="golden-btn golden-btn-outline">
              <span>Research & Grants</span>
              {render_svg_icon('arrow-right')}
            </a>
            <a href="prospective-students.html" class="golden-btn golden-btn-accent">
              <span>Join Research Lab (Ph.D./Master)</span>
              {render_svg_icon('arrow-right')}
            </a>
            <a href="cv.html" class="golden-btn golden-btn-outline">
              <span>Curriculum Vitae (PDF)</span>
              {render_svg_icon('arrow-right')}
            </a>
          </div>

          <!-- Scholarly Icons Cluster -->
          <div class="golden-icons-cluster">
            <a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" class="golden-icon-pill" title="Google Scholar">
              {render_svg_icon('scholar')}
            </a>
            <a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" class="golden-icon-pill" title="ORCID ({profile['metrics']['orcid_id']})">
              {render_svg_icon('orcid')}
            </a>
            <a href="{profile['social_links']['github']}" target="_blank" rel="noopener" class="golden-icon-pill" title="GitHub (@zaeedh)">
              {render_svg_icon('github')}
            </a>
            <a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="golden-icon-pill" title="LinkedIn">
              {render_svg_icon('linkedin')}
            </a>
            <a href="mailto:{profile['social_links']['email']}" class="golden-icon-pill" title="Email Dr. Amin">
              {render_svg_icon('email')}
            </a>
          </div>
        </div>

        <!-- Academic Metrics Card -->
        <div class="golden-metrics-card">
          <div style="font-size:0.8rem; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-muted); margin-bottom:12px;">Track Record Highlights</div>
          <div class="metrics-row">
            <span>Indexed Publications</span>
            <span class="metrics-val">24+ Works</span>
          </div>
          <div class="metrics-row">
            <span>High-Impact Venues</span>
            <span class="metrics-val">Q1 IEEE Access & MDPI</span>
          </div>
          <div class="metrics-row">
            <span>Academic Leadership</span>
            <span class="metrics-val">10+ Years (Ex-Program Head)</span>
          </div>
          <div class="metrics-row">
            <span>Doctorate</span>
            <span class="metrics-val">UKM (Malaysia)</span>
          </div>
        </div>

        <!-- Postgraduate Recruitment Callout -->
        <div class="golden-recruitment-box">
          <div style="font-size:0.75rem; font-weight:800; color:#fbbf24; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">Graduate Mentorship</div>
          <div class="recruitment-callout-title">Accepting Ph.D. Scholars</div>
          <p class="recruitment-callout-desc">
            Supervising research in Agentic AI Alignment, The Proxy Trap, and Attention-Based Interface Interventions.
          </p>
          <a href="prospective-students.html" class="golden-btn golden-btn-accent" style="justify-content:center;">
            View Topics & Apply
          </a>
        </div>
      </aside>

    </main>

    <!-- Site Footer -->
    <footer class="golden-footer">
      <div>
        <strong>Dr. Zaid Amin, Ph.D.</strong> &bull; Faculty of Data Science and Information Technology, INTI International University, Malaysia.<br>
        Email: <a href="mailto:{profile['social_links']['email']}" style="color:var(--brand-blue); text-decoration:underline;">zaid.amin@newinti.edu.my</a> &bull; Domain: <strong>zaidamin.org</strong>
      </div>

      <div style="display:flex; align-items:center; gap:16px;">
        <span>&copy; 2026 Dr. Zaid Amin</span>
        <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle theme">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        </button>
      </div>
    </footer>

  </div>

  <script src="assets/js/rain-lighting.js"></script>
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
      <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--brand-blue);">Scholarly Archive</span>
      <h1 style="font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; margin: 6px 0 10px 0;">Publications & Citations ({len(publications)})</h1>
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

        <h3 style="font-size:1.25rem; font-weight:800; margin-bottom:6px; line-height:1.35;">{pub['title']}</h3>
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
      <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--brand-blue);">Scholarly Agenda</span>
      <h1 style="font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; margin: 6px 0 10px 0;">Research Pillars & Grants</h1>
      <p style="font-size: 1.05rem; color: var(--text-muted); max-width: 820px; line-height: 1.6;">
        {research['vision']}
      </p>
    </div>

    <div style="display: flex; flex-direction: column; gap: 32px;">
    """
    for pillar in research["pillars"]:
        topics = " ".join([f'<span style="font-size:0.775rem; font-weight:600; padding:4px 10px; background:var(--bg-subtle); border:1px solid var(--border-light); border-radius:4px; margin-right:6px; margin-bottom:6px; display:inline-block;">{t}</span>' for t in pillar["key_topics"]])
        html += f"""
      <div style="background:var(--bg-card); border:1px solid var(--border-light); border-radius:16px; padding:36px; box-shadow:0 8px 24px -10px rgba(0,0,0,0.04);">
        <h2 style="font-size: 1.7rem; font-weight: 800; margin-bottom: 12px;">{pillar['title']}</h2>
        <p style="font-size: 1rem; color: var(--text-body); line-height: 1.7; margin-bottom: 20px;">
          {pillar['full_desc']}
        </p>

        <div style="margin-bottom: 20px;">
          <div style="font-size: 0.85rem; font-weight: 800; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Key Technical Frontiers:</div>
          {topics}
        </div>

        <div style="background: var(--brand-gold-light); color: var(--brand-gold); padding: 12px 18px; border-radius: 6px; font-size: 0.85rem; font-weight: 700; border-left: 4px solid var(--brand-gold);">
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
      <span style="font-size: 0.75rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--brand-blue);">Academic Mentorship</span>
      <h1 style="font-size: 2.8rem; font-weight: 900; letter-spacing: -0.03em; margin: 6px 0 10px 0;">{supervision['heading']}</h1>
      <p style="font-size: 1.05rem; color: var(--text-body); line-height: 1.7; max-width: 820px;">
        {supervision['statement']}
      </p>
    </div>

    <div style="margin-bottom: 40px;">
      <h2 style="font-size: 1.6rem; font-weight: 800; margin-bottom: 20px;">Open Supervised Research Directions</h2>
      <div style="display: flex; flex-direction: column; gap: 20px;">
    """
    for t in supervision["open_topics"]:
        pills = " ".join([f'<span style="background:var(--brand-blue-light); color:var(--brand-blue); padding:3px 10px; border-radius:4px; font-size:0.75rem; font-weight:700;">{d}</span>' for d in t["degree_levels"]])
        html += f"""
        <div style="background:var(--bg-card); border:1px solid var(--border-light); border-radius:14px; padding:28px;">
          <div style="margin-bottom: 8px;">{pills}</div>
          <h3 style="font-size: 1.35rem; font-weight: 800; margin-bottom: 8px;">{t['title']}</h3>
          <p style="font-size: 0.95rem; color: var(--text-body); line-height: 1.6; margin-bottom: 12px;">{t['description']}</p>
          <div style="font-size: 0.825rem; color: var(--text-muted);"><strong>Prerequisites:</strong> {t['skills_required']}</div>
        </div>
        """
    html += f"""
      </div>
    </div>

    <div style="background: var(--bg-card); border: 2px solid var(--brand-blue); border-radius: 16px; padding: 32px;">
      <h2 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 16px;">How to Submit an Inquiry for Supervision</h2>
      <ol style="margin-left: 20px; font-size: 0.95rem; line-height: 1.8; color: var(--text-body);">
        <li>Review my recent publications on Attention-Based Design (IEEE Access) or Agentic AI Governance (Smart Cities 2026).</li>
        <li>Prepare your Academic CV, transcripts, and a 1-page Research Proposal outlining your core problem.</li>
        <li>Email your materials to <a href="mailto:zaid.amin@newinti.edu.my" style="font-weight:700; color:var(--brand-blue); text-decoration:underline;">zaid.amin@newinti.edu.my</a> with the subject: <code>[Prospective Postgraduate] - [Your Name] - [Ph.D./Master]</code>.</li>
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
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; border-bottom: 2px solid var(--border-light); padding-bottom: 24px;">
      <div>
        <h1 style="font-size: 2.6rem; font-weight: 900; margin-bottom: 4px;">Dr. Zaid Amin</h1>
        <div style="font-size: 1.15rem; color: var(--brand-blue); font-weight: 700;">Curriculum Vitae</div>
        <div style="font-size: 0.9rem; color: var(--text-body); margin-top: 4px;">
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
      <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid var(--border-light); padding-bottom: 6px; margin-bottom: 16px;">1. Education</h2>
    """
    for edu in profile["education"]:
        html += f"""
      <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between;">
          <strong>{edu['degree']}</strong>
          <span style="color: var(--text-muted);">{edu['country']}</span>
        </div>
        <div style="color: var(--brand-navy); font-size: 0.95rem;">{edu['institution']}</div>
        <div style="font-size: 0.85rem; color: var(--text-muted);">{edu['focus']}</div>
      </div>
        """

    html += f"""
    </div>

    <div style="margin-bottom: 32px;">
      <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid var(--border-light); padding-bottom: 6px; margin-bottom: 16px;">2. Academic Leadership History</h2>
    """
    for role in profile["leadership_roles"]:
        html += f"""
      <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between;">
          <strong>{role['role']}</strong>
          <span style="color: var(--text-muted); font-size: 0.85rem;">{role['period']}</span>
        </div>
        <div style="color: var(--brand-navy);">{role['institution']}</div>
        <div style="font-size: 0.85rem; color: var(--text-body);">{role['description']}</div>
      </div>
        """

    html += f"""
    </div>

    <div style="margin-bottom: 32px;">
      <h2 style="font-size: 1.4rem; font-weight: 800; border-bottom: 1px solid var(--border-light); padding-bottom: 6px; margin-bottom: 16px;">3. Complete Publication Record ({len(publications)} Works)</h2>
      <ol style="margin-left: 20px; font-size: 0.9rem; line-height: 1.7;">
    """
    for pub in publications:
        doi_str = f' DOI: <a href="{pub["url"]}" target="_blank" style="color:var(--brand-blue);">{pub["doi"]}</a>' if pub.get("doi") else ""
        html += f"""
        <li style="margin-bottom: 10px;">
          <strong>Zaid Amin</strong> et al. ({pub['year']}). "{pub['title']}". <em>{pub['venue']}</em>.{doi_str}
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
