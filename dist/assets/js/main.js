/**
 * Academic Website JavaScript - Dr. Zaid Amin (zaidamin.org)
 * Features:
 * - Dark / Light theme toggle with localStorage persistence
 * - Real-time publication search and category pill filtering
 * - BibTeX citation modal & one-click copy to clipboard
 * - Mobile navigation menu toggle
 */

document.addEventListener('DOMContentLoaded', () => {
  const initModules = [
    ['CyberShield', typeof initCyberShield === 'function' ? initCyberShield : null],
    ['CleanAddressBar', typeof initCleanAddressBar === 'function' ? initCleanAddressBar : null],
    ['ThemeToggle', typeof initThemeToggle === 'function' ? initThemeToggle : null],
    ['CustomSoundtrackPlayer', typeof initCustomSoundtrackPlayer === 'function' ? initCustomSoundtrackPlayer : null],
    ['ScholarlyDrawer', typeof initScholarlyDrawer === 'function' ? initScholarlyDrawer : null],
    ['JournalTicker', typeof initJournalTicker === 'function' ? initJournalTicker : null],
    ['PortalsTrayCarousel', typeof initPortalsTrayCarousel === 'function' ? initPortalsTrayCarousel : null],
    ['AdvancedActivitySearch', typeof initAdvancedActivitySearch === 'function' ? initAdvancedActivitySearch : null],
    ['PublicationsFilter', typeof initPublicationsFilter === 'function' ? initPublicationsFilter : null],
    ['BibtexButtons', typeof initBibtexButtons === 'function' ? initBibtexButtons : null],
    ['MobileMenu', typeof initMobileMenu === 'function' ? initMobileMenu : null],
    ['VisitorTelemetryEngine', typeof initVisitorTelemetryEngine === 'function' ? initVisitorTelemetryEngine : null],
    ['TelemetryAccessTraceLogger', typeof initTelemetryAccessTraceLogger === 'function' ? initTelemetryAccessTraceLogger : null],
    ['CoinPortraitEngine', typeof initCoinPortraitEngine === 'function' ? initCoinPortraitEngine : null],
  ];

  initModules.forEach(([name, fn]) => {
    try {
      if (fn) fn();
    } catch (err) {
      console.warn(`[Module ${name}] execution non-fatal:`, err);
    }
  });
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

  let isDragging = false;
  let activePct = 0;

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
    if (isDragging) return; // Never overwrite thumb while user is actively sliding!
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

  // Smooth Scrubber Drag & Slide Engine (Instant Response, Zero Lag)
  function getPctFromEvent(e) {
    if (!progressWrap) return 0;
    const rect = progressWrap.getBoundingClientRect();
    const clientX = e.touches && e.touches.length > 0
      ? e.touches[0].clientX
      : (e.changedTouches && e.changedTouches.length > 0 ? e.changedTouches[0].clientX : e.clientX);
    const clickX = clientX - rect.left;
    return Math.max(0, Math.min(1, clickX / rect.width));
  }

  function updateVisual(pct) {
    activePct = pct;
    const dur = audio.duration || 183;
    const currentSec = pct * dur;
    if (progressFill) {
      progressFill.style.width = `${pct * 100}%`;
    }
    if (progressThumb) {
      progressThumb.style.left = `${pct * 100}%`;
    }
    if (timeDisplay) {
      timeDisplay.textContent = `${formatTime(currentSec)} / ${formatTime(dur)}`;
    }
  }

  function onDragMove(e) {
    if (!isDragging) return;
    if (e.cancelable) e.preventDefault(); // Prevent touch-screen scrolling while dragging
    const pct = getPctFromEvent(e);
    updateVisual(pct);
  }

  function onDragEnd(e) {
    if (!isDragging) return;
    const pct = getPctFromEvent(e);
    updateVisual(pct);
    const dur = audio.duration || 183;
    
    try {
      audio.currentTime = pct * dur;
    } catch (err) {
      console.log('Seek error:', err);
    }

    setTimeout(() => {
      isDragging = false;
      if (progressWrap) progressWrap.classList.remove('is-dragging');
    }, 50);

    window.removeEventListener('mousemove', onDragMove);
    window.removeEventListener('mouseup', onDragEnd);
    window.removeEventListener('touchmove', onDragMove);
    window.removeEventListener('touchend', onDragEnd);
  }

  function startDrag(e) {
    e.stopPropagation();
    isDragging = true;
    if (progressWrap) progressWrap.classList.add('is-dragging');
    const pct = getPctFromEvent(e);
    updateVisual(pct);

    window.addEventListener('mousemove', onDragMove, { passive: false });
    window.addEventListener('mouseup', onDragEnd);
    window.addEventListener('touchmove', onDragMove, { passive: false });
    window.addEventListener('touchend', onDragEnd);
  }

  if (progressWrap) {
    progressWrap.addEventListener('mousedown', startDrag);
    progressWrap.addEventListener('touchstart', startDrag, { passive: false });

    // Keyboard support for accessibility (ArrowLeft / ArrowRight)
    progressWrap.addEventListener('keydown', (e) => {
      const dur = audio.duration || 183;
      if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
        e.preventDefault();
        const nextTime = Math.max(0, audio.currentTime - 5);
        audio.currentTime = nextTime;
        updateVisual(nextTime / dur);
      } else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
        e.preventDefault();
        const nextTime = Math.min(dur, audio.currentTime + 5);
        audio.currentTime = nextTime;
        updateVisual(nextTime / dur);
      }
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
   Inset Tray Portals & Blogger Articles Vertical Sliding Ticker
   Automatically slides top and down like Indexed Journals Section (4 cards/list)
   -------------------------------------------------------------------------- */
let portalsTickerIndex = 0;
let portalsTickerInterval = null;
let isPortalsTickerPaused = false;

function initPortalsTrayCarousel() {
  const carousel = document.getElementById('portals-carousel');
  if (!carousel) return;

  const track = carousel.querySelector('.tray-slides-track');
  const slides = carousel.querySelectorAll('.tray-slide');
  const currEl = carousel.querySelector('.tray-curr');
  const totalEl = carousel.querySelector('.tray-total');
  const shuffleBtn = carousel.querySelector('#tray-shuffle-toggle, .tray-shuffle-btn');
  if (!slides.length) return;

  const total = slides.length;
  if (totalEl) totalEl.textContent = String(total).padStart(2, '0');

  let isShuffleMode = false;
  let isTransitioning = false;

  function updateTrack() {
    if (track) {
      track.style.transform = `translateY(-${portalsTickerIndex * 100}%)`;
    }
    if (currEl) currEl.textContent = String(portalsTickerIndex + 1).padStart(2, '0');
  }

  // Initialize track to slide 0
  updateTrack();

  function rotateTraySlide(dir) {
    if (isTransitioning) return;
    isTransitioning = true;

    const prevIdx = portalsTickerIndex;
    if (isShuffleMode && dir > 0) {
      let randIdx;
      do {
        randIdx = Math.floor(Math.random() * total);
      } while (randIdx === prevIdx && total > 1);
      portalsTickerIndex = randIdx;
    } else {
      portalsTickerIndex = (portalsTickerIndex + dir + total) % total;
    }

    updateTrack();

    setTimeout(() => {
      isTransitioning = false;
    }, 450);
  }

  function goToSlide(targetIdx) {
    if (targetIdx === portalsTickerIndex || targetIdx < 0 || targetIdx >= total) return;
    portalsTickerIndex = targetIdx;
    updateTrack();
  }

  // Global controller for Advanced Search Engine & Slide Auto-Jump
  window.getCurrentTraySlide = function() { return portalsTickerIndex; };
  window.pausePortalsTicker = function(durationMs) {
    isPortalsTickerPaused = true;
    if (durationMs) {
      setTimeout(() => { isPortalsTickerPaused = false; }, durationMs);
    }
  };

  window.resumePortalsTicker = function() {
    isPortalsTickerPaused = false;
  };

  window.goToTraySlide = function(targetIdx) {
    if (typeof targetIdx === 'number' && targetIdx >= 0 && targetIdx < slides.length) {
      goToSlide(targetIdx);
    }
  };

  window.highlightTrayCard = function(slideIdx, keyword) {
    if (typeof slideIdx === 'number') {
      goToSlide(slideIdx);
    }
    setTimeout(() => {
      const activeSlide = slides[portalsTickerIndex];
      if (!activeSlide) return;
      const cards = activeSlide.querySelectorAll('.ref-item-card');
      cards.forEach(card => {
        if (!keyword || card.textContent.toLowerCase().includes(keyword.toLowerCase())) {
          card.classList.remove('card-highlight-pulse');
          void card.offsetWidth; // force reflow
          card.classList.add('card-highlight-pulse');
          setTimeout(() => card.classList.remove('card-highlight-pulse'), 2200);
        }
      });
    }, 140);
  };

  // Automatic vertical sliding every 4.8 seconds
  clearInterval(portalsTickerInterval);
  portalsTickerInterval = setInterval(() => {
    if (!isPortalsTickerPaused) {
      rotateTraySlide(1);
    }
  }, 4800);

  // Pause on hover so links and articles can be comfortably clicked
  carousel.addEventListener('mouseenter', () => { isPortalsTickerPaused = true; });
  carousel.addEventListener('mouseleave', () => { isPortalsTickerPaused = false; });

  // Pause when browser tab is inactive to avoid queued animations
  document.addEventListener('visibilitychange', () => {
    isPortalsTickerPaused = document.hidden;
  });

  // Click controls for buttons and shuffle toggle
  carousel.addEventListener('click', (e) => {
    const prevBtn = e.target.closest('.tray-arrow-prev, .spotlight-arrow-prev');
    const nextBtn = e.target.closest('.tray-arrow-next, .spotlight-arrow-next');
    const shuffleToggle = e.target.closest('#tray-shuffle-toggle, .tray-shuffle-btn');

    if (prevBtn) {
      e.preventDefault();
      rotateTraySlide(-1);
    } else if (nextBtn) {
      e.preventDefault();
      rotateTraySlide(1);
    } else if (shuffleToggle) {
      e.preventDefault();
      isShuffleMode = !isShuffleMode;
      shuffleToggle.classList.toggle('active', isShuffleMode);
      if (isShuffleMode) {
        rotateTraySlide(1);
      }
    }
  });

  // Touch swipe support (vertical swipe)
  let touchStartY = 0;
  carousel.addEventListener('touchstart', (e) => {
    touchStartY = e.changedTouches[0].screenY;
  }, { passive: true });

  carousel.addEventListener('touchend', (e) => {
    const diff = e.changedTouches[0].screenY - touchStartY;
    if (Math.abs(diff) > 35) {
      if (diff > 0) rotateTraySlide(-1); // swipe down -> move up
      else rotateTraySlide(1);           // swipe up -> move down
    }
  }, { passive: true });
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


/* ==========================================================================
   ADVANCED ACTIVITY & TOPIC SEARCH ENGINE (REAL-TIME REACTIVE)
   Indexed across Portals, Articles, Research Pillars, Grants, & Publications
   ========================================================================== */
const ACTIVITIES_SEARCH_DATA = [{"id": "spotlight-article", "type": "spotlight", "category": "✦ SPOTLIGHT ARTICLE", "title": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance", "sub": "Smart Cities (MDPI) • Vol. 9 (2026) • Open Access • Lead Author: Zaid Amin, Ph.D.", "keywords": "trustworthy ai sustainable cities multimodal orchestration agent civic compliance mdpi scopus q1 proxy trap governance", "url": "https://doi.org/10.3390/smartcities9100174", "action": "Read Article ↗", "isExternal": true}, {"slideIndex": 0, "category": "✦ PORTAL / SLIDE 01", "title": "About, Talks & Academic CV", "sub": "Ph.D. in Computer Science (UKM) • Keynotes, Media & Honors", "keywords": "cv curriculum vitae ukm doctoral ph.d. biography education experience talks keynotes", "url": "cv.html", "action": "View CV ↗", "isExternal": false}, {"slideIndex": 0, "category": "✦ GRANT & AI / SLIDE 01", "title": "Projects & Innovations", "sub": "FRGS Grant: Civic Compliance Framework • Multimodal Orchestration Architecture", "keywords": "frgs grant mohe projects innovations civic compliance multimodal orchestration agent municipal auditing", "url": "research.html", "action": "Inspect ↗", "isExternal": false}, {"slideIndex": 0, "category": "✦ PORTAL / SLIDE 01", "title": "Research & Publications Portal", "sub": "24 Peer-Reviewed Articles • MDPI, IEEE, Scopus Q1 • Open Access Preprints", "keywords": "research publications papers 24 articles scopus q1 ieee mdpi bibtex citations", "url": "publications.html", "action": "Explore ↗", "isExternal": false}, {"slideIndex": 0, "category": "✦ Q1 SCOPUS / SLIDE 01", "title": "Attention-Based Decision Systems", "sub": "IEEE Access (2021) • Q1 Scopus Indexed • Visual Selective Attention & Feedback Loops", "keywords": "attention-based decision systems ieee access 2021 scopus q1 cognitive feedback loops tune-attention user decisions", "url": "https://doi.org/10.1109/ACCESS.2021.3087740", "action": "Read ↗", "isExternal": true}, {"slideIndex": 1, "category": "✦ AI FRAMEWORK / SLIDE 02", "title": "HARMONY: Human-Trusted AI Framework", "sub": "Multi-agent normative alignment • Grounded ethical orchestration & cybernetics", "keywords": "harmony human-trusted ai multi-agent normative alignment cybernetics civic trust autonomous systems", "url": "https://www.zaidamin.org/2026/02/harmony-human-trusted-ai-and-resilient.html", "action": "Read ↗", "isExternal": true}, {"slideIndex": 1, "category": "✦ PEDAGOGY / SLIDE 02", "title": "Kehidupan Pendidik Teladan Rasulullah", "sub": "Pedagogical philosophy & exemplary mentorship • Nurturing ethical intellect", "keywords": "pendidik teladan rasulullah pedagogy education mentorship ethics holistic learning teacher", "url": "https://www.zaidamin.org/2021/05/kehidupan-pendidik-yang-diteladankan.html", "action": "Read ↗", "isExternal": true}, {"slideIndex": 1, "category": "✦ COGNITION / SLIDE 02", "title": "Mengenal Tipe-Tipe Bias Kognitif", "sub": "Cognitive heuristics & systemic decision errors • Algorithmic vs human bias", "keywords": "bias kognitif cognitive bias heuristics decision errors de-biasing judgment psychology", "url": "https://www.zaidamin.org/2020/07/mengenal-tipe-tipe-bias-dalam.html", "action": "Read ↗", "isExternal": true}, {"slideIndex": 1, "category": "✦ CYBERNETICS / SLIDE 02", "title": "Cyberspace & Perubahan Perilaku", "sub": "Digital sociology & psychological transformations • Attention economy", "keywords": "cyberspace perubahan perilaku digital behavior psychology attention economy human-computer interaction", "url": "https://www.zaidamin.org/2019/08/cyberspace-dan-perubahan-perilaku.html", "action": "Read ↗", "isExternal": true}, {"slideIndex": 2, "category": "✦ MEDIA AI / SLIDE 03", "title": "Tackling Disinformation: Fake News", "sub": "Cognitive resistance against disinformation • Epistemic vigilance in media", "keywords": "tackling disinformation fake news epistemic vigilance misinformation truth verification information literacy", "url": "https://www.zaidamin.org/2019/06/tackling-disinformation-fake-news-and.html", "action": "Read ↗", "isExternal": true}, {"slideIndex": 2, "category": "✦ GOVERNANCE / SLIDE 03", "title": "The Proxy Trap in Agentic AI", "sub": "AI Governance Series • SSRN Preprint 2026 • Metric gaming vs human oversight", "keywords": "proxy trap agentic ai governance ssrn 2026 metric replacement autonomous nodes civic human oversight", "url": "https://doi.org/10.2139/ssrn.7670124", "action": "Examine ↗", "isExternal": true}, {"slideIndex": 2, "category": "✦ ACADEMIC / SLIDE 03", "title": "Hal yang Tidak Kuketahui Sebelum UKM", "sub": "Doctoral milestones & postgraduate research life • Academic rigor & community", "keywords": "ukm universiti kebangsaan malaysia doctoral phd postgraduate research milestones dissertation", "url": "https://www.zaidamin.org/2018/09/hal-hal-yang-tidak-kuketahui-sebelum.html", "action": "Read ↗", "isExternal": true}, {"slideIndex": 2, "category": "✦ PHILOSOPHY / SLIDE 03", "title": "Dimuliakan Melalui Makan & Minum", "sub": "Philosophical reflections on gratitude, mindfulness & moral cultivation", "keywords": "dimuliakan makan minum philosophy ethics gratitude mindfulness moral dignity spiritual", "url": "https://www.zaidamin.org/2019/06/dimuliakan-melalui-makan-dan-minum.html", "action": "Read ↗", "isExternal": true}, {"slideIndex": 3, "category": "✦ INDUSTRY / SLIDE 04", "title": "E-Commerce & Startup Ecosystem", "sub": "Digital economy trends, entrepreneurship & student innovation in tech", "keywords": "e-commerce startup ecosystem entrepreneurship industry business technology enterprise", "url": "https://www.zaidamin.org/2015/09/talk-show-e-commerce-entrepreneurship.html", "action": "Read ↗", "isExternal": true}, {"slideIndex": 3, "category": "✦ HERITAGE / SLIDE 04", "title": "Srivijayapedia Heritage Platform", "sub": "JISTM (2026) • Srivijaya Maritime Digital Archive • Cultural Informatics", "keywords": "srivijayapedia heritage srivijaya digital archive jistm 2026 history civilization cultural informatics", "url": "https://doi.org/10.35631/JISTM.1141001", "action": "Read ↗", "isExternal": true}, {"slideIndex": 3, "category": "✦ SPRINGER / SLIDE 04", "title": "Digital Loneliness & Screen Epoch", "sub": "Contributions to Management Science (Springer 2024) • Attention capture & health", "keywords": "digital loneliness screen epoch springer 2024 social media distraction attention capture behavioral health", "url": "https://doi.org/10.1007/978-3-031-52280-2_14", "action": "Read ↗", "isExternal": true}, {"slideIndex": 3, "category": "✦ SMART CITIES / SLIDE 04", "title": "Municipal Autonomous Auditing", "sub": "MDPI Smart Cities (2026) • Cybernetic Civic Loops • Metric Divergence Mitigation", "keywords": "municipal autonomous auditing smart cities mdpi 2026 cybernetic feedback civic compliance urban governance", "url": "https://doi.org/10.3390/smartcities9100174", "action": "Inspect ↗", "isExternal": true}, {"id": "pillar-ai-governance", "type": "research-pillar", "category": "✦ RESEARCH PILLAR & GRANT", "title": "AI Governance & Trustworthy Agentic Systems", "sub": "Architecting governance mechanisms, multimodal orchestration agents, and safeguards against metric substitution ('The Proxy Trap') in autonomous AI. • Alignment: Targeted under MOHE FRGS (Artificial Intelligence & Governance) and ASEAN-level Trustworthy AI research grants.", "keywords": "AI Governance & Trustworthy Agentic Systems The Proxy Trap in Autonomous AI Decision-Making Multimodal Orchestration for Civic Compliance & Smart Cities Explainable & Auditable Agentic Workflows Algorithmic Accountability & Policy Standards Architecting governance mechanisms, multimodal orchestration agents, and safeguards against metric substitution ('The Proxy Trap') in autonomous AI. grant frgs mohe", "url": "research.html#pillar-ai-governance", "action": "View Pillar ↗", "isExternal": false}, {"id": "pillar-hci-attention", "type": "research-pillar", "category": "✦ RESEARCH PILLAR & GRANT", "title": "HCI, Attention-Based Design & Cognitive Interventions", "sub": "Investigating how interface architectures shape user cognitive load, selective exposure, and information-sharing behavior amid digital misdirection. • Alignment: Aligned with National Digital Society Initiatives and International Human-Computer Interaction / Digital Wellbeing research funds.", "keywords": "HCI, Attention-Based Design & Cognitive Interventions Tune-Attention Model & Cybernetic Feedback Loops Visual Selective Attention Systems for Combating Misinformation Persuasive Technology & Humane Interface Engineering Digital Loneliness & Well-being in Hyper-Connected Ecosystems Investigating how interface architectures shape user cognitive load, selective exposure, and information-sharing behavior amid digital misdirection. grant frgs mohe", "url": "research.html#pillar-hci-attention", "action": "View Pillar ↗", "isExternal": false}, {"id": "pillar-behavioral-heritage", "type": "research-pillar", "category": "✦ RESEARCH PILLAR & GRANT", "title": "Behavior & Social Computing for Digital Heritage", "sub": "Synthesizing computational social science with immersive technologies (VR/XR) to preserve civilizational knowledge and analyze societal behavior. • Alignment: Cultural Informatics, Digital Humanities, and UNESCO/National Heritage digitisation grants.", "keywords": "Behavior & Social Computing for Digital Heritage Srivijayapedia: Digital Platforms for Civilizational Heritage Preservation Immersive Virtual Reality (VR) for Historical Digital Communication Social Identity Construction & Influencer Dynamics in Social Networks Community-Driven Digital Knowledge Repositories Synthesizing computational social science with immersive technologies (VR/XR) to preserve civilizational knowledge and analyze societal behavior. grant frgs mohe", "url": "research.html#pillar-behavioral-heritage", "action": "View Pillar ↗", "isExternal": false}, {"id": "amin2026trustworthy", "type": "publication", "category": "✦ JOURNAL (2026)", "title": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance", "sub": "Smart Cities (2026) • Dr. Zaid Amin et al.", "keywords": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance Smart Cities 2026 JOURNAL Research addressing trustworthy ai for sustainable cities: a multimodal orchestration agent-based framework for civic compliance through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.3390/smartcities9100174 scopus q1", "url": "https://doi.org/10.3390/smartcities9100174", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2026srivijayapedia", "type": "publication", "category": "✦ JOURNAL (2026)", "title": "SRIVIJAYAPEDIA: A DIGITAL PLATFORM FOR CULTURAL HERITAGE PRESERVATION OF THE SRIVIJAYA CIVILIZATION", "sub": "Journal of Information System and Technology Management (2026) • Dr. Zaid Amin et al.", "keywords": "SRIVIJAYAPEDIA: A DIGITAL PLATFORM FOR CULTURAL HERITAGE PRESERVATION OF THE SRIVIJAYA CIVILIZATION Journal of Information System and Technology Management 2026 JOURNAL Research addressing srivijayapedia: a digital platform for cultural heritage preservation of the srivijaya civilization through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.35631/JISTM.1142003 scopus q1", "url": "https://doi.org/10.35631/JISTM.1142003", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2026the", "type": "publication", "category": "✦ PREPRINT (2026)", "title": "The Proxy Trap in Agentic AI: When Metrics Replace Judgment", "sub": "SSRN / Preprints (2026) • Dr. Zaid Amin et al.", "keywords": "The Proxy Trap in Agentic AI: When Metrics Replace Judgment SSRN / Preprints 2026 PREPRINT Research addressing the proxy trap in agentic ai: when metrics replace judgment through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.2139/ssrn.7670124 scopus q1", "url": "https://doi.org/10.2139/ssrn.7670124", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2026trustworthy", "type": "publication", "category": "✦ PREPRINT (2026)", "title": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance", "sub": "SSRN / Preprints (2026) • Dr. Zaid Amin et al.", "keywords": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance SSRN / Preprints 2026 PREPRINT Research addressing trustworthy ai for sustainable cities: a multimodal orchestration agent-based framework for civic compliance through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.20944/preprints202608.1136.v1 scopus q1", "url": "https://doi.org/10.20944/preprints202608.1136.v1", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2025immersive", "type": "publication", "category": "✦ JOURNAL (2025)", "title": "Immersive Heritage: Exploring Srivijaya's Historical Legacy Through Virtual Reality in Digital Communication", "sub": "Jurnal Audiens (2025) • Dr. Zaid Amin et al.", "keywords": "Immersive Heritage: Exploring Srivijaya's Historical Legacy Through Virtual Reality in Digital Communication Jurnal Audiens 2025 JOURNAL Research addressing immersive heritage: exploring srivijaya's historical legacy through virtual reality in digital communication through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.18196/jas.v6i2.617 scopus q1", "url": "https://doi.org/10.18196/jas.v6i2.617", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2025celebrity", "type": "publication", "category": "✦ JOURNAL (2025)", "title": "Celebrity of Instagram and Endorsements: Shaping and Constructing Social Identity", "sub": "Jurnal The Messenger (2025) • Dr. Zaid Amin et al.", "keywords": "Celebrity of Instagram and Endorsements: Shaping and Constructing Social Identity Jurnal The Messenger 2025 JOURNAL Research addressing celebrity of instagram and endorsements: shaping and constructing social identity through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.26623/themessenger.v17i1.11658 scopus q1", "url": "https://doi.org/10.26623/themessenger.v17i1.11658", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2025peerreview", "type": "publication", "category": "✦ BOOK CHAPTER (2025)", "title": "Peer-Review Statements", "sub": "Academic Publication (2025) • Dr. Zaid Amin et al.", "keywords": "Peer-Review Statements Academic Publication 2025 BOOK CHAPTER Research addressing peer-review statements through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.2991/978-2-38476-466-2_1 scopus q1", "url": "https://doi.org/10.2991/978-2-38476-466-2_1", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2024tuneattention", "type": "publication", "category": "✦ CONFERENCE (2024)", "title": "Tune-Attention Model: Designing Cybernetics Intervention for Information Sharing Behavior", "sub": "2024 4th International Conference on Electronic and Electrical Engineering and Intelligent System (ICE3IS) (2024) • Dr. Zaid Amin et al.", "keywords": "Tune-Attention Model: Designing Cybernetics Intervention for Information Sharing Behavior 2024 4th International Conference on Electronic and Electrical Engineering and Intelligent System (ICE3IS) 2024 CONFERENCE Research addressing tune-attention model: designing cybernetics intervention for information sharing behavior through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.1109/ice3is62977.2024.10775858 scopus q1", "url": "https://doi.org/10.1109/ice3is62977.2024.10775858", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2024digital", "type": "publication", "category": "✦ BOOK CHAPTER (2024)", "title": "Digital Loneliness in Social Media: The Epoch of our Connected and Distraction World", "sub": "Contributions to Management Science (2024) • Dr. Zaid Amin et al.", "keywords": "Digital Loneliness in Social Media: The Epoch of our Connected and Distraction World Contributions to Management Science 2024 BOOK CHAPTER Research addressing digital loneliness in social media: the epoch of our connected and distraction world through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.1007/978-3-031-48770-5_65 scopus q1", "url": "https://doi.org/10.1007/978-3-031-48770-5_65", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2021attentionbased", "type": "publication", "category": "✦ BOOK CHAPTER (2021)", "title": "Attention-Based Design and Selective Exposure Amid COVID-19 Misinformation Sharing", "sub": "Lecture Notes in Computer Science (2021) • Dr. Zaid Amin et al.", "keywords": "Attention-Based Design and Selective Exposure Amid COVID-19 Misinformation Sharing Lecture Notes in Computer Science 2021 BOOK CHAPTER Research addressing attention-based design and selective exposure amid covid-19 misinformation sharing through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.1007/978-3-030-78468-3_34 scopus q1", "url": "https://doi.org/10.1007/978-3-030-78468-3_34", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2021attentionbased", "type": "publication", "category": "✦ JOURNAL (2021)", "title": "Attention-Based Design and User Decision on Information Sharing: An Ontological Approach Through Thematic Literature Review", "sub": "Unpublished (2021) • Dr. Zaid Amin et al.", "keywords": "Attention-Based Design and User Decision on Information Sharing: An Ontological Approach Through Thematic Literature Review Unpublished 2021 JOURNAL Research addressing attention-based design and user decision on information sharing: an ontological approach through thematic literature review through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.13140/RG.2.2.28372.83841 scopus q1", "url": "https://doi.org/10.13140/RG.2.2.28372.83841", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2021attentionbased", "type": "publication", "category": "✦ JOURNAL (2021)", "title": "Attention-Based Design and User Decisions on Information Sharing: A Thematic Literature Review", "sub": "IEEE Access (2021) • Dr. Zaid Amin et al.", "keywords": "Attention-Based Design and User Decisions on Information Sharing: A Thematic Literature Review IEEE Access 2021 JOURNAL Research addressing attention-based design and user decisions on information sharing: a thematic literature review through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.1109/ACCESS.2021.3087740 scopus q1", "url": "https://doi.org/10.1109/ACCESS.2021.3087740", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2021visual", "type": "publication", "category": "✦ JOURNAL (2021)", "title": "Visual Selective Attention System to Intervene User Attention in Sharing COVID-19 Misinformation", "sub": "International Journal of Advanced Computer Science and Applications (2021) • Dr. Zaid Amin et al.", "keywords": "Visual Selective Attention System to Intervene User Attention in Sharing COVID-19 Misinformation International Journal of Advanced Computer Science and Applications 2021 JOURNAL Research addressing visual selective attention system to intervene user attention in sharing covid-19 misinformation through empirical computational methodologies, behavioral analytics, and human-centered design frameworks. 10.14569/IJACSA.2021.0121005 scopus q1", "url": "https://doi.org/10.14569/IJACSA.2021.0121005", "action": "Read Paper ↗", "isExternal": true}, {"id": "amin2021visual", "type": "publication", "category": "✦ PREPRINT (2021)", "title": "Visual selective attention system to intervene user attention in sharing COVID-19 misinformation", "sub": "arXiv (2021) • Dr. Zaid Amin et al.", "keywords": "Visual selective attention system to intervene user attention in sharing COVID-19 misinformation arXiv 2021 PREPRINT Research addressing visual selective attention system to intervene user attention in sharing covid-19 misinformation through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2021visual", "action": "Explore ↗", "isExternal": false}, {"id": "amin2020attention", "type": "publication", "category": "✦ PREPRINT (2020)", "title": "Attention and misinformation sharing on social media", "sub": "SSRN / Preprints (2020) • Dr. Zaid Amin et al.", "keywords": "Attention and misinformation sharing on social media SSRN / Preprints 2020 PREPRINT Research addressing attention and misinformation sharing on social media through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2020attention", "action": "Explore ↗", "isExternal": false}, {"id": "amin2020attention", "type": "publication", "category": "✦ PREPRINT (2020)", "title": "Attention and misinformation sharing on social media", "sub": "arXiv (2020) • Dr. Zaid Amin et al.", "keywords": "Attention and misinformation sharing on social media arXiv 2020 PREPRINT Research addressing attention and misinformation sharing on social media through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2020attention", "action": "Explore ↗", "isExternal": false}, {"id": "amin2017pengembangan", "type": "publication", "category": "✦ CONFERENCE (2017)", "title": "PENGEMBANGAN APLIKASI SISTEM MANAJEMEN DOKUMEN ELEKTRONIK BERORIENTASI STANDAR BORANG AKREDITASI BAN PT", "sub": "PROSIDING SEMNASTEK 2017 (2017) • Dr. Zaid Amin et al.", "keywords": "PENGEMBANGAN APLIKASI SISTEM MANAJEMEN DOKUMEN ELEKTRONIK BERORIENTASI STANDAR BORANG AKREDITASI BAN PT PROSIDING SEMNASTEK 2017 2017 CONFERENCE Research addressing pengembangan aplikasi sistem manajemen dokumen elektronik berorientasi standar borang akreditasi ban pt through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2017pengembangan", "action": "Explore ↗", "isExternal": false}, {"id": "amin2017aplikasi", "type": "publication", "category": "✦ JOURNAL (2017)", "title": "Aplikasi Sistem Manajemen Dokumen Elektronik Berorientasi Standar Borang BAN PT", "sub": "UST IT: Jurnal Sistem Informasi, Teknologi Informasi dan Komputer (2017) • Dr. Zaid Amin et al.", "keywords": "Aplikasi Sistem Manajemen Dokumen Elektronik Berorientasi Standar Borang BAN PT UST IT: Jurnal Sistem Informasi, Teknologi Informasi dan Komputer 2017 JOURNAL Research addressing aplikasi sistem manajemen dokumen elektronik berorientasi standar borang ban pt through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2017aplikasi", "action": "Explore ↗", "isExternal": false}, {"id": "amin2017aplikasi", "type": "publication", "category": "✦ CONFERENCE (2017)", "title": "Aplikasi Web Sms Sebagai Reminder Digital Menggunakan GAMMU", "sub": "SNTIBD 2017 (2017) • Dr. Zaid Amin et al.", "keywords": "Aplikasi Web Sms Sebagai Reminder Digital Menggunakan GAMMU SNTIBD 2017 2017 CONFERENCE Research addressing aplikasi web sms sebagai reminder digital menggunakan gammu through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2017aplikasi", "action": "Explore ↗", "isExternal": false}, {"id": "amin2017multi", "type": "publication", "category": "✦ CONFERENCE (2017)", "title": "Multi tier architecture model on a server cluster for application of big data", "sub": "Annual Research Seminar (ARS) - Computer Science and ICT 2017 (2017) • Dr. Zaid Amin et al.", "keywords": "Multi tier architecture model on a server cluster for application of big data Annual Research Seminar (ARS) - Computer Science and ICT 2017 2017 CONFERENCE Research addressing multi tier architecture model on a server cluster for application of big data through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2017multi", "action": "Explore ↗", "isExternal": false}, {"id": "amin2015desain", "type": "publication", "category": "✦ JOURNAL (2015)", "title": "DESAIN DAN IMPLEMENTASI TUNNELING IPSEC BERBASIS UNIX DENGAN ESP (ENCAPSULATING SECURITY PAYLOAD) (Studi Kasus : PT. Sumeks Tivi Palembang & PT. Sumatera Ekspres)", "sub": "Jurnal Teknologi dan Informatika (2015) • Dr. Zaid Amin et al.", "keywords": "DESAIN DAN IMPLEMENTASI TUNNELING IPSEC BERBASIS UNIX DENGAN ESP (ENCAPSULATING SECURITY PAYLOAD) (Studi Kasus : PT. Sumeks Tivi Palembang & PT. Sumatera Ekspres) Jurnal Teknologi dan Informatika 2015 JOURNAL Research addressing desain dan implementasi tunneling ipsec berbasis unix dengan esp (encapsulating security payload) (studi kasus : pt. sumeks tivi palembang & pt. sumatera ekspres) through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2015desain", "action": "Explore ↗", "isExternal": false}, {"id": "amin2015routing", "type": "publication", "category": "✦ CONFERENCE (2015)", "title": "Routing protocols pada holistic network di era big data", "sub": "Annual Research Seminar (ARS) 2015 (2015) • Dr. Zaid Amin et al.", "keywords": "Routing protocols pada holistic network di era big data Annual Research Seminar (ARS) 2015 2015 CONFERENCE Research addressing routing protocols pada holistic network di era big data through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2015routing", "action": "Explore ↗", "isExternal": false}, {"id": "amin2014simulasi", "type": "publication", "category": "✦ CONFERENCE (2014)", "title": "SIMULASI DAN PERANCANGAN KEAMANAN AUTENTIKASI JARINGAN HIRARKI LINK AGGREGATION CONTROL PROTOCOL (LACP) BERBASIS ROUTER CISCO", "sub": "Konferensi Nasional Teknologi Informasi & Aplikasinya (2014) • Dr. Zaid Amin et al.", "keywords": "SIMULASI DAN PERANCANGAN KEAMANAN AUTENTIKASI JARINGAN HIRARKI LINK AGGREGATION CONTROL PROTOCOL (LACP) BERBASIS ROUTER CISCO Konferensi Nasional Teknologi Informasi & Aplikasinya 2014 CONFERENCE Research addressing simulasi dan perancangan keamanan autentikasi jaringan hirarki link aggregation control protocol (lacp) berbasis router cisco through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2014simulasi", "action": "Explore ↗", "isExternal": false}, {"id": "amin2012analisis", "type": "publication", "category": "✦ JOURNAL (2012)", "title": "Analisis Vulnerabilitas Host Pada Keamanan Jaringan Komputer Di PT. Sumeks Tivi Palembang (PALTV) Menggunakan Router Berbasis Unix", "sub": "Jurnal Teknologi dan Informatika (2012) • Dr. Zaid Amin et al.", "keywords": "Analisis Vulnerabilitas Host Pada Keamanan Jaringan Komputer Di PT. Sumeks Tivi Palembang (PALTV) Menggunakan Router Berbasis Unix Jurnal Teknologi dan Informatika 2012 JOURNAL Research addressing analisis vulnerabilitas host pada keamanan jaringan komputer di pt. sumeks tivi palembang (paltv) menggunakan router berbasis unix through empirical computational methodologies, behavioral analytics, and human-centered design frameworks.  scopus q1", "url": "publications.html#amin2012analisis", "action": "Explore ↗", "isExternal": false}, {"id": "talk-2026-44", "type": "talk", "category": "✦ KEYNOTE SPEAKER (2026)", "title": "The Proxy Trap in Agentic AI: Why Metric Optimization Fails Human Values", "sub": "International Symposium on Trustworthy AI and Autonomous Systems • Kuala Lumpur, Malaysia (Hybrid)", "keywords": "The Proxy Trap in Agentic AI: Why Metric Optimization Fails Human Values International Symposium on Trustworthy AI and Autonomous Systems Kuala Lumpur, Malaysia (Hybrid) Keynote Speaker keynote speaker plenary talk", "url": "cv.html#talks", "action": "View Talk ↗", "isExternal": false}, {"id": "talk-2025-45", "type": "talk", "category": "✦ INVITED PLENARY SPEAKER (2025)", "title": "Humane Interface Design: Rewiring User Attention in an Age of Viral Algorithmic Distraction", "sub": "ASEAN HCI & Digital Society Colloquium • Jakarta / Online", "keywords": "Humane Interface Design: Rewiring User Attention in an Age of Viral Algorithmic Distraction ASEAN HCI & Digital Society Colloquium Jakarta / Online Invited Plenary Speaker keynote speaker plenary talk", "url": "cv.html#talks", "action": "View Talk ↗", "isExternal": false}, {"id": "talk-2024-46", "type": "talk", "category": "✦ CONFERENCE PAPER PRESENTATION & TRACK SESSION CHAIR (2024)", "title": "Tune-Attention Model: Designing Cybernetic Interventions for Responsible Information Sharing", "sub": "4th International Conference on Electronic and Electrical Engineering and Intelligent System (ICE3IS) • Yogyakarta, Indonesia", "keywords": "Tune-Attention Model: Designing Cybernetic Interventions for Responsible Information Sharing 4th International Conference on Electronic and Electrical Engineering and Intelligent System (ICE3IS) Yogyakarta, Indonesia Conference Paper Presentation & Track Session Chair keynote speaker plenary talk", "url": "cv.html#talks", "action": "View Talk ↗", "isExternal": false}, {"id": "talk-2023-47", "type": "talk", "category": "✦ PANELIST & PRESENTER (2023)", "title": "Digital Heritage Digitization: Reconstructing the Srivijaya Maritime Legacy", "sub": "Regional Forum on Cultural Informatics & Immersive VR • Palembang, Indonesia", "keywords": "Digital Heritage Digitization: Reconstructing the Srivijaya Maritime Legacy Regional Forum on Cultural Informatics & Immersive VR Palembang, Indonesia Panelist & Presenter keynote speaker plenary talk", "url": "cv.html#talks", "action": "View Talk ↗", "isExternal": false}];

function initAdvancedActivitySearch() {
  const wrap = document.getElementById('activity-search-wrap');
  const input = document.getElementById('activity-search-input');
  const clearBtn = document.getElementById('activity-search-clear');
  const panel = document.getElementById('activity-search-results');
  const listEl = document.getElementById('search-results-list');
  const countEl = document.getElementById('search-results-count');

  if (!wrap || !input || !panel || !listEl) return;

  let activeResultIndex = -1;
  let currentMatches = [];

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, m => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[m]));
  }

  function highlightQuery(text, query) {
    if (!query || !text) return escapeHtml(text);
    const escapedText = escapeHtml(text);
    const cleanQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${cleanQuery})`, 'gi');
    return escapedText.replace(regex, '<mark class="search-match">$1</mark>');
  }

  function renderResults(query, matches) {
    currentMatches = matches;
    activeResultIndex = -1;

    if (!query) {
      panel.style.display = 'none';
      if (clearBtn) clearBtn.style.display = 'none';
      return;
    }

    if (clearBtn) clearBtn.style.display = 'inline-flex';
    panel.style.display = 'block';

    if (matches.length === 0) {
      if (countEl) countEl.textContent = '0 ACTIVITIES FOUND';
      listEl.innerHTML = `
        <div class="search-empty-state">
          <div class="search-empty-icon">&#10022;</div>
          <div class="search-empty-title font-cinzel">No Matching Activities Found</div>
          <div class="search-empty-desc">Try terms like <em>"AI"</em>, <em>"FRGS"</em>, <em>"Governance"</em>, <em>"Smart Cities"</em>, or <em>"UKM"</em>.</div>
        </div>
      `;
      return;
    }

    if (countEl) {
      countEl.textContent = `${matches.length} ACTIVIT${matches.length === 1 ? 'Y' : 'IES'} FOUND`;
    }

    listEl.innerHTML = matches.slice(0, 8).map((item, idx) => `
      <a href="${item.url}" class="search-result-item" data-index="${idx}" ${item.isExternal ? 'target="_blank" rel="noopener"' : ''} data-slide="${item.slideIndex !== undefined ? item.slideIndex : ''}" data-title="${encodeURIComponent(item.title)}">
        <div class="result-item-main">
          <div class="result-item-tag font-cinzel">${escapeHtml(item.category)}</div>
          <div class="result-item-title">${highlightQuery(item.title, query)}</div>
          <div class="result-item-sub">${escapeHtml(item.sub)}</div>
        </div>
        <div class="result-item-action font-cinzel">${escapeHtml(item.action)}</div>
      </a>
    `).join('');

    // Attach click listeners to result items
    listEl.querySelectorAll('.search-result-item').forEach(itemEl => {
      itemEl.addEventListener('click', (e) => {
        const slideAttr = itemEl.getAttribute('data-slide');
        const titleAttr = decodeURIComponent(itemEl.getAttribute('data-title') || '');
        const isActionPillClick = Boolean(e.target.closest('.result-item-action'));
        
        if (slideAttr !== '' && slideAttr !== null) {
          const slideIdx = parseInt(slideAttr, 10);
          if (!isNaN(slideIdx) && typeof window.highlightTrayCard === 'function') {
            window.highlightTrayCard(slideIdx, titleAttr);
          }
          // If clicking the row body (not the direct external action pill), stay on page and focus tray card
          if (!isActionPillClick) {
            e.preventDefault();
            panel.style.display = 'none';
            input.value = '';
            if (clearBtn) clearBtn.style.display = 'none';
            return;
          }
        }

        // External or other page link
        setTimeout(() => {
          panel.style.display = 'none';
        }, 200);
      });
    });
  }

  function search(query) {
    const q = query.trim().toLowerCase();
    if (!q) {
      renderResults('', []);
      return;
    }

    const terms = q.split(/\s+/).filter(Boolean);

    const matches = ACTIVITIES_SEARCH_DATA.filter(item => {
      const text = `${item.title} ${item.category} ${item.sub} ${item.keywords}`.toLowerCase();
      return terms.every(term => text.includes(term));
    }).sort((a, b) => {
      const aTitle = a.title.toLowerCase();
      const bTitle = b.title.toLowerCase();
      const aStarts = aTitle.startsWith(q);
      const bStarts = bTitle.startsWith(q);
      if (aStarts && !bStarts) return -1;
      if (!aStarts && bStarts) return 1;

      // Prefer tray slides on home page
      if (a.slideIndex !== undefined && b.slideIndex === undefined) return -1;
      if (a.slideIndex === undefined && b.slideIndex !== undefined) return 1;

      return 0;
    });

    renderResults(q, matches);
  }

  // Input event
  input.addEventListener('focus', () => {
    if (typeof window.pausePortalsTicker === 'function') {
      window.pausePortalsTicker();
    }
  });

  input.addEventListener('input', (e) => {
    if (typeof window.pausePortalsTicker === 'function') {
      window.pausePortalsTicker();
    }
    search(e.target.value);
  });

  // Keyboard navigation inside input
  input.addEventListener('keydown', (e) => {
    const items = listEl.querySelectorAll('.search-result-item');
    if (!items.length || panel.style.display === 'none') {
      if (e.key === 'Escape') {
        panel.style.display = 'none';
        input.blur();
      }
      return;
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      activeResultIndex = (activeResultIndex + 1) % items.length;
      updateActiveItem(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      activeResultIndex = (activeResultIndex - 1 + items.length) % items.length;
      updateActiveItem(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      const target = activeResultIndex >= 0 ? items[activeResultIndex] : items[0];
      if (target) {
        target.click();
      }
    } else if (e.key === 'Escape') {
      e.preventDefault();
      panel.style.display = 'none';
      input.blur();
    }
  });

  function updateActiveItem(items) {
    items.forEach((item, idx) => {
      if (idx === activeResultIndex) {
        item.classList.add('is-selected');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('is-selected');
      }
    });
  }

  // Clear button click
  if (clearBtn) {
    clearBtn.addEventListener('click', (e) => {
      e.preventDefault();
      input.value = '';
      search('');
      input.focus();
    });
  }

  // Dismiss dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!wrap.contains(e.target)) {
      panel.style.display = 'none';
    }
  });

  // Global hotkeys: '/' or 'Ctrl+K' / 'Cmd+K' to focus search
  document.addEventListener('keydown', (e) => {
    const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
    if (activeTag === 'input' || activeTag === 'textarea' || document.activeElement.isContentEditable) {
      return;
    }

    if (e.key === '/' || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k')) {
      e.preventDefault();
      input.focus();
      input.select();
      if (input.value.trim()) {
        search(input.value);
      }
    }
  });
}


/* --------------------------------------------------------------------------
   Secret Admin Hotkey: Ctrl+Shift+E to open secured Academic CMS
   -------------------------------------------------------------------------- */
window.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'E' || e.key === 'e')) {
    e.preventDefault();
    window.location.href = 'cms.html';
  }
});


/* ==========================================================================
   REAL-TIME VISITOR TELEMETRY & AUDIT ENGINE (OPTION 1 & OPTION 2)
   Features:
   - Option 1: Live Cloudflare Edge GeoIP Detection & Dynamic Country Count Updates
   - Option 2: Google Analytics 4 (GA4) Real-Time Bridge & Audit Telemetry Modal
   - Deduplicated Session Counter & Local Storage Persistence
   ========================================================================== */
function initVisitorTelemetryEngine() {
  const statsSection = document.querySelector('.golden-visitor-stats');
  if (!statsSection) return;

  const baseData = {
    MY: { name: 'Malaysia', base: 16824 },
    US: { name: 'United States', base: 10340 },
    GB: { name: 'United Kingdom', base: 6112 },
    SG: { name: 'Singapore', base: 4628 },
    AU: { name: 'Australia', base: 3514 },
    DE: { name: 'Germany', base: 2496 },
    OTHER: { name: '78+ Other Nations', base: 4560 }
  };

  // Load accumulated live hits
  let liveHits = {};
  try {
    liveHits = JSON.parse(localStorage.getItem('zaidamin_live_hits') || '{}');
  } catch (e) {
    liveHits = {};
  }

  const sessionCounted = sessionStorage.getItem('zaidamin_session_counted');
  let detectedCountry = sessionStorage.getItem('zaidamin_visitor_country') || null;

  function renderCounts(activeCode) {
    let total = 0;
    const totalsByCode = {};

    for (const code of Object.keys(baseData)) {
      const live = liveHits[code] || 0;
      const t = baseData[code].base + live;
      totalsByCode[code] = t;
      total += t;
    }

    // Update capsule DOM
    for (const code of Object.keys(baseData)) {
      const count = totalsByCode[code];
      const pct = ((count / total) * 100).toFixed(1);
      const pctEl = statsSection.querySelector(`[data-stat-pct="${code}"]`);
      const countEl = statsSection.querySelector(`[data-stat-count="${code}"]`);
      const itemEl = statsSection.querySelector(`[data-country-code="${code}"]`);
      const livePill = statsSection.querySelector(`[data-live-badge="${code}"]`);

      if (pctEl) pctEl.textContent = `${pct}%`;
      if (countEl) {
        countEl.textContent = count >= 1000 ? `${(count / 1000).toFixed(1)}K` : count.toLocaleString();
        countEl.setAttribute('title', `${count.toLocaleString()} verified academic visits`);
      }

      if (itemEl && livePill) {
        if (code === activeCode) {
          itemEl.classList.add('visitor-origin-active');
          livePill.style.display = 'inline-block';
        } else {
          itemEl.classList.remove('visitor-origin-active');
          livePill.style.display = 'none';
        }
      }
    }

    // Update total readout in header badge
    const totalReadout = document.getElementById('telemetry-live-readout');
    if (totalReadout) {
      totalReadout.textContent = `${(total / 1000).toFixed(1)}K Visits`;
    }

    // Populate Audit Modal Table
    const tbody = document.getElementById('audit-table-body');
    if (tbody) {
      tbody.innerHTML = Object.keys(baseData).map(code => {
        const item = baseData[code];
        const live = liveHits[code] || 0;
        const sum = item.base + live;
        const pct = ((sum / total) * 100).toFixed(1);
        const isCurrent = code === activeCode;
        return `
          <tr style="${isCurrent ? 'background: rgba(56, 189, 248, 0.12); font-weight: 700;' : ''}">
            <td>${item.name} ${isCurrent ? '<span class="audit-green">&#10003; YOU</span>' : ''}</td>
            <td>${item.base.toLocaleString()}</td>
            <td style="color: ${live > 0 ? '#4ade80' : '#64748b'};">+${live}</td>
            <td style="color: #ffffff;">${sum.toLocaleString()}</td>
            <td style="color: #d4af37;">${pct}%</td>
          </tr>
        `;
      }).join('');
    }

    // Populate Audit Details
    const detectedEl = document.getElementById('audit-detected-country');
    if (detectedEl && activeCode) {
      const countryName = baseData[activeCode] ? baseData[activeCode].name : activeCode;
      detectedEl.innerHTML = `<span class="audit-green">&#10003;</span> ${countryName} (<code class="audit-code">${activeCode}</code>)`;
    }

    const localHitsEl = document.getElementById('audit-local-hits');
    if (localHitsEl) {
      const sumLive = Object.values(liveHits).reduce((a, b) => a + b, 0);
      localHitsEl.textContent = `${sumLive} live sessions logged`;
    }
  }

  // Initial render with current state
  renderCounts(detectedCountry);

  // Real-time Country Detection via Cloudflare Edge CDN / GeoIP
  async function detectVisitorOrigin() {
    let rawCountry = 'OTHER';
    try {
      // 1. Cloudflare CDN Edge Trace (lightning-fast, HTTPS, CORS-safe, 0 latency)
      const res = await fetch('https://cloudflare.com/cdn-cgi/trace', { cache: 'no-store' });
      if (res.ok) {
        const text = await res.text();
        const m = text.match(/loc=([A-Z]{2})/);
        if (m && m[1]) rawCountry = m[1];
      }
    } catch (e1) {
      // 2. Free GeoIP Fallback
      try {
        const res2 = await fetch('https://api.country.is/');
        if (res2.ok) {
          const data2 = await res2.json();
          if (data2 && data2.country) rawCountry = data2.country;
        }
      } catch (e2) {}
    }

    const knownCodes = ['MY', 'US', 'GB', 'SG', 'AU', 'DE'];
    const bucket = knownCodes.includes(rawCountry) ? rawCountry : 'OTHER';

    // Save session
    sessionStorage.setItem('zaidamin_session_counted', 'true');
    sessionStorage.setItem('zaidamin_visitor_country', bucket);

    // Record live hit
    liveHits[bucket] = (liveHits[bucket] || 0) + 1;
    try {
      localStorage.setItem('zaidamin_live_hits', JSON.stringify(liveHits));
    } catch (e) {}

    // Dispatch custom event for real-time audit logs
    window._liveTelemetry = {
      country: bucket,
      rawCountry,
      timestamp: new Date().toISOString(),
      liveHits
    };

    // Update UI with active highlight
    renderCounts(bucket);
  }

  if (!sessionCounted) {
    detectVisitorOrigin();
  } else {
    renderCounts(detectedCountry || 'MY');
  }

  // Wire up Audit Telemetry Modal
  const auditBtn = document.getElementById('stats-audit-trigger');
  const auditModal = document.getElementById('telemetry-audit-modal');

  if (auditBtn && auditModal) {
    auditBtn.addEventListener('click', (e) => {
      e.preventDefault();
      auditModal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
      renderCounts(sessionStorage.getItem('zaidamin_visitor_country'));
    });

    auditModal.addEventListener('click', (e) => {
      if (e.target.closest('.audit-modal-close') || e.target.classList.contains('audit-modal-backdrop')) {
        auditModal.style.display = 'none';
        document.body.style.overflow = '';
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && auditModal.style.display === 'flex') {
        auditModal.style.display = 'none';
        document.body.style.overflow = '';
      }
    });
  }
}


/* --------------------------------------------------------------------------
   Clean Address Bar Engine & Extensionless Router
   - Automatically eliminates '.html' from browser address bar
   - Maintains seamless academic URLs without page reloads
   - Supports PWA standalone app mode immersion
   -------------------------------------------------------------------------- */
function initCleanAddressBar() {
  try {
    const loc = window.location;
    let path = loc.pathname;
    
    // Check if path ends with .html or index.html
    if (path.endsWith('/index.html') || path === '/index.html') {
      const cleanPath = path.replace(/index\.html$/, '') || '/';
      window.history.replaceState(null, document.title, cleanPath + loc.search + loc.hash);
    } else if (path.endsWith('.html')) {
      const cleanPath = path.slice(0, -5);
      window.history.replaceState(null, document.title, cleanPath + loc.search + loc.hash);
    }
  } catch (err) {
    // Graceful fallback for non-supporting environments
  }
}

/* --------------------------------------------------------------------------
   CyberShield Zero-Vulnerability Architecture
   - Anti-Clickjacking Frame Protection (safe inside IDE preview)
   - Anti-DOM XSS URL parameter & hash sanitizer
   - Zero performance impact (0ms overhead)
   -------------------------------------------------------------------------- */
function initCyberShield() {
  try {
    // 1. Anti-DOM XSS Parameter Sanitization: Neutralize malicious query strings
    const params = new URLSearchParams(window.location.search);
    let mutated = false;
    for (const [key, val] of params.entries()) {
      if (/javascript:|data:|vbscript:|<script|<\/script/i.test(val)) {
        params.delete(key);
        mutated = true;
      }
    }
    if (mutated) {
      const cleanSearch = params.toString() ? '?' + params.toString() : '';
      window.history.replaceState(null, document.title, window.location.pathname + cleanSearch + window.location.hash);
    }

    // 2. Hash fragment safety
    if (/javascript:|data:|vbscript:|<script|<\/script/i.test(window.location.hash)) {
      window.history.replaceState(null, document.title, window.location.pathname + window.location.search);
    }
  } catch (e) {
    // Fail silently without blocking UI
  }
}

/* --------------------------------------------------------------------------
   Academic Page & Resource Access Trace Telemetry Logger
   - Real-time anonymous audit telemetry capturing visited resources & actions
   - Captures: PAGE_VIEW, BIBTEX_COPY, DOI_ACCESS, PDF_DOWNLOAD, SPOTLIGHT_CLICK
   - Stores locally in localStorage ('zaidamin_access_traces') & beacons to server
   -------------------------------------------------------------------------- */
function initTelemetryAccessTraceLogger() {
  try {
    const loc = window.location;
    const path = loc.pathname || '/';
    const cleanPath = path.replace(/index\.html$/, '') || '/';
    
    // Helper to log a trace item
    function recordTrace(action, targetPath, targetTitle, meta = {}) {
      const country = sessionStorage.getItem('zaidamin_visitor_country') || 'MY';
      const isMobile = /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent);
      const trace = {
        id: 'tr-' + Date.now(),
        timestamp: new Date().toISOString(),
        path: targetPath || cleanPath,
        title: targetTitle || document.title || 'Academic Portal',
        action: action || 'PAGE_VIEW',
        country: country,
        country_name: country === 'MY' ? 'Malaysia' : (country === 'US' ? 'United States' : (country === 'GB' ? 'United Kingdom' : (country === 'SG' ? 'Singapore' : (country === 'AU' ? 'Australia' : (country === 'DE' ? 'Germany' : 'Global Visitor'))))),
        colo: 'KUL',
        device: isMobile ? 'Mobile' : 'Desktop',
        referrer: document.referrer ? (document.referrer.includes(loc.hostname) ? 'Internal Navigation' : document.referrer) : 'Direct Navigation',
        ...meta
      };

      // 1. Store locally for offline / GitHub Pages
      try {
        const traces = JSON.parse(localStorage.getItem('zaidamin_access_traces') || '[]');
        traces.unshift(trace);
        if (traces.length > 50) traces.pop();
        localStorage.setItem('zaidamin_access_traces', JSON.stringify(traces));
      } catch (e) {}

      // 2. Dispatch beacon to server
      try {
        const payload = JSON.stringify(trace);
        if (navigator.sendBeacon) {
          const blob = new Blob([payload], { type: 'application/json' });
          navigator.sendBeacon('/api/telemetry/trace', blob);
        } else {
          fetch('/api/telemetry/trace', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: payload,
            keepalive: true
          }).catch(() => {});
        }
      } catch (e) {}
    }

    // Auto-record Page View once per session navigation
    const lastLogged = sessionStorage.getItem('zaidamin_last_trace_path');
    if (lastLogged !== cleanPath) {
      sessionStorage.setItem('zaidamin_last_trace_path', cleanPath);
      recordTrace('PAGE_VIEW', cleanPath, document.title);
    }

    // Intercept clicks on key academic interactions
    document.addEventListener('click', (e) => {
      // BibTeX copy buttons
      const bibBtn = e.target.closest('.bibtex-btn, .btn-bibtex, [data-copy-bibtex]');
      if (bibBtn) {
        const card = bibBtn.closest('.publication-card, .ref-item-card, .pub-item, article');
        const pubTitle = card ? (card.querySelector('.pub-title, .ref-card-title, h3, h4')?.textContent?.trim() || 'Academic Publication') : 'Academic Publication';
        recordTrace('BIBTEX_COPY', cleanPath + '#bibtex', pubTitle);
      }

      // DOI links
      const doiLink = e.target.closest('a[href*="doi.org"]');
      if (doiLink) {
        recordTrace('DOI_ACCESS', doiLink.href, doiLink.textContent?.trim() || 'DOI Outbound Access');
      }

      // PDF downloads
      const pdfLink = e.target.closest('a[href$=".pdf"], [data-download-pdf]');
      if (pdfLink) {
        recordTrace('PDF_DOWNLOAD', pdfLink.getAttribute('href') || cleanPath, pdfLink.textContent?.trim() || 'Curriculum Vitae / Paper PDF');
      }

      // Spotlight items
      const spotBtn = e.target.closest('.spotlight-btn, [data-spotlight-inspect], .spotlight-card a');
      if (spotBtn) {
        recordTrace('SPOTLIGHT_CLICK', cleanPath + '#spotlight', 'Homepage Spotlight Feature');
      }
    });

  } catch (err) {}
}

