# `zaidamin.org` — Academic Portal & Static Site Generator

> **Official Personal Academic Website of Dr. Zaid Amin, Ph.D.**  
> Senior Lecturer in Data Science & Information Technology  
> Faculty of Data Science and Information Technology (FDSIT), INTI International University, Malaysia.

---

## 🌟 Strategic Vision & Academic Positioning

This platform is specifically engineered to advance Dr. Zaid Amin's career trajectory toward:
1. **Associate Professorship Portfolio**: Comprehensive documentation of research velocity, high-impact Q1 publications (IEEE Access, MDPI Smart Cities, Springer LNCS), academic service, and program leadership track record.
2. **Major Research Grants (FRGS / PRGS / International AI Alignment)**: 3 clearly defined research pillars with targeted grant themes and methodological frameworks.
3. **Postgraduate Lab Recruitment**: Dedicated "Postgraduate Research Opportunities" portal with transparent research topics, candidate prerequisites, and clear contact protocols for top Ph.D. and Master's applicants.
4. **International Keynotes & Speaking Opportunities**: Curated track record of keynotes, conference chairs, and peer-review appointments (IEEE, ACM, Springer, MDPI).
5. **Preserving Scholarly Heritage**: Incorporating Dr. Zaid's intellectual identity (*"Das Sein, das Sollen"*) and bridging empirical computing with ethical imperatives.

---

## 🚀 Quick Start (Local Preview)

The website is 100% self-contained with **zero external npm dependencies**!

### Option 1: Run the Local Python Server
```powershell
python serve.py
```
Then open your browser to **`http://localhost:8000`**.

### Option 2: Open Directly in Any Browser
You can directly double-click or open `index.html` (or `cv.html`) in Google Chrome, Microsoft Edge, Firefox, or Safari.

---

## 🛠️ How to Deploy to `zaidamin.org` via GitHub Pages (100% Free Hosting & SSL)

Because Dr. Zaid already has GitHub account `@zaeedh`, deploying is completely automated:

### Step 1: Create a Repository on GitHub
1. Go to [github.com/new](https://github.com/new)
2. Create a repository named `zaidamin.org` (or `zaeedh.github.io`).
3. Push this directory to the repository:
   ```bash
   git init
   git add .
   git commit -m "Launch new academic website for zaidamin.org"
   git branch -M main
   git remote add origin https://github.com/zaeedh/zaidamin.org.git
   git push -u origin main
   ```

### Step 2: Configure GitHub Pages Custom Domain
1. In your GitHub repository, go to **Settings** &rarr; **Pages**.
2. Under **Build and deployment**:
   - Source: **GitHub Actions** (The pre-configured `.github/workflows/deploy.yml` workflow will automatically build and deploy `dist/` whenever you push).
   - Alternatively: Source: **Deploy from a branch** &rarr; Branch: `main` / folder `/ (root)` or `/dist`.
3. Under **Custom domain**, enter: `zaidamin.org`.
4. Check **Enforce HTTPS** (GitHub provides free automatic SSL certificate renewal).

### Step 3: Configure Your Domain Registrar (DNS for `zaidamin.org`)
At your domain registrar where `zaidamin.org` is registered (e.g. Namecheap, GoDaddy, Cloudflare, etc.):
* Create **4 A Records** pointing to GitHub Pages IP addresses:
  - `185.199.108.153`
  - `185.199.109.153`
  - `185.199.110.153`
  - `185.199.111.153`
* Create **1 CNAME Record** for `www`:
  - Name: `www` &rarr; Target: `zaeedh.github.io`

---

## 📁 Project Architecture

```
d:\WEBSITE ZAID AMIN\
├── CNAME                         # Domain binding for zaidamin.org
├── build.py                      # Academic Static Site Generator compiler
├── serve.py                      # Local development preview server
├── index.html                    # Root web portal (ready to open directly)
├── cv.html                       # Print-ready web Curriculum Vitae
├── .github/workflows/deploy.yml  # Automated GitHub Actions deployment
│
├── data/                         # Pure JSON & BibTeX Data Layer
│   ├── profile.json              # Affiliation, bio, metrics, leadership history
│   ├── publications.json         # All 24 papers indexed from ORCID
│   ├── publications.bib          # Full BibTeX database for researchers
│   ├── research.json             # 3 Research pillars & grant alignments
│   ├── supervision.json          # Ph.D. & Master's recruitment portal
│   ├── teaching.json             # Curricula, teaching philosophy & leadership
│   ├── talks.json                # Keynotes, peer review, academic service
│   └── essays.json               # "Das Sein, das Sollen" intellectual essays
│
├── assets/
│   ├── css/style.css             # High-end Academic Design System (Dark/Light)
│   ├── js/main.js                # Search, category filters, BibTeX copy
│   └── images/                   # Academic headshot & graphical figures
│
└── dist/                         # Compiled production output
```

---

## 📝 Updating Your Content in the Future

### Adding a New Publication
1. Open `data/publications.json`.
2. Add your new paper to the top of the list.
3. Run `python build.py`. Everything updates instantly!

### Updating Research Grants or Student Openings
Edit `data/research.json` or `data/supervision.json`, then run `python build.py`.

