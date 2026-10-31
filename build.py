"""
Academic Static Site Generator - zaidamin.org
Compiler for Dr. Zaid Amin's Premium Academic Portal
Generates:
- index.html (Compact, hook-catchy, premium executive showroom)
- publications.html (Complete 24-paper interactive catalog with search & BibTeX)
- research.html (In-depth research pillars & grant dossier)
- prospective-students.html (Postgraduate recruitment & supervision guide)
- cv.html (Print-ready academic Curriculum Vitae)
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
        "arrow-right": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>',
        "pdf": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>',
        "shield": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
        "eye": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>',
        "globe": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line></svg>',
        "award": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg>',
        "book": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>',
        "search": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
        "external": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'
    }
    return icons.get(name, "")

def get_base_header(active_nav="home", title="Dr. Zaid Amin | Academic & Computational Researcher", description="", extra_meta=""):
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

    def nav_class(name):
        return "nav-link active" if active_nav == name else "nav-link"

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
  {extra_meta}

  <!-- JSON-LD -->
  <script type="application/ld+json">
  {json.dumps(schema_json, indent=2)}
  </script>

  <!-- Typography & Styling -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="icon" href="favicon.ico">
</head>
<body>
  <nav class="navbar" role="navigation" aria-label="Main Navigation">
    <div class="container nav-container">
      <a href="index.html" class="nav-brand">
        <span class="nav-brand-title">Dr. Zaid Amin</span>
        <span class="nav-brand-subtitle">Das Sein, das Sollen</span>
      </a>

      <ul class="nav-links">
        <li><a href="index.html" class="{nav_class('home')}">Home</a></li>
        <li><a href="publications.html" class="{nav_class('publications')}">Publications (24+)</a></li>
        <li><a href="research.html" class="{nav_class('research')}">Research & Grants</a></li>
        <li><a href="prospective-students.html" class="{nav_class('lab')}">Join Lab (Ph.D./Master)</a></li>
        <li><a href="cv.html" class="{nav_class('cv')}">CV</a></li>
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
          <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-primary); margin-bottom: 6px;">Dr. Zaid Amin, Ph.D.</div>
          <div style="font-family: var(--font-serif); font-style: italic; color: var(--brand-blue); margin-bottom: 12px;">"Das Sein, das Sollen" &bull; {profile['tagline']}</div>
          <p style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.6; max-width: 480px;">
            {profile['affiliation']['faculty']}<br>
            <strong>{profile['affiliation']['institution']}</strong>, {profile['affiliation']['location']}.
          </p>
        </div>
        <div>
          <h4 style="margin-bottom: 12px; font-size: 0.95rem;">Academic Navigation</h4>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 8px;">
            <li><a href="publications.html" style="color: var(--text-muted); font-size: 0.85rem;">Publications & BibTeX (24 Works)</a></li>
            <li><a href="research.html" style="color: var(--text-muted); font-size: 0.85rem;">Research Pillars & Grants</a></li>
            <li><a href="prospective-students.html" style="color: var(--text-muted); font-size: 0.85rem;">Postgraduate Lab (Open Positions)</a></li>
            <li><a href="cv.html" style="color: var(--text-muted); font-size: 0.85rem;">Curriculum Vitae (PDF)</a></li>
          </ul>
        </div>
        <div>
          <h4 style="margin-bottom: 12px; font-size: 0.95rem;">Scholarly Identifiers</h4>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 8px;">
            <li><a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" style="color: var(--text-muted); font-size: 0.85rem;">ORCID: {profile['metrics']['orcid_id']}</a></li>
            <li><a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" style="color: var(--text-muted); font-size: 0.85rem;">Google Scholar</a></li>
            <li><a href="{profile['social_links']['github']}" target="_blank" rel="noopener" style="color: var(--text-muted); font-size: 0.85rem;">GitHub (@zaeedh)</a></li>
            <li><a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" style="color: var(--text-muted); font-size: 0.85rem;">LinkedIn</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div>&copy; 2026 Dr. Zaid Amin. Developed with Academic Rigor & Clean Web Standards.</div>
        <div>Domain: <strong>zaidamin.org</strong></div>
      </div>
    </div>
  </footer>
  <script src="assets/js/main.js"></script>
</body>
</html>
"""