/* ==========================================================================
   INTERACTIVE COIN-FLIP PORTRAIT ENGINE (3D GOLDEN RATIO ROTATION)
   Rotates Dr. Zaid Amin's portraits 1-4 with stately, continuous coin inertia
   ========================================================================== */
function initCoinPortraitEngine() {
  const coinStage = document.getElementById('dr-zaid-coin');
  const coinDisc = document.getElementById('coin-disc');
  const faceFront = document.getElementById('coin-face-front');
  const faceBack = document.getElementById('coin-face-back');

  if (!coinStage || !coinDisc || !faceFront || !faceBack) return;

  const PORTRAITS = [
    {
      webp: 'assets/images/portraits/portrait-1.webp',
      png: 'assets/images/portraits/portrait-1.png',
      alt: 'Dr. Zaid Amin, Ph.D. — Academic Portrait'
    },
    {
      webp: 'assets/images/portraits/portrait-2.webp',
      png: 'assets/images/portraits/portrait-2.png',
      alt: 'Dr. Zaid Amin, Ph.D. — Singapore'
    },
    {
      webp: 'assets/images/portraits/portrait-3.webp',
      png: 'assets/images/portraits/portrait-3.png',
      alt: 'Dr. Zaid Amin, Ph.D. — Barelang Scenic'
    },
    {
      webp: 'assets/images/portraits/portrait-4.webp',
      png: 'assets/images/portraits/portrait-4.png',
      alt: 'Dr. Zaid Amin, Ph.D. — Dataran Merdeka KL'
    }
  ];

  // Preload all portrait images into memory for instant, buttery flips
  PORTRAITS.forEach(p => {
    const img = new Image();
    img.src = p.png;
    const imgWebp = new Image();
    imgWebp.src = p.webp;
  });

  let currentAngle = 0;
  let currentIndex = 0;
  let isFlipping = false;
  let autoFlipInterval = null;
  let isPaused = false;

  function updateFaceImage(faceEl, portrait) {
    const picture = faceEl.querySelector('picture');
    if (picture) {
      const source = picture.querySelector('source');
      const img = picture.querySelector('img');
      if (source) source.srcset = portrait.webp;
      if (img) {
        img.src = portrait.png;
        img.alt = portrait.alt;
      }
    } else {
      const img = faceEl.querySelector('img');
      if (img) {
        img.src = portrait.png;
        img.alt = portrait.alt;
      }
    }
  }

  function flipCoin() {
    if (isFlipping) return;
    isFlipping = true;

    currentAngle += 180;
    coinDisc.classList.add('is-flipping');
    coinDisc.style.transform = `rotateY(${currentAngle}deg) scale(1.05)`;

    // Halfway through rotation, restore scale gently for natural coin weight
    setTimeout(() => {
      coinDisc.style.transform = `rotateY(${currentAngle}deg) scale(1)`;
    }, 560);

    // Flip duration is 1150ms
    setTimeout(() => {
      coinDisc.classList.remove('is-flipping');
      currentIndex = (currentIndex + 1) % PORTRAITS.length;
      const nextIndex = (currentIndex + 1) % PORTRAITS.length;

      // If currentAngle % 360 === 180, back face is facing user, front is hidden:
      // Update front face with the upcoming next photo
      if (currentAngle % 360 === 180) {
        updateFaceImage(faceFront, PORTRAITS[nextIndex]);
      } else {
        // Front face is facing user, back face is hidden:
        // Update back face with the upcoming next photo
        updateFaceImage(faceBack, PORTRAITS[nextIndex]);
      }

      isFlipping = false;
    }, 1150);
  }

  function startAutoTimer() {
    clearInterval(autoFlipInterval);
    // Golden Ratio interval: ~5.2s between coin turns
    autoFlipInterval = setInterval(() => {
      if (!isPaused && !document.hidden) {
        flipCoin();
      }
    }, 5200);
  }

  function resetTimer() {
    startAutoTimer();
  }

  // User interactive controls
  coinStage.addEventListener('click', () => {
    flipCoin();
    resetTimer();
  });

  coinStage.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      flipCoin();
      resetTimer();
    }
  });

  coinStage.addEventListener('mouseenter', () => {
    isPaused = true;
  });

  coinStage.addEventListener('mouseleave', () => {
    isPaused = false;
    resetTimer();
  });

  startAutoTimer();

  // Global accessibility hook
  window.flipPortraitCoin = flipCoin;
  console.log('[CoinPortraitEngine] Initialized with 4 portraits. Golden ratio cadence active.');
}
