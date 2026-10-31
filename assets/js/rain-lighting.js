/**
 * Lighthouse Storm Banner Engine: Soft Rain & Ambient Lighting
 * Atmospheric Canvas for Dr. Zaid Amin (zaidamin.org)
 * Features:
 * - Subtle, realistic falling rain with wind slant
 * - Gentle raindrop ripples on impact
 * - Soft distant ambient thunder flashes (gentle illumination, non-strobe)
 * - Volumetric lighthouse beam illumination on raindrops
 */

(function() {
  const canvas = document.getElementById('rain-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = 0;
  let height = 0;
  let raindrops = [];
  let ripples = [];
  let ambientFlashAlpha = 0;
  let targetFlash = 0;

  function resize() {
    const parent = canvas.parentElement;
    width = canvas.width = parent.clientWidth;
    height = canvas.height = parent.clientHeight;
    initRain();
  }

  window.addEventListener('resize', resize);

  // Raindrop definition
  class Raindrop {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 200) - 100;
      this.y = initial ? Math.random() * height : -20;
      this.speed = Math.random() * 8 + 12;
      this.length = Math.random() * 18 + 14;
      this.angle = 0.22; // subtle wind slant to the right
      this.alpha = Math.random() * 0.35 + 0.15;
      this.width = Math.random() * 1.2 + 0.6;
    }

    update() {
      this.x += Math.sin(this.angle) * this.speed;
      this.y += Math.cos(this.angle) * this.speed;

      // When reaching lower region (crashing water/shore line)
      if (this.y > height * 0.88 + Math.random() * 50) {
        if (Math.random() < 0.2) {
          ripples.push(new Ripple(this.x, this.y));
        }
        this.reset();
      }

      if (this.x > width + 100) {
        this.reset();
      }
    }

    draw() {
      ctx.save();
      ctx.strokeStyle = `rgba(215, 235, 255, ${this.alpha})`;
      ctx.lineWidth = this.width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(
        this.x + Math.sin(this.angle) * this.length,
        this.y + Math.cos(this.angle) * this.length
      );
      ctx.stroke();
      ctx.restore();
    }
  }

  // Ripple / Splash effect
  class Ripple {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.radius = 1;
      this.maxRadius = Math.random() * 8 + 4;
      this.alpha = 0.4;
      this.growth = Math.random() * 0.4 + 0.3;
    }

    update() {
      this.radius += this.growth;
      this.alpha -= 0.02;
    }

    draw() {
      if (this.alpha <= 0) return;
      ctx.save();
      ctx.strokeStyle = `rgba(186, 230, 253, ${this.alpha})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.ellipse(this.x, this.y, this.radius * 2, this.radius * 0.7, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }
  }

  function initRain() {
    const count = Math.min(Math.floor((width * height) / 4500), 160);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new Raindrop());
    }
  }

  // Soft Ambient Lightning (Gentle, cinematic illumination)
  let lastFlashTime = Date.now();
  function checkSoftLighting() {
    const now = Date.now();
    if (now - lastFlashTime > (Math.random() * 5000 + 6000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.22 + 0.08; // very soft, not blinding
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    // 1. Soft Ambient Lightning Glow across the storm clouds
    ambientFlashAlpha += (targetFlash - ambientFlashAlpha) * 0.08;
    if (targetFlash > 0 && Math.abs(targetFlash - ambientFlashAlpha) < 0.01) {
      targetFlash = 0;
    }
    if (ambientFlashAlpha > 0.005) {
      ctx.fillStyle = `rgba(192, 202, 245, ${ambientFlashAlpha})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 2. Draw & Update Ripples
    for (let i = ripples.length - 1; i >= 0; i--) {
      ripples[i].update();
      ripples[i].draw();
      if (ripples[i].alpha <= 0) {
        ripples.splice(i, 1);
      }
    }

    // 3. Draw & Update Raindrops
    for (let drop of raindrops) {
      drop.update();
      drop.draw();
    }

    checkSoftLighting();
    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