# ==============================================================================
# 1. COMPACT, HOOK-CATCHY PREMIUM LANDING PAGE (index.html)
# ==============================================================================
def generate_compact_home():
    profile = load_json("profile.json")
    publications = load_json("publications.json")
    research = load_json("research.json")
    supervision = load_json("supervision.json")
    essays = load_json("essays.json")

    html = get_base_header("home", "Dr. Zaid Amin | Academic & Computational Researcher | zaidamin.org")

    # Hero Hook
    html += f"""
    <section class="hero-compact">
      <div class="container hero-compact-header">
        <div class="hero-pill-hook">
          <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background-color:var(--brand-emerald);"></span>
          Senior Lecturer in Data Science &bull; INTI International University &bull; Ph.D. UKM
        </div>

        <h1 class="hero-main-title">{profile['name']}<span style="color:var(--brand-accent); font-size:2rem;">, Ph.D.</span></h1>
        <div class="hero-creds">Human-Computer Interaction &bull; AI Governance &bull; Behavioral Computing</div>

        <p class="hero-tagline-quote font-serif">
          &ldquo;<strong>Das Sein, das Sollen</strong> &mdash; Bridging the gap between what computational systems <em>are</em>, and what human society <em>ought</em> to become.&rdquo;
        </p>

        <p class="hero-mission-statement">
          Senior Lecturer and computational researcher investigating the frontiers of <strong>Agentic AI Governance</strong>, <strong>Attention-Based Interface Interventions</strong>, and <strong>Digital Ethics</strong>. Former Head of Master in Informatics Engineering, actively architecting verified guardrails to ensure artificial intelligence serves human dignity rather than exploitation.
        </p>

        <div class="hero-cta-group">
          <a href="publications.html" class="btn btn-primary">
            Explore Publications (24+)
            {render_svg_icon('arrow-right')}
          </a>
          <a href="prospective-students.html" class="btn btn-accent">
            Join My Research Group
          </a>
          <a href="cv.html" class="btn btn-secondary">
            {render_svg_icon('pdf')}
            View CV
          </a>
        </div>

        <div class="academic-badges-center">
          <a href="{profile['social_links']['scholar']}" target="_blank" rel="noopener" class="badge-link">
            {render_svg_icon('scholar')} Google Scholar
          </a>
          <a href="{profile['social_links']['orcid']}" target="_blank" rel="noopener" class="badge-link">
            {render_svg_icon('orcid')} ORCID ({profile['metrics']['orcid_id']})
          </a>
          <a href="{profile['social_links']['github']}" target="_blank" rel="noopener" class="badge-link">
            {render_svg_icon('github')} GitHub
          </a>
          <a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="badge-link">
            {render_svg_icon('linkedin')} LinkedIn
          </a>
        </div>
      </div>
    </section>
    """

    # Bento Grid Showroom
    html += f"""
    <section class="bento-section">
      <div class="container">
        <div style="text-align: center; max-width: 680px; margin: 0 auto 36px auto;">
          <span style="font-size: 0.75rem; font-weight: 700; color: var(--brand-blue); text-transform: uppercase; letter-spacing: 0.1em;">Executive Dossier</span>
          <h2 style="font-size: 2.1rem; line-height: 1.25; margin-top: 6px;">Research Vision & Academic Leadership</h2>
        </div>

        <div class="bento-grid">
          <!-- Card 1: Agentic AI (Span 2) -->
          <div class="bento-card bento-card-span-2">
            <div class="bento-icon-box">
              {render_svg_icon('shield')}
            </div>
            <h3 class="bento-card-title">AI Governance & The Proxy Trap in Agentic Systems</h3>
            <p class="bento-card-desc">
              When autonomous agentic AI models optimize surrogate metrics, they inevitably divert from underlying human purpose. Our framework investigates multi-agent orchestration for civic compliance, urban sustainability, and structural safeguards where human judgment cannot be automated away.
            </p>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 14px;">
              <span style="font-size: 0.8rem; color: var(--brand-accent); font-weight: 700;">★ High-Impact 2026 Focus</span>
              <a href="research.html" class="bento-link">Explore Research Pillars {render_svg_icon('arrow-right')}</a>
            </div>
          </div>

          <!-- Card 2: HCI & Attention -->
          <div class="bento-card">
            <div class="bento-icon-box" style="background-color: var(--brand-emerald-light); color: var(--brand-emerald);">
              {render_svg_icon('eye')}
            </div>
            <h3 class="bento-card-title">HCI & Cognitive Interventions</h3>
            <p class="bento-card-desc">
              Building upon the <strong>Tune-Attention Model</strong> developed during doctoral work at UKM, developing humane interface interventions to counteract misinformation, viral distraction, and digital loneliness.
            </p>
            <a href="research.html" class="bento-link">Learn More {render_svg_icon('arrow-right')}</a>
          </div>

          <!-- Card 3: Digital Heritage -->
          <div class="bento-card">
            <div class="bento-icon-box" style="background-color: var(--brand-accent-light); color: var(--brand-accent);">
              {render_svg_icon('globe')}
            </div>
            <h3 class="bento-card-title">Digital Heritage Preservation</h3>
            <p class="bento-card-desc">
              Synthesizing social computing and immersive VR through <strong>Srivijayapedia</strong> to digitally preserve ancient maritime civilizations and cultural memory for future generations.
            </p>
            <a href="research.html" class="bento-link">View Projects {render_svg_icon('arrow-right')}</a>
          </div>

          <!-- Card 4: Academic Track Record (Span 2) -->
          <div class="bento-card bento-card-span-2">
            <div class="bento-icon-box">
              {render_svg_icon('award')}
            </div>
            <h3 class="bento-card-title">Academic Leadership & Track Record</h3>
            <p class="bento-card-desc">
              Senior Lecturer at INTI International University, former Head of Master in Informatics Engineering and Head of Information Systems. Supervised graduate dissertations, led BAN-PT university accreditations, and actively reviewing for top journals.
            </p>
            <div class="bento-metrics-mini">
              <div>
                <div class="bento-metric-num">24+</div>
                <div class="bento-metric-lbl">Indexed Publications</div>
              </div>
              <div>
                <div class="bento-metric-num">Q1</div>
                <div class="bento-metric-lbl">IEEE Access & MDPI</div>
              </div>
              <div>
                <div class="bento-metric-num">10+</div>
                <div class="bento-metric-lbl">Years Academic Leadership</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    """

    # Featured Crown-Jewel Publications (Top 3)
    html += f"""
    <section class="featured-pubs-section">
      <div class="container">
        <div class="section-head-compact">
          <div class="section-head-compact-left">
            <span style="font-size: 0.75rem; font-weight: 700; color: var(--brand-blue); text-transform: uppercase; letter-spacing: 0.1em;">Selected Scholarship</span>
            <h2 style="font-size: 2.1rem; line-height: 1.25; margin-top: 4px;">Featured Publications</h2>
            <p style="font-size: 0.95rem; color: var(--text-muted);">Highlighted recent and foundational contributions from our 24 peer-reviewed works.</p>
          </div>
          <div>
            <a href="publications.html" class="btn btn-secondary">
              View All 24 Publications & BibTeX
              {render_svg_icon('arrow-right')}
            </a>
          </div>
        </div>

        <div>
          <!-- Featured 1 -->
          <article class="featured-pub-card">
            <div class="featured-tag-badge">★ Journal Article &bull; 2026 &bull; MDPI Smart Cities</div>
            <h3 class="featured-pub-title">Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance</h3>
            <div class="featured-pub-authors"><strong>Dr. Zaid Amin</strong> and collaborators</div>
            <div class="featured-pub-venue">Smart Cities (MDPI) &bull; DOI: 10.3390/smartcities9100174</div>
            <div class="featured-pub-actions">
              <a href="https://doi.org/10.3390/smartcities9100174" target="_blank" rel="noopener" class="pub-btn">DOI Article {render_svg_icon('external')}</a>
              <a href="publications.html" class="pub-btn">Cite / BibTeX</a>
            </div>
          </article>

          <!-- Featured 2 -->
          <article class="featured-pub-card">
            <div class="featured-tag-badge">★ SSRN / Working Paper &bull; 2026</div>
            <h3 class="featured-pub-title">The Proxy Trap in Agentic AI: When Metrics Replace Judgment</h3>
            <div class="featured-pub-authors"><strong>Dr. Zaid Amin</strong></div>
            <div class="featured-pub-venue">Social Science Research Network (SSRN) &bull; DOI: 10.2139/ssrn.7670124</div>
            <div class="featured-pub-actions">
              <a href="https://doi.org/10.2139/ssrn.7670124" target="_blank" rel="noopener" class="pub-btn">DOI Article {render_svg_icon('external')}</a>
              <a href="publications.html" class="pub-btn">Cite / BibTeX</a>
            </div>
          </article>

          <!-- Featured 3 -->
          <article class="featured-pub-card">
            <div class="featured-tag-badge">★ Q1 Flagship &bull; 2021 &bull; IEEE Access</div>
            <h3 class="featured-pub-title">Attention-Based Design and User Decisions on Information Sharing: A Thematic Literature Review</h3>
            <div class="featured-pub-authors"><strong>Dr. Zaid Amin</strong> et al.</div>
            <div class="featured-pub-venue">IEEE Access &bull; DOI: 10.1109/ACCESS.2021.3087740</div>
            <div class="featured-pub-actions">
              <a href="https://doi.org/10.1109/ACCESS.2021.3087740" target="_blank" rel="noopener" class="pub-btn">DOI Article {render_svg_icon('external')}</a>
              <a href="publications.html" class="pub-btn">Cite / BibTeX</a>
            </div>
          </article>
        </div>
      </div>
    </section>
    """

    # Postgraduate Lab Hook Banner
    html += f"""
    <section class="section" style="padding: 48px 0;">
      <div class="container">
        <div class="lab-banner-compact">
          <div>
            <span style="font-size: 0.75rem; font-weight: 700; color: #fbbf24; text-transform: uppercase; letter-spacing: 0.08em; display: inline-block; margin-bottom: 8px;">Graduate Opportunities</span>
            <h2 class="lab-banner-title">Accepting Ph.D. & Master's by Research Scholars</h2>
            <p class="lab-banner-desc">
              Join Dr. Zaid Amin's research initiative at INTI International University. Open supervision topics in Agentic AI Alignment, The Proxy Trap, and Attention-Based Interface Interventions.
            </p>
          </div>
          <div>
            <a href="prospective-students.html" class="btn btn-accent" style="white-space: nowrap;">
              Explore Open Topics & Apply
              {render_svg_icon('arrow-right')}
            </a>
          </div>
        </div>
      </div>
    </section>
    """

    # Thought Leadership ("Das Sein, das Sollen")
    html += f"""
    <section class="section section-subtle">
      <div class="container" style="max-width: 860px; text-align: center;">
        <span style="font-size: 0.75rem; font-weight: 700; color: var(--brand-blue); text-transform: uppercase; letter-spacing: 0.1em;">Public Intellectual Writing</span>
        <h2 style="font-size: 2rem; margin: 6px 0 12px 0;">Das Sein, das Sollen</h2>
        <p style="font-size: 1.05rem; color: var(--text-secondary); font-family: var(--font-serif); font-style: italic; margin-bottom: 24px; line-height: 1.6;">
          &ldquo;Every millisecond of digital engagement today has been monetized. Designing systems that honor human stillness requires reimagining friction not as an engineering defect, but as a sacred cognitive sanctuary.&rdquo;
        </p>
        <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.7; margin-bottom: 24px;">
          From Hume's is-ought problem to autonomous LLM alignment: why descriptive machine learning training data ('Das Sein') cannot automatically manufacture moral discernment ('Das Sollen').
        </p>
        <a href="index.html#contact" class="btn btn-secondary">Inquire for Speaking & Keynotes</a>
      </div>
    </section>
    """

    # Contact Section
    html += f"""
    <section class="section" id="contact">
      <div class="container" style="max-width: 760px; text-align: center;">
        <span style="font-size: 0.75rem; font-weight: 700; color: var(--brand-blue); text-transform: uppercase; letter-spacing: 0.1em;">Direct Inquiries</span>
        <h2 style="font-size: 2rem; margin: 6px 0 12px 0;">Connect & Collaborate</h2>
        <p style="font-size: 0.95rem; color: var(--text-muted); margin-bottom: 28px;">
          For research partnerships, keynote invitations, grant applications, or postgraduate inquiries:
        </p>

        <div style="display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; margin-bottom: 28px;">
          <a href="mailto:{profile['social_links']['email']}" class="btn btn-primary">
            zaid.amin@newinti.edu.my
          </a>
          <a href="{profile['social_links']['linkedin']}" target="_blank" rel="noopener" class="btn btn-secondary">
            LinkedIn Profile
          </a>
        </div>

        <div style="font-size: 0.85rem; color: var(--text-muted);">
          Faculty of Data Science and Information Technology (FDSIT)<br>
          INTI International University, Nilai, Negeri Sembilan, Malaysia.
        </div>
      </div>
    </section>
    """

    html += get_base_footer()
    return html

