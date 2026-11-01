/**
 * Academic Website JavaScript - Dr. Zaid Amin (zaidamin.org)
 * Features:
 * - Dark / Light theme toggle with localStorage persistence
 * - Real-time publication search and category pill filtering
 * - BibTeX citation modal & one-click copy to clipboard
 * - Mobile navigation menu toggle
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initCustomSoundtrackPlayer();
  initScholarlyDrawer();
  initJournalTicker();
  initPortalMenuTicker();
  initPublicationsFilter();
  initBibtexButtons();
  initMobileMenu();
});

/* --------------------------------------------------------------------------
   Theme Switcher (Dark / Light)
   -------------------------------------------------------------------------- */
/* --------------------------------------------------------------------------
   Permanent Dark Theme Enforcer (Light mode disabled)
   -------------------------------------------------------------------------- */
function initThemeToggle() {
  setTheme('dark');
}

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', 'dark');
  localStorage.setItem('theme', 'dark');
}

/* --------------------------------------------------------------------------
   Publications Filtering & Search Engine
   -------------------------------------------------------------------------- */
function initPublicationsFilter() {
  const searchInput = document.getElementById('pub-search');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const pubItems = document.querySelectorAll('.pub-item');
  const countIndicator = document.getElementById('pub-count-indicator');

  if (!pubItems.length) return;

  let currentCategory = 'all';
  let currentQuery = '';

  function applyFilters() {
    let visibleCount = 0;

    pubItems.forEach(item => {
      const category = item.getAttribute('data-category') || '';
      const textContent = item.textContent.toLowerCase();

      const matchesCategory = (currentCategory === 'all') || (category.toLowerCase() === currentCategory.toLowerCase());
      const matchesQuery = !currentQuery || textContent.includes(currentQuery);

      if (matchesCategory && matchesQuery) {
        item.style.display = 'block';
        visibleCount++;
      } else {
        item.style.display = 'none';
      }
    });

    if (countIndicator) {
      countIndicator.textContent = `Showing ${visibleCount} of ${pubItems.length} publications`;
    }
  }

  // Filter pills event
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.getAttribute('data-filter') || 'all';
      applyFilters();
    });
  });

  // Search input event
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      currentQuery = e.target.value.trim().toLowerCase();
      applyFilters();
    });
  }
}

/* --------------------------------------------------------------------------
   BibTeX Toggle & Copy to Clipboard
   -------------------------------------------------------------------------- */
function initBibtexButtons() {
  document.querySelectorAll('.btn-bibtex-toggle').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = btn.getAttribute('data-target');
      const box = document.getElementById(targetId);
      if (box) {
        box.classList.toggle('show');
        btn.textContent = box.classList.contains('show') ? 'Hide BibTeX' : 'Cite / BibTeX';
      }
    });
  });

  document.querySelectorAll('.bibtex-copy-btn').forEach(copyBtn => {
    copyBtn.addEventListener('click', () => {
      const targetId = copyBtn.getAttribute('data-target');
      const codeElement = document.getElementById(targetId);
      if (codeElement) {
        const textToCopy = codeElement.innerText;
        navigator.clipboard.writeText(textToCopy).then(() => {
          const originalText = copyBtn.textContent;
          copyBtn.textContent = 'Copied!';
          copyBtn.style.backgroundColor = 'var(--brand-emerald-light)';
          copyBtn.style.color = 'var(--brand-emerald)';
          setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.backgroundColor = '';
            copyBtn.style.color = '';
          }, 2000);
        });
      }
    });
  });
}

/* --------------------------------------------------------------------------
   Mobile Menu Toggle
   -------------------------------------------------------------------------- */
function initMobileMenu() {
  const toggle = document.querySelector('.mobile-nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('mobile-active');
    });

    // Close when clicking any nav link
    links.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        links.classList.remove('mobile-active');
      });
    });
  }
}


