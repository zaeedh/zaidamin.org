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
  initScholarlyDrawer();
  initJournalTicker();
  initPublicationsFilter();
  initBibtexButtons();
  initMobileMenu();
});

/* --------------------------------------------------------------------------
   Theme Switcher (Dark / Light)
   -------------------------------------------------------------------------- */
function initThemeToggle() {
  const themeToggleBtn = document.getElementById('theme-toggle');
  if (!themeToggleBtn) return;

  const currentTheme = localStorage.getItem('theme') || 'dark';

  setTheme(currentTheme);

  themeToggleBtn.addEventListener('click', () => {
    const activeTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  });
}

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);

  const themeToggleBtn = document.getElementById('theme-toggle');
  if (themeToggleBtn) {
    themeToggleBtn.innerHTML = theme === 'dark' 
      ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`
      : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
    themeToggleBtn.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
  }
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