# ==============================================================================
# 2. FULL DEDICATED PUBLICATIONS CATALOG (publications.html)
# ==============================================================================
def generate_publications_page():
    publications = load_json("publications.json")

    html = get_base_header("publications", f"Publications ({len(publications)}) | Dr. Zaid Amin")
    html += f"""
    <section class="section" style="padding-top: 48px;">
      <div class="container">
        <div style="margin-bottom: 32px;">
          <span style="font-size: 0.75rem; font-weight: 700; color: var(--brand-blue); text-transform: uppercase; letter-spacing: 0.1em;">Scholarly Archive</span>
          <h1 style="font-size: 2.5rem; margin-top: 4px;">Complete Publication Catalog ({len(publications)})</h1>
          <p style="font-size: 1rem; color: var(--text-muted); max-width: 780px;">
            Full indexed record across Human-Computer Interaction, AI Governance, Behavioral Computing, and Information Systems. Search in real-time or filter by venue category.
          </p>
        </div>

        <div class="publications-controls">
          <div class="search-input-box">
            <span class="search-icon">{render_svg_icon('search')}</span>
            <input type="text" id="pub-search" class="search-input" placeholder="Search by paper title, venue, year, or keyword...">
          </div>

          <div class="filter-pills">
            <button class="filter-btn active" data-filter="all">All ({len(publications)})</button>
            <button class="filter-btn" data-filter="journal">Journals</button>
            <button class="filter-btn" data-filter="conference">Conferences</button>
            <button class="filter-btn" data-filter="book chapter">Book Chapters</button>
            <button class="filter-btn" data-filter="preprint">Preprints</button>
          </div>
        </div>

        <div id="pub-count-indicator" style="margin-bottom: 16px; font-size: 0.85rem; color: var(--text-muted); font-weight: 600;">
          Showing all {len(publications)} publications
        </div>

        <div class="publications-list">
    """
    for pub in publications:
        type_class = f"type-{pub['category'].lower().replace(' ', '')}"
        doi_link = f'<a href="{pub["url"]}" target="_blank" rel="noopener" class="pub-btn">DOI: {pub["doi"]} {render_svg_icon("external")}</a>' if pub.get("doi") else ""

        html += f"""
          <article class="pub-item" data-category="{pub['category'].lower()}">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <span style="font-size:0.75rem; font-weight:700; color:var(--brand-blue); text-transform:uppercase;">{pub['category']} &bull; {pub['year']}</span>
              {f'<span style="font-size:0.75rem; color:var(--brand-accent); font-weight:700;">★ Featured</span>' if pub.get('featured') else ''}
            </div>

            <h3 style="font-size:1.2rem; margin-bottom:6px; line-height:1.35;">{pub['title']}</h3>
            <div style="font-size:0.9rem; color:var(--text-secondary); margin-bottom:6px;"><strong>Dr. Zaid Amin</strong> and collaborators</div>
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
    </section>
    """
    html += get_base_footer()
    return html

