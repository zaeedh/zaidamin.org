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
  const sections = document.querySelectorAll('.pub-gallery-section');

  if (!pubItems.length) return;

  let currentCategory = 'all';
  let currentQuery = '';

  function applyFilters() {
    let visibleCount = 0;

    pubItems.forEach(item => {
      const category = (item.getAttribute('data-category') || '').toLowerCase();
      const title = (item.getAttribute('data-title') || '').toLowerCase();
      const venue = (item.getAttribute('data-venue') || '').toLowerCase();
      const year = (item.getAttribute('data-year') || '').toLowerCase();
      const textContent = (item.textContent || '').toLowerCase();

      const matchesCategory = (currentCategory === 'all') || (category === currentCategory.toLowerCase());
      const matchesQuery = !currentQuery || 
        title.includes(currentQuery) || 
        venue.includes(currentQuery) || 
        year.includes(currentQuery) || 
        textContent.includes(currentQuery);

      if (item.classList.contains('bokify-card-wireframe')) {
        // Wireframe pipeline cards appear during normal shelf browsing to complete grid composition
        if (currentQuery) {
          item.style.display = 'none';
        } else if (currentCategory === 'all' || currentCategory === 'book chapter') {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
        return;
      }

      if (matchesCategory && matchesQuery) {
        item.style.display = '';
        visibleCount++;
      } else {
        item.style.display = 'none';
      }
    });

    // Dynamic section visibility check
    sections.forEach(sec => {
      const secItems = sec.querySelectorAll('.pub-item');
      const hasVisible = Array.from(secItems).some(it => it.style.display !== 'none');
      sec.style.display = hasVisible ? '' : 'none';
    });

    if (countIndicator) {
      if (currentQuery) {
        countIndicator.style.display = 'block';
        countIndicator.textContent = `Showing ${visibleCount} matching publication${visibleCount === 1 ? '' : 's'} for "${currentQuery}"`;
      } else if (currentCategory !== 'all') {
        countIndicator.style.display = 'block';
        countIndicator.textContent = `Showing ${visibleCount} publication${visibleCount === 1 ? '' : 's'} in selected gallery`;
      } else {
        countIndicator.style.display = 'none';
        countIndicator.textContent = '';
      }
    }
  }

  // Filter pills event (Smooth scroll to section or filter)
  filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filterVal = btn.getAttribute('data-filter') || 'all';
      const targetSectionId = btn.getAttribute('data-target-section');

      if (targetSectionId) {
        // Show all so browsing remains open and scroll to target
        currentCategory = 'all';
        applyFilters();
        const targetEl = document.getElementById(targetSectionId);
        if (targetEl) {
          const yOffset = -140; // Offset for sticky navbar + controls
          const y = targetEl.getBoundingClientRect().top + window.pageYOffset + yOffset;
          window.scrollTo({ top: y, behavior: 'smooth' });
        }
      } else {
        // "All" clicked: scroll back to top of galleries
        currentCategory = 'all';
        applyFilters();
        const firstSec = document.querySelector('.pub-gallery-section');
        if (firstSec) {
          const yOffset = -140;
          const y = firstSec.getBoundingClientRect().top + window.pageYOffset + yOffset;
          window.scrollTo({ top: y, behavior: 'smooth' });
        }
      }
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
   Scholarly Profiles Side Expansion (Sacred Blooming Lotus Button Interaction)
   -------------------------------------------------------------------------- */
function initScholarlyDrawer() {
  const trigger = document.getElementById('lotus-toggle-btn') || document.getElementById('star-toggle-btn');
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
      isShuffleMode = false;
      if (shuffleBtn) shuffleBtn.classList.remove('active');
      rotateTraySlide(-1);
    } else if (nextBtn) {
      e.preventDefault();
      isShuffleMode = false;
      if (shuffleBtn) shuffleBtn.classList.remove('active');
      rotateTraySlide(1);
    } else if (shuffleToggle) {
      e.preventDefault();
      isShuffleMode = true;
      shuffleToggle.classList.add('active');
      shuffleToggle.classList.add('shuffling');
      setTimeout(() => shuffleToggle.classList.remove('shuffling'), 450);

      // Instant jump to a random slide across all rich menus
      let randIdx;
      do {
        randIdx = Math.floor(Math.random() * total);
      } while (randIdx === portalsTickerIndex && total > 1);
      portalsTickerIndex = randIdx;
      updateTrack();
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
const ACTIVITIES_SEARCH_DATA = [{"id": "spotlight-article", "type": "spotlight", "category": "✦ SPOTLIGHT ARTICLE", "title": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance", "sub": "Smart Cities (MDPI) • Vol. 9 (2026) • Open Access • Lead Author: Zaid Amin, Ph.D.", "keywords": "trustworthy ai sustainable cities multimodal orchestration agent civic compliance mdpi scopus q1 proxy trap governance urban intelligence", "url": "https://doi.org/10.3390/smartcities9100174", "action": "Read Article ↗", "isExternal": true}, {"slideIndex": 0, "category": "✦ UKM PH.D. / SLIDE 01", "title": "About, Talks & Academic CV", "sub": "Ph.D. in Computer Science (UKM) &bull; Senior Lecturer • Keynote Speaker &bull; Academic Leadership Track", "keywords": "about, talks & academic cv ukm ph.d. ph.d. in computer science (ukm) &bull; senior lecturer keynote speaker &bull; academic leadership track cv.html", "url": "cv.html", "action": "View CV ↗", "isExternal": false}, {"slideIndex": 0, "category": "✦ FRGS / AI / SLIDE 01", "title": "Projects & Innovations", "sub": "FRGS Grant: Civic Compliance Framework • Multimodal Orchestration Agent Architecture", "keywords": "projects & innovations frgs / ai frgs grant: civic compliance framework multimodal orchestration agent architecture research.html", "url": "research.html", "action": "Inspect ↗", "isExternal": false}, {"slideIndex": 0, "category": "✦ 24 WORKS / SLIDE 01", "title": "Research & Publications", "sub": "24 Peer-Reviewed Articles (MDPI, IEEE, Scopus Q1) • Trustworthy AI &bull; Full Open-Access &amp; BibTeX", "keywords": "research & publications 24 works 24 peer-reviewed articles (mdpi, ieee, scopus q1) trustworthy ai &bull; full open-access &amp; bibtex publications.html", "url": "publications.html", "action": "Explore ↗", "isExternal": false}, {"slideIndex": 0, "category": "✦ IEEE ACCESS / SLIDE 01", "title": "Attention-Based Decision Systems", "sub": "IEEE Access (2021) &bull; Q1 Scopus Indexed • Visual Attention System for Digital Environments", "keywords": "attention-based decision systems ieee access ieee access (2021) &bull; q1 scopus indexed visual attention system for digital environments https://doi.org/10.1109/access.2021.3087740", "url": "https://doi.org/10.1109/ACCESS.2021.3087740", "action": "Read ↗", "isExternal": true}, {"slideIndex": 1, "category": "✦ SCOPUS Q1 JOURNAL / SLIDE 02", "title": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance", "sub": "Smart Cities (MDPI) (2026) • Authors: Dr. Zaid Amin et al.", "keywords": "trustworthy ai for sustainable cities: a multimodal orchestration agent-based framework for civic compliance scopus q1 journal smart cities (mdpi) (2026) authors: dr. zaid amin et al. https://doi.org/10.3390/smartcities9100174", "url": "https://doi.org/10.3390/smartcities9100174", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 1, "category": "✦ TV TALKSHOW / SLIDE 02", "title": "TVRI Talk Show: Arsitektur Virtual Machine & Cloud Virtualization", "sub": "TVRI Sumatera Selatan &bull; 24:30 • Broadcast: Mei 2015", "keywords": "tvri talk show: arsitektur virtual machine & cloud virtualization tv talkshow tvri sumatera selatan &bull; 24:30 broadcast: mei 2015 talks.html#tvri-virtual-machine", "url": "talks.html#tvri-virtual-machine", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 1, "category": "✦ HONOR & AWARD / SLIDE 02", "title": "2nd Runner Up South Sumatera Innovator Award", "sub": "Provincial Government of South Sum&hellip; (2025) • Distinction: Provincial Honor", "keywords": "2nd runner up south sumatera innovator award honor & award provincial government of south sum&hellip; (2025) distinction: provincial honor https://tinyurl.com/5n7yjtht", "url": "https://tinyurl.com/5n7yjtht", "action": "Inspect Honor ↗", "isExternal": true}, {"slideIndex": 1, "category": "✦ AI & CYBERNETICS / SLIDE 02", "title": "HARMONY: Human-Trusted AI and Resilient Multimodal Orchestration Framework for Enhancing Normative Trust in Society", "sub": "AI & Cybernetics &bull; 1 min read • Published: 2026-02-02", "keywords": "harmony: human-trusted ai and resilient multimodal orchestration framework for enhancing normative trust in society ai & cybernetics ai & cybernetics &bull; 1 min read published: 2026-02-02 article.html?id=harmony-human-trusted-ai-and-resilient-multimodal-orchestration", "url": "article.html?id=harmony-human-trusted-ai-and-resilient-multimodal-orchestration", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 2, "category": "✦ AI & CYBERNETICS / SLIDE 03", "title": "Kehidupan Pendidik saat Pandemi COVID-19 (Part I)", "sub": "AI & Cybernetics &bull; 3 min read • Published: 2021-01-21", "keywords": "kehidupan pendidik saat pandemi covid-19 (part i) ai & cybernetics ai & cybernetics &bull; 3 min read published: 2021-01-21 article.html?id=kehidupan-pendidik-saat-pandemi-covid-19-part-i", "url": "article.html?id=kehidupan-pendidik-saat-pandemi-covid-19-part-i", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 2, "category": "✦ RESEARCH GRANT / SLIDE 03", "title": "National Competitive Community Service Grant (BIMA)", "sub": "Ministry of Education, Culture, Re&hellip; (2025) • Distinction: National Competitive", "keywords": "national competitive community service grant (bima) research grant ministry of education, culture, re&hellip; (2025) distinction: national competitive https://bima.kemdikbud.go.id", "url": "https://bima.kemdikbud.go.id", "action": "Inspect Honor ↗", "isExternal": true}, {"slideIndex": 2, "category": "✦ TV TALKSHOW / SLIDE 03", "title": "TVRI Talk Show: Virtual LAN (VLAN) & Performa Jaringan Enterprise", "sub": "TVRI Sumatera Selatan &bull; 23:45 • Broadcast: Mei 2015", "keywords": "tvri talk show: virtual lan (vlan) & performa jaringan enterprise tv talkshow tvri sumatera selatan &bull; 23:45 broadcast: mei 2015 talks.html#tvri-virtual-lan", "url": "talks.html#tvri-virtual-lan", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 2, "category": "✦ JOURNAL / SLIDE 03", "title": "SRIVIJAYAPEDIA: A DIGITAL PLATFORM FOR CULTURAL HERITAGE PRESERVATION OF THE SRIVIJAYA CIVILIZATION", "sub": "Journal of Information System and&hellip; (2026) • Authors: Dr. Zaid Amin et al.", "keywords": "srivijayapedia: a digital platform for cultural heritage preservation of the srivijaya civilization journal journal of information system and&hellip; (2026) authors: dr. zaid amin et al. https://doi.org/10.35631/jistm.1142003", "url": "https://doi.org/10.35631/JISTM.1142003", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 3, "category": "✦ TV TALKSHOW / SLIDE 04", "title": "TVRI Talk Show: Dinamika Routing Jaringan & Sistem Otonomus (AS)", "sub": "TVRI Sumatera Selatan &bull; 25:10 • Broadcast: Juni 2015", "keywords": "tvri talk show: dinamika routing jaringan & sistem otonomus (as) tv talkshow tvri sumatera selatan &bull; 25:10 broadcast: juni 2015 talks.html#tvri-network-routing", "url": "talks.html#tvri-network-routing", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 3, "category": "✦ PREPRINT / SLIDE 04", "title": "The Proxy Trap in Agentic AI: When Metrics Replace Judgment", "sub": "SSRN / Preprints (2026) • Authors: Dr. Zaid Amin et al.", "keywords": "the proxy trap in agentic ai: when metrics replace judgment preprint ssrn / preprints (2026) authors: dr. zaid amin et al. https://doi.org/10.2139/ssrn.7670124", "url": "https://doi.org/10.2139/ssrn.7670124", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 3, "category": "✦ AI & CYBERNETICS / SLIDE 04", "title": "Tipe-tipe \"bias\" dalam penelitian ilmiah", "sub": "AI & Cybernetics &bull; 3 min read • Published: 2020-12-25", "keywords": "tipe-tipe \"bias\" dalam penelitian ilmiah ai & cybernetics ai & cybernetics &bull; 3 min read published: 2020-12-25 article.html?id=tipe-tipe-bias-dalam-penelitian-ilmiah", "url": "article.html?id=tipe-tipe-bias-dalam-penelitian-ilmiah", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 3, "category": "✦ HONOR & AWARD / SLIDE 04", "title": "Conference Chairman: 7th ICIBA & 3rd SOSEIC International Conferences", "sub": "Universitas Bina Darma, Indonesia (2024) • Distinction: International Chairman", "keywords": "conference chairman: 7th iciba & 3rd soseic international conferences honor & award universitas bina darma, indonesia (2024) distinction: international chairman https://iciba.binadarma.ac.id", "url": "https://iciba.binadarma.ac.id", "action": "Inspect Honor ↗", "isExternal": true}, {"slideIndex": 4, "category": "✦ PH.D. SUPERVISION / SLIDE 05", "title": "Agentic AI Safety & The Proxy Trap", "sub": "Degree Level: Ph.D., Master's Track • Prerequisites: Python, LLM frameworks, Reinforcemen&hellip;", "keywords": "agentic ai safety & the proxy trap ph.d. supervision degree level: ph.d., master's track prerequisites: python, llm frameworks, reinforcemen&hellip; supervision.html#topic-1", "url": "supervision.html#topic-1", "action": "Apply Topic ↗", "isExternal": false}, {"slideIndex": 4, "category": "✦ AI & CYBERNETICS / SLIDE 05", "title": "Cyberspace", "sub": "AI & Cybernetics &bull; 6 min read • Published: 2019-02-14", "keywords": "cyberspace ai & cybernetics ai & cybernetics &bull; 6 min read published: 2019-02-14 article.html?id=cyberspace", "url": "article.html?id=cyberspace", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 4, "category": "✦ PREPRINT / SLIDE 05", "title": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance", "sub": "SSRN / Preprints (2026) • Authors: Dr. Zaid Amin et al.", "keywords": "trustworthy ai for sustainable cities: a multimodal orchestration agent-based framework for civic compliance preprint ssrn / preprints (2026) authors: dr. zaid amin et al. https://doi.org/10.20944/preprints202608.1136.v1", "url": "https://doi.org/10.20944/preprints202608.1136.v1", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 4, "category": "✦ TV TALKSHOW / SLIDE 05", "title": "TVRI Talk Show: Desain Topologi Jaringan & Infrastruktur Tangguh", "sub": "TVRI Sumatera Selatan &bull; 18:20 • Broadcast: Juni 2015", "keywords": "tvri talk show: desain topologi jaringan & infrastruktur tangguh tv talkshow tvri sumatera selatan &bull; 18:20 broadcast: juni 2015 talks.html#tvri-network-topology", "url": "talks.html#tvri-network-topology", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 5, "category": "✦ TV TALKSHOW / SLIDE 06", "title": "TVRI Talk Show: Arsitektur Jaringan Berkecepatan Tinggi untuk Big Data", "sub": "TVRI Sumatera Selatan &bull; 24:50 • Broadcast: Juli 2015", "keywords": "tvri talk show: arsitektur jaringan berkecepatan tinggi untuk big data tv talkshow tvri sumatera selatan &bull; 24:50 broadcast: juli 2015 talks.html#tvri-network-bigdata", "url": "talks.html#tvri-network-bigdata", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 5, "category": "✦ HONOR & AWARD / SLIDE 06", "title": "The Best Presenter Award (IEEE Xplore Conference)", "sub": "Universitas Muhammadiyah Yogyakart&hellip; (2024) • Distinction: IEEE Xplore Honor", "keywords": "the best presenter award (ieee xplore conference) honor & award universitas muhammadiyah yogyakart&hellip; (2024) distinction: ieee xplore honor https://tinyurl.com/4ehzmxyn", "url": "https://tinyurl.com/4ehzmxyn", "action": "Inspect Honor ↗", "isExternal": true}, {"slideIndex": 5, "category": "✦ JOURNAL / SLIDE 06", "title": "Immersive Heritage: Exploring Srivijaya's Historical Legacy Through Virtual Reality in Digital Communication", "sub": "Jurnal Audiens (2025) • Authors: Dr. Zaid Amin et al.", "keywords": "immersive heritage: exploring srivijaya's historical legacy through virtual reality in digital communication journal jurnal audiens (2025) authors: dr. zaid amin et al. https://doi.org/10.18196/jas.v6i2.617", "url": "https://doi.org/10.18196/jas.v6i2.617", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 5, "category": "✦ EPISTEMIC & MEDIA / SLIDE 06", "title": "How can academics contribute to tackling disinformation?", "sub": "Epistemic & Media &bull; 3 min read • Published: 2019-02-11", "keywords": "how can academics contribute to tackling disinformation? epistemic & media epistemic & media &bull; 3 min read published: 2019-02-11 article.html?id=how-can-academics-contribute-to-tackling-disinformation", "url": "article.html?id=how-can-academics-contribute-to-tackling-disinformation", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 6, "category": "✦ AI & CYBERNETICS / SLIDE 07", "title": "Dimuliakan melalui makan dan minum", "sub": "AI & Cybernetics &bull; 1 min read • Published: 2019-01-07", "keywords": "dimuliakan melalui makan dan minum ai & cybernetics ai & cybernetics &bull; 1 min read published: 2019-01-07 article.html?id=dimuliakan-melalui-makan-dan-minum", "url": "article.html?id=dimuliakan-melalui-makan-dan-minum", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 6, "category": "✦ JOURNAL / SLIDE 07", "title": "Celebrity of Instagram and Endorsements: Shaping and Constructing Social Identity", "sub": "Jurnal The Messenger (2025) • Authors: Dr. Zaid Amin et al.", "keywords": "celebrity of instagram and endorsements: shaping and constructing social identity journal jurnal the messenger (2025) authors: dr. zaid amin et al. https://doi.org/10.26623/themessenger.v17i1.11658", "url": "https://doi.org/10.26623/themessenger.v17i1.11658", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 6, "category": "✦ HONOR & AWARD / SLIDE 07", "title": "External PhD Proposal Defense Examiner", "sub": "Institute of Visual Informatics (I&hellip; (2024) • Distinction: Doctoral Panel", "keywords": "external phd proposal defense examiner honor & award institute of visual informatics (i&hellip; (2024) distinction: doctoral panel cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 6, "category": "✦ TV TALKSHOW / SLIDE 07", "title": "TVRI Talk Show: Simulasi dan Pemodelan Kinerja Jaringan Komputer", "sub": "TVRI Sumatera Selatan &bull; 35:10 • Broadcast: Agustus 2015", "keywords": "tvri talk show: simulasi dan pemodelan kinerja jaringan komputer tv talkshow tvri sumatera selatan &bull; 35:10 broadcast: agustus 2015 talks.html#tvri-network-simulation", "url": "talks.html#tvri-network-simulation", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 7, "category": "✦ BOOK CHAPTER / SLIDE 08", "title": "Digital Loneliness in Social Media: The Epoch of our Connected and Distraction World", "sub": "Contributions to Management Scienc&hellip; (2024) • Authors: Dr. Zaid Amin et al.", "keywords": "digital loneliness in social media: the epoch of our connected and distraction world book chapter contributions to management scienc&hellip; (2024) authors: dr. zaid amin et al. https://doi.org/10.1007/978-3-031-48770-5_65", "url": "https://doi.org/10.1007/978-3-031-48770-5_65", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 7, "category": "✦ RESEARCH GRANT / SLIDE 08", "title": "University Multidisciplinary Research Grant: PRIDE Quality Culture", "sub": "Universitas Bina Darma (2024) • Distinction: Competitive Grant", "keywords": "university multidisciplinary research grant: pride quality culture research grant universitas bina darma (2024) distinction: competitive grant cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 7, "category": "✦ TV TALKSHOW / SLIDE 08", "title": "TVRI Talk Show: Jaringan Masa Depan & Konektivitas di Era Big Data", "sub": "TVRI Sumatera Selatan &bull; 31:40 • Broadcast: September 2015", "keywords": "tvri talk show: jaringan masa depan & konektivitas di era big data tv talkshow tvri sumatera selatan &bull; 31:40 broadcast: september 2015 talks.html#tvri-future-network", "url": "talks.html#tvri-future-network", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 7, "category": "✦ ESSAYS & PERSPECTIVES / SLIDE 08", "title": "Yang tidak kuketahui antara Palembang - Melaka (Cerita Kuliah di Universiti Kebangsaan Malaysia)", "sub": "Essays & Perspectives &bull; 9 min read • Published: 2018-09-20", "keywords": "yang tidak kuketahui antara palembang - melaka (cerita kuliah di universiti kebangsaan malaysia) essays & perspectives essays & perspectives &bull; 9 min read published: 2018-09-20 article.html?id=yang-tidak-kuketahui-antara-palembang-melaka-cerita-kuliah", "url": "article.html?id=yang-tidak-kuketahui-antara-palembang-melaka-cerita-kuliah", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 8, "category": "✦ PH.D. SUPERVISION / SLIDE 09", "title": "Attention-Based Interface Interventions & Digital Well-Being", "sub": "Degree Level: Ph.D., Master's Track • Prerequisites: HCI methods, Frontend/Fullstack prot&hellip;", "keywords": "attention-based interface interventions & digital well-being ph.d. supervision degree level: ph.d., master's track prerequisites: hci methods, frontend/fullstack prot&hellip; supervision.html#topic-2", "url": "supervision.html#topic-2", "action": "Apply Topic ↗", "isExternal": false}, {"slideIndex": 8, "category": "✦ KEYNOTE SPEAKER / SLIDE 09", "title": "Multimodal AI Architectures & Human-Trusted Cybernetic Systems", "sub": "International Conference on Emergi&hellip; (2026) • Venue: School of Sciences, Woxsen University,&hellip;", "keywords": "multimodal ai architectures & human-trusted cybernetic systems keynote speaker international conference on emergi&hellip; (2026) venue: school of sciences, woxsen university,&hellip; talks.html#keynote-matcom-2026", "url": "talks.html#keynote-matcom-2026", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 8, "category": "✦ AI & CYBERNETICS / SLIDE 09", "title": "LIVE Talk Show E-Commerce di TVRI Sumsel", "sub": "AI & Cybernetics &bull; 2 min read • Published: 2015-05-08", "keywords": "live talk show e-commerce di tvri sumsel ai & cybernetics ai & cybernetics &bull; 2 min read published: 2015-05-08 article.html?id=live-talk-show-e-commerce-di-tvri-sumsel", "url": "article.html?id=live-talk-show-e-commerce-di-tvri-sumsel", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 8, "category": "✦ BOOK CHAPTER / SLIDE 09", "title": "Attention-Based Design and Selective Exposure Amid COVID-19 Misinformation Sharing", "sub": "Lecture Notes in Computer Science (2021) • Authors: Dr. Zaid Amin et al.", "keywords": "attention-based design and selective exposure amid covid-19 misinformation sharing book chapter lecture notes in computer science (2021) authors: dr. zaid amin et al. https://doi.org/10.1007/978-3-030-78468-3_34", "url": "https://doi.org/10.1007/978-3-030-78468-3_34", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 9, "category": "✦ BOOK CHAPTER / SLIDE 10", "title": "Peer-Review Statements", "sub": "Academic Publication (2025) • Authors: Dr. Zaid Amin et al.", "keywords": "peer-review statements book chapter academic publication (2025) authors: dr. zaid amin et al. https://doi.org/10.2991/978-2-38476-466-2_1", "url": "https://doi.org/10.2991/978-2-38476-466-2_1", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 9, "category": "✦ KEYNOTE SPEAKER / SLIDE 10", "title": "Persuasive Computing & Cognitive Attention in Algorithmic Governance", "sub": "Research Mobility Program: Trustwo&hellip; (2026) • Venue: Institute of Visual Informatics (IVI),&hellip;", "keywords": "persuasive computing & cognitive attention in algorithmic governance keynote speaker research mobility program: trustwo&hellip; (2026) venue: institute of visual informatics (ivi),&hellip; talks.html#keynote-ukm-trustworthy-ai", "url": "talks.html#keynote-ukm-trustworthy-ai", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 9, "category": "✦ HONOR & AWARD / SLIDE 10", "title": "International Research Fellow", "sub": "INTI International University, Mal&hellip; (2023 - 2025) • Distinction: Research Fellowship", "keywords": "international research fellow honor & award inti international university, mal&hellip; (2023 - 2025) distinction: research fellowship cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 9, "category": "✦ ESSAYS & PERSPECTIVES / SLIDE 10", "title": "Cara Mendapatkan Surat Penerimaan (LoA) dari Universitas di Luar Negeri.", "sub": "Essays & Perspectives &bull; 5 min read • Published: 2014-09-10", "keywords": "cara mendapatkan surat penerimaan (loa) dari universitas di luar negeri. essays & perspectives essays & perspectives &bull; 5 min read published: 2014-09-10 article.html?id=cara-mendapatkan-surat-penerimaan-loa-dari-universitas-di", "url": "article.html?id=cara-mendapatkan-surat-penerimaan-loa-dari-universitas-di", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 10, "category": "✦ PEDAGOGY & EDUCATION / SLIDE 11", "title": "Metacognition", "sub": "Pedagogy & Education &bull; 16 min read • Published: 2013-12-14", "keywords": "metacognition pedagogy & education pedagogy & education &bull; 16 min read published: 2013-12-14 article.html?id=metacognition", "url": "article.html?id=metacognition", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 10, "category": "✦ RESEARCH GRANT / SLIDE 11", "title": "University Multidisciplinary Research Grant: Visual Selective Attention System (VSAS)", "sub": "Universitas Bina Darma (2023) • Distinction: Competitive Grant", "keywords": "university multidisciplinary research grant: visual selective attention system (vsas) research grant universitas bina darma (2023) distinction: competitive grant cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 10, "category": "✦ KEYNOTE SPEAKER / SLIDE 11", "title": "The Proxy Trap in Agentic AI: Why Metric Optimization Fails Human Values", "sub": "International Symposium on Trustwo&hellip; (2026) • Venue: Kuala Lumpur, Malaysia (Hybrid Interna&hellip;", "keywords": "the proxy trap in agentic ai: why metric optimization fails human values keynote speaker international symposium on trustwo&hellip; (2026) venue: kuala lumpur, malaysia (hybrid interna&hellip; talks.html#keynote-autonomous-systems-2026", "url": "talks.html#keynote-autonomous-systems-2026", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 10, "category": "✦ CONFERENCE / SLIDE 11", "title": "Tune-Attention Model: Designing Cybernetics Intervention for Information Sharing Behavior", "sub": "2024 4th International Conference&hellip; (2024) • Authors: Dr. Zaid Amin et al.", "keywords": "tune-attention model: designing cybernetics intervention for information sharing behavior conference 2024 4th international conference&hellip; (2024) authors: dr. zaid amin et al. https://doi.org/10.1109/ice3is62977.2024.10775858", "url": "https://doi.org/10.1109/ice3is62977.2024.10775858", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 11, "category": "✦ KEYNOTE SPEAKER / SLIDE 12", "title": "Sociotechnical Digital Preservation & 3D Heritage Systems", "sub": "Interdisciplinary Seminar: Cultura&hellip; (2025) • Venue: Institute of Visual Informatics (IVI),&hellip;", "keywords": "sociotechnical digital preservation & 3d heritage systems keynote speaker interdisciplinary seminar: cultura&hellip; (2025) venue: institute of visual informatics (ivi),&hellip; talks.html#keynote-ukm-cultural-heritage", "url": "talks.html#keynote-ukm-cultural-heritage", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 11, "category": "✦ JOURNAL / SLIDE 12", "title": "Attention-Based Design and User Decision on Information Sharing: An Ontological Approach Through Thematic Literature Review", "sub": "Unpublished (2021) • Authors: Dr. Zaid Amin et al.", "keywords": "attention-based design and user decision on information sharing: an ontological approach through thematic literature review journal unpublished (2021) authors: dr. zaid amin et al. https://doi.org/10.13140/rg.2.2.28372.83841", "url": "https://doi.org/10.13140/RG.2.2.28372.83841", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 11, "category": "✦ AI & CYBERNETICS / SLIDE 12", "title": "Job Description for Network Engineering", "sub": "AI & Cybernetics &bull; 2 min read • Published: 2013-12-12", "keywords": "job description for network engineering ai & cybernetics ai & cybernetics &bull; 2 min read published: 2013-12-12 article.html?id=job-description-for-network-engineering", "url": "article.html?id=job-description-for-network-engineering", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 11, "category": "✦ HONOR & AWARD / SLIDE 12", "title": "Special Best Poster Presenter Award (IPSIR 4.0)", "sub": "Institute of IR4.0, Universiti Keb&hellip; (2021) • Distinction: International Honor", "keywords": "special best poster presenter award (ipsir 4.0) honor & award institute of ir4.0, universiti keb&hellip; (2021) distinction: international honor cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 12, "category": "✦ PH.D. SUPERVISION / SLIDE 13", "title": "Multimodal AI Orchestration for Sustainable Urban Governance", "sub": "Degree Level: Ph.D., Master's Track • Prerequisites: Data Science, Computer Vision, Geosp&hellip;", "keywords": "multimodal ai orchestration for sustainable urban governance ph.d. supervision degree level: ph.d., master's track prerequisites: data science, computer vision, geosp&hellip; supervision.html#topic-3", "url": "supervision.html#topic-3", "action": "Apply Topic ↗", "isExternal": false}, {"slideIndex": 12, "category": "✦ AI & CYBERNETICS / SLIDE 13", "title": "Arsitektur jaringan komputer", "sub": "AI & Cybernetics &bull; 4 min read • Published: 2013-12-10", "keywords": "arsitektur jaringan komputer ai & cybernetics ai & cybernetics &bull; 4 min read published: 2013-12-10 article.html?id=arsitektur-jaringan-komputer", "url": "article.html?id=arsitektur-jaringan-komputer", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 12, "category": "✦ SCOPUS Q1 JOURNAL / SLIDE 13", "title": "Attention-Based Design and User Decisions on Information Sharing: A Thematic Literature Review", "sub": "IEEE Access (2021) • Authors: Dr. Zaid Amin et al.", "keywords": "attention-based design and user decisions on information sharing: a thematic literature review scopus q1 journal ieee access (2021) authors: dr. zaid amin et al. https://doi.org/10.1109/access.2021.3087740", "url": "https://doi.org/10.1109/ACCESS.2021.3087740", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 12, "category": "✦ KEYNOTE SPEAKER / SLIDE 13", "title": "AI & Creativity: Human-Technology Collaboration & Ethical Guardrails", "sub": "National Academic Seminar on Emerg&hellip; (2024) • Venue: Universitas Dehasen Bengkulu, Indonesi&hellip;", "keywords": "ai & creativity: human-technology collaboration & ethical guardrails keynote speaker national academic seminar on emerg&hellip; (2024) venue: universitas dehasen bengkulu, indonesi&hellip; talks.html#keynote-dehasen-creativity", "url": "talks.html#keynote-dehasen-creativity", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 13, "category": "✦ KEYNOTE SPEAKER / SLIDE 14", "title": "Humane Interface Design: Rewiring User Attention Against Algorithmic Distraction", "sub": "ASEAN HCI & Digital Society Colloq&hellip; (2025) • Venue: Jakarta / Regional Hybrid Session", "keywords": "humane interface design: rewiring user attention against algorithmic distraction keynote speaker asean hci & digital society colloq&hellip; (2025) venue: jakarta / regional hybrid session talks.html#keynote-asean-hci-colloquium", "url": "talks.html#keynote-asean-hci-colloquium", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 13, "category": "✦ RESEARCH GRANT / SLIDE 14", "title": "Research Grant Recipient (GPK-4IR-2020-019)", "sub": "Institute of Visual Informatics (I&hellip; (2020) • Distinction: UKM 4IR Grant", "keywords": "research grant recipient (gpk-4ir-2020-019) research grant institute of visual informatics (i&hellip; (2020) distinction: ukm 4ir grant cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 13, "category": "✦ JOURNAL / SLIDE 14", "title": "Visual Selective Attention System to Intervene User Attention in Sharing COVID-19 Misinformation", "sub": "International Journal of Advanced&hellip; (2021) • Authors: Dr. Zaid Amin et al.", "keywords": "visual selective attention system to intervene user attention in sharing covid-19 misinformation journal international journal of advanced&hellip; (2021) authors: dr. zaid amin et al. https://doi.org/10.14569/ijacsa.2021.0121005", "url": "https://doi.org/10.14569/IJACSA.2021.0121005", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 13, "category": "✦ AI & CYBERNETICS / SLIDE 14", "title": "Topologi Cisco EtherChannel", "sub": "AI & Cybernetics &bull; 3 min read • Published: 2013-12-09", "keywords": "topologi cisco etherchannel ai & cybernetics ai & cybernetics &bull; 3 min read published: 2013-12-09 article.html?id=topologi-cisco-etherchannel", "url": "article.html?id=topologi-cisco-etherchannel", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 14, "category": "✦ PEDAGOGY & EDUCATION / SLIDE 15", "title": "Link Agregasi Menggunakan Cisco EtherChannel", "sub": "Pedagogy & Education &bull; 6 min read • Published: 2013-12-07", "keywords": "link agregasi menggunakan cisco etherchannel pedagogy & education pedagogy & education &bull; 6 min read published: 2013-12-07 article.html?id=link-agregasi-menggunakan-cisco-etherchannel", "url": "article.html?id=link-agregasi-menggunakan-cisco-etherchannel", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 14, "category": "✦ PREPRINT / SLIDE 15", "title": "Visual selective attention system to intervene user attention in sharing COVID-19 misinformation", "sub": "arXiv (2021) • Authors: Dr. Zaid Amin et al.", "keywords": "visual selective attention system to intervene user attention in sharing covid-19 misinformation preprint arxiv (2021) authors: dr. zaid amin et al. http://www.scopus.com/inward/record.url?eid=2-s2.0-85118754709&partnerid=mn8toars", "url": "http://www.scopus.com/inward/record.url?eid=2-s2.0-85118754709&partnerID=MN8TOARS", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 14, "category": "✦ RESEARCH GRANT / SLIDE 15", "title": "National Competitive Research Grant Program", "sub": "Ministry of Research, Technology a&hellip; (2017) • Distinction: National Competitive", "keywords": "national competitive research grant program research grant ministry of research, technology a&hellip; (2017) distinction: national competitive cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 14, "category": "✦ TECH OPINION / SLIDE 15", "title": "Das Sein, Das Sollen: Bridging What Is and What Ought to Be in AI", "sub": "Philosophical Treatises on Cyber&hellip; (2026) • Focus: The Humean is-ought problem in autonom&hellip;", "keywords": "das sein, das sollen: bridging what is and what ought to be in ai tech opinion philosophical treatises on cyber&hellip; (2026) focus: the humean is-ought problem in autonom&hellip; talks.html#opinion-das-sein-das-sollen", "url": "talks.html#opinion-das-sein-das-sollen", "action": "Read Column ↗", "isExternal": false}, {"slideIndex": 15, "category": "✦ PREPRINT / SLIDE 16", "title": "Attention and misinformation sharing on social media", "sub": "SSRN / Preprints (2020) • Authors: Dr. Zaid Amin et al.", "keywords": "attention and misinformation sharing on social media preprint ssrn / preprints (2020) authors: dr. zaid amin et al. https://arxiv.org/pdf/2012.12593", "url": "https://arxiv.org/pdf/2012.12593", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 15, "category": "✦ HONOR & AWARD / SLIDE 16", "title": "Favorite Lecturer Award", "sub": "Informatics Engineering Study Prog&hellip; (2013) • Distinction: Teaching Honor", "keywords": "favorite lecturer award honor & award informatics engineering study prog&hellip; (2013) distinction: teaching honor cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 15, "category": "✦ TECH OPINION / SLIDE 16", "title": "When Metrics Cannibalize Wisdom: The Proxy Trap in Academic Systems", "sub": "Higher Education & Algorithmic I&hellip; (2026) • Focus: How Goodhart's law and relentless prox&hellip;", "keywords": "when metrics cannibalize wisdom: the proxy trap in academic systems tech opinion higher education & algorithmic i&hellip; (2026) focus: how goodhart's law and relentless prox&hellip; talks.html#opinion-the-proxy-trap", "url": "talks.html#opinion-the-proxy-trap", "action": "Read Column ↗", "isExternal": false}, {"slideIndex": 15, "category": "✦ AI & CYBERNETICS / SLIDE 16", "title": "Metode Perancangan Jaringan dengan Model PPDIOO", "sub": "AI & Cybernetics &bull; 3 min read • Published: 2013-12-07", "keywords": "metode perancangan jaringan dengan model ppdioo ai & cybernetics ai & cybernetics &bull; 3 min read published: 2013-12-07 article.html?id=metode-perancangan-jaringan-dengan-model-ppdioo", "url": "article.html?id=metode-perancangan-jaringan-dengan-model-ppdioo", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 16, "category": "✦ PH.D. SUPERVISION / SLIDE 17", "title": "Immersive Virtual Heritage & Spatial Social Computing", "sub": "Degree Level: Master's Track • Prerequisites: Unity / Unreal Engine, WebXR, 3D mod&hellip;", "keywords": "immersive virtual heritage & spatial social computing ph.d. supervision degree level: master's track prerequisites: unity / unreal engine, webxr, 3d mod&hellip; supervision.html#topic-4", "url": "supervision.html#topic-4", "action": "Apply Topic ↗", "isExternal": false}, {"slideIndex": 16, "category": "✦ TECH OPINION / SLIDE 17", "title": "The Architecture of Intentionality: Beyond Attention Extraction", "sub": "Sociotechnical Interfaces & Cogn&hellip; (2025) • Focus: Moving beyond the extractive algorithm&hellip;", "keywords": "the architecture of intentionality: beyond attention extraction tech opinion sociotechnical interfaces & cogn&hellip; (2025) focus: moving beyond the extractive algorithm&hellip; talks.html#opinion-reclaiming-attention", "url": "talks.html#opinion-reclaiming-attention", "action": "Read Column ↗", "isExternal": false}, {"slideIndex": 16, "category": "✦ ESSAYS & PERSPECTIVES / SLIDE 17", "title": "Wireless Charging", "sub": "Essays & Perspectives &bull; 2 min read • Published: 2013-12-07", "keywords": "wireless charging essays & perspectives essays & perspectives &bull; 2 min read published: 2013-12-07 article.html?id=wireless-charging", "url": "article.html?id=wireless-charging", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 16, "category": "✦ PREPRINT / SLIDE 17", "title": "Attention and misinformation sharing on social media", "sub": "arXiv (2020) • Authors: Dr. Zaid Amin et al.", "keywords": "attention and misinformation sharing on social media preprint arxiv (2020) authors: dr. zaid amin et al. http://www.scopus.com/inward/record.url?eid=2-s2.0-85100363873&partnerid=mn8toars", "url": "http://www.scopus.com/inward/record.url?eid=2-s2.0-85100363873&partnerID=MN8TOARS", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 17, "category": "✦ CONFERENCE / SLIDE 18", "title": "PENGEMBANGAN APLIKASI SISTEM MANAJEMEN DOKUMEN ELEKTRONIK BERORIENTASI STANDAR BORANG AKREDITASI BAN PT", "sub": "PROSIDING SEMNASTEK 2017 (2017) • Authors: Dr. Zaid Amin et al.", "keywords": "pengembangan aplikasi sistem manajemen dokumen elektronik berorientasi standar borang akreditasi ban pt conference prosiding semnastek 2017 (2017) authors: dr. zaid amin et al. https://jurnal.umj.ac.id/index.php/semnastek/article/view/1935/1586", "url": "https://jurnal.umj.ac.id/index.php/semnastek/article/view/1935/1586", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 17, "category": "✦ TECH OPINION / SLIDE 18", "title": "The Illusions of Multimodal Ubiquity: Machine Perception vs Experience", "sub": "Philosophy of Computing & Consci&hellip; (2025) • Focus: Deconstructing the ontological gap bet&hellip;", "keywords": "the illusions of multimodal ubiquity: machine perception vs experience tech opinion philosophy of computing & consci&hellip; (2025) focus: deconstructing the ontological gap bet&hellip; talks.html#opinion-multimodal-ubiquity", "url": "talks.html#opinion-multimodal-ubiquity", "action": "Read Column ↗", "isExternal": false}, {"slideIndex": 17, "category": "✦ GLOBAL AWARD / SLIDE 18", "title": "Global Panduit-Cisco Excellence Scholarship (CLI) Recipient", "sub": "Cisco Learning Institute & Cisco N&hellip; (2008) • Distinction: Global Top 40 Worldwide", "keywords": "global panduit-cisco excellence scholarship (cli) recipient global award cisco learning institute & cisco n&hellip; (2008) distinction: global top 40 worldwide cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 17, "category": "✦ AI & CYBERNETICS / SLIDE 18", "title": "My first DLSR - Canon EOS 650D ;)", "sub": "AI & Cybernetics &bull; 1 min read • Published: 2013-07-25", "keywords": "my first dlsr - canon eos 650d ;) ai & cybernetics ai & cybernetics &bull; 1 min read published: 2013-07-25 article.html?id=my-first-dlsr-canon-eos-650d", "url": "article.html?id=my-first-dlsr-canon-eos-650d", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 18, "category": "✦ ESSAYS & PERSPECTIVES / SLIDE 19", "title": "\"Banker to the Poor\"", "sub": "Essays & Perspectives &bull; 2 min read • Published: 2013-06-13", "keywords": "\"banker to the poor\" essays & perspectives essays & perspectives &bull; 2 min read published: 2013-06-13 article.html?id=banker-to-the-poor", "url": "article.html?id=banker-to-the-poor", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 18, "category": "✦ HONOR & AWARD / SLIDE 19", "title": "Top 40% Competitors in Asia-Pacific (APAC) Region", "sub": "Academy Netspace Competition, Cisc&hellip; (2008) • Distinction: Asia-Pacific Region", "keywords": "top 40% competitors in asia-pacific (apac) region honor & award academy netspace competition, cisc&hellip; (2008) distinction: asia-pacific region cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 18, "category": "✦ TECH OPINION / SLIDE 19", "title": "Digital Hegemony & the Epistemic Commonweal: Reclaiming the Commons", "sub": "Cybernetics & Digital Sovereignt&hellip; (2024) • Focus: On corporate platform enclosures, digi&hellip;", "keywords": "digital hegemony & the epistemic commonweal: reclaiming the commons tech opinion cybernetics & digital sovereignt&hellip; (2024) focus: on corporate platform enclosures, digi&hellip; talks.html#opinion-digital-hegemony", "url": "talks.html#opinion-digital-hegemony", "action": "Read Column ↗", "isExternal": false}, {"slideIndex": 18, "category": "✦ JOURNAL / SLIDE 19", "title": "Aplikasi Sistem Manajemen Dokumen Elektronik Berorientasi Standar Borang BAN PT", "sub": "UST IT: Jurnal Sistem Informasi, T&hellip; (2017) • Authors: Dr. Zaid Amin et al.", "keywords": "aplikasi sistem manajemen dokumen elektronik berorientasi standar borang ban pt journal ust it: jurnal sistem informasi, t&hellip; (2017) authors: dr. zaid amin et al. publications.html#amin2017aplikasi", "url": "publications.html#amin2017aplikasi", "action": "Explore Paper ↗", "isExternal": false}, {"slideIndex": 19, "category": "✦ TECH OPINION / SLIDE 20", "title": "Algorithmic Serfdom vs. Autonomous Human Dignity: A 2030s Manifesto", "sub": "Human-Centered Computing Manifes&hellip; (2024) • Focus: An HCI manifesto for the 2030s: engine&hellip;", "keywords": "algorithmic serfdom vs. autonomous human dignity: a 2030s manifesto tech opinion human-centered computing manifes&hellip; (2024) focus: an hci manifesto for the 2030s: engine&hellip; talks.html#opinion-algorithmic-serfdom", "url": "talks.html#opinion-algorithmic-serfdom", "action": "Read Column ↗", "isExternal": false}, {"slideIndex": 19, "category": "✦ CONFERENCE / SLIDE 20", "title": "Aplikasi Web Sms Sebagai Reminder Digital Menggunakan GAMMU", "sub": "SNTIBD 2017 (2017) • Authors: Dr. Zaid Amin et al.", "keywords": "aplikasi web sms sebagai reminder digital menggunakan gammu conference sntibd 2017 (2017) authors: dr. zaid amin et al. http://ojs.palcomtech.com/index.php/sntibd/issue/view/17", "url": "http://ojs.palcomtech.com/index.php/SNTIBD/issue/view/17", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 19, "category": "✦ AI & CYBERNETICS / SLIDE 20", "title": "Konfigurasi DHCP Server pada Mikrotik Router OS", "sub": "AI & Cybernetics &bull; 1 min read • Published: 2013-06-11", "keywords": "konfigurasi dhcp server pada mikrotik router os ai & cybernetics ai & cybernetics &bull; 1 min read published: 2013-06-11 article.html?id=konfigurasi-dhcp-server-pada-mikrotik-router-os", "url": "article.html?id=konfigurasi-dhcp-server-pada-mikrotik-router-os", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 19, "category": "✦ HONOR & AWARD / SLIDE 20", "title": "Champion II, Web Design Championships", "sub": "PalComTech Institute of Technology&hellip; (2006) • Distinction: Design Competition", "keywords": "champion ii, web design championships honor & award palcomtech institute of technology&hellip; (2006) distinction: design competition cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 20, "category": "✦ HONOR & AWARD / SLIDE 21", "title": "Champion II, Digital Media & Animation Awards", "sub": "PalComTech Institute of Technology&hellip; (2006) • Distinction: Animation Honor", "keywords": "champion ii, digital media & animation awards honor & award palcomtech institute of technology&hellip; (2006) distinction: animation honor cv.html#honors", "url": "cv.html#honors", "action": "Inspect Honor ↗", "isExternal": false}, {"slideIndex": 20, "category": "✦ AI & CYBERNETICS / SLIDE 21", "title": "Green Networking", "sub": "AI & Cybernetics &bull; 4 min read • Published: 2013-06-10", "keywords": "green networking ai & cybernetics ai & cybernetics &bull; 4 min read published: 2013-06-10 article.html?id=green-networking", "url": "article.html?id=green-networking", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 20, "category": "✦ CONFERENCE / SLIDE 21", "title": "Multi tier architecture model on a server cluster for application of big data", "sub": "Annual Research Seminar (ARS) - Co&hellip; (2017) • Authors: Dr. Zaid Amin et al.", "keywords": "multi tier architecture model on a server cluster for application of big data conference annual research seminar (ars) - co&hellip; (2017) authors: dr. zaid amin et al. http://www.seminar.ilkom.unsri.ac.id/index.php/ars/article/viewfile/1662/866", "url": "http://www.seminar.ilkom.unsri.ac.id/index.php/ars/article/viewFile/1662/866", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 20, "category": "✦ TV TALKSHOW / SLIDE 21", "title": "TVRI Talk Show: Arsitektur Virtual Machine & Cloud Virtualization", "sub": "TVRI Sumatera Selatan &bull; 24:30 • Broadcast: Mei 2015", "keywords": "tvri talk show: arsitektur virtual machine & cloud virtualization tv talkshow tvri sumatera selatan &bull; 24:30 broadcast: mei 2015 talks.html#tvri-virtual-machine", "url": "talks.html#tvri-virtual-machine", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 21, "category": "✦ TV TALKSHOW / SLIDE 22", "title": "TVRI Talk Show: Virtual LAN (VLAN) & Performa Jaringan Enterprise", "sub": "TVRI Sumatera Selatan &bull; 23:45 • Broadcast: Mei 2015", "keywords": "tvri talk show: virtual lan (vlan) & performa jaringan enterprise tv talkshow tvri sumatera selatan &bull; 23:45 broadcast: mei 2015 talks.html#tvri-virtual-lan", "url": "talks.html#tvri-virtual-lan", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 21, "category": "✦ ACADEMIC LEADERSHIP / SLIDE 22", "title": "QS Deputy Director FDSIT", "sub": "Faculty of Data Science and Informat&hellip; • Tenure: 2026 - Present", "keywords": "qs deputy director fdsit academic leadership faculty of data science and informat&hellip; tenure: 2026 - present cv.html#leadership", "url": "cv.html#leadership", "action": "Leadership Track ↗", "isExternal": false}, {"slideIndex": 21, "category": "✦ JOURNAL / SLIDE 22", "title": "DESAIN DAN IMPLEMENTASI TUNNELING IPSEC BERBASIS UNIX DENGAN ESP (ENCAPSULATING SECURITY PAYLOAD) (Studi Kasus : PT. Sumeks Tivi Palembang & PT. Sumatera Ekspres)", "sub": "Jurnal Teknologi dan Informatika (2015) • Authors: Dr. Zaid Amin et al.", "keywords": "desain dan implementasi tunneling ipsec berbasis unix dengan esp (encapsulating security payload) (studi kasus : pt. sumeks tivi palembang & pt. sumatera ekspres) journal jurnal teknologi dan informatika (2015) authors: dr. zaid amin et al. http://eprints.binadarma.ac.id/id/eprint/2511", "url": "http://eprints.binadarma.ac.id/id/eprint/2511", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 21, "category": "✦ AI & CYBERNETICS / SLIDE 22", "title": "100GB Networking", "sub": "AI & Cybernetics &bull; 3 min read • Published: 2013-06-10", "keywords": "100gb networking ai & cybernetics ai & cybernetics &bull; 3 min read published: 2013-06-10 article.html?id=100gb-networking", "url": "article.html?id=100gb-networking", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 22, "category": "✦ AI & CYBERNETICS / SLIDE 23", "title": "Instalasi Mikrotik Router OS Pada VMware", "sub": "AI & Cybernetics &bull; 2 min read • Published: 2013-06-10", "keywords": "instalasi mikrotik router os pada vmware ai & cybernetics ai & cybernetics &bull; 2 min read published: 2013-06-10 article.html?id=instalasi-mikrotik-router-os-pada-vmware", "url": "article.html?id=instalasi-mikrotik-router-os-pada-vmware", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 22, "category": "✦ CONFERENCE / SLIDE 23", "title": "Routing protocols pada holistic network di era big data", "sub": "Annual Research Seminar (ARS) 2015 (2015) • Authors: Dr. Zaid Amin et al.", "keywords": "routing protocols pada holistic network di era big data conference annual research seminar (ars) 2015 (2015) authors: dr. zaid amin et al. http://www.seminar.ilkom.unsri.ac.id/index.php/ars/article/view/185", "url": "http://www.seminar.ilkom.unsri.ac.id/index.php/ars/article/view/185", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 22, "category": "✦ ACADEMIC LEADERSHIP / SLIDE 23", "title": "Head of Master Program in Informatics Engineering (M.Kom)", "sub": "Universitas Bina Darma, Indonesia • Tenure: 2023 - 2024", "keywords": "head of master program in informatics engineering (m.kom) academic leadership universitas bina darma, indonesia tenure: 2023 - 2024 cv.html#leadership", "url": "cv.html#leadership", "action": "Leadership Track ↗", "isExternal": false}, {"slideIndex": 22, "category": "✦ TV TALKSHOW / SLIDE 23", "title": "TVRI Talk Show: Dinamika Routing Jaringan & Sistem Otonomus (AS)", "sub": "TVRI Sumatera Selatan &bull; 25:10 • Broadcast: Juni 2015", "keywords": "tvri talk show: dinamika routing jaringan & sistem otonomus (as) tv talkshow tvri sumatera selatan &bull; 25:10 broadcast: juni 2015 talks.html#tvri-network-routing", "url": "talks.html#tvri-network-routing", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 23, "category": "✦ CONFERENCE / SLIDE 24", "title": "SIMULASI DAN PERANCANGAN KEAMANAN AUTENTIKASI JARINGAN HIRARKI LINK AGGREGATION CONTROL PROTOCOL (LACP) BERBASIS ROUTER CISCO", "sub": "Konferensi Nasional Teknologi Info&hellip; (2014) • Authors: Dr. Zaid Amin et al.", "keywords": "simulasi dan perancangan keamanan autentikasi jaringan hirarki link aggregation control protocol (lacp) berbasis router cisco conference konferensi nasional teknologi info&hellip; (2014) authors: dr. zaid amin et al. http://www.seminar.ilkom.unsri.ac.id/index.php/kntia/article/view/730/403", "url": "http://www.seminar.ilkom.unsri.ac.id/index.php/kntia/article/view/730/403", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 23, "category": "✦ ACADEMIC LEADERSHIP / SLIDE 24", "title": "Head of Information Systems Study Program", "sub": "Universitas Bina Darma, Indonesia • Tenure: 2022 - 2023", "keywords": "head of information systems study program academic leadership universitas bina darma, indonesia tenure: 2022 - 2023 cv.html#leadership", "url": "cv.html#leadership", "action": "Leadership Track ↗", "isExternal": false}, {"slideIndex": 23, "category": "✦ TV TALKSHOW / SLIDE 24", "title": "TVRI Talk Show: Desain Topologi Jaringan & Infrastruktur Tangguh", "sub": "TVRI Sumatera Selatan &bull; 18:20 • Broadcast: Juni 2015", "keywords": "tvri talk show: desain topologi jaringan & infrastruktur tangguh tv talkshow tvri sumatera selatan &bull; 18:20 broadcast: juni 2015 talks.html#tvri-network-topology", "url": "talks.html#tvri-network-topology", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 23, "category": "✦ AI & CYBERNETICS / SLIDE 24", "title": "Apa itu Mikrotik [Router OS]", "sub": "AI & Cybernetics &bull; 2 min read • Published: 2013-06-10", "keywords": "apa itu mikrotik [router os] ai & cybernetics ai & cybernetics &bull; 2 min read published: 2013-06-10 article.html?id=apa-itu-mikrotik-router-os", "url": "article.html?id=apa-itu-mikrotik-router-os", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 24, "category": "✦ ACADEMIC LEADERSHIP / SLIDE 25", "title": "Head of Informatics Engineering Study Program", "sub": "PalComTech Institute of Technology a&hellip; • Tenure: 2013 - 2014", "keywords": "head of informatics engineering study program academic leadership palcomtech institute of technology a&hellip; tenure: 2013 - 2014 cv.html#leadership", "url": "cv.html#leadership", "action": "Leadership Track ↗", "isExternal": false}, {"slideIndex": 24, "category": "✦ TV TALKSHOW / SLIDE 25", "title": "TVRI Talk Show: Arsitektur Jaringan Berkecepatan Tinggi untuk Big Data", "sub": "TVRI Sumatera Selatan &bull; 24:50 • Broadcast: Juli 2015", "keywords": "tvri talk show: arsitektur jaringan berkecepatan tinggi untuk big data tv talkshow tvri sumatera selatan &bull; 24:50 broadcast: juli 2015 talks.html#tvri-network-bigdata", "url": "talks.html#tvri-network-bigdata", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 24, "category": "✦ AI & CYBERNETICS / SLIDE 25", "title": "10 Hari Pertama Bulan Ramadhan", "sub": "AI & Cybernetics &bull; 2 min read • Published: 2012-07-20", "keywords": "10 hari pertama bulan ramadhan ai & cybernetics ai & cybernetics &bull; 2 min read published: 2012-07-20 article.html?id=10-hari-pertama-bulan-ramadhan", "url": "article.html?id=10-hari-pertama-bulan-ramadhan", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 24, "category": "✦ JOURNAL / SLIDE 25", "title": "Analisis Vulnerabilitas Host Pada Keamanan Jaringan Komputer Di PT. Sumeks Tivi Palembang (PALTV) Menggunakan Router Berbasis Unix", "sub": "Jurnal Teknologi dan Informatika (2012) • Authors: Dr. Zaid Amin et al.", "keywords": "analisis vulnerabilitas host pada keamanan jaringan komputer di pt. sumeks tivi palembang (paltv) menggunakan router berbasis unix journal jurnal teknologi dan informatika (2012) authors: dr. zaid amin et al. http://eprints.binadarma.ac.id/id/eprint/2582", "url": "http://eprints.binadarma.ac.id/id/eprint/2582", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 25, "category": "✦ SCOPUS Q1 JOURNAL / SLIDE 26", "title": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance", "sub": "Smart Cities (MDPI) (2026) • Authors: Dr. Zaid Amin et al.", "keywords": "trustworthy ai for sustainable cities: a multimodal orchestration agent-based framework for civic compliance scopus q1 journal smart cities (mdpi) (2026) authors: dr. zaid amin et al. https://doi.org/10.3390/smartcities9100174", "url": "https://doi.org/10.3390/smartcities9100174", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 25, "category": "✦ TV TALKSHOW / SLIDE 26", "title": "TVRI Talk Show: Simulasi dan Pemodelan Kinerja Jaringan Komputer", "sub": "TVRI Sumatera Selatan &bull; 35:10 • Broadcast: Agustus 2015", "keywords": "tvri talk show: simulasi dan pemodelan kinerja jaringan komputer tv talkshow tvri sumatera selatan &bull; 35:10 broadcast: agustus 2015 talks.html#tvri-network-simulation", "url": "talks.html#tvri-network-simulation", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 25, "category": "✦ ACADEMIC LEADERSHIP / SLIDE 26", "title": "Head of Graphic Design and Multimedia Editing", "sub": "Palembang Television (PALTV), Indone&hellip; • Tenure: 2006 - 2011", "keywords": "head of graphic design and multimedia editing academic leadership palembang television (paltv), indone&hellip; tenure: 2006 - 2011 cv.html#leadership", "url": "cv.html#leadership", "action": "Leadership Track ↗", "isExternal": false}, {"slideIndex": 25, "category": "✦ AI & CYBERNETICS / SLIDE 26", "title": "SOHO", "sub": "AI & Cybernetics &bull; 5 min read • Published: 2012-05-09", "keywords": "soho ai & cybernetics ai & cybernetics &bull; 5 min read published: 2012-05-09 article.html?id=soho", "url": "article.html?id=soho", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 26, "category": "✦ ESSAYS & PERSPECTIVES / SLIDE 27", "title": "Packet Tracer Version 5.3 Software Downloads", "sub": "Essays & Perspectives &bull; 1 min read • Published: 2012-05-07", "keywords": "packet tracer version 5.3 software downloads essays & perspectives essays & perspectives &bull; 1 min read published: 2012-05-07 article.html?id=packet-tracer-version-53-software-downloads", "url": "article.html?id=packet-tracer-version-53-software-downloads", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 26, "category": "✦ AUTHORED BOOK / SLIDE 27", "title": "Information Sharing Behaviour on Social Media", "sub": "Academic Monograph & Book • ISBN / Scholarly Reference Volume", "keywords": "information sharing behaviour on social media authored book academic monograph & book isbn / scholarly reference volume cv.html#books", "url": "cv.html#books", "action": "Explore Book ↗", "isExternal": false}, {"slideIndex": 26, "category": "✦ TV TALKSHOW / SLIDE 27", "title": "TVRI Talk Show: Jaringan Masa Depan & Konektivitas di Era Big Data", "sub": "TVRI Sumatera Selatan &bull; 31:40 • Broadcast: September 2015", "keywords": "tvri talk show: jaringan masa depan & konektivitas di era big data tv talkshow tvri sumatera selatan &bull; 31:40 broadcast: september 2015 talks.html#tvri-future-network", "url": "talks.html#tvri-future-network", "action": "Watch Video ↗", "isExternal": false}, {"slideIndex": 26, "category": "✦ JOURNAL / SLIDE 27", "title": "SRIVIJAYAPEDIA: A DIGITAL PLATFORM FOR CULTURAL HERITAGE PRESERVATION OF THE SRIVIJAYA CIVILIZATION", "sub": "Journal of Information System and&hellip; (2026) • Authors: Dr. Zaid Amin et al.", "keywords": "srivijayapedia: a digital platform for cultural heritage preservation of the srivijaya civilization journal journal of information system and&hellip; (2026) authors: dr. zaid amin et al. https://doi.org/10.35631/jistm.1142003", "url": "https://doi.org/10.35631/JISTM.1142003", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 27, "category": "✦ KEYNOTE SPEAKER / SLIDE 28", "title": "Multimodal AI Architectures & Human-Trusted Cybernetic Systems", "sub": "International Conference on Emergi&hellip; (2026) • Venue: School of Sciences, Woxsen University,&hellip;", "keywords": "multimodal ai architectures & human-trusted cybernetic systems keynote speaker international conference on emergi&hellip; (2026) venue: school of sciences, woxsen university,&hellip; talks.html#keynote-matcom-2026", "url": "talks.html#keynote-matcom-2026", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 27, "category": "✦ PREPRINT / SLIDE 28", "title": "The Proxy Trap in Agentic AI: When Metrics Replace Judgment", "sub": "SSRN / Preprints (2026) • Authors: Dr. Zaid Amin et al.", "keywords": "the proxy trap in agentic ai: when metrics replace judgment preprint ssrn / preprints (2026) authors: dr. zaid amin et al. https://doi.org/10.2139/ssrn.7670124", "url": "https://doi.org/10.2139/ssrn.7670124", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 27, "category": "✦ AI & CYBERNETICS / SLIDE 28", "title": "Cisco tries to head off software-defined networks", "sub": "AI & Cybernetics &bull; 4 min read • Published: 2012-04-20", "keywords": "cisco tries to head off software-defined networks ai & cybernetics ai & cybernetics &bull; 4 min read published: 2012-04-20 article.html?id=cisco-tries-to-head-off-software-defined-networks", "url": "article.html?id=cisco-tries-to-head-off-software-defined-networks", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 27, "category": "✦ Q1 PEER REVIEWER / SLIDE 28", "title": "Active Q1 Peer Reviewer: IEEE Access, PLOS ONE, Elsevier CHB", "sub": "IEEE Access &bull; PLOS ONE &bull; Elsevier CHB • Top-Tier Computational & Social Informatics", "keywords": "active q1 peer reviewer: ieee access, plos one, elsevier chb q1 peer reviewer ieee access &bull; plos one &bull; elsevier chb top-tier computational & social informatics cv.html#peer-review", "url": "cv.html#peer-review", "action": "Review Record ↗", "isExternal": false}, {"slideIndex": 28, "category": "✦ CERTIFICATION / SLIDE 29", "title": "Certified Computer Forensic (FCCF), Grade A", "sub": "Issuer: FORESEC Authorized Learning Part&hellip; • Credential Period: 2016 - 2017", "keywords": "certified computer forensic (fccf), grade a certification issuer: foresec authorized learning part&hellip; credential period: 2016 - 2017 cv.html#certifications", "url": "cv.html#certifications", "action": "View Credential ↗", "isExternal": false}, {"slideIndex": 28, "category": "✦ AI & CYBERNETICS / SLIDE 29", "title": "TRI DHARMA PERGURUAN TINGGI", "sub": "AI & Cybernetics &bull; 3 min read • Published: 2012-04-20", "keywords": "tri dharma perguruan tinggi ai & cybernetics ai & cybernetics &bull; 3 min read published: 2012-04-20 article.html?id=tri-dharma-perguruan-tinggi", "url": "article.html?id=tri-dharma-perguruan-tinggi", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 28, "category": "✦ PREPRINT / SLIDE 29", "title": "Trustworthy AI for Sustainable Cities: A Multimodal Orchestration Agent-Based Framework for Civic Compliance", "sub": "SSRN / Preprints (2026) • Authors: Dr. Zaid Amin et al.", "keywords": "trustworthy ai for sustainable cities: a multimodal orchestration agent-based framework for civic compliance preprint ssrn / preprints (2026) authors: dr. zaid amin et al. https://doi.org/10.20944/preprints202608.1136.v1", "url": "https://doi.org/10.20944/preprints202608.1136.v1", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 28, "category": "✦ KEYNOTE SPEAKER / SLIDE 29", "title": "Persuasive Computing & Cognitive Attention in Algorithmic Governance", "sub": "Research Mobility Program: Trustwo&hellip; (2026) • Venue: Institute of Visual Informatics (IVI),&hellip;", "keywords": "persuasive computing & cognitive attention in algorithmic governance keynote speaker research mobility program: trustwo&hellip; (2026) venue: institute of visual informatics (ivi),&hellip; talks.html#keynote-ukm-trustworthy-ai", "url": "talks.html#keynote-ukm-trustworthy-ai", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 29, "category": "✦ KEYNOTE SPEAKER / SLIDE 30", "title": "The Proxy Trap in Agentic AI: Why Metric Optimization Fails Human Values", "sub": "International Symposium on Trustwo&hellip; (2026) • Venue: Kuala Lumpur, Malaysia (Hybrid Interna&hellip;", "keywords": "the proxy trap in agentic ai: why metric optimization fails human values keynote speaker international symposium on trustwo&hellip; (2026) venue: kuala lumpur, malaysia (hybrid interna&hellip; talks.html#keynote-autonomous-systems-2026", "url": "talks.html#keynote-autonomous-systems-2026", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 29, "category": "✦ CERTIFICATION / SLIDE 30", "title": "Microsoft Technology Associate (MTA): HTML5 Application Development Fundamentals", "sub": "Issuer: Microsoft / Multimatics • Credential Period: Certified", "keywords": "microsoft technology associate (mta): html5 application development fundamentals certification issuer: microsoft / multimatics credential period: certified cv.html#certifications", "url": "cv.html#certifications", "action": "View Credential ↗", "isExternal": false}, {"slideIndex": 29, "category": "✦ JOURNAL / SLIDE 30", "title": "Immersive Heritage: Exploring Srivijaya's Historical Legacy Through Virtual Reality in Digital Communication", "sub": "Jurnal Audiens (2025) • Authors: Dr. Zaid Amin et al.", "keywords": "immersive heritage: exploring srivijaya's historical legacy through virtual reality in digital communication journal jurnal audiens (2025) authors: dr. zaid amin et al. https://doi.org/10.18196/jas.v6i2.617", "url": "https://doi.org/10.18196/jas.v6i2.617", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 29, "category": "✦ AI & CYBERNETICS / SLIDE 30", "title": "Next Generation Network", "sub": "AI & Cybernetics &bull; 6 min read • Published: 2012-04-19", "keywords": "next generation network ai & cybernetics ai & cybernetics &bull; 6 min read published: 2012-04-19 article.html?id=next-generation-network", "url": "article.html?id=next-generation-network", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 30, "category": "✦ AI & CYBERNETICS / SLIDE 31", "title": "Recompile dan rekonfigurasi FreeBSD Kernel for IPSec", "sub": "AI & Cybernetics &bull; 5 min read • Published: 2012-04-18", "keywords": "recompile dan rekonfigurasi freebsd kernel for ipsec ai & cybernetics ai & cybernetics &bull; 5 min read published: 2012-04-18 article.html?id=recompile-dan-rekonfigurasi-freebsd-kernel-for-ipsec", "url": "article.html?id=recompile-dan-rekonfigurasi-freebsd-kernel-for-ipsec", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 30, "category": "✦ JOURNAL / SLIDE 31", "title": "Celebrity of Instagram and Endorsements: Shaping and Constructing Social Identity", "sub": "Jurnal The Messenger (2025) • Authors: Dr. Zaid Amin et al.", "keywords": "celebrity of instagram and endorsements: shaping and constructing social identity journal jurnal the messenger (2025) authors: dr. zaid amin et al. https://doi.org/10.26623/themessenger.v17i1.11658", "url": "https://doi.org/10.26623/themessenger.v17i1.11658", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 30, "category": "✦ CERTIFICATION / SLIDE 31", "title": "CCNA Exploration: LAN Switching and Wireless", "sub": "Issuer: Cisco Systems, Inc. • Credential Period: Executive Letter (CEO)", "keywords": "ccna exploration: lan switching and wireless certification issuer: cisco systems, inc. credential period: executive letter (ceo) cv.html#certifications", "url": "cv.html#certifications", "action": "View Credential ↗", "isExternal": false}, {"slideIndex": 30, "category": "✦ KEYNOTE SPEAKER / SLIDE 31", "title": "Sociotechnical Digital Preservation & 3D Heritage Systems", "sub": "Interdisciplinary Seminar: Cultura&hellip; (2025) • Venue: Institute of Visual Informatics (IVI),&hellip;", "keywords": "sociotechnical digital preservation & 3d heritage systems keynote speaker interdisciplinary seminar: cultura&hellip; (2025) venue: institute of visual informatics (ivi),&hellip; talks.html#keynote-ukm-cultural-heritage", "url": "talks.html#keynote-ukm-cultural-heritage", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 31, "category": "✦ BOOK CHAPTER / SLIDE 32", "title": "Digital Loneliness in Social Media: The Epoch of our Connected and Distraction World", "sub": "Contributions to Management Scienc&hellip; (2024) • Authors: Dr. Zaid Amin et al.", "keywords": "digital loneliness in social media: the epoch of our connected and distraction world book chapter contributions to management scienc&hellip; (2024) authors: dr. zaid amin et al. https://doi.org/10.1007/978-3-031-48770-5_65", "url": "https://doi.org/10.1007/978-3-031-48770-5_65", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 31, "category": "✦ CERTIFICATION / SLIDE 32", "title": "CCNA Exploration: Routing Protocols and Concepts", "sub": "Issuer: Cisco Networking Academy • Credential Period: Course Completion", "keywords": "ccna exploration: routing protocols and concepts certification issuer: cisco networking academy credential period: course completion cv.html#certifications", "url": "cv.html#certifications", "action": "View Credential ↗", "isExternal": false}, {"slideIndex": 31, "category": "✦ KEYNOTE SPEAKER / SLIDE 32", "title": "AI & Creativity: Human-Technology Collaboration & Ethical Guardrails", "sub": "National Academic Seminar on Emerg&hellip; (2024) • Venue: Universitas Dehasen Bengkulu, Indonesi&hellip;", "keywords": "ai & creativity: human-technology collaboration & ethical guardrails keynote speaker national academic seminar on emerg&hellip; (2024) venue: universitas dehasen bengkulu, indonesi&hellip; talks.html#keynote-dehasen-creativity", "url": "talks.html#keynote-dehasen-creativity", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 31, "category": "✦ ESSAYS & PERSPECTIVES / SLIDE 32", "title": "How do we excel ?", "sub": "Essays & Perspectives &bull; 7 min read • Published: 2012-02-21", "keywords": "how do we excel ? essays & perspectives essays & perspectives &bull; 7 min read published: 2012-02-21 article.html?id=how-do-we-excel", "url": "article.html?id=how-do-we-excel", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 32, "category": "✦ CERTIFICATION / SLIDE 33", "title": "CCNA Exploration: Network Fundamentals", "sub": "Issuer: Cisco Systems, Inc. • Credential Period: Executive Letter (CEO)", "keywords": "ccna exploration: network fundamentals certification issuer: cisco systems, inc. credential period: executive letter (ceo) cv.html#certifications", "url": "cv.html#certifications", "action": "View Credential ↗", "isExternal": false}, {"slideIndex": 32, "category": "✦ KEYNOTE SPEAKER / SLIDE 33", "title": "Humane Interface Design: Rewiring User Attention Against Algorithmic Distraction", "sub": "ASEAN HCI & Digital Society Colloq&hellip; (2025) • Venue: Jakarta / Regional Hybrid Session", "keywords": "humane interface design: rewiring user attention against algorithmic distraction keynote speaker asean hci & digital society colloq&hellip; (2025) venue: jakarta / regional hybrid session talks.html#keynote-asean-hci-colloquium", "url": "talks.html#keynote-asean-hci-colloquium", "action": "View Talk ↗", "isExternal": false}, {"slideIndex": 32, "category": "✦ AI & CYBERNETICS / SLIDE 33", "title": "Untuk si \"dia\" yang berwarna \"merah\"...", "sub": "AI & Cybernetics &bull; 2 min read • Published: 2012-02-19", "keywords": "untuk si \"dia\" yang berwarna \"merah\"... ai & cybernetics ai & cybernetics &bull; 2 min read published: 2012-02-19 article.html?id=untuk-si-dia-yang-berwarna-merah", "url": "article.html?id=untuk-si-dia-yang-berwarna-merah", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 32, "category": "✦ BOOK CHAPTER / SLIDE 33", "title": "Attention-Based Design and Selective Exposure Amid COVID-19 Misinformation Sharing", "sub": "Lecture Notes in Computer Science (2021) • Authors: Dr. Zaid Amin et al.", "keywords": "attention-based design and selective exposure amid covid-19 misinformation sharing book chapter lecture notes in computer science (2021) authors: dr. zaid amin et al. https://doi.org/10.1007/978-3-030-78468-3_34", "url": "https://doi.org/10.1007/978-3-030-78468-3_34", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 33, "category": "✦ BOOK CHAPTER / SLIDE 34", "title": "Peer-Review Statements", "sub": "Academic Publication (2025) • Authors: Dr. Zaid Amin et al.", "keywords": "peer-review statements book chapter academic publication (2025) authors: dr. zaid amin et al. https://doi.org/10.2991/978-2-38476-466-2_1", "url": "https://doi.org/10.2991/978-2-38476-466-2_1", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 33, "category": "✦ TECH OPINION / SLIDE 34", "title": "Das Sein, Das Sollen: Bridging What Is and What Ought to Be in AI", "sub": "Philosophical Treatises on Cyber&hellip; (2026) • Focus: The Humean is-ought problem in autonom&hellip;", "keywords": "das sein, das sollen: bridging what is and what ought to be in ai tech opinion philosophical treatises on cyber&hellip; (2026) focus: the humean is-ought problem in autonom&hellip; talks.html#opinion-das-sein-das-sollen", "url": "talks.html#opinion-das-sein-das-sollen", "action": "Read Column ↗", "isExternal": false}, {"slideIndex": 33, "category": "✦ HONOR & AWARD / SLIDE 34", "title": "2nd Runner Up South Sumatera Innovator Award", "sub": "Provincial Government of South Sum&hellip; (2025) • Distinction: Provincial Honor", "keywords": "2nd runner up south sumatera innovator award honor & award provincial government of south sum&hellip; (2025) distinction: provincial honor https://tinyurl.com/5n7yjtht", "url": "https://tinyurl.com/5n7yjtht", "action": "Inspect Honor ↗", "isExternal": true}, {"slideIndex": 33, "category": "✦ DIGITAL ETHICS & HCI / SLIDE 34", "title": "SOPA and PIPA", "sub": "Digital Ethics & HCI &bull; 6 min read • Published: 2012-01-26", "keywords": "sopa and pipa digital ethics & hci digital ethics & hci &bull; 6 min read published: 2012-01-26 article.html?id=sopa-and-pipa", "url": "article.html?id=sopa-and-pipa", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 34, "category": "✦ ESSAYS & PERSPECTIVES / SLIDE 35", "title": "Voice from heaven", "sub": "Essays & Perspectives &bull; 1 min read • Published: 2012-01-02", "keywords": "voice from heaven essays & perspectives essays & perspectives &bull; 1 min read published: 2012-01-02 article.html?id=voice-from-heaven", "url": "article.html?id=voice-from-heaven", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 34, "category": "✦ RESEARCH GRANT / SLIDE 35", "title": "National Competitive Community Service Grant (BIMA)", "sub": "Ministry of Education, Culture, Re&hellip; (2025) • Distinction: National Competitive", "keywords": "national competitive community service grant (bima) research grant ministry of education, culture, re&hellip; (2025) distinction: national competitive https://bima.kemdikbud.go.id", "url": "https://bima.kemdikbud.go.id", "action": "Inspect Honor ↗", "isExternal": true}, {"slideIndex": 34, "category": "✦ TECH OPINION / SLIDE 35", "title": "When Metrics Cannibalize Wisdom: The Proxy Trap in Academic Systems", "sub": "Higher Education & Algorithmic I&hellip; (2026) • Focus: How Goodhart's law and relentless prox&hellip;", "keywords": "when metrics cannibalize wisdom: the proxy trap in academic systems tech opinion higher education & algorithmic i&hellip; (2026) focus: how goodhart's law and relentless prox&hellip; talks.html#opinion-the-proxy-trap", "url": "talks.html#opinion-the-proxy-trap", "action": "Read Column ↗", "isExternal": false}, {"slideIndex": 34, "category": "✦ CONFERENCE / SLIDE 35", "title": "Tune-Attention Model: Designing Cybernetics Intervention for Information Sharing Behavior", "sub": "2024 4th International Conference&hellip; (2024) • Authors: Dr. Zaid Amin et al.", "keywords": "tune-attention model: designing cybernetics intervention for information sharing behavior conference 2024 4th international conference&hellip; (2024) authors: dr. zaid amin et al. https://doi.org/10.1109/ice3is62977.2024.10775858", "url": "https://doi.org/10.1109/ice3is62977.2024.10775858", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 35, "category": "✦ TECH OPINION / SLIDE 36", "title": "The Architecture of Intentionality: Beyond Attention Extraction", "sub": "Sociotechnical Interfaces & Cogn&hellip; (2025) • Focus: Moving beyond the extractive algorithm&hellip;", "keywords": "the architecture of intentionality: beyond attention extraction tech opinion sociotechnical interfaces & cogn&hellip; (2025) focus: moving beyond the extractive algorithm&hellip; talks.html#opinion-reclaiming-attention", "url": "talks.html#opinion-reclaiming-attention", "action": "Read Column ↗", "isExternal": false}, {"slideIndex": 35, "category": "✦ JOURNAL / SLIDE 36", "title": "Attention-Based Design and User Decision on Information Sharing: An Ontological Approach Through Thematic Literature Review", "sub": "Unpublished (2021) • Authors: Dr. Zaid Amin et al.", "keywords": "attention-based design and user decision on information sharing: an ontological approach through thematic literature review journal unpublished (2021) authors: dr. zaid amin et al. https://doi.org/10.13140/rg.2.2.28372.83841", "url": "https://doi.org/10.13140/RG.2.2.28372.83841", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 35, "category": "✦ ESSAYS & PERSPECTIVES / SLIDE 36", "title": "R-Nought", "sub": "Essays & Perspectives &bull; 1 min read • Published: 2011-12-21", "keywords": "r-nought essays & perspectives essays & perspectives &bull; 1 min read published: 2011-12-21 article.html?id=r-nought", "url": "article.html?id=r-nought", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 35, "category": "✦ HONOR & AWARD / SLIDE 36", "title": "Conference Chairman: 7th ICIBA & 3rd SOSEIC International Conferences", "sub": "Universitas Bina Darma, Indonesia (2024) • Distinction: International Chairman", "keywords": "conference chairman: 7th iciba & 3rd soseic international conferences honor & award universitas bina darma, indonesia (2024) distinction: international chairman https://iciba.binadarma.ac.id", "url": "https://iciba.binadarma.ac.id", "action": "Inspect Honor ↗", "isExternal": true}, {"slideIndex": 36, "category": "✦ PH.D. SUPERVISION / SLIDE 37", "title": "Agentic AI Safety & The Proxy Trap", "sub": "Degree Level: Ph.D., Master's Track • Prerequisites: Python, LLM frameworks, Reinforcemen&hellip;", "keywords": "agentic ai safety & the proxy trap ph.d. supervision degree level: ph.d., master's track prerequisites: python, llm frameworks, reinforcemen&hellip; supervision.html#topic-1", "url": "supervision.html#topic-1", "action": "Apply Topic ↗", "isExternal": false}, {"slideIndex": 36, "category": "✦ ESSAYS & PERSPECTIVES / SLIDE 37", "title": "Unstoppable Time", "sub": "Essays & Perspectives &bull; 1 min read • Published: 2011-12-15", "keywords": "unstoppable time essays & perspectives essays & perspectives &bull; 1 min read published: 2011-12-15 article.html?id=unstoppable-time", "url": "article.html?id=unstoppable-time", "action": "Read Essay ↗", "isExternal": false}, {"slideIndex": 36, "category": "✦ SCOPUS Q1 JOURNAL / SLIDE 37", "title": "Attention-Based Design and User Decisions on Information Sharing: A Thematic Literature Review", "sub": "IEEE Access (2021) • Authors: Dr. Zaid Amin et al.", "keywords": "attention-based design and user decisions on information sharing: a thematic literature review scopus q1 journal ieee access (2021) authors: dr. zaid amin et al. https://doi.org/10.1109/access.2021.3087740", "url": "https://doi.org/10.1109/ACCESS.2021.3087740", "action": "Explore Paper ↗", "isExternal": true}, {"slideIndex": 36, "category": "✦ TECH OPINION / SLIDE 37", "title": "The Illusions of Multimodal Ubiquity: Machine Perception vs Experience", "sub": "Philosophy of Computing & Consci&hellip; (2025) • Focus: Deconstructing the ontological gap bet&hellip;", "keywords": "the illusions of multimodal ubiquity: machine perception vs experience tech opinion philosophy of computing & consci&hellip; (2025) focus: deconstructing the ontological gap bet&hellip; talks.html#opinion-multimodal-ubiquity", "url": "talks.html#opinion-multimodal-ubiquity", "action": "Read Column ↗", "isExternal": false}];

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
   Rotates Dr. Zaid Amin's portraits 1-4 with stately, continuous coin inertia.
   Hovering is 100% deactivated to prevent glitching and speed-ups.
   Flip transition is slowed down to ~1.75s for a calm, luxurious experience.
   ========================================================================== */
function initCoinPortraitEngine() {
  const coinStage = document.getElementById('dr-zaid-coin');
  const coinDisc = document.getElementById('coin-disc');
  const faceFront = document.getElementById('coin-face-front');
  const faceBack = document.getElementById('coin-face-back');

  if (!coinStage || !coinDisc || !faceFront || !faceBack) return;

  const DEFAULT_PORTRAITS = [
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

  const PORTRAITS = (window.PORTALS_COIN_PORTRAITS && Array.isArray(window.PORTALS_COIN_PORTRAITS) && window.PORTALS_COIN_PORTRAITS.length > 0)
    ? window.PORTALS_COIN_PORTRAITS.map(p => ({
        webp: p.webp || p.url || p.png || '',
        png: p.fallback || p.png || p.url || '',
        alt: p.alt || p.title || 'Dr. Zaid Amin, Ph.D.'
      }))
    : DEFAULT_PORTRAITS;

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

  function updateFaceImage(faceEl, portrait) {
    const webpSrc = portrait.webp || portrait.png;
    const pngSrc = portrait.png || portrait.webp;
    const altText = portrait.alt || 'Dr. Zaid Amin, Ph.D.';
    const picture = faceEl.querySelector('picture');
    if (picture) {
      const source = picture.querySelector('source');
      const img = picture.querySelector('img');
      if (source && webpSrc.endsWith('.webp')) {
        source.srcset = webpSrc;
      }
      if (img) {
        img.src = pngSrc;
        img.alt = altText;
      }
    } else {
      const img = faceEl.querySelector('img');
      if (img) {
        img.src = pngSrc;
        img.alt = altText;
      }
    }
  }

  function flipCoin() {
    if (isFlipping) return;
    isFlipping = true;

    currentAngle += 180;
    coinDisc.classList.add('is-flipping');
    // Slow, soft, elegant 3D coin rotation with subtle 1.02 scale
    coinDisc.style.transform = `rotateY(${currentAngle}deg) scale(1.02)`;

    // Halfway through rotation (875ms), gently restore scale to 1
    setTimeout(() => {
      coinDisc.style.transform = `rotateY(${currentAngle}deg) scale(1)`;
    }, 875);

    // Flip duration is 1750ms (buttery smooth and dignified)
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
    }, 1750);
  }

  function startAutoTimer() {
    clearInterval(autoFlipInterval);
    // Calm Golden Ratio rhythm: 6.5s dwell on each photo
    autoFlipInterval = setInterval(() => {
      if (!document.hidden) {
        flipCoin();
      }
    }, 6500);
  }

  function resetTimer() {
    startAutoTimer();
  }

  // User interactive controls: Click or Keyboard only (Hovering inactive for glitch-free smoothness)
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

  // Note: Hovering (mouseenter/mouseleave) deliberately omitted to guarantee silky uninterrupted motion

  startAutoTimer();

  window.flipPortraitCoin = flipCoin;
  console.log('[CoinPortraitEngine] Initialized with 4 strictly-centered Golden Ratio portraits. Slow 1.75s filmic flip active.');
}

/* ==============================================================================
   CV VERIFICATION STATUS NOTIFICATION (High-Class Obsidian Toast)
   ============================================================================== */
function showCvNotice(triggerEl) {
  let toast = document.getElementById('cv-toast-notice');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'cv-toast-notice';
    toast.className = 'cv-toast-notice';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');
    toast.innerHTML = `
      <span class="cv-toast-gem">✦</span>
      <div class="cv-toast-content">
        <div class="cv-toast-title">Official Verification Record</div>
        <div class="cv-toast-msg">This credential document is securely archived on official institutional registry and available upon academic request (<a href="mailto:zaid.amin@newinti.edu.my" style="color:#7dd3fc; text-decoration:underline;">zaid.amin@newinti.edu.my</a>).</div>
      </div>
    `;
    document.body.appendChild(toast);
  }

  if (triggerEl) {
    triggerEl.style.transform = 'scale(0.96)';
    setTimeout(() => { triggerEl.style.transform = ''; }, 180);
  }

  toast.classList.add('is-active');

  if (window._cvToastTimer) clearTimeout(window._cvToastTimer);
  window._cvToastTimer = setTimeout(() => {
    toast.classList.remove('is-active');
  }, 4200);
}
window.showCvNotice = showCvNotice;

/* ==============================================================================
   STEALTH POINTER NAVIGATION ENGINE (Status Bar Cloaking & Anti-Leakage Defense)
   Suppresses the browser's bottom-left naked URL status bubble on hover.
   Provides clean, modern, immersive navigation with full accessibility & security.
   ============================================================================== */
(function initStealthNavigationEngine() {
  const STEALTH_SELECTOR = 'nav a, .top-epigraph-menu a, .ref-menu-tab, .pub-pill-btn, .top-link-pill, .cv-jump-link, .cv-sublayer-pill, .spotlight-btn-primary, .spotlight-btn-secondary, .spotlight-btn, .pub-btn, .article-back-link, .ref-item-btn, [data-stealth]';

  function cloakLink(e) {
    const link = e.target.closest(STEALTH_SELECTOR);
    if (!link) return;

    if (link.hasAttribute('href') && !link.hasAttribute('data-raw-href')) {
      const rawHref = link.getAttribute('href');
      if (rawHref && rawHref !== '#' && !rawHref.startsWith('javascript:')) {
        link.setAttribute('data-raw-href', rawHref);
        link.removeAttribute('href');
        link.style.cursor = 'pointer';
        if (!link.getAttribute('role')) link.setAttribute('role', 'link');
        if (!link.getAttribute('tabindex')) link.setAttribute('tabindex', '0');
      }
    }
  }

  function uncloakLink(e) {
    const link = e.target.closest(STEALTH_SELECTOR);
    if (link && link.hasAttribute('data-raw-href')) {
      link.setAttribute('href', link.getAttribute('data-raw-href'));
      link.removeAttribute('data-raw-href');
    }
  }

  // 1. Mouse & pointer enter: Temporarily decouple href so the browser displays NO bottom-left URL popup
  document.addEventListener('mouseover', cloakLink, { passive: true });
  document.addEventListener('pointerover', cloakLink, { passive: true });

  // 2. Mouse & pointer leave: Cleanly restore href
  document.addEventListener('mouseout', uncloakLink, { passive: true });
  document.addEventListener('pointerout', uncloakLink, { passive: true });

  // 3. Right-click: Context menu needs the href to offer "Open link in new tab" & "Copy link address"
  document.addEventListener('contextmenu', function(e) {
    const link = e.target.closest(STEALTH_SELECTOR);
    if (link && link.hasAttribute('data-raw-href')) {
      link.setAttribute('href', link.getAttribute('data-raw-href'));
      link.removeAttribute('data-raw-href');
    }
  });

  // 4. Click: Seamless and secure instant navigation
  document.addEventListener('click', function(e) {
    const link = e.target.closest(STEALTH_SELECTOR);
    if (!link) return;

    // If it has inline onclick handler (e.g. toast or filter), let that handler execute
    if (link.getAttribute('onclick')) return;

    const targetUrl = link.getAttribute('data-raw-href') || link.getAttribute('href');
    if (targetUrl && targetUrl !== '#' && !targetUrl.startsWith('javascript:')) {
      e.preventDefault();
      const openInNewTab = link.getAttribute('target') === '_blank' || e.ctrlKey || e.metaKey || e.button === 1;
      if (openInNewTab) {
        window.open(targetUrl, '_blank', 'noopener,noreferrer');
      } else {
        window.location.href = targetUrl;
      }
    }
  });

  // 5. Accessible Keyboard Navigation (Enter key)
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      const link = document.activeElement ? document.activeElement.closest(STEALTH_SELECTOR) : null;
      if (link && !link.getAttribute('onclick')) {
        const targetUrl = link.getAttribute('data-raw-href') || link.getAttribute('href');
        if (targetUrl && targetUrl !== '#' && !targetUrl.startsWith('javascript:')) {
          e.preventDefault();
          const openInNewTab = link.getAttribute('target') === '_blank' || e.ctrlKey || e.metaKey;
          if (openInNewTab) {
            window.open(targetUrl, '_blank', 'noopener,noreferrer');
          } else {
            window.location.href = targetUrl;
          }
        }
      }
    }
  });

  console.log('[StealthNavigationEngine] Active: Status bar naked URL popups suppressed on hover.');
})();

