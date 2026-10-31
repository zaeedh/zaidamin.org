/**
 * Realistic Ocean Wave Storm & Splash Engine
 * Lighthouse Storm Banner for Dr. Zaid Amin (zaidamin.org)
 * 
 * Features:
 * - Fluid Trochoidal Wave Swells & Foamy Breakers moving across the sea
 * - Dynamic Lighthouse Cliff Splashes (explosive breaker impact, spray droplets, mist)
 * - Foreground Reef Breakers & Churning Foamy Backwash
 * - Windblown Spindrift (sea spray whipping off crests)
 * - Realistic Slanted Storm Rain with dynamic ocean surface collision
 * - Ambient Lightning illumination that reflects realistically off churning water
 * - Silky smooth 60 FPS canvas performance
 */

(function() {
  const canvas = document.getElementById('rain-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = 0;
  let height = 0;
  let time = 0;

  // Pools
  let raindrops = [];
  let ripples = [];
  let splashParticles = [];
  let mistClouds = [];
  let spindriftParticles = [];

  // Lighting
  let ambientFlashAlpha = 0;
  let targetFlash = 0;
  let lastFlashTime = Date.now();

  // Lighthouse Splash Timer
  let nextLighthouseSplash = 0;

  function resize() {
    const parent = canvas.parentElement;
    width = canvas.width = parent.clientWidth;
    height = canvas.height = parent.clientHeight;
    initRain();
  }

  window.addEventListener('resize', resize);

  // --------------------------------------------------------------------------
  // 1. WAVE HEIGHT MATHEMATICAL MODELS
  // --------------------------------------------------------------------------
  // Distant swells (Horizon to mid ocean, y ~ 0.44H to 0.56H)
  function getBackWaveY(x, t) {
    const baseY = height * 0.49;
    const s1 = Math.sin(x * 0.007 + t * 0.8) * 4.5;
    const s2 = Math.cos(x * 0.013 - t * 0.6) * 3.0;
    const s3 = Math.sin(x * 0.021 + t * 1.2) * 2.0;
    return baseY + s1 + s2 + s3;
  }

  // Main Middle Breaker (The big rolling foamy wave in center, y ~ 0.58H to 0.72H)
  function getMidWaveY(x, t) {
    const baseY = height * 0.63;
    // Trochoidal sharpening via sin^3 for steep peaked crests
    const wave1 = Math.sin(x * 0.0055 - t * 1.1);
    const sharp1 = Math.pow(Math.abs(wave1), 1.6) * Math.sign(wave1) * 11.0;
    const wave2 = Math.sin(x * 0.012 + t * 0.75) * 5.0;
    const wave3 = Math.cos(x * 0.022 - t * 1.4) * 3.5;
    // Local swell near the lighthouse cliff (x ~ 0.3W)
    const distFromCliff = Math.abs(x - width * 0.32);
    const cliffSwell = Math.exp(-distFromCliff / (width * 0.14)) * Math.sin(t * 1.8) * 8.0;
    return baseY + sharp1 + wave2 + wave3 - cliffSwell;
  }

  // Foreground Shore Surge (Turbulent rocky reef wash, y ~ 0.74H to 0.95H)
  function getForeWaveY(x, t) {
    const baseY = height * 0.81;
    const s1 = Math.sin(x * 0.006 - t * 1.3) * 10.0;
    const s2 = Math.cos(x * 0.014 + t * 0.9) * 6.0;
    const s3 = Math.sin(x * 0.028 - t * 1.7) * 4.0;
    return baseY + s1 + s2 + s3;
  }

  // Global ocean surface height for rain collision
  function getSurfaceY(x, t) {
    return Math.min(getForeWaveY(x, t), getMidWaveY(x, t) + 20);
  }

  // --------------------------------------------------------------------------
  // 2. SPLASH & MIST PARTICLE CLASSES
  // --------------------------------------------------------------------------
  class SplashDrop {
    constructor(x, y, vx, vy, size, alpha = 0.9) {
      this.x = x;
      this.y = y;
      this.vx = vx;
      this.vy = vy;
      this.size = size;
      this.alpha = alpha;
      this.decay = Math.random() * 0.018 + 0.012;
      this.gravity = 0.22;
      this.wind = 0.08;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.vy += this.gravity;
      this.vx += this.wind; // wind blows spray rightward
      this.vx *= 0.985;     // air resistance
      this.alpha -= this.decay;
    }

    draw(boost) {
      if (this.alpha <= 0) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 1);
      ctx.fillStyle = `rgba(235, 245, 255, ${a})`;
      ctx.beginPath();
      // Slightly elongated droplet in motion direction
      const angle = Math.atan2(this.vy, this.vx);
      const len = Math.min(Math.hypot(this.vx, this.vy) * 0.6, 6);
      ctx.ellipse(this.x, this.y, this.size + len * 0.5, this.size, angle, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  class MistCloud {
    constructor(x, y, radius, maxRadius, alpha = 0.35) {
      this.x = x;
      this.y = y;
      this.radius = radius;
      this.maxRadius = maxRadius;
      this.alpha = alpha;
      this.growth = (maxRadius - radius) / (Math.random() * 25 + 30);
      this.vx = Math.random() * 1.5 + 0.8; // drifts right with storm wind
      this.vy = -(Math.random() * 0.8 + 0.4); // drifts slightly up
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.radius += this.growth;
      this.alpha *= 0.955;
    }

    draw(boost) {
      if (this.alpha <= 0.01) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.6);
      const grad = ctx.createRadialGradient(
        this.x, this.y, 0,
        this.x, this.y, Math.max(this.radius, 1)
      );
      grad.addColorStop(0, `rgba(240, 248, 255, ${a})`);
      grad.addColorStop(0.5, `rgba(215, 235, 250, ${a * 0.5})`);
      grad.addColorStop(1, 'rgba(200, 230, 250, 0)');

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  class Spindrift {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.vx = Math.random() * 5 + 4; // fast gale drift
      this.vy = -(Math.random() * 1.2 + 0.2);
      this.alpha = Math.random() * 0.45 + 0.25;
      this.size = Math.random() * 1.4 + 0.8;
      this.length = Math.random() * 8 + 6;
      this.life = Math.random() * 30 + 20;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.alpha -= 0.016;
      this.life--;
    }

    draw(boost) {
      if (this.alpha <= 0 || this.life <= 0) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.8);
      ctx.strokeStyle = `rgba(224, 242, 254, ${a})`;
      ctx.lineWidth = this.size;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(this.x + this.length, this.y + this.vy * 2);
      ctx.stroke();
      ctx.restore();
    }
  }

  // --------------------------------------------------------------------------
  // 3. EXPLOSIVE BREAKER & CLIFF SMASH SYSTEM
  // --------------------------------------------------------------------------
  function triggerLighthouseSmash() {
    // Lighthouse base rocks located at ~31.8% width, ~50% height
    const impactX = width * 0.318 + (Math.random() * 20 - 10);
    const impactY = height * 0.505 + (Math.random() * 12 - 6);

    // 1. High Velocity Splash Droplet Eruption (50-70 droplets)
    const count = Math.floor(Math.random() * 25 + 50);
    for (let i = 0; i < count; i++) {
      // Fan out upwards, biased downwind to the right
      const angle = -(Math.PI * 0.25 + Math.random() * Math.PI * 0.55);
      const speed = Math.random() * 9 + 4;
      const vx = Math.cos(angle) * speed + (Math.random() * 2 + 1);
      const vy = Math.sin(angle) * speed;
      const size = Math.random() * 2.2 + 1.2;
      splashParticles.push(new SplashDrop(impactX, impactY, vx, vy, size, 0.95));
    }

    // 2. Rising Sea Spray Mist Clouds (4-6 clouds)
    for (let i = 0; i < 5; i++) {
      const offsetX = impactX + (Math.random() * 24 - 12);
      const offsetY = impactY + (Math.random() * 14 - 10);
      const initR = Math.random() * 10 + 8;
      const maxR = Math.random() * 28 + 35;
      mistClouds.push(new MistCloud(offsetX, offsetY, initR, maxR, 0.42));
    }
  }

  function triggerRockSplash(x, y, intensity = 1) {
    const count = Math.floor(intensity * 12 + 6);
    for (let i = 0; i < count; i++) {
      const angle = -(Math.PI * 0.2 + Math.random() * Math.PI * 0.6);
      const speed = Math.random() * 5 + 2.5;
      const vx = Math.cos(angle) * speed + 0.8;
      const vy = Math.sin(angle) * speed;
      splashParticles.push(new SplashDrop(x, y, vx, vy, Math.random() * 1.6 + 0.8, 0.75));
    }
  }

  // --------------------------------------------------------------------------
  // 4. RAINDROP & IMPACT RIPPLE ENGINE
  // --------------------------------------------------------------------------
  class Raindrop {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 250) - 100;
      this.y = initial ? Math.random() * height : -20;
      this.speed = Math.random() * 9 + 13;
      this.length = Math.random() * 16 + 14;
      this.angle = 0.22; // subtle storm wind angle
      this.alpha = Math.random() * 0.32 + 0.18;
      this.width = Math.random() * 1.1 + 0.6;
    }

    update() {
      this.x += Math.sin(this.angle) * this.speed;
      this.y += Math.cos(this.angle) * this.speed;

      // Check collision with dynamic moving ocean wave surface
      const waterY = getSurfaceY(this.x, time);
      if (this.y >= waterY) {
        if (Math.random() < 0.25) {
          ripples.push(new Ripple(this.x, waterY));
        }
        if (Math.random() < 0.08) {
          // Micro splash droplet on wave impact
          splashParticles.push(new SplashDrop(
            this.x, waterY,
            (Math.random() - 0.5) * 2 + 0.5,
            -(Math.random() * 2.5 + 1.2),
            0.9, 0.6
          ));
        }
        this.reset();
      }

      if (this.x > width + 100 || this.y > height + 20) {
        this.reset();
      }
    }

    draw(boost) {
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.9);
      ctx.strokeStyle = `rgba(220, 238, 255, ${a})`;
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
      this.maxRadius = Math.random() * 9 + 5;
      this.alpha = 0.45;
      this.growth = Math.random() * 0.45 + 0.35;
    }

    update() {
      this.radius += this.growth;
      this.alpha -= 0.024;
    }

    draw(boost) {
      if (this.alpha <= 0) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.8);
      ctx.strokeStyle = `rgba(186, 230, 253, ${a})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.ellipse(this.x, this.y, this.radius * 2.2, this.radius * 0.65, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }
  }

  function initRain() {
    const count = Math.min(Math.floor((width * height) / 4800), 160);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new Raindrop());
    }
  }

  // --------------------------------------------------------------------------
  // 5. WAVE MESH RENDERING (SURGING SWELLS, BREAKER CRESTS & FOAM)
  // --------------------------------------------------------------------------

  // Layer A: Distant Swells (Smooth undulation across the horizon)
  function renderBackWave(boost) {
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(0, height);

    const step = 20;
    for (let x = 0; x <= width + step; x += step) {
      const y = getBackWaveY(x, time);
      ctx.lineTo(x, y);
    }

    ctx.lineTo(width, height);
    ctx.closePath();

    // Translucent dark teal ocean gradient
    const grad = ctx.createLinearGradient(0, height * 0.46, 0, height * 0.65);
    grad.addColorStop(0, 'rgba(12, 28, 44, 0.28)');
    grad.addColorStop(1, 'rgba(6, 16, 28, 0.45)');
    ctx.fillStyle = grad;
    ctx.fill();

    // Crest highlight line
    ctx.beginPath();
    for (let x = 0; x <= width + step; x += step) {
      const y = getBackWaveY(x, time);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = `rgba(186, 230, 253, ${0.18 * boost})`;
    ctx.lineWidth = 1.2;
    ctx.stroke();
    ctx.restore();
  }

  // Layer B: Midground Breaker Wave (The dominant crashing surge)
  function renderMidBreaker(boost) {
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(0, height);

    const step = 14;
    for (let x = 0; x <= width + step; x += step) {
      const y = getMidWaveY(x, time);
      ctx.lineTo(x, y);
    }

    ctx.lineTo(width, height);
    ctx.closePath();

    // Deep stormy ocean body
    const grad = ctx.createLinearGradient(0, height * 0.55, 0, height * 0.78);
    grad.addColorStop(0, 'rgba(14, 38, 62, 0.38)');
    grad.addColorStop(0.4, 'rgba(10, 26, 44, 0.50)');
    grad.addColorStop(1, 'rgba(4, 12, 22, 0.62)');
    ctx.fillStyle = grad;
    ctx.fill();

    // Luminous foaming crest line
    ctx.beginPath();
    for (let x = 0; x <= width + step; x += step) {
      const y = getMidWaveY(x, time);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = `rgba(224, 242, 254, ${0.45 * boost})`;
    ctx.lineWidth = 2.4;
    ctx.stroke();

    // Foam curls and frothing whitecaps along the crest
    for (let x = 0; x <= width; x += 32) {
      const y = getMidWaveY(x, time);
      const curlOffset = Math.sin(x * 0.05 + time * 3) * 3;
      const foamSize = Math.sin(x * 0.02 - time * 2) * 5 + 7;
      
      ctx.fillStyle = `rgba(240, 249, 255, ${0.35 * boost})`;
      ctx.beginPath();
      ctx.ellipse(x, y + curlOffset, foamSize * 1.8, foamSize * 0.55, 0.1, 0, Math.PI * 2);
      ctx.fill();

      // Chance to whip spindrift off high wave crests
      if (Math.random() < 0.06 && foamSize > 9) {
        spindriftParticles.push(new Spindrift(x, y - 2));
      }
    }

    ctx.restore();
  }

  // Layer C: Foreground Shore Surge & Churning Foamy Reef Wash
  function renderForeSurge(boost) {
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(0, height);

    const step = 16;
    for (let x = 0; x <= width + step; x += step) {
      const y = getForeWaveY(x, time);
      ctx.lineTo(x, y);
    }

    ctx.lineTo(width, height);
    ctx.closePath();

    const grad = ctx.createLinearGradient(0, height * 0.72, 0, height);
    grad.addColorStop(0, 'rgba(18, 54, 82, 0.32)');
    grad.addColorStop(0.6, 'rgba(8, 22, 36, 0.52)');
    grad.addColorStop(1, 'rgba(3, 8, 16, 0.70)');
    ctx.fillStyle = grad;
    ctx.fill();

    // Frothy edge wash over rocks
    ctx.beginPath();
    for (let x = 0; x <= width + step; x += step) {
      const y = getForeWaveY(x, time);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = `rgba(235, 248, 255, ${0.55 * boost})`;
    ctx.lineWidth = 2.0;
    ctx.stroke();

    // Floating lace foam patches across foreground water
    for (let x = 20; x < width; x += 45) {
      const y = getForeWaveY(x, time) + 12 + Math.sin(x * 0.03 + time) * 8;
      if (y < height) {
        const patchW = Math.sin(x * 0.04 - time) * 8 + 16;
        const patchH = Math.cos(x * 0.03 + time * 1.5) * 3 + 5;
        ctx.fillStyle = `rgba(215, 238, 255, ${0.28 * boost})`;
        ctx.beginPath();
        ctx.ellipse(x, y, patchW, patchH, 0.05, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    ctx.restore();
  }

  // --------------------------------------------------------------------------
  // 6. MAIN ANIMATION LOOP
  // --------------------------------------------------------------------------
  function checkLightingAndSplashes() {
    const now = Date.now();

    // Ambient Lightning
    if (now - lastFlashTime > (Math.random() * 5000 + 6000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.22 + 0.08;
    }

    // Periodic Lighthouse Cliff Breaker Collision (every 2.5 - 3.6 seconds)
    if (now > nextLighthouseSplash) {
      triggerLighthouseSmash();
      nextLighthouseSplash = now + (Math.random() * 1100 + 2500);
    }

    // Occasional foreground reef splash
    if (Math.random() < 0.04) {
      const rockX = width * (Math.random() * 0.8 + 0.1);
      const rockY = getForeWaveY(rockX, time) + 4;
      triggerRockSplash(rockX, rockY, Math.random() * 0.8 + 0.4);
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);
    time += 0.022; // smooth wave phase increment

    checkLightingAndSplashes();

    // 1. Soft Ambient Lightning
    ambientFlashAlpha += (targetFlash - ambientFlashAlpha) * 0.08;
    if (targetFlash > 0 && Math.abs(targetFlash - ambientFlashAlpha) < 0.01) {
      targetFlash = 0;
    }
    const flashBoost = 1 + ambientFlashAlpha * 2.8;

    if (ambientFlashAlpha > 0.005) {
      ctx.fillStyle = `rgba(192, 210, 245, ${ambientFlashAlpha})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 2. Render Moving Ocean Waves (Distant -> Mid Breaker -> Fore Surge)
    renderBackWave(flashBoost);
    renderMidBreaker(flashBoost);
    renderForeSurge(flashBoost);

    // 3. Render Spindrift Particles (Windblown sea spray)
    for (let i = spindriftParticles.length - 1; i >= 0; i--) {
      spindriftParticles[i].update();
      spindriftParticles[i].draw(flashBoost);
      if (spindriftParticles[i].alpha <= 0 || spindriftParticles[i].life <= 0) {
        spindriftParticles.splice(i, 1);
      }
    }

    // 4. Render Mist Clouds (Expanding sea spray vapor from impacts)
    for (let i = mistClouds.length - 1; i >= 0; i--) {
      mistClouds[i].update();
      mistClouds[i].draw(flashBoost);
      if (mistClouds[i].alpha <= 0.01) {
        mistClouds.splice(i, 1);
      }
    }

    // 5. Render Splash Droplets (Lighthouse & rock impact explosions)
    for (let i = splashParticles.length - 1; i >= 0; i--) {
      splashParticles[i].update();
      splashParticles[i].draw(flashBoost);
      if (splashParticles[i].alpha <= 0 || splashParticles[i].y > height + 20) {
        splashParticles.splice(i, 1);
      }
    }

    // 6. Render Ripples on Water
    for (let i = ripples.length - 1; i >= 0; i--) {
      ripples[i].update();
      ripples[i].draw(flashBoost);
      if (ripples[i].alpha <= 0) {
        ripples.splice(i, 1);
      }
    }

    // 7. Render Raindrops
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flashBoost);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