# ==============================================================================
# 3. RESEARCH PILLARS & GRANTS DOSSIER (research.html)
# ==============================================================================
def generate_research_page():
    research = load_json("research.json")

    html = get_base_header("research", "Research Pillars & Grants | Dr. Zaid Amin")
    html += f"""
    <section class="section" style="padding-top: 48px;">
      <div class="container">
        <div style="margin-bottom: 40px;">
          <span style="font-size: 0.75rem; font-weight: 700; color: var(--brand-blue); text-transform: uppercase; letter-spacing: 0.1em;">Scholarly Mission</span>
          <h1 style="font-size: 2.5rem; margin-top: 4px;">Research Pillars & Grant Themes</h1>
          <p style="font-size: 1.05rem; color: var(--text-muted); max-width: 820px; line-height: 1.6;">
            {research['vision']}
          </p>
        </div>

        <div style="display: flex; flex-direction: column; gap: 32px;">
    """
    for pillar in research["pillars"]:
        topics_html = " ".join([f'<span class="topic-chip" style="font-size:0.8rem; padding:4px 10px; background:var(--bg-subtle); border-radius:4px; margin-right:6px; margin-bottom:6px; display:inline-block;">{t}</span>' for t in pillar["key_topics"]])
        html += f"""
          <div style="background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 36px; box-shadow: var(--shadow-sm);">
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:16px;">
              <div class="bento-icon-box" style="margin-bottom:0;">
                {render_svg_icon(pillar['icon'])}
              </div>
              <h2 style="font-size: 1.6rem; margin:0;">{pillar['title']}</h2>
            </div>

            <p style="font-size: 1rem; color: var(--text-secondary); line-height: 1.7; margin-bottom: 20px;">
              {pillar['full_desc']}
            </p>

            <div style="margin-bottom: 20px;">
              <div style="font-size:0.85rem; font-weight:700; margin-bottom:8px; color:var(--text-primary);">Key Theoretical & Technical Areas:</div>
              {topics_html}
            </div>

            <div style="background-color: var(--brand-accent-light); color: var(--brand-accent); padding: 12px 18px; border-radius: var(--radius-sm); font-size: 0.85rem; font-weight: 600; border-left: 4px solid var(--brand-accent);">
              <strong>Grant Alignment:</strong> {pillar['grant_alignment']}
            </div>
          </div>
        """
    html += """
        </div>
      </div>
    </section>
    """
    html += get_base_footer()
    return html