/* --------------------------------------------------------------------------
   Wardiere Showcase: 3D Research Focus Carousel & Quick Package Filter
   -------------------------------------------------------------------------- */
let activeCarouselIndex = 1;

function setCarouselCard(index) {
  activeCarouselIndex = (index + 3) % 3;
  updateCarouselView();
}

function rotateCarousel(dir) {
  setCarouselCard(activeCarouselIndex + dir);
}

function updateCarouselView() {
  const c0 = document.getElementById('carousel-card-0');
  const c1 = document.getElementById('carousel-card-1');
  const c2 = document.getElementById('carousel-card-2');
  const dots = document.querySelectorAll('.carousel-dots .dot');

  if (!c0 || !c1 || !c2) return;

  const cards = [c0, c1, c2];

  cards.forEach(c => {
    c.className = 'carousel-preview-card';
  });

  const prevIdx = (activeCarouselIndex + 2) % 3;
  const nextIdx = (activeCarouselIndex + 1) % 3;

  cards[prevIdx].classList.add('card-prev');
  cards[activeCarouselIndex].classList.add('card-active');
  cards[nextIdx].classList.add('card-next');

  dots.forEach((dot, idx) => {
    if (idx === activeCarouselIndex) {
      dot.classList.add('active');
    } else {
      dot.classList.remove('active');
    }
  });
}

function filterHomePackages(query) {
  const items = document.querySelectorAll('#home-packages-list .package-item-card');
  const q = (query || '').toLowerCase().trim();

  items.forEach(item => {
    const text = item.textContent.toLowerCase();
    if (!q || text.includes(q)) {
      item.style.display = 'grid';
    } else {
      item.style.display = 'none';
    }
  });
}

/* --------------------------------------------------------------------------
   Scholarly Profiles Side Expansion (Star of David Button Interaction)
   -------------------------------------------------------------------------- */
function initScholarlyDrawer() {
  const trigger = document.getElementById('star-toggle-btn');
  const linksContainer = document.getElementById('top-scholarly-links');
  const mainNav = document.getElementById('top-main-nav');
  if (!trigger || !linksContainer) return;

  let closeTimeout = null;
  let isPinned = false;

  function openLinks() {
    clearTimeout(closeTimeout);
    if (mainNav) mainNav.classList.add('nav-hidden');
    linksContainer.classList.add('is-open');
    linksContainer.setAttribute('aria-hidden', 'false');
    trigger.classList.add('is-active');
    trigger.setAttribute('aria-expanded', 'true');
  }

  function closeLinks(force = false) {
    if (isPinned && !force) return;
    clearTimeout(closeTimeout);
    closeTimeout = setTimeout(() => {
      linksContainer.classList.remove('is-open');
      linksContainer.setAttribute('aria-hidden', 'true');
      trigger.classList.remove('is-active');
      trigger.setAttribute('aria-expanded', 'false');
      if (mainNav) mainNav.classList.remove('nav-hidden');
      if (force) isPinned = false;
    }, 280);
  }

  // Click toggle (Pins or unpins)
  trigger.addEventListener('click', (e) => {
    e.stopPropagation();
    e.preventDefault();
    if (linksContainer.classList.contains('is-open') && isPinned) {
      closeLinks(true);
    } else {
      isPinned = true;
      openLinks();
    }
  });

  // Hover support
  trigger.addEventListener('mouseenter', openLinks);
  trigger.addEventListener('mouseleave', () => closeLinks(false));

  linksContainer.addEventListener('mouseenter', () => {
    clearTimeout(closeTimeout);
  });
  linksContainer.addEventListener('mouseleave', () => closeLinks(false));

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!linksContainer.contains(e.target) && !trigger.contains(e.target)) {
      closeLinks(true);
    }
  });

  // Close on ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeLinks(true);
    }
  });
}


/* --------------------------------------------------------------------------
   Journal Publication Ticker (Animate fade in/out move from top to down)
   -------------------------------------------------------------------------- */
