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
  initPortalsTrayCarousel();
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
   Inset Tray Portals & Blogger Articles Carousel Controller
   Paginates 4 slides of 3 cards each with counter, arrows & indicator dots
   -------------------------------------------------------------------------- */
function initPortalsTrayCarousel() {
  const carousel = document.getElementById('portals-carousel');
  if (!carousel) return;

  const slides = carousel.querySelectorAll('.tray-slide');
  const dots = carousel.querySelectorAll('.spotlight-dot');
  const currEl = carousel.querySelector('.tray-curr');
  const totalEl = carousel.querySelector('.tray-total');
  if (!slides.length) return;

  let currentIndex = 0;
  const total = slides.length;
  if (totalEl) totalEl.textContent = String(total).padStart(2, '0');

  function goToSlide(idx) {
    if (idx < 0) idx = total - 1;
    if (idx >= total) idx = 0;
    currentIndex = idx;

    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === currentIndex);
    });

    dots.forEach((dot, dIdx) => {
      dot.classList.toggle('active', dIdx === currentIndex);
    });

    if (currEl) currEl.textContent = String(currentIndex + 1).padStart(2, '0');
  }

  carousel.addEventListener('click', (e) => {
    const prevBtn = e.target.closest('.tray-arrow-prev, .spotlight-arrow-prev');
    const nextBtn = e.target.closest('.tray-arrow-next, .spotlight-arrow-next');
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