# ==============================================================================
# 4. POSTGRADUATE LAB & SUPERVISION (prospective-students.html)
# ==============================================================================
def generate_supervision_page():
    supervision = load_json("supervision.json")

    html = get_base_header("lab", "Postgraduate Lab & Supervision | Dr. Zaid Amin")
    html += f"""
    <section class="section" style="padding-top: 48px;">
      <div class="container" style="max-width: 920px;">
        <div style="margin-bottom: 32px;">
          <span style="font-size: 0.75rem; font-weight: 700; color: var(--brand-emerald); text-transform: uppercase; letter-spacing: 0.1em;">Academic Mentorship</span>
          <h1 style="font-size: 2.5rem; margin-top: 4px;">{supervision['heading']}</h1>
          <p style="font-size: 1.05rem; color: var(--text-secondary); line-height: 1.7; margin-top: 12px;">
            {supervision['statement']}
          </p>
        </div>

        <div style="margin-bottom: 40px;">
          <h2 style="font-size: 1.5rem; margin-bottom: 20px;">Open Supervised Research Directions</h2>
          <div style="display: flex; flex-direction: column; gap: 20px;">
    """
    for t in supervision["open_topics"]:
        pills = " ".join([f'<span style="background:var(--brand-blue-light); color:var(--brand-blue); padding:3px 10px; border-radius:4px; font-size:0.75rem; font-weight:600;">{d}</span>' for d in t["degree_levels"]])
        html += f"""
            <div style="background-color: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 24px;">
              <div style="margin-bottom: 8px;">{pills}</div>
              <h3 style="font-size: 1.25rem; margin-bottom: 8px;">{t['title']}</h3>
              <p style="font-size: 0.925rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 12px;">{t['description']}</p>
              <div style="font-size: 0.8rem; color: var(--text-muted);"><strong>Prerequisites:</strong> {t['skills_required']}</div>
            </div>
        """
    html += f"""
          </div>
        </div>

        <div style="background-color: var(--bg-surface); border: 2px solid var(--brand-blue); border-radius: var(--radius-lg); padding: 32px;">
          <h2 style="font-size: 1.4rem; color: var(--brand-navy); margin-bottom: 16px;">How to Submit an Inquiry</h2>
          <ol style="margin-left: 20px; font-size: 0.95rem; line-height: 1.8; color: var(--text-secondary);">
            <li>Review my recent papers on Attention-Based Design (IEEE Access) or Agentic AI Governance (Smart Cities 2026).</li>
            <li>Prepare your Academic CV, transcripts, and a 1-page Research Proposal outlining the research questions you wish to pursue.</li>
            <li>Email your dossier to <a href="mailto:zaid.amin@newinti.edu.my" style="font-weight:700; color:var(--brand-blue);">zaid.amin@newinti.edu.my</a> with the subject line <code>[Prospective Postgraduate] - [Your Full Name] - [Ph.D./Master]</code>.</li>
          </ol>
        </div>
      </div>
    </section>
    """
    html += get_base_footer()
    return html

