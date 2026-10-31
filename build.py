"""
Academic Static Site Generator - zaidamin.org
Compiler for Dr. Zaid Amin's Personal Academic Portal
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
        "pdf": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>',
        "shield-check": '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><polyline points="9 12 11 14 15 10"></polyline></svg>',
        "eye": '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>',
        "globe": '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>',
        "search": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
        "external": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'
    }
    return icons.get(name, "")

def get_base_header(title="Dr. Zaid Amin | Academic & Computational Researcher", description="", extra_meta=""):
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
            {"@type": "CollegeOrUniversity", "name": "Universitas Bina Darma"},
            {"@type": "CollegeOrUniversity", "name": "Palcomtech Institute of Technology and Business"}
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

  <!-- Open Graph / Social Media -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://zaidamin.org/">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="https://zaidamin.org/assets/images/zaid-amin-preview.png">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">

  <!-- Google Scholar Indexing Meta Tags -->
  <meta name="citation_author" content="Amin, Zaid">
  <meta name="citation_author_institution" content="INTI International University">
  {extra_meta}

  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
  {json.dumps(schema_json, indent=2)}
  </script>

  <!-- Typography & Styling -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
  <nav class="navbar" role="navigation" aria-label="Main Navigation">
    <div class="container nav-container">
      <a href="index.html" class="nav-brand">
        <span class="nav-brand-title">Dr. Zaid Amin</span>
        <span class="nav-brand-subtitle">Das Sein, das Sollen</span>
      </a>

      <ul class="nav-links">
        <li><a href="index.html#about" class="nav-link">About</a></li>
        <li><a href="index.html#research" class="nav-link">Research & Grants</a></li>
        <li><a href="index.html#publications" class="nav-link">Publications</a></li>
        <li><a href="index.html#recruitment" class="nav-link">Postgraduate Lab</a></li>
        <li><a href="index.html#teaching" class="nav-link">Teaching & Service</a></li>
        <li><a href="index.html#essays" class="nav-link">Essays</a></li>
        <li><a href="cv.html" class="nav-link">CV</a></li>
        <li><a href="index.html#contact" class="nav-link">Contact</a></li>
      </ul>

      <div class="nav-actions">
        <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle dark/light theme">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        </button>
        <button class="mobile-nav-toggle" aria-label="Open mobile menu">☰</button>
      </div>
    </div>
  </nav>
  <main>
"""