let journalTickerIndex = 0;
let journalTickerInterval = null;
let isJournalTickerPaused = false;

function initJournalTicker() {
  const slides = document.querySelectorAll('.ticker-slide-item');
  if (!slides || slides.length === 0) return;

  // Set initial state
  slides.forEach((slide, idx) => {
    slide.classList.remove('active', 'slide-out-down');
    if (idx === 0) slide.classList.add('active');
  });

  const counter = document.getElementById('ticker-counter');
  if (counter) counter.textContent = `1 / ${slides.length}`;

  // Start smooth auto-advance every 4.8s
  clearInterval(journalTickerInterval);
  journalTickerInterval = setInterval(() => {
    if (!isJournalTickerPaused) {
      rotateJournalTicker(1);
    }
  }, 4800);
}

function rotateJournalTicker(dir) {
  const slides = document.querySelectorAll('.ticker-slide-item');
  if (!slides || slides.length === 0) return;

  const prevIdx = journalTickerIndex;
  journalTickerIndex = (journalTickerIndex + dir + slides.length) % slides.length;

  // Animate: current slide slides out downwards (0 -> +20px, fade out)
  slides[prevIdx].classList.remove('active');
  slides[prevIdx].classList.add('slide-out-down');

  // Next slide enters from top (-20px -> 0, fade in)
  slides[journalTickerIndex].classList.remove('slide-out-down');
  slides[journalTickerIndex].classList.add('active');

  const counter = document.getElementById('ticker-counter');
  if (counter) {
    counter.textContent = `${journalTickerIndex + 1} / ${slides.length}`;
  }
}

function pauseJournalTicker() {
  isJournalTickerPaused = true;
}

function resumeJournalTicker() {
  isJournalTickerPaused = false;
}

/* --------------------------------------------------------------------------
   Custom Soft-Transparent Soundtrack Player (Test Driving Toothless)
   -------------------------------------------------------------------------- */
function initCustomSoundtrackPlayer() {
  const audio = document.getElementById('soundtrack-audio');
  const playBtn = document.getElementById('royal-play-btn');
  const playIcon = playBtn ? playBtn.querySelector('.play-icon') : null;
  const pauseIcon = playBtn ? playBtn.querySelector('.pause-icon') : null;
  const timeDisplay = document.getElementById('royal-time-display');
  const progressWrap = document.getElementById('royal-progress-wrap');
  const progressFill = document.getElementById('royal-progress-fill');
  const progressThumb = document.getElementById('royal-progress-thumb');
  const muteBtn = document.getElementById('royal-mute-btn');
  const volHigh = muteBtn ? muteBtn.querySelector('.volume-high') : null;
  const volMuted = muteBtn ? muteBtn.querySelector('.volume-muted') : null;

  if (!audio || !playBtn) return;

  function formatTime(sec) {
    if (isNaN(sec) || sec < 0) return '0:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }

  playBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (audio.paused) {
      audio.play().catch(err => console.log('Audio playback info:', err));
    } else {
      audio.pause();
    }
  });

  audio.addEventListener('play', () => {
    if (playIcon) playIcon.style.display = 'none';
    if (pauseIcon) pauseIcon.style.display = 'block';
  });

  audio.addEventListener('pause', () => {
    if (playIcon) playIcon.style.display = 'block';
    if (pauseIcon) pauseIcon.style.display = 'none';
  });

  audio.addEventListener('ended', () => {
    if (playIcon) playIcon.style.display = 'block';
    if (pauseIcon) pauseIcon.style.display = 'none';
    if (progressFill) progressFill.style.width = '0%';
    if (progressThumb) progressThumb.style.left = '0%';
    audio.currentTime = 0;
  });

  audio.addEventListener('timeupdate', () => {
    const cur = audio.currentTime;
    const dur = audio.duration || 183;
    const pct = (cur / dur) * 100;

    if (timeDisplay) {
      timeDisplay.textContent = `${formatTime(cur)} / ${formatTime(dur)}`;
    }
    if (progressFill) {
      progressFill.style.width = `${pct}%`;
    }
    if (progressThumb) {
      progressThumb.style.left = `${pct}%`;
    }
  });

  audio.addEventListener('loadedmetadata', () => {
    if (timeDisplay && audio.duration) {
      timeDisplay.textContent = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
    }
  });

  if (progressWrap) {
    progressWrap.addEventListener('click', (e) => {
      const rect = progressWrap.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const width = rect.width;
      const pct = Math.max(0, Math.min(1, clickX / width));
      const dur = audio.duration || 183;
      audio.currentTime = pct * dur;
    });
  }

  if (muteBtn) {
    muteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      audio.muted = !audio.muted;
      if (volHigh) volHigh.style.display = audio.muted ? 'none' : 'block';
      if (volMuted) volMuted.style.display = audio.muted ? 'block' : 'none';
    });
  }
}