# ==============================================================================
# 5. CURRICULUM VITAE (cv.html)
# ==============================================================================
def generate_cv_page():
    profile = load_json("profile.json")
    publications = load_json("publications.json")

    html = get_base_header("cv", "Curriculum Vitae | Dr. Zaid Amin, Ph.D.")
    html += f"""
    <section class="section" style="padding-top: 48px;">
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

    html += """
          </ol>
        </div>
      </div>
    </section>
    """
    html += get_base_footer()
    return html

# ==============================================================================
# MAIN COMPILER BUILD
# ==============================================================================
def build_all():
    print("Compiling Premium Academic Static Site for zaidamin.org...")
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    pages = {
        "index.html": generate_compact_home(),
        "publications.html": generate_publications_page(),
        "research.html": generate_research_page(),
        "prospective-students.html": generate_supervision_page(),
        "cv.html": generate_cv_page()
    }

    for filename, content in pages.items():
        with open(DIST_DIR / filename, "w", encoding="utf-8") as f:
            f.write(content)
        # Also copy to workspace root for direct preview
        with open(BASE_DIR / filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Compiled: {filename} ({len(content)} chars)")

    # Copy assets
    dist_assets = DIST_DIR / "assets"
    if dist_assets.exists():
        shutil.rmtree(dist_assets)
    shutil.copytree(ASSETS_DIR, dist_assets)

    # Copy CNAME, favicon, and BibTeX
    for extra in ["CNAME", "favicon.ico", "data/publications.bib"]:
        src = BASE_DIR / extra
        if src.exists():
            shutil.copy(src, DIST_DIR / Path(extra).name)

    print("Build complete! All pages successfully generated in dist/ and workspace root.")

if __name__ == "__main__":
    build_all()
