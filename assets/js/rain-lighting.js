/**
 * Cinematic Rotating Lighthouse Beacon & Atmospheric Storm Rain Engine
 * For Dr. Zaid Amin (zaidamin.org)
 * 
 * Features:
 * 1. 3D Rotating Lighthouse Beacon:
 *    - Sweeps out across the dark ocean waves with a volumetric conical beam.
 *    - Rotates towards the viewer: erupts into a soft, dazzling lens flare & warm eye-splash bloom.
 *    - Rotates away from the viewer: flare dissolves and beam sweeps back out over the ocean.
 * 2. Soft, Multi-Layered Storm Rain:
 *    - 420+ delicate, whisper-thin raindrops across 3 depth tiers (mist veil, driving rain, foreground streaks).
 *    - Dynamic storm wind gusting: rain angle and speed sway in breathing waves, following the storm.
 *    - Raindrops catch golden glints when illuminated by the sweeping lighthouse beam.
 * 3. Thin Sea Spray & Living Foam:
 *    - Ultra-fine micro-droplets and sheer vapor mist at the lighthouse cliff base.
 *    - Breathing foam luminosity blended with screen mode over the real painting.
 * 4. Silky smooth 60 FPS performance, fully responsive.
 */

(function() {
  const canvas = document.getElementById('rain-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = 0;
  let height = 0;
  let simTime = 0;

  // Pools
  let raindrops = [];
  let splashParticles = [];
  let mistClouds = [];
  let spindriftWisps = [];
  let ripples = [];

  // Wind & Storm Dynamics
  let currentWindAngle = 0.24;
  let windGustFactor = 1.0;

  // Ambient Lightning
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

  // ==========================================================================
  // 1. ROTATING LIGHTHOUSE BEACON & EYE-SPLASH BLOOM ENGINE
  // ==========================================================================
  const beacon = {
    // Exact lantern room in lighthouse-banner.jpg
    get lx() { return width * 0.318; },
    get ly() { return height * 0.262; },
    angle: 0.2, // rotational phase
    speed: 0.0135, // majestic revolution ~7.5 seconds per 360 deg

    update() {
      this.angle += this.speed;
      if (this.angle > Math.PI * 2) {
        this.angle -= Math.PI * 2;
      }
    },

    draw(flashBoost) {
      const lx = this.lx;
      const ly = this.ly;

      // 3D Direction Cosines:
      // facingOcean: peaks when beam is pointing right (towards +X, out to ocean)
      // facingViewer: peaks when beam points at viewer (+Z, "splash into my eyes")
      const facingOcean = Math.cos(this.angle);
      const facingViewer = Math.sin(this.angle);

      ctx.save();

      // ----------------------------------------------------------------------
      // A. Steady Base Lantern Glow (Warm filament core)
      // ----------------------------------------------------------------------
      const baseCoreGrad = ctx.createRadialGradient(lx, ly, 0, lx, ly, 18);
      baseCoreGrad.addColorStop(0, 'rgba(255, 255, 245, 0.95)');
      baseCoreGrad.addColorStop(0.3, 'rgba(254, 240, 138, 0.7)');
      baseCoreGrad.addColorStop(0.7, 'rgba(234, 179, 8, 0.3)');
      baseCoreGrad.addColorStop(1, 'rgba(234, 179, 8, 0)');

      ctx.globalCompositeOperation = 'screen';
      ctx.fillStyle = baseCoreGrad;
      ctx.beginPath();
      ctx.arc(lx, ly, 18, 0, Math.PI * 2);
      ctx.fill();

      // ----------------------------------------------------------------------
      // B. Volumetric Beam Sweeping Across the Ocean (facingOcean > 0)
      // ----------------------------------------------------------------------
      if (facingOcean > 0.02) {
        const beamIntensity = Math.pow(facingOcean, 1.35) * flashBoost;
        const beamLength = width * 0.75;
        
        // Gentle vertical wobble as beam rotates
        const beamPitch = 0.02 + Math.sin(this.angle * 2) * 0.015;
        const endY = ly + Math.sin(beamPitch) * beamLength;
        const beamHalfWidth = 24 + facingOcean * 12;

        const p1x = lx;
        const p1y = ly - 3;
        const p2x = lx;
        const p2y = ly + 3;
        const p3x = lx + beamLength;
        const p3y = endY + beamHalfWidth;
        const p4x = lx + beamLength;
        const p4y = endY - beamHalfWidth;

        // Conical volumetric gradient
        const beamGrad = ctx.createLinearGradient(lx, ly, lx + beamLength, endY);
        beamGrad.addColorStop(0, `rgba(255, 250, 225, ${0.75 * beamIntensity})`);
        beamGrad.addColorStop(0.15, `rgba(254, 240, 138, ${0.45 * beamIntensity})`);
        beamGrad.addColorStop(0.55, `rgba(186, 230, 253, ${0.15 * beamIntensity})`);
        beamGrad.addColorStop(1, 'rgba(186, 230, 253, 0)');

        ctx.fillStyle = beamGrad;
        ctx.beginPath();
        ctx.moveTo(p1x, p1y);
        ctx.lineTo(p4x, p4y);
        ctx.lineTo(p3x, p3y);
        ctx.lineTo(p2x, p2y);
        ctx.closePath();
        ctx.fill();

        // Soft outer feathered beam aura
        const auraGrad = ctx.createLinearGradient(lx, ly, lx + beamLength * 0.7, endY);
        auraGrad.addColorStop(0, `rgba(253, 224, 71, ${0.35 * beamIntensity})`);
        auraGrad.addColorStop(0.6, `rgba(147, 197, 253, ${0.08 * beamIntensity})`);
        auraGrad.addColorStop(1, 'rgba(147, 197, 253, 0)');

        ctx.fillStyle = auraGrad;
        ctx.beginPath();
        ctx.moveTo(p1x, p1y - 6);
        ctx.lineTo(p4x, p4y - 14);
        ctx.lineTo(p3x, p3y + 14);
        ctx.lineTo(p2x, p2y + 6);
        ctx.closePath();
        ctx.fill();
      }

      // ----------------------------------------------------------------------
      // C. "Splash into My Eyes" Lens Flare & Eye Bloom (facingViewer > 0)
      // ----------------------------------------------------------------------
      if (facingViewer > 0.05) {
        // High exponent creates realistic sharp peaking optical bloom
        const eyeSplash = Math.pow(facingViewer, 3.2);
        const flareAlpha = Math.min(eyeSplash * flashBoost, 1.0);

        // 1. Full-Banner Atmospheric Eye Bloom (soft warm wash over viewer)
        const eyeWashGrad = ctx.createRadialGradient(lx, ly, 10, lx, ly, Math.max(width, height) * 0.75);
        eyeWashGrad.addColorStop(0, `rgba(255, 250, 220, ${0.22 * flareAlpha})`);
        eyeWashGrad.addColorStop(0.35, `rgba(253, 224, 71, ${0.09 * flareAlpha})`);
        eyeWashGrad.addColorStop(0.7, `rgba(186, 230, 253, ${0.03 * flareAlpha})`);
        eyeWashGrad.addColorStop(1, 'rgba(186, 230, 253, 0)');

        ctx.fillStyle = eyeWashGrad;
        ctx.fillRect(0, 0, width, height);

        // 2. Large Radiant Lens Flare Corona
        const flareRadius = 80 + eyeSplash * 70;
        const coronaGrad = ctx.createRadialGradient(lx, ly, 0, lx, ly, flareRadius);
        coronaGrad.addColorStop(0, `rgba(255, 255, 255, ${0.95 * flareAlpha})`);
        coronaGrad.addColorStop(0.2, `rgba(255, 245, 180, ${0.75 * flareAlpha})`);
        coronaGrad.addColorStop(0.5, `rgba(251, 191, 36, ${0.35 * flareAlpha})`);
        coronaGrad.addColorStop(0.8, `rgba(147, 197, 253, ${0.12 * flareAlpha})`);
        coronaGrad.addColorStop(1, 'rgba(147, 197, 253, 0)');

        ctx.fillStyle = coronaGrad;
        ctx.beginPath();
        ctx.arc(lx, ly, flareRadius, 0, Math.PI * 2);
        ctx.fill();

        // 3. Anamorphic Horizontal Glare Streak (Cinematic flare across lens)
        const streakLength = 120 + eyeSplash * 180;
        const streakHeight = 2.5 + eyeSplash * 2.5;
        const streakGrad = ctx.createLinearGradient(lx - streakLength, ly, lx + streakLength, ly);
        streakGrad.addColorStop(0, 'rgba(255, 255, 255, 0)');
        streakGrad.addColorStop(0.35, `rgba(186, 230, 253, ${0.35 * flareAlpha})`);
        streakGrad.addColorStop(0.5, `rgba(255, 255, 255, ${0.90 * flareAlpha})`);
        streakGrad.addColorStop(0.65, `rgba(186, 230, 253, ${0.35 * flareAlpha})`);
        streakGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.fillStyle = streakGrad;
        ctx.beginPath();
        ctx.ellipse(lx, ly, streakLength, streakHeight, 0, 0, Math.PI * 2);
        ctx.fill();

        // 4. Brilliant White Filament Hotspot
        ctx.fillStyle = `rgba(255, 255, 255, ${0.98 * flareAlpha})`;
        ctx.beginPath();
        ctx.arc(lx, ly, 5 + eyeSplash * 3, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.restore();
    }
  };

  // ==========================================================================
  // 2. SOFT, DENSE, WIND-SWAYING STORM RAIN ENGINE
  // ==========================================================================
  class Raindrop {
    constructor() {
      // 3 Depth Tiers:
      // 0 = Distant mist veil (slow, faint, ultra thin)
      // 1 = Midground driving rain (steady gale sheets)
      // 2 = Foreground fast streaks (motion blurred)
      const r = Math.random();
      if (r < 0.50) {
        this.tier = 0;
        this.baseSpeed = Math.random() * 4 + 7;
        this.baseLength = Math.random() * 8 + 8;
        this.width = Math.random() * 0.25 + 0.45; // ultra thin mist
        this.baseAlpha = Math.random() * 0.08 + 0.07;
      } else if (r < 0.85) {
        this.tier = 1;
        this.baseSpeed = Math.random() * 5 + 11;
        this.baseLength = Math.random() * 10 + 13;
        this.width = Math.random() * 0.25 + 0.60;
        this.baseAlpha = Math.random() * 0.10 + 0.12;
      } else {
        this.tier = 2;
        this.baseSpeed = Math.random() * 6 + 15;
        this.baseLength = Math.random() * 12 + 18;
        this.width = Math.random() * 0.30 + 0.75;
        this.baseAlpha = Math.random() * 0.12 + 0.18;
      }

      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 300) - 150;
      this.y = initial ? Math.random() * height : -30;
      this.speed = this.baseSpeed * (0.9 + Math.random() * 0.2);
      this.length = this.baseLength;
      this.alpha = this.baseAlpha;
    }

    update() {
      // Rain trajectory sways dynamically with current storm wind gusts
      const vx = Math.sin(currentWindAngle) * this.speed * windGustFactor;
      const vy = Math.cos(currentWindAngle) * this.speed;

      this.x += vx;
      this.y += vy;

      // Water collision in ocean zone
      if (this.y > height * 0.56 + Math.random() * (height * 0.40)) {
        if (Math.random() < 0.06 && this.tier > 0) {
          ripples.push(new Ripple(this.x, this.y));
        }
        this.reset();
      }

      if (this.x > width + 150 || this.y > height + 30) {
        this.reset();
      }
    }

    draw(flashBoost) {
      ctx.save();

      // Check if raindrop is illuminated by the sweeping lighthouse beam!
      let beamGlint = 1.0;
      const lx = beacon.lx;
      const ly = beacon.ly;
      if (this.x > lx && Math.abs(this.y - ly) < 45) {
        const facingOcean = Math.max(0, Math.cos(beacon.angle));
        beamGlint = 1.0 + facingOcean * 1.8;
      }

      const a = Math.min(this.alpha * flashBoost * beamGlint, 0.75);
      
      // Drops catch subtle golden-white sheen if in lighthouse beam
      if (beamGlint > 1.2) {
        ctx.strokeStyle = `rgba(254, 243, 199, ${a})`;
      } else {
        ctx.strokeStyle = `rgba(215, 235, 255, ${a})`;
      }

      ctx.lineWidth = this.width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(
        this.x + Math.sin(currentWindAngle) * this.length,
        this.y + Math.cos(currentWindAngle) * this.length
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
      this.maxRadius = Math.random() * 5 + 3;
      this.alpha = 0.28;
      this.growth = Math.random() * 0.35 + 0.25;
    }

    update() {
      this.radius += this.growth;
      this.alpha -= 0.024;
    }

    draw(boost) {
      if (this.alpha <= 0) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.5);
      ctx.strokeStyle = `rgba(186, 230, 253, ${a})`;
      ctx.lineWidth = 0.7;
      ctx.beginPath();
      ctx.ellipse(this.x, this.y, this.radius * 2.0, this.radius * 0.6, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }
  }

  function initRain() {
    // Dense storm rain: 420 soft raindrops
    const count = Math.min(Math.floor((width * height) / 1600), 450);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new Raindrop());
    }
  }

  // ==========================================================================
  // 3. THIN SEA SPRAY & LIVING FOAM BREATHING
  // ==========================================================================
  class ThinSplashParticle {
    constructor(originX, originY, power = 1.0) {
      this.x = originX + (Math.random() - 0.5) * 14;
      this.y = originY + (Math.random() - 0.5) * 8;
      const angle = -(Math.PI * 0.28 + Math.random() * Math.PI * 0.44);
      const speed = (Math.random() * 2.4 + 1.1) * power;
      this.vx = Math.cos(angle) * speed + (Math.random() * 0.7 + 0.5);
      this.vy = Math.sin(angle) * speed;
      this.size = Math.random() * 0.6 + 0.5; // whisper thin: 0.5px - 1.1px
      this.alpha = Math.random() * 0.35 + 0.25;
      this.decay = Math.random() * 0.009 + 0.007;
      this.gravity = 0.045;
      this.life = Math.random() * 45 + 35;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.vy += this.gravity;
      this.vx *= 0.988;
      this.alpha -= this.decay;
      this.life--;
    }

    draw(boost) {
      if (this.alpha <= 0 || this.life <= 0) return;
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      const a = Math.min(this.alpha * boost, 0.7);
      ctx.fillStyle = `rgba(230, 245, 255, ${a})`;
      ctx.beginPath();
      const speed = Math.hypot(this.vx, this.vy);
      const angle = Math.atan2(this.vy, this.vx);
      ctx.ellipse(this.x, this.y, this.size + speed * 0.3, this.size * 0.8, angle, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  class SeaSprayMist {
    constructor(x, y, maxRadius = 35) {
      this.x = x;
      this.y = y;
      this.radius = Math.random() * 8 + 6;
      this.maxRadius = maxRadius;
      this.growth = (maxRadius - this.radius) / (Math.random() * 35 + 45);
      this.vx = Math.random() * 0.75 + 0.35;
      this.vy = -(Math.random() * 0.45 + 0.2);
      this.alpha = Math.random() * 0.15 + 0.09;
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
      const a = Math.min(this.alpha * boost, 0.3);
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

  class SpindriftWisp {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.vx = Math.random() * 4.5 + 3.0;
      this.vy = -(Math.random() * 0.5 + 0.15);
      this.alpha = Math.random() * 0.22 + 0.10;
      this.length = Math.random() * 10 + 6;
      this.width = Math.random() * 0.7 + 0.5;
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
      const a = Math.min(this.alpha * boost, 0.5);
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

  function renderBlendedFoamBreathing(time, boost) {
    ctx.save();
    ctx.globalCompositeOperation = 'screen';

    // 1. Foam surge at the lighthouse cliff base
    const cliffPulse = (Math.sin(time * 1.6) * 0.5 + 0.5) * 0.11;
    const cliffGrad = ctx.createRadialGradient(
      width * 0.34, height * 0.54, 0,
      width * 0.34, height * 0.54, width * 0.09
    );
    cliffGrad.addColorStop(0, `rgba(230, 245, 255, ${(0.11 + cliffPulse) * boost})`);
    cliffGrad.addColorStop(0.55, `rgba(185, 225, 250, ${(0.05 + cliffPulse * 0.5) * boost})`);
    cliffGrad.addColorStop(1, 'rgba(180, 220, 245, 0)');
    ctx.fillStyle = cliffGrad;
    ctx.beginPath();
    ctx.ellipse(width * 0.34, height * 0.54, width * 0.09, height * 0.05, 0.04, 0, Math.PI * 2);
    ctx.fill();

    // 2. Soft horizontal breaker wave glow across the mid ocean
    const wavePulse1 = (Math.sin(time * 1.1) * 0.5 + 0.5) * 0.07;
    const waveGrad1 = ctx.createLinearGradient(0, height * 0.59, 0, height * 0.67);
    waveGrad1.addColorStop(0, 'rgba(215, 238, 255, 0)');
    waveGrad1.addColorStop(0.5, `rgba(225, 245, 255, ${(0.06 + wavePulse1) * boost})`);
    waveGrad1.addColorStop(1, 'rgba(215, 238, 255, 0)');
    ctx.fillStyle = waveGrad1;
    ctx.fillRect(width * 0.16, height * 0.59, width * 0.72, height * 0.08);

    // 3. Foreground reef foam wash
    const wavePulse2 = (Math.cos(time * 0.85) * 0.5 + 0.5) * 0.05;
    const waveGrad2 = ctx.createLinearGradient(0, height * 0.76, 0, height * 0.85);
    waveGrad2.addColorStop(0, 'rgba(215, 238, 255, 0)');
    waveGrad2.addColorStop(0.5, `rgba(220, 242, 255, ${(0.04 + wavePulse2) * boost})`);
    waveGrad2.addColorStop(1, 'rgba(215, 238, 255, 0)');
    ctx.fillStyle = waveGrad2;
    ctx.fillRect(width * 0.08, height * 0.76, width * 0.86, height * 0.09);

    ctx.restore();
  }

  function triggerCliffBreakerSplash() {
    const originX = width * 0.335 + (Math.random() * 16 - 8);
    const originY = height * 0.525 + (Math.random() * 8 - 4);

    const count = Math.floor(Math.random() * 12 + 18);
    for (let i = 0; i < count; i++) {
      splashParticles.push(new ThinSplashParticle(originX, originY, Math.random() * 0.5 + 0.8));
    }

    for (let i = 0; i < 2; i++) {
      const ox = originX + (Math.random() * 14 - 7);
      const oy = originY + (Math.random() * 8 - 6);
      mistClouds.push(new SeaSprayMist(ox, oy, Math.random() * 16 + 22));
    }
  }

  // ==========================================================================
  // 4. ANIMATION & TIMING LOOP
  // ==========================================================================
  function updateStormDynamics() {
    const now = Date.now();

    // Wind gust oscillation (rain angle and wind sway in breathing waves)
    currentWindAngle = 0.24 + Math.sin(simTime * 0.45) * 0.07 + Math.cos(simTime * 1.05) * 0.03;
    windGustFactor = 1.0 + Math.sin(simTime * 0.45) * 0.22;

    // Ambient Lightning
    if (now - lastFlashTime > (Math.random() * 5000 + 6000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.18 + 0.07;
    }

    // Breaker impact at lighthouse rocks
    if (now > nextLighthouseBreaker) {
      triggerCliffBreakerSplash();
      nextLighthouseBreaker = now + (Math.random() * 1200 + 2600);
    }

    // Gentle micro-spray
    if (Math.random() < 0.22) {
      const sprayX = width * 0.33 + (Math.random() * 18 - 9);
      const sprayY = height * 0.53 + (Math.random() * 6 - 3);
      splashParticles.push(new ThinSplashParticle(sprayX, sprayY, 0.65));
    }

    // Windblown spindrift wisp
    if (Math.random() < 0.06) {
      const sx = Math.random() * (width * 0.6) + (width * 0.25);
      const sy = height * (Math.random() * 0.16 + 0.58);
      spindriftWisps.push(new SpindriftWisp(sx, sy));
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);
    simTime += 0.022;

    updateStormDynamics();
    beacon.update();

    // Ambient Lightning calculation
    ambientFlashAlpha += (targetFlash - ambientFlashAlpha) * 0.08;
    if (targetFlash > 0 && Math.abs(targetFlash - ambientFlashAlpha) < 0.01) {
      targetFlash = 0;
    }
    const flashBoost = 1 + ambientFlashAlpha * 2.2;

    // Soft sky flash
    if (ambientFlashAlpha > 0.005) {
      ctx.fillStyle = `rgba(195, 210, 245, ${ambientFlashAlpha * 0.75})`;
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

    // 6. Rotating Lighthouse Beacon & Eye-Splash Bloom
    beacon.draw(flashBoost);

    // 7. Soft, Dense, Swaying Storm Rain
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flashBoost);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