/* --------------------------------------------------------------------------
   Dynamic Top-to-Down Portal Menu Ticker (Changing Randomly like Indexed Journals)
   Supports:
   - Mode 'waterfall': Cards glide down top-to-down in unison as a new item enters
   - Mode 'slot_flip': Individual card slots flip top-to-down mirroring .ticker-slide-item
   Pauses automatically on user hover so links are easily clickable.
   -------------------------------------------------------------------------- */
const PORTAL_ANIM_MODE = 'waterfall'; // Options: 'waterfall' | 'slot_flip'
let portalTickerInterval = null;
let isPortalTickerPaused = false;

const PORTAL_CATALOG = [
  {
    tag: "24 Works",
    tagClass: "font-cinzel",
    thumbWebp: "assets/images/thumb-research.webp",
    thumbJpg: "assets/images/thumb-research.jpg",
    title: "Research & Publications",
    bullets: [
      "24 Peer-Reviewed Articles (MDPI, IEEE, Scopus Q1)",
      "Trustworthy AI & Civic Autonomous Systems",
      "Full Open-Access Preprints & BibTeX Citations"
    ],
    btnText: "Explore",
    btnHref: "publications.html",
    target: "_self"
  },
  {
    tag: "FRGS / AI",
    tagClass: "font-cinzel",
    thumbWebp: "assets/images/thumb-projects.webp",
    thumbJpg: "assets/images/thumb-projects.jpg",
    title: "Projects & Innovations",
    bullets: [
      "FRGS Grant: Civic Compliance Framework",
      "Multimodal Orchestration Agent Architecture",
      "Municipal Autonomous Auditing Prototypes"
    ],
    btnText: "Inspect",
    btnHref: "research.html",
    target: "_self"
  },
  {
    tag: "IEEE Access",
    tagClass: "font-cinzel",
    thumbWebp: "assets/images/thumb-attention.webp",
    thumbJpg: "assets/images/thumb-attention.jpg",
    title: "Attention-Based Decision Systems",
    bullets: [
      "IEEE Access (2021) • Q1 Scopus Indexed",
      "Visual Attention System for Digital Environments",
      "Empirical Intervention & Cognitive Feedback Loops"
    ],
    btnText: "Read",
    btnHref: "https://doi.org/10.1109/ACCESS.2021.3087740",
    target: "_blank"
  },
  {
    tag: "Governance",
    tagClass: "font-cinzel",
    thumbWebp: "assets/images/thumb-governance.webp",
    thumbJpg: "assets/images/thumb-governance.jpg",
    title: "The Proxy Trap in Agentic AI",
    bullets: [
      "AI Governance Series • SSRN Preprint 2026",
      "When Metrics Replace Judgment in Autonomous Nodes",
      "Preserving Civic Human Oversight in Admin Protocols"
    ],
    btnText: "Examine",
    btnHref: "https://doi.org/10.2139/ssrn.7670124",
    target: "_blank"
  },
  {
    tag: "UKM Ph.D.",
    tagClass: "font-cinzel",
    thumbWebp: "assets/images/dr-zaid.webp",
    thumbJpg: "assets/images/dr-zaid.png",
    title: "About, Talks & Academic CV",
    bullets: [
      "Ph.D. in Computer Science (UKM)",
      "Keynote Speaker, Media Interviews & Panels",
      "Awards, Academic Honors & Leadership Track"
    ],
    btnText: "View CV",
    btnHref: "cv.html",
    target: "_self"
  },
  {
    tag: "JISTM 2026",
    tagClass: "font-cinzel",
    thumbWebp: "assets/images/thumb-research.webp",
    thumbJpg: "assets/images/thumb-research.jpg",
    title: "Srivijayapedia Heritage Platform",
    bullets: [
      "Preservation of Srivijaya Maritime Civilization",
      "Semantic Digital Archive & Spatial Mapping",
      "Human-Centered Cultural Heritage Informatics"
    ],
    btnText: "Read",
    btnHref: "https://doi.org/10.35631/JISTM.1141001",
    target: "_blank"
  },
  {
    tag: "Springer",
    tagClass: "font-cinzel",
    thumbWebp: "assets/images/thumb-attention.webp",
    thumbJpg: "assets/images/thumb-attention.jpg",
    title: "Digital Loneliness & Screen Epoch",
    bullets: [
      "Contributions to Management Science (Springer 2024)",
      "Cognitive Distraction in Social Media Ecosystems",
      "Algorithmic Attention Capture & Behavioral Health"
    ],
    btnText: "Read",
    btnHref: "https://doi.org/10.1007/978-3-031-52280-2_14",
    target: "_blank"
  },
  {
    tag: "Smart Cities",
    tagClass: "font-cinzel",
    thumbWebp: "assets/images/spotlight-smart-cities.webp",
    thumbJpg: "assets/images/spotlight-smart-cities.jpg",
    title: "Municipal Autonomous Auditing",
    bullets: [
      "MDPI Smart Cities (2026) • Volume 9 Lead Author",
      "Multi-Agent Governance & Civic Feedback Loops",
      "Mitigating Reward Hacking in Autonomous Urbanism"
    ],
    btnText: "Inspect",
    btnHref: "https://doi.org/10.3390/smartcities9100174",
    target: "_blank"
  }
];

