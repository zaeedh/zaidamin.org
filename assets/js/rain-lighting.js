/**
 * Realistic, Thin, Premium Sea Spray & Ambient Storm Engine
 * Lighthouse Storm Banner for Dr. Zaid Amin (zaidamin.org)
 * 
 * Design Principles:
 * - 100% Unwarped Original Painting: The real picture remains crisp, stable, and photorealistic.
 * - Thin, Whisper-Fine Splashes: Ultra-fine airborne micro-droplets (0.5px-1.2px) floating naturally on the wind.
 * - Feathered Sea Spray Vapor: Soft, sheer radial mist plumes that bloom from the crashing wave and dissipate.
 * - Blended Living Foam: Gentle, organic luminosity that pulses softly over the existing painted foam using screen blend mode.
 * - Delicate Storm Rain: Thin, elegant, translucent raindrops falling at a natural wind angle.
 * - Pure 60 FPS performance, seamless blending, zero cartoon shapes or geometric lines.
 */

(function() {
  const canvas = document.getElementById('rain-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = 0;
  let height = 0;
  let simTime = 0;

  // Particle Pools
  let splashParticles = [];
  let mistClouds = [];
  let spindriftWisps = [];
  let raindrops = [];
  let ripples = [];

  // Lighting
  let ambientFlashAlpha = 0;
  let targetFlash = 0;
  let lastFlashTime = Date.now();
  let nextLighthouseBreaker = 0;

  function resize() {
    const parent = canvas.parentElement;
    width = canvas.width = parent.clientWidth;
    height = canvas.height = parent.clientHeight;
    initRain();
  }

  window.addEventListener('resize', resize);

  // --------------------------------------------------------------------------
  // 1. THIN SPLASH PARTICLES (Ultra-fine crystalline water droplets)
  // --------------------------------------------------------------------------
  class ThinSplashParticle {
    constructor(originX, originY, power = 1.0) {
      this.x = originX + (Math.random() - 0.5) * 14;
      this.y = originY + (Math.random() - 0.5) * 8;
      
      // Fan out upward and drift downwind to the right
      const angle = -(Math.PI * 0.28 + Math.random() * Math.PI * 0.44);
      const speed = (Math.random() * 2.6 + 1.2) * power;
      this.vx = Math.cos(angle) * speed + (Math.random() * 0.7 + 0.5);
      this.vy = Math.sin(angle) * speed;

      this.size = Math.random() * 0.7 + 0.5; // whisper thin: 0.5px to 1.2px
      this.alpha = Math.random() * 0.35 + 0.30;
      this.decay = Math.random() * 0.009 + 0.007; // smooth, lingering evaporation
      this.gravity = 0.045; // gentle floating buoyant spray
      this.life = Math.random() * 45 + 35;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.vy += this.gravity;
      this.vx *= 0.988; // air drag
      this.alpha -= this.decay;
      this.life--;
    }

    draw(boost) {
      if (this.alpha <= 0 || this.life <= 0) return;
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      const a = Math.min(this.alpha * boost, 0.75);
      ctx.fillStyle = `rgba(230, 245, 255, ${a})`;
      ctx.beginPath();
      // Slight motion elongation in trajectory direction
      const speed = Math.hypot(this.vx, this.vy);
      const angle = Math.atan2(this.vy, this.vx);
      ctx.ellipse(this.x, this.y, this.size + speed * 0.35, this.size * 0.8, angle, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  // --------------------------------------------------------------------------
  // 2. SHEER SEA SPRAY MIST (Feathered radial vapor puffs)
  // --------------------------------------------------------------------------
  class SeaSprayMist {
    constructor(x, y, maxRadius = 36) {
      this.x = x;
      this.y = y;
      this.radius = Math.random() * 8 + 6;
      this.maxRadius = maxRadius;
      this.growth = (maxRadius - this.radius) / (Math.random() * 35 + 45);
      this.vx = Math.random() * 0.8 + 0.4;  // drifts softly downwind
      this.vy = -(Math.random() * 0.45 + 0.2); // rises gently into the air
      this.alpha = Math.random() * 0.16 + 0.10; // sheer, delicate translucency
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.radius += this.growth;
      this.alpha *= 0.965;
    }

    draw(boost) {
      if (this.alpha <= 0.004) return;
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      const a = Math.min(this.alpha * boost, 0.32);
      const grad = ctx.createRadialGradient(
        this.x, this.y, 0,
        this.x, this.y, Math.max(this.radius, 1)
      );
      grad.addColorStop(0, `rgba(235, 245, 255, ${a})`);
      grad.addColorStop(0.5, `rgba(205, 230, 250, ${a * 0.45})`);
      grad.addColorStop(1, 'rgba(180, 220, 245, 0)');

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  // --------------------------------------------------------------------------
  // 3. WINDBLOWN SPINDRIFT (Thin wisps off wave crests)
  // --------------------------------------------------------------------------
  class SpindriftWisp {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.vx = Math.random() * 4.5 + 3.2; // gale drift
      this.vy = -(Math.random() * 0.6 + 0.15);
      this.alpha = Math.random() * 0.24 + 0.12;
      this.length = Math.random() * 10 + 6;
      this.width = Math.random() * 0.8 + 0.5; // ultra fine
      this.life = Math.random() * 28 + 18;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.alpha -= 0.015;
      this.life--;
    }

    draw(boost) {
      if (this.alpha <= 0 || this.life <= 0) return;
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      const a = Math.min(this.alpha * boost, 0.55);
      ctx.strokeStyle = `rgba(225, 240, 255, ${a})`;
      ctx.lineWidth = this.width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(this.x + this.length, this.y + this.vy * 1.5);
      ctx.stroke();
      ctx.restore();
    }
  }

  // --------------------------------------------------------------------------
  // 4. LIVING FOAM BREATHING (Seamlessly blended over the real picture)
  // --------------------------------------------------------------------------
  function renderBlendedFoamBreathing(time, boost) {
    ctx.save();
    ctx.globalCompositeOperation = 'screen';

    // 1. Foam surge at the lighthouse cliff base (where wave smashes in the painting)
    // Coords in painting: x ~ 31% to 38%, y ~ 50% to 58%
    const cliffPulse = (Math.sin(time * 1.6) * 0.5 + 0.5) * 0.12;
    const cliffGrad = ctx.createRadialGradient(
      width * 0.34, height * 0.54, 0,
      width * 0.34, height * 0.54, width * 0.09
    );
    cliffGrad.addColorStop(0, `rgba(230, 245, 255, ${(0.12 + cliffPulse) * boost})`);
    cliffGrad.addColorStop(0.55, `rgba(185, 225, 250, ${(0.05 + cliffPulse * 0.5) * boost})`);
    cliffGrad.addColorStop(1, 'rgba(180, 220, 245, 0)');
    ctx.fillStyle = cliffGrad;
    ctx.beginPath();
    ctx.ellipse(width * 0.34, height * 0.54, width * 0.09, height * 0.05, 0.04, 0, Math.PI * 2);
    ctx.fill();

    // 2. Soft horizontal breaker wave glow across the mid ocean
    const wavePulse1 = (Math.sin(time * 1.1) * 0.5 + 0.5) * 0.08;
    const waveGrad1 = ctx.createLinearGradient(0, height * 0.59, 0, height * 0.67);
    waveGrad1.addColorStop(0, 'rgba(215, 238, 255, 0)');
    waveGrad1.addColorStop(0.5, `rgba(225, 245, 255, ${(0.07 + wavePulse1) * boost})`);
    waveGrad1.addColorStop(1, 'rgba(215, 238, 255, 0)');
    ctx.fillStyle = waveGrad1;
    ctx.fillRect(width * 0.16, height * 0.59, width * 0.72, height * 0.08);

    // 3. Foreground reef foam wash
    const wavePulse2 = (Math.cos(time * 0.85) * 0.5 + 0.5) * 0.06;
    const waveGrad2 = ctx.createLinearGradient(0, height * 0.76, 0, height * 0.85);
    waveGrad2.addColorStop(0, 'rgba(215, 238, 255, 0)');
    waveGrad2.addColorStop(0.5, `rgba(220, 242, 255, ${(0.05 + wavePulse2) * boost})`);
    waveGrad2.addColorStop(1, 'rgba(215, 238, 255, 0)');
    ctx.fillStyle = waveGrad2;
    ctx.fillRect(width * 0.08, height * 0.76, width * 0.86, height * 0.09);

    ctx.restore();
  }

  // --------------------------------------------------------------------------
  // 5. THIN SPLASH TRIGGERS
  // --------------------------------------------------------------------------
  function triggerCliffBreakerSplash() {
    // Exact cliff base in the painting: ~32% to 35% width, ~52% height
    const originX = width * 0.335 + (Math.random() * 16 - 8);
    const originY = height * 0.525 + (Math.random() * 8 - 4);

    // 22-35 thin, fine splash particles
    const count = Math.floor(Math.random() * 14 + 22);
    for (let i = 0; i < count; i++) {
      splashParticles.push(new ThinSplashParticle(originX, originY, Math.random() * 0.6 + 0.8));
    }

    // 2 sheer mist vapor clouds
    for (let i = 0; i < 2; i++) {
      const ox = originX + (Math.random() * 14 - 7);
      const oy = originY + (Math.random() * 8 - 6);
      mistClouds.push(new SeaSprayMist(ox, oy, Math.random() * 16 + 24));
    }
  }

  // --------------------------------------------------------------------------
  // 6. DELICATE STORM RAIN
  // --------------------------------------------------------------------------
  class Raindrop {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 250) - 100;
      this.y = initial ? Math.random() * height : -20;
      this.speed = Math.random() * 7 + 11;
      this.length = Math.random() * 14 + 12;
      this.angle = 0.22; // subtle storm wind slant
      this.alpha = Math.random() * 0.22 + 0.12; // soft, non-intrusive
      this.width = Math.random() * 0.6 + 0.5; // very thin line
    }

    update() {
      this.x += Math.sin(this.angle) * this.speed;
      this.y += Math.cos(this.angle) * this.speed;

      // When reaching ocean zone
      if (this.y > height * 0.55 + Math.random() * (height * 0.42)) {
        if (Math.random() < 0.08) {
          ripples.push(new Ripple(this.x, this.y));
        }
        this.reset();
      }

      if (this.x > width + 100 || this.y > height + 20) {
        this.reset();
      }
    }

    draw(boost) {
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.65);
      ctx.strokeStyle = `rgba(215, 235, 255, ${a})`;
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

  class Ripple {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.radius = 1;
      this.maxRadius = Math.random() * 6 + 3;
      this.alpha = 0.32;
      this.growth = Math.random() * 0.35 + 0.25;
    }

    update() {
      this.radius += this.growth;
      this.alpha -= 0.024;
    }

    draw(boost) {
      if (this.alpha <= 0) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.55);
      ctx.strokeStyle = `rgba(186, 230, 253, ${a})`;
      ctx.lineWidth = 0.8;
      ctx.beginPath();
      ctx.ellipse(this.x, this.y, this.radius * 2.0, this.radius * 0.6, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }
  }

  function initRain() {
    const count = Math.min(Math.floor((width * height) / 5200), 130);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new Raindrop());
    }
  }

  // --------------------------------------------------------------------------
  // 7. RENDER & TIMING LOOP
  // --------------------------------------------------------------------------
  function updateEvents() {
    const now = Date.now();

    // Soft Ambient Lightning
    if (now - lastFlashTime > (Math.random() * 5000 + 6000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.18 + 0.07;
    }

    // Gentle rhythmic breaker collision (every 2.6 - 3.8s)
    if (now > nextLighthouseBreaker) {
      triggerCliffBreakerSplash();
      nextLighthouseBreaker = now + (Math.random() * 1200 + 2600);
    }

    // Occasional continuous micro-spray from wave crests
    if (Math.random() < 0.25) {
      const sprayX = width * 0.33 + (Math.random() * 20 - 10);
      const sprayY = height * 0.53 + (Math.random() * 6 - 3);
      splashParticles.push(new ThinSplashParticle(sprayX, sprayY, 0.7));
    }

    // Occasional windblown spindrift wisp along mid breaker
    if (Math.random() < 0.07) {
      const sx = Math.random() * (width * 0.6) + (width * 0.25);
      const sy = height * (Math.random() * 0.16 + 0.58);
      spindriftWisps.push(new SpindriftWisp(sx, sy));
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);
    simTime += 0.022;

    updateEvents();

    // Soft Ambient Lightning calculation
    ambientFlashAlpha += (targetFlash - ambientFlashAlpha) * 0.08;
    if (targetFlash > 0 && Math.abs(targetFlash - ambientFlashAlpha) < 0.01) {
      targetFlash = 0;
    }
    const flashBoost = 1 + ambientFlashAlpha * 2.2;

    // Ambient cloud flash
    if (ambientFlashAlpha > 0.005) {
      ctx.fillStyle = `rgba(195, 210, 245, ${ambientFlashAlpha * 0.8})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 1. Living Foam Breathing (Blended directly over painting's foam)
    renderBlendedFoamBreathing(simTime, flashBoost);

    // 2. Sheer Sea Spray Mist Puffs
    for (let i = mistClouds.length - 1; i >= 0; i--) {
      mistClouds[i].update();
      mistClouds[i].draw(flashBoost);
      if (mistClouds[i].alpha <= 0.004) {
        mistClouds.splice(i, 1);
      }
    }

    // 3. Thin Splash Micro-Droplets
    for (let i = splashParticles.length - 1; i >= 0; i--) {
      splashParticles[i].update();
      splashParticles[i].draw(flashBoost);
      if (splashParticles[i].alpha <= 0 || splashParticles[i].life <= 0) {
        splashParticles.splice(i, 1);
      }
    }

    // 4. Windblown Spindrift Wisps
    for (let i = spindriftWisps.length - 1; i >= 0; i--) {
      spindriftWisps[i].update();
      spindriftWisps[i].draw(flashBoost);
      if (spindriftWisps[i].alpha <= 0 || spindriftWisps[i].life <= 0) {
        spindriftWisps.splice(i, 1);
      }
    }

    // 5. Water Ripples
    for (let i = ripples.length - 1; i >= 0; i--) {
      ripples[i].update();
      ripples[i].draw(flashBoost);
      if (ripples[i].alpha <= 0) {
        ripples.splice(i, 1);
      }
    }

    // 6. Delicate Raindrops
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flashBoost);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