def get_base_footer():
    profile = load_json("profile.json")
    return f"""
  </main>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand-title">Dr. Zaid Amin, Ph.D.</div>
          <div class="footer-motto">"Das Sein, das Sollen" &mdash; {profile['tagline']}</div>
          <p style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.6; max-width: 480px;">
            {profile['affiliation']['faculty']}<br>
            <strong>{profile['affiliation']['institution']}</strong>, {profile['affiliation']['location']}.
          </p>
        </div>
        <div>
          <h4 style="margin-bottom: 12px; font-size: 0.95rem;">Academic Navigation</h4>
          <ul class="footer-links-list">
            <li><a href="index.html#research" class="footer-link">Research Pillars & Grants</a></li>
            <li><a href="index.html#publications" class="footer-link">Publications & BibTeX</a></li>
            <li><a href="index.html#recruitment" class="footer-link">Join My Lab (Ph.D./Master)</a></li>
            <li><a href="index.html#teaching" class="footer-link">Teaching & Leadership</a></li>
            <li><a href="cv.html" class="footer-link">Curriculum Vitae (PDF)</a></li>
          </ul>
        </div>
        <div>
          <h4 style="margin-bottom: 12px; font-size: 0.95rem;">Profiles & Identifiers</h4>
          <ul class="footer-links-list">
            <li><a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" class="footer-link">ORCID: {profile['metrics']['orcid_id']}</a></li>
            <li><a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" class="footer-link">Google Scholar Profile</a></li>
            <li><a href="{profile['social_links']['sciprofiles']}" target="_blank" rel="noopener" class="footer-link">SciProfiles</a></li>
            <li><a href="{profile['social_links']['github']}" target="_blank" rel="noopener" class="footer-link">GitHub (@zaeedh)</a></li>
            <li><a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="footer-link">LinkedIn</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div>&copy; 2026 Dr. Zaid Amin. Built with Academic Rigor & Clean Web Architecture.</div>
        <div>Hosted on <strong>zaidamin.org</strong></div>
      </div>
    </div>
  </footer>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""

def generate_index_html():
    profile = load_json("profile.json")
    research = load_json("research.json")
    publications = load_json("publications.json")
    supervision = load_json("supervision.json")
    teaching = load_json("teaching.json")
    talks = load_json("talks.json")
    essays = load_json("essays.json")

    # Generate Scholar Meta tags for the top papers
    scholar_meta = ""
    for pub in publications[:5]:
        scholar_meta += f'\n  <meta name="citation_title" content="{pub["title"]}">'
        if pub.get("doi"):
            scholar_meta += f'\n  <meta name="citation_doi" content="{pub["doi"]}">'
        if pub.get("year"):
            scholar_meta += f'\n  <meta name="citation_publication_date" content="{pub["year"]}">'

    html = get_base_header("Dr. Zaid Amin | Academic & Computational Researcher | zaidamin.org", extra_meta=scholar_meta)

    # 1. Hero Section
    html += f"""
    <section class="hero-section" id="about">
      <div class="container hero-grid">
        <div>
          <div class="hero-badge-pill">
            <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background-color:var(--brand-blue);"></span>
            {profile['affiliation']['institution']} &bull; Senior Lecturer
          </div>
          <h1 class="hero-title">{profile['name']}<span style="color:var(--brand-accent); font-size:1.8rem;">, Ph.D.</span></h1>
          <div class="hero-subtitle font-serif">{profile['tagline']}</div>
          
          <div class="hero-affiliation">
            <div><strong>{profile['title']}</strong></div>
            <div>{profile['affiliation']['faculty']} &bull; {profile['affiliation']['institution']}, Malaysia</div>
            <div style="font-size:0.875rem; color:var(--text-muted); margin-top:2px;">Ph.D., Universiti Kebangsaan Malaysia (UKM)</div>
          </div>

          <p class="hero-bio">
            {profile['short_bio']}
          </p>

          <div class="hero-actions">
            <a href="index.html#recruitment" class="btn btn-primary">Join My Research Group</a>
            <a href="index.html#publications" class="btn btn-secondary">Explore Publications ({len(publications)})</a>
            <a href="cv.html" class="btn btn-secondary">
              {render_svg_icon('pdf')}
              Download CV
            </a>
          </div>

          <div class="academic-badges">
            <a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" class="badge-link">
              {render_svg_icon('scholar')}
              Google Scholar
            </a>
            <a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" class="badge-link">
              {render_svg_icon('orcid')}
              ORCID ({profile['metrics']['orcid_id']})
            </a>
            <a href="{profile['social_links']['sciprofiles']}" target="_blank" rel="noopener" class="badge-link">
              {render_svg_icon('external')}
              SciProfiles
            </a>
            <a href="{profile['social_links']['github']}" target="_blank" rel="noopener" class="badge-link">
              {render_svg_icon('github')}
              GitHub
            </a>
            <a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="badge-link">
              {render_svg_icon('linkedin')}
              LinkedIn
            </a>
          </div>
        </div>

        <div class="hero-card">
          <div class="avatar-wrapper">
            ZA
          </div>
          <h3 class="card-name">{profile['name']}</h3>
          <div class="card-title">Senior Lecturer & Researcher</div>
          <div class="card-status-pill">
            <span class="card-status-dot"></span>
            Accepting Ph.D. & Master's Students
          </div>

          <ul class="card-details-list">
            <li class="card-details-item">
              <span class="card-details-label">Affiliation</span>
              <span>INTI Intl. University</span>
            </li>
            <li class="card-details-item">
              <span class="card-details-label">Doctorate</span>
              <span>UKM (Malaysia)</span>
            </li>
            <li class="card-details-item">
              <span class="card-details-label">Focus Area</span>
              <span>HCI & AI Governance</span>
            </li>
            <li class="card-details-item">
              <span class="card-details-label">Location</span>
              <span>Nilai, Malaysia</span>
            </li>
          </ul>
        </div>
      </div>
    </section>
    """

    # 2. Metrics Strip
    html += f"""
    <div class="metrics-strip">
      <div class="container metrics-grid">
        <div class="metric-card">
          <div class="metric-value">{len(publications)}+</div>
          <div class="metric-label">Publications</div>
          <div class="metric-sub">Journals, Conferences & Chapters</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">Q1</div>
          <div class="metric-label">High-Impact Venues</div>
          <div class="metric-sub">IEEE Access, MDPI Smart Cities</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">10+</div>
          <div class="metric-label">Academic Experience</div>
          <div class="metric-sub">Senior Lecturer & Program Head</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">4</div>
          <div class="metric-label">Target Grant Themes</div>
          <div class="metric-sub">FRGS, AI Ethics, Civic Tech</div>
        </div>
      </div>
    </div>
    """

    # 3. Research Pillars & Grants Section (Crucial for Associate Professorship & Funding)
    html += f"""
    <section class="section" id="research">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Scholarly Vision & Grants</span>
          <h2 class="section-title">Research Pillars & Grant Themes</h2>
          <p class="section-desc">{research['vision']}</p>
        </div>

        <div class="pillars-grid">
    """
    for pillar in research["pillars"]:
        topics_html = "".join([f'<li class="topic-chip">{t}</li>' for t in pillar["key_topics"]])
        html += f"""
          <div class="pillar-card">
            <div class="pillar-icon-box">
              {render_svg_icon(pillar['icon'])}
            </div>
            <h3 class="pillar-title">{pillar['title']}</h3>
            <p class="pillar-desc">{pillar['full_desc']}</p>
            <ul class="pillar-topics-list">
              {topics_html}
            </ul>
            <div class="grant-alignment-badge">
              <strong>Grant Alignment:</strong> {pillar['grant_alignment']}
            </div>
          </div>
        """
    html += """
        </div>
      </div>
    </section>
    """

    # 4. Publications Section (All 24 real works with search, filter tabs, BibTeX copy)
    html += f"""
    <section class="section section-subtle" id="publications">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Peer-Reviewed Scholarship</span>
          <h2 class="section-title">Publications & Citations ({len(publications)})</h2>
          <p class="section-desc">
            Complete indexed record across Human-Computer Interaction, AI Governance, Behavioral Computing, and Information Systems. Filter by venue type or search topics in real-time.
          </p>
        </div>

        <div class="publications-controls">
          <div class="search-input-box">
            <span class="search-icon">{render_svg_icon('search')}</span>
            <input type="text" id="pub-search" class="search-input" placeholder="Search publications by title, venue, year, or keyword...">
          </div>

          <div class="filter-pills">
            <button class="filter-btn active" data-filter="all">All ({len(publications)})</button>
            <button class="filter-btn" data-filter="journal">Journals</button>
            <button class="filter-btn" data-filter="conference">Conferences</button>
            <button class="filter-btn" data-filter="book chapter">Book Chapters</button>
            <button class="filter-btn" data-filter="preprint">Preprints</button>
          </div>
        </div>

        <div id="pub-count-indicator" style="margin-bottom: 16px; font-size: 0.85rem; color: var(--text-muted); font-weight: 500;">
          Showing all {len(publications)} publications
        </div>

        <div class="publications-list">
    """

    for pub in publications:
        type_class = f"type-{pub['category'].lower().replace(' ', '')}"
        doi_link = f'<a href="{pub["url"]}" target="_blank" rel="noopener" class="pub-btn">DOI: {pub["doi"]} {render_svg_icon("external")}</a>' if pub.get("doi") else ""
        url_link = f'<a href="{pub["url"]}" target="_blank" rel="noopener" class="pub-btn">Link {render_svg_icon("external")}</a>' if (pub.get("url") and not pub.get("doi")) else ""

        html += f"""
          <article class="pub-item" data-category="{pub['category'].lower()}">
            <div class="pub-meta-top">
              <span class="pub-type-badge {type_class}">{pub['category']}</span>
              <span class="pub-year">{pub['year']}</span>
              {f'<span style="font-size:0.75rem; color:var(--brand-accent); font-weight:700;">★ Featured Paper</span>' if pub.get('featured') else ''}
            </div>

            <h3 class="pub-title">{pub['title']}</h3>
            <div class="pub-authors"><strong>Dr. Zaid Amin</strong> and collaborators</div>
            <div class="pub-venue">{pub['venue']}</div>

            <div class="pub-actions">
              {doi_link}
              {url_link}
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
    </section>
    """

    # 5. Prospective Students & Lab Recruitment Section (Target #3 for Dr. Zaid)
    html += f"""
    <section class="section" id="recruitment">
      <div class="container">
        <div class="recruitment-card">
          <div class="recruitment-tag">Academic Mentorship & Opportunities</div>
          <h2 class="recruitment-title">{supervision['heading']}</h2>
          <p class="recruitment-text">{supervision['statement']}</p>

          <h3 style="color:#ffffff; font-size:1.25rem; margin-bottom:20px;">Open Supervised Research Directions</h3>
          <div class="recruitment-topics-grid">
    """
    for t in supervision["open_topics"]:
        degrees_pills = " ".join([f'<span style="background:rgba(255,255,255,0.15); padding:2px 8px; border-radius:4px; font-size:0.75rem;">{d}</span>' for d in t["degree_levels"]])
        html += f"""
            <div class="recruitment-topic-box">
              <div style="margin-bottom:6px;">{degrees_pills}</div>
              <div class="topic-box-title">{t['title']}</div>
              <p class="topic-box-desc">{t['description']}</p>
              <div style="font-size:0.75rem; color:#94a3b8; margin-top:8px;"><strong>Skills:</strong> {t['skills_required']}</div>
            </div>
        """
    html += f"""
          </div>

          <div style="background-color:rgba(0,0,0,0.25); border-radius:var(--radius-md); padding:24px; border:1px solid rgba(255,255,255,0.1);">
            <h4 style="color:#fbbf24; font-size:1.05rem; margin-bottom:12px;">How to Inquire for Supervision:</h4>
            <ol style="margin-left:20px; font-size:0.9rem; line-height:1.7; color:#e2e8f0;">
              <li>Verify that your background in Computer Science / IT / Data Science meets postgraduate entry requirements.</li>
              <li>Read my recent papers on Attention-Based Design (IEEE Access 2021) or Agentic Governance (Smart Cities 2026).</li>
              <li>Email your CV and a 1-page Research Proposal to <a href="mailto:zaid.amin@newinti.edu.my" style="color:#60a5fa; text-decoration:underline;">zaid.amin@newinti.edu.my</a> with the subject <code>[Prospective Postgraduate] - [Your Name]</code>.</li>
            </ol>
          </div>
        </div>
      </div>
    </section>
    """

    # 6. Teaching, Academic Leadership & Talks
    html += f"""
    <section class="section" id="teaching">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Pedagogy & Professional Standing</span>
          <h2 class="section-title">Teaching, Leadership & Service</h2>
          <p class="section-desc">{teaching['philosophy']}</p>
        </div>

        <div class="two-col-grid">
          <div>
            <h3 style="margin-bottom: 24px; font-size: 1.35rem;">Academic Leadership History</h3>
            <div class="timeline-list">
    """
    for role in profile["leadership_roles"]:
        html += f"""
              <div class="timeline-item">
                <div class="timeline-date">{role['period']}</div>
                <div class="timeline-title">{role['role']}</div>
                <div class="timeline-org">{role['institution']}</div>
                <div class="timeline-desc">{role['description']}</div>
              </div>
        """
    html += f"""
            </div>
          </div>

          <div>
            <h3 style="margin-bottom: 24px; font-size: 1.35rem;">Keynotes, Talks & Peer Review</h3>
            <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px;">
    """
    for talk in talks["talks"]:
        html += f"""
              <div style="background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <span style="font-size: 0.75rem; font-weight: 700; color: var(--brand-blue); text-transform: uppercase;">{talk['type']} &bull; {talk['year']}</span>
                  <span style="font-size: 0.775rem; color: var(--text-muted);">{talk['location']}</span>
                </div>
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: var(--text-primary);">{talk['title']}</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); font-style: italic;">{talk['event']}</div>
              </div>
        """

    html += f"""
            </div>

            <div style="background-color: var(--bg-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 20px;">
              <h4 style="font-size: 0.95rem; margin-bottom: 10px;">Peer Reviewer for Prestigious Venues</h4>
              <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
                IEEE Access &bull; International Journal of Human-Computer Interaction (Taylor & Francis) &bull; MDPI Smart Cities &bull; Springer LNCS &bull; IJACSA &bull; ICE3IS Program Committee.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
    """

    # 7. Essays & Reflections ("Das sein, das sollen")
    html += f"""
    <section class="section section-subtle" id="essays">
      <div class="container">
        <div class="section-header">
          <span class="section-tag">Public Scholarship</span>
          <h2 class="section-title">Essays & Intellectual Dispatches ("Das Sein, das Sollen")</h2>
          <p class="section-desc">
            Bridging empirical computing with normative philosophy, examining what technology is versus what human society ought to become.
          </p>
        </div>

        <div class="essays-grid">
    """
    for e in essays:
        tags_html = " ".join([f'<span class="topic-chip">{t}</span>' for t in e["tags"]])
        html += f"""
          <article class="essay-card">
            <div class="essay-date">{e['date']} &bull; {e['reading_time']}</div>
            <h3 class="essay-title">{e['title']}</h3>
            <p class="essay-summary">{e['summary']}</p>
            <div class="essay-footer">
              <div style="display:flex; gap:4px;">{tags_html}</div>
              <a href="index.html#essays" style="font-weight:600; font-size:0.8rem;">Read Essay &rarr;</a>
            </div>
          </article>
        """
    html += """
        </div>
      </div>
    </section>
    """

    # 8. Contact Section
    html += f"""
    <section class="section" id="contact">
      <div class="container" style="max-width: 800px; text-align: center;">
        <span class="section-tag">Connect & Collaborate</span>
        <h2 class="section-title">Academic & Research Inquiries</h2>
        <p class="section-desc" style="margin: 0 auto 36px auto;">
          For research collaborations, keynote invitations, grant partnerships, or postgraduate supervision at INTI International University, please reach out directly.
        </p>

        <div style="display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; margin-bottom: 32px;">
          <a href="mailto:{profile['social_links']['email']}" class="btn btn-primary" style="font-size: 1rem; padding: 14px 28px;">
            {render_svg_icon('email')}
            zaid.amin@newinti.edu.my
          </a>
          <a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="btn btn-secondary" style="font-size: 1rem; padding: 14px 28px;">
            {render_svg_icon('linkedin')}
            Connect on LinkedIn
          </a>
        </div>

        <div style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6;">
          <strong>Office Address:</strong><br>
          Faculty of Data Science and Information Technology (FDSIT)<br>
          INTI International University, Persiaran Perdana BBN, Putra Nilai, 71800 Nilai, Negeri Sembilan, Malaysia.
        </div>
      </div>
    </section>
    """

    html += get_base_footer()
    return html

def generate_cv_html():
    profile = load_json("profile.json")
    publications = load_json("publications.json")
    teaching = load_json("teaching.json")
    talks = load_json("talks.json")

    html = get_base_header("Curriculum Vitae | Dr. Zaid Amin, Ph.D. | zaidamin.org")
    html += f"""
    <section class="section">
      <div class="container" style="max-width: 900px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; border-bottom: 2px solid var(--border-strong); padding-bottom: 24px;">
          <div>
            <h1 style="font-size: 2.4rem; margin-bottom: 6px;">Dr. Zaid Amin</h1>
            <div style="font-size: 1.15rem; color: var(--brand-blue); font-weight: 600;">Curriculum Vitae</div>
            <div style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 4px;">
              Senior Lecturer &bull; Faculty of Data Science and Information Technology, INTI International University<br>
              Email: zaid.amin@newinti.edu.my &bull; Website: zaidamin.org &bull; ORCID: 0000-0001-5223-3058
            </div>
          </div>
          <div>
            <button onclick="window.print()" class="btn btn-secondary">
              {render_svg_icon('pdf')}
              Print / Save as PDF
            </button>
          </div>
        </div>

        <div style="margin-bottom: 32px;">
          <h2 style="font-size: 1.35rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 6px; margin-bottom: 16px;">1. Education</h2>
    """
    for edu in profile["education"]:
        html += f"""
          <div style="margin-bottom: 12px;">
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
          <h2 style="font-size: 1.35rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 6px; margin-bottom: 16px;">2. Academic Appointments & Leadership</h2>
    """
    for role in profile["leadership_roles"]:
        html += f"""
          <div style="margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between;">
              <strong>{role['role']}</strong>
              <span style="color: var(--text-muted); font-size: 0.85rem;">{role['period']}</span>
            </div>
            <div style="color: var(--brand-navy);">{role['institution']}</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary);">{role['description']}</div>
          </div>
        """

    html += f"""
        </div>

        <div style="margin-bottom: 32px;">
          <h2 style="font-size: 1.35rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 6px; margin-bottom: 16px;">3. Complete Publication Record ({len(publications)} Works)</h2>
          <ol style="margin-left: 20px; font-size: 0.9rem; line-height: 1.7;">
    """
    for pub in publications:
        doi_str = f' DOI: <a href="{pub["url"]}" target="_blank">{pub["doi"]}</a>' if pub.get("doi") else ""
        html += f"""
            <li style="margin-bottom: 10px;">
              <strong>Zaid Amin</strong> et al. ({pub['year']}). "{pub['title']}". <em>{pub['venue']}</em>.{doi_str}
            </li>
        """

    html += f"""
          </ol>
        </div>

        <div style="margin-bottom: 32px;">
          <h2 style="font-size: 1.35rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 6px; margin-bottom: 16px;">4. Academic Service & Peer Review</h2>
          <ul style="margin-left: 20px; font-size: 0.9rem; line-height: 1.7;">
            <li><strong>Peer Reviewer:</strong> IEEE Access, International Journal of Human-Computer Interaction, MDPI Smart Cities, IJACSA, Springer LNCS.</li>
            <li><strong>Conference Committee:</strong> ICE3IS (Track Chair), Annual Research Seminar (ARS).</li>
            <li><strong>Professional Memberships:</strong> IEEE, ACM SIGCHI, Malaysian Software Engineering Interest Group (MySEIG).</li>
          </ul>
        </div>
      </div>
    </section>
    """
    html += get_base_footer()
    return html

def build_all():
    print("Starting Academic Static Site Build for zaidamin.org...")
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Compile pages
    index_content = generate_index_html()
    cv_content = generate_cv_html()

    with open(DIST_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    with open(DIST_DIR / "cv.html", "w", encoding="utf-8") as f:
        f.write(cv_content)

    # Also keep index.html and cv.html at workspace root for immediate browser previewing
    with open(BASE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    with open(BASE_DIR / "cv.html", "w", encoding="utf-8") as f:
        f.write(cv_content)

    # 2. Copy assets
    dist_assets = DIST_DIR / "assets"
    if dist_assets.exists():
        shutil.rmtree(dist_assets)
    shutil.copytree(ASSETS_DIR, dist_assets)

    # 3. Copy CNAME
    cname_src = BASE_DIR / "CNAME"
    if cname_src.exists():
        shutil.copy(cname_src, DIST_DIR / "CNAME")

    # 4. Copy BibTeX
    bib_src = DATA_DIR / "publications.bib"
    if bib_src.exists():
        shutil.copy(bib_src, DIST_DIR / "publications.bib")
        shutil.copy(bib_src, BASE_DIR / "publications.bib")

    print("Build completed successfully!")
    print(f"- Production distribution: {DIST_DIR}")
    print(f"- Main index page: {DIST_DIR / 'index.html'}")
    print(f"- Curriculum Vitae page: {DIST_DIR / 'cv.html'}")

if __name__ == "__main__":
    build_all()