function initPortalMenuTicker() {
  const tray = document.querySelector('.ref-inset-tray');
  if (!tray) return;

  // Pause rotation on hover
  tray.addEventListener('mouseenter', () => { isPortalTickerPaused = true; });
  tray.addEventListener('mouseleave', () => { isPortalTickerPaused = false; });

  // Rotate every 4.5 seconds
  clearInterval(portalTickerInterval);
  portalTickerInterval = setInterval(() => {
    if (!isPortalTickerPaused) {
      if (PORTAL_ANIM_MODE === 'waterfall') {
        rotatePortalWaterfallDown();
      } else {
        rotatePortalSlotFlip();
      }
    }
  }, 4500);
}

function rotatePortalWaterfallDown() {
  const tray = document.querySelector('.ref-inset-tray');
  if (!tray) return;
  const cards = tray.querySelectorAll('.ref-item-card');
  if (cards.length === 0) return;

  // Pick an item from PORTAL_CATALOG that is not currently displayed in the tray
  const visibleTitles = Array.from(cards).map(c => {
    const t = c.querySelector('.ref-item-title');
    return t ? t.textContent.trim().toLowerCase() : '';
  });

  const available = PORTAL_CATALOG.filter(item => !visibleTitles.includes(item.title.toLowerCase()));
  const pool = available.length > 0 ? available : PORTAL_CATALOG;
  const nextItem = pool[Math.floor(Math.random() * pool.length)];

  // Measure card height for seamless margin-top animation
  const cardHeight = cards[0].offsetHeight || 74;

  // Create incoming card element
  const newCard = document.createElement('div');
  newCard.className = 'ref-item-card ref-card-incoming';
  newCard.style.marginTop = `-${cardHeight + 8}px`;
  newCard.style.opacity = '0';
  newCard.style.transform = 'translateY(-16px)';
  newCard.style.transition = 'margin-top 0.65s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.50s ease, transform 0.60s cubic-bezier(0.16, 1, 0.3, 1)';

  newCard.innerHTML = `
    <div class="ref-item-thumb-box">
      <picture>
        <source srcset="${nextItem.thumbWebp}" type="image/webp">
        <img src="${nextItem.thumbJpg}" alt="${nextItem.title}" class="ref-item-thumb" width="82" height="60" loading="lazy">
      </picture>
    </div>
    <div class="ref-item-info">
      <h4 class="ref-item-title ${nextItem.tagClass}">${nextItem.title}</h4>
      <ul class="ref-item-bullets">
        ${nextItem.bullets.map(b => `<li>${b}</li>`).join('')}
      </ul>
    </div>
    <div class="ref-item-meta-action">
      <span class="ref-item-tag ${nextItem.tagClass}">${nextItem.tag}</span>
      <a href="${nextItem.btnHref}" ${nextItem.target === '_blank' ? 'target="_blank" rel="noopener"' : ''} class="ref-item-btn">${nextItem.btnText}</a>
    </div>
  `;

  // Prepend new card
  tray.insertBefore(newCard, cards[0]);

  // Fade out bottom card
  const lastCard = cards[cards.length - 1];
  lastCard.style.transition = 'opacity 0.45s ease, transform 0.55s ease';
  lastCard.style.opacity = '0';
  lastCard.style.transform = 'translateY(16px)';

  // Animate new card down
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      newCard.style.marginTop = '0px';
      newCard.style.opacity = '1';
      newCard.style.transform = 'translateY(0)';
    });
  });

  // Cleanup after animation completes
  setTimeout(() => {
    if (lastCard && lastCard.parentNode) {
      lastCard.parentNode.removeChild(lastCard);
    }
    newCard.style.marginTop = '';
    newCard.style.opacity = '';
    newCard.style.transform = '';
    newCard.style.transition = '';
    newCard.classList.remove('ref-card-incoming');
  }, 680);
}

