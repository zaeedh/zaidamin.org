/**
 * Instant Navigation Engine - zaidamin.org
 * Speculatively preloads internal HTML links on cursor hover (>65ms) or touchstart,
 * cutting perceived page transition latency to 0ms.
 */
(function() {
  'use strict';
  if (typeof window === 'undefined' || !window.fetch || !document.createElement) return;
  
  var prefetched = new Set();
  var hoverTimer = null;
  
  function canPreload(url) {
    if (!url) return false;
    var loc = window.location;
    // Only same-origin links
    if (url.origin !== loc.origin) return false;
    // Don't prefetch current URL or anchor hashes on same page
    if (url.pathname === loc.pathname && url.search === loc.search) return false;
    // Skip binary assets, archives, and media
    var path = url.pathname.toLowerCase();
    if (path.match(/\.(pdf|zip|png|jpg|jpeg|webp|gif|svg|ico|xml|txt|json)$/)) return false;
    // Don't duplicate requests
    if (prefetched.has(url.href)) return false;
    return true;
  }
  
  function preload(urlStr) {
    try {
      var url = new URL(urlStr, window.location.href);
      if (!canPreload(url)) return;
      prefetched.add(url.href);
      
      var link = document.createElement('link');
      link.rel = 'prefetch';
      link.href = url.href;
      link.as = 'document';
      document.head.appendChild(link);
    } catch(e) {}
  }
  
  function onPointerOver(e) {
    var a = e.target && e.target.closest('a');
    if (!a || !a.href) return;
    hoverTimer = setTimeout(function() {
      preload(a.href);
    }, 65);
  }
  
  function onPointerOut() {
    if (hoverTimer) {
      clearTimeout(hoverTimer);
      hoverTimer = null;
    }
  }
  
  function onTouchStart(e) {
    var a = e.target && e.target.closest('a');
    if (a && a.href) preload(a.href);
  }
  
  document.addEventListener('mouseover', onPointerOver, { passive: true });
  document.addEventListener('mouseout', onPointerOut, { passive: true });
  document.addEventListener('touchstart', onTouchStart, { passive: true });
})();