function rotatePortalSlotFlip() {
  const tray = document.querySelector('.ref-inset-tray');
  if (!tray) return;
  const cards = tray.querySelectorAll('.ref-item-card');
  if (cards.length === 0) return;

  // Pick a random slot to update
  const slotIdx = Math.floor(Math.random() * cards.length);
  const targetCard = cards[slotIdx];

  const visibleTitles = Array.from(cards).map(c => {
    const t = c.querySelector('.ref-item-title');
    return t ? t.textContent.trim().toLowerCase() : '';
  });

  const available = PORTAL_CATALOG.filter(item => !visibleTitles.includes(item.title.toLowerCase()));
  const pool = available.length > 0 ? available : PORTAL_CATALOG;
  const nextItem = pool[Math.floor(Math.random() * pool.length)];

  // Animate slot out downwards
  targetCard.style.transition = 'transform 0.40s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease';
  targetCard.style.transform = 'translateY(18px)';
  targetCard.style.opacity = '0';

  setTimeout(() => {
    targetCard.innerHTML = `
      <div class="ref-item-thumb-box">
        <picture>
          <source srcset="${nextItem.thumbWebp}" type="image/webp">
          <img src="${nextItem.thumbJpg}" alt="${nextItem.title}" class="ref-item-thumb" width="82" height="60" loading="lazy">
        </picture>
      </div>
      <div class="ref-item-info">
        <h4 class="ref-item-title ${nextItem.tagClass}">${nextItem.title}</h4>
        <ul class="ref-item-bullets">
          ${nextItem.bullets.map(b => `<li>${b}</li>`).join('')}
        </ul>
      </div>
      <div class="ref-item-meta-action">
        <span class="ref-item-tag ${nextItem.tagClass}">${nextItem.tag}</span>
        <a href="${nextItem.btnHref}" ${nextItem.target === '_blank' ? 'target="_blank" rel="noopener"' : ''} class="ref-item-btn">${nextItem.btnText}</a>
      </div>
    `;

    // Slide in from top
    targetCard.style.transform = 'translateY(-18px)';
    targetCard.style.opacity = '0';

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        targetCard.style.transform = 'translateY(0)';
        targetCard.style.opacity = '1';
      });
    });

    setTimeout(() => {
      targetCard.style.transition = '';
      targetCard.style.transform = '';
      targetCard.style.opacity = '';
    }, 450);
  }, 400);
}


// ==============================================================================
// VISITOR METRICS POPUP TOUCH / CLICK TOGGLE
// ==============================================================================
document.addEventListener('DOMContentLoaded', () => {
  const statsTrigger = document.querySelector('.stats-title-interactive');
  if (statsTrigger) {
    statsTrigger.addEventListener('click', (e) => {
      if (!e.target.closest('.stats-tooltip-popup')) {
        const popup = statsTrigger.querySelector('.stats-tooltip-popup');
        if (popup) popup.classList.toggle('is-active');
      }
    });
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.stats-title-interactive')) {
        const popup = statsTrigger.querySelector('.stats-tooltip-popup');
        if (popup) popup.classList.remove('is-active');
      }
    });
  }
});


// ==============================================================================
// FLOATING SCROLL TO TOP CONTROLLER (HIGH-PERFORMANCE PASSIVE LISTENER)
// ==============================================================================
document.addEventListener('DOMContentLoaded', () => {
  const scrollBtn = document.getElementById('scroll-to-top');
  if (scrollBtn) {
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (window.scrollY > 300) {
            scrollBtn.classList.add('visible');
          } else {
            scrollBtn.classList.remove('visible');
          }
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    scrollBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
});

// ==============================================================================
// SPOTLIGHT & BLOGGER ARTICLES CAROUSEL CONTROLLER
// ==============================================================================
document.addEventListener('DOMContentLoaded', () => {
  const carousel = document.getElementById('spotlight-carousel');
  if (!carousel) return;
  
  const slides = carousel.querySelectorAll('.spotlight-slide');
  if (!slides.length) return;
  
  let currentIndex = 0;
  const total = slides.length;
  
  function goToSlide(idx) {
    if (idx < 0) idx = total - 1;
    if (idx >= total) idx = 0;
    currentIndex = idx;
    
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === currentIndex);
      const dots = slide.querySelectorAll('.spotlight-dot');
      dots.forEach((dot, dIdx) => {
        dot.classList.toggle('active', dIdx === currentIndex);
      });
    });
  }
  
  carousel.addEventListener('click', (e) => {
    const prevBtn = e.target.closest('.spotlight-arrow-prev');
    const nextBtn = e.target.closest('.spotlight-arrow-next');
    const dotBtn = e.target.closest('.spotlight-dot');
    
    if (prevBtn) {
      e.preventDefault();
      goToSlide(currentIndex - 1);
    } else if (nextBtn) {
      e.preventDefault();
      goToSlide(currentIndex + 1);
    } else if (dotBtn) {
      e.preventDefault();
      const target = parseInt(dotBtn.getAttribute('data-slide-target'), 10);
      if (!isNaN(target)) goToSlide(target);
    }
  });
  
  // Touch swipe support
  let touchStartX = 0;
  carousel.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });
  
  carousel.addEventListener('touchend', (e) => {
    const diff = e.changedTouches[0].screenX - touchStartX;
    if (Math.abs(diff) > 45) {
      if (diff > 0) goToSlide(currentIndex - 1);
      else goToSlide(currentIndex + 1);
    }
  }, { passive: true });
});
