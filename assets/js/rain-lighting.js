/**
 * Cinematic Natural Storm Atmosphere:
 * - Natural Wind-Field Rain: curved, non-single-angle rainfall that organically follows the storm flow
 * - Soft Moving Waves & Blended Foam Surges: living light ribbons harmoniously layered over the real picture
 * - Realistic Sea Spray & Cliff Breaker Splash: delicate micro-spray and sheer vapor mist at the lighthouse rocks
 * - 3D Rotating Lighthouse Beacon: ocean sweep & soft eye-splash bloom
 * - 60 FPS silky smooth, elegant, and perfectly blended
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

  // Ambient Lighting & Events
  let ambientFlashAlpha = 0;
  let targetFlash = 0;
  let lastFlashTime = Date.now();
  let nextCliffBreaker = 0;

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
    get lx() { return width * 0.318; },
    get ly() { return height * 0.262; },
    angle: 0.2,
    speed: 0.011, // majestic ~9s per revolution

    update() {
      this.angle += this.speed;
      if (this.angle > Math.PI * 2) {
        this.angle -= Math.PI * 2;
      }
    },

    draw(flashBoost) {
      const lx = this.lx;
      const ly = this.ly;

      const facingOcean = Math.cos(this.angle);
      const facingViewer = Math.sin(this.angle);

      ctx.save();

      // A. Steady Warm Lantern Core Glow
      const baseCoreGrad = ctx.createRadialGradient(lx, ly, 0, lx, ly, 16);
      baseCoreGrad.addColorStop(0, 'rgba(255, 255, 245, 0.95)');
      baseCoreGrad.addColorStop(0.3, 'rgba(254, 240, 138, 0.65)');
      baseCoreGrad.addColorStop(0.7, 'rgba(234, 179, 8, 0.25)');
      baseCoreGrad.addColorStop(1, 'rgba(234, 179, 8, 0)');

      ctx.globalCompositeOperation = 'screen';
      ctx.fillStyle = baseCoreGrad;
      ctx.beginPath();
      ctx.arc(lx, ly, 16, 0, Math.PI * 2);
      ctx.fill();

      // B. Volumetric Beam Sweeping Across the Ocean
      if (facingOcean > 0.02) {
        const beamIntensity = Math.pow(facingOcean, 1.3) * flashBoost;
        const beamLength = width * 0.75;
        
        const beamPitch = 0.02 + Math.sin(this.angle * 2) * 0.012;
        const endY = ly + Math.sin(beamPitch) * beamLength;
        const beamHalfWidth = 24 + facingOcean * 12;

        const p1x = lx;
        const p1y = ly - 2.5;
        const p2x = lx;
        const p2y = ly + 2.5;
        const p3x = lx + beamLength;
        const p3y = endY + beamHalfWidth;
        const p4x = lx + beamLength;
        const p4y = endY - beamHalfWidth;

        const beamGrad = ctx.createLinearGradient(lx, ly, lx + beamLength, endY);
        beamGrad.addColorStop(0, `rgba(255, 250, 225, ${0.70 * beamIntensity})`);
        beamGrad.addColorStop(0.18, `rgba(254, 240, 138, ${0.40 * beamIntensity})`);
        beamGrad.addColorStop(0.60, `rgba(186, 230, 253, ${0.12 * beamIntensity})`);
        beamGrad.addColorStop(1, 'rgba(186, 230, 253, 0)');

        ctx.fillStyle = beamGrad;
        ctx.beginPath();
        ctx.moveTo(p1x, p1y);
        ctx.lineTo(p4x, p4y);
        ctx.lineTo(p3x, p3y);
        ctx.lineTo(p2x, p2y);
        ctx.closePath();
        ctx.fill();

        // Soft outer feathered aura
        const auraGrad = ctx.createLinearGradient(lx, ly, lx + beamLength * 0.7, endY);
        auraGrad.addColorStop(0, `rgba(253, 224, 71, ${0.28 * beamIntensity})`);
        auraGrad.addColorStop(0.6, `rgba(147, 197, 253, ${0.06 * beamIntensity})`);
        auraGrad.addColorStop(1, 'rgba(147, 197, 253, 0)');

        ctx.fillStyle = auraGrad;
        ctx.beginPath();
        ctx.moveTo(p1x, p1y - 5);
        ctx.lineTo(p4x, p4y - 12);
        ctx.lineTo(p3x, p3y + 12);
        ctx.lineTo(p2x, p2y + 5);
        ctx.closePath();
        ctx.fill();
      }

      // C. Soft "Splash into My Eyes" Lens Flare & Eye Bloom
      if (facingViewer > 0.05) {
        const eyeSplash = Math.pow(facingViewer, 3.2);
        const flareAlpha = Math.min(eyeSplash * flashBoost, 1.0);

        // Soft warm atmospheric wash over viewer
        const eyeWashGrad = ctx.createRadialGradient(lx, ly, 10, lx, ly, Math.max(width, height) * 0.75);
        eyeWashGrad.addColorStop(0, `rgba(255, 250, 220, ${0.18 * flareAlpha})`);
        eyeWashGrad.addColorStop(0.35, `rgba(253, 224, 71, ${0.07 * flareAlpha})`);
        eyeWashGrad.addColorStop(0.7, `rgba(186, 230, 253, ${0.02 * flareAlpha})`);
        eyeWashGrad.addColorStop(1, 'rgba(186, 230, 253, 0)');

        ctx.fillStyle = eyeWashGrad;
        ctx.fillRect(0, 0, width, height);

        // Radiant Lens Flare Corona
        const flareRadius = 70 + eyeSplash * 60;
        const coronaGrad = ctx.createRadialGradient(lx, ly, 0, lx, ly, flareRadius);
        coronaGrad.addColorStop(0, `rgba(255, 255, 255, ${0.92 * flareAlpha})`);
        coronaGrad.addColorStop(0.2, `rgba(255, 245, 180, ${0.70 * flareAlpha})`);
        coronaGrad.addColorStop(0.5, `rgba(251, 191, 36, ${0.30 * flareAlpha})`);
        coronaGrad.addColorStop(0.8, `rgba(147, 197, 253, ${0.10 * flareAlpha})`);
        coronaGrad.addColorStop(1, 'rgba(147, 197, 253, 0)');

        ctx.fillStyle = coronaGrad;
        ctx.beginPath();
        ctx.arc(lx, ly, flareRadius, 0, Math.PI * 2);
        ctx.fill();

        // Anamorphic Horizontal Glare Streak
        const streakLength = 110 + eyeSplash * 150;
        const streakHeight = 2.2 + eyeSplash * 2.0;
        const streakGrad = ctx.createLinearGradient(lx - streakLength, ly, lx + streakLength, ly);
        streakGrad.addColorStop(0, 'rgba(255, 255, 255, 0)');
        streakGrad.addColorStop(0.35, `rgba(186, 230, 253, ${0.30 * flareAlpha})`);
        streakGrad.addColorStop(0.5, `rgba(255, 255, 255, ${0.85 * flareAlpha})`);
        streakGrad.addColorStop(0.65, `rgba(186, 230, 253, ${0.30 * flareAlpha})`);
        streakGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.fillStyle = streakGrad;
        ctx.beginPath();
        ctx.ellipse(lx, ly, streakLength, streakHeight, 0, 0, Math.PI * 2);
        ctx.fill();

        // Brilliant Filament Core
        ctx.fillStyle = `rgba(255, 255, 255, ${0.95 * flareAlpha})`;
        ctx.beginPath();
        ctx.arc(lx, ly, 4 + eyeSplash * 3, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.restore();
    }
  };

  // ==========================================================================
  // 2. NATURAL STORM WIND-FIELD RAIN (Not in single angle - follows storm flow)
  // ==========================================================================
  // Computes the dynamic local wind angle across space (x, y) and time
  function getStormWindAngle(x, y, t, individualBias) {
    // Base slant ~18 degrees
    const base = 0.28;
    // Altitude wind shear: rain falls steeper up in clouds, tilts harder near sea
    const altitudeShear = (y / Math.max(height, 1)) * 0.12;
    // Harmonic atmospheric wind wave across the storm
    const stormWave = Math.sin(x * 0.003 - t * 0.8 + y * 0.002) * 0.09;
    const eddy = Math.cos(y * 0.006 + t * 0.5) * 0.04;
    return base + altitudeShear + stormWave + eddy + individualBias;
  }

  class NaturalRaindrop {
    constructor() {
      const r = Math.random();
      if (r < 0.45) {
        this.tier = 0; // distant soft rain
        this.baseSpeed = Math.random() * 2.0 + 3.8;
        this.baseLength = Math.random() * 4 + 11;
        this.width = 0.55;
        this.baseAlpha = Math.random() * 0.06 + 0.13;
        this.bias = (Math.random() - 0.5) * 0.08;
      } else if (r < 0.82) {
        this.tier = 1; // midground driving rain
        this.baseSpeed = Math.random() * 2.5 + 5.5;
        this.baseLength = Math.random() * 5 + 15;
        this.width = 0.70;
        this.baseAlpha = Math.random() * 0.08 + 0.19;
        this.bias = (Math.random() - 0.5) * 0.06;
      } else {
        this.tier = 2; // foreground graceful streaks
        this.baseSpeed = Math.random() * 2.8 + 7.2;
        this.baseLength = Math.random() * 6 + 19;
        this.width = 0.85;
        this.baseAlpha = Math.random() * 0.10 + 0.26;
        this.bias = (Math.random() - 0.5) * 0.04;
      }

      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 400) - 200;
      this.y = initial ? Math.random() * height : -30;
      this.speed = this.baseSpeed * (0.94 + Math.random() * 0.12);
      this.alpha = this.baseAlpha;
    }

    update() {
      // Each drop calculates its local wind angle from the storm field
      const currentAngle = getStormWindAngle(this.x, this.y, simTime, this.bias);
      const vx = Math.sin(currentAngle) * this.speed;
      const vy = Math.cos(currentAngle) * this.speed;

      this.x += vx;
      this.y += vy;

      // Clean seamless reset without artificial splash dots
      if (this.y > height + 35 || this.x > width + 250) {
        this.reset();
      }
    }

    draw(flashBoost) {
      const currentAngle = getStormWindAngle(this.x, this.y, simTime, this.bias);
      const tailAngle = getStormWindAngle(this.x, this.y - this.baseLength * 0.5, simTime, this.bias);

      ctx.save();
      ctx.globalCompositeOperation = 'screen'; // seamlessly blends into the painting pixels

      // Check if illuminated by rotating lighthouse beam
      let beamGlint = 1.0;
      const lx = beacon.lx;
      const ly = beacon.ly;
      if (this.x > lx && Math.abs(this.y - ly) < 42) {
        const facingOcean = Math.max(0, Math.cos(beacon.angle));
        beamGlint = 1.0 + facingOcean * 1.4;
      }

      const a = Math.min(this.alpha * flashBoost * beamGlint, 0.55);

      const endX = this.x + Math.sin(currentAngle) * this.baseLength;
      const endY = this.y + Math.cos(currentAngle) * this.baseLength;
      const midX = this.x + Math.sin((currentAngle + tailAngle) * 0.5) * (this.baseLength * 0.5);
      const midY = this.y + Math.cos((currentAngle + tailAngle) * 0.5) * (this.baseLength * 0.5);

      // Feathered linear gradient along streak (tail fades smoothly into air)
      const grad = ctx.createLinearGradient(this.x, this.y, endX, endY);
      if (beamGlint > 1.15) {
        grad.addColorStop(0, `rgba(254, 243, 199, ${a * 0.35})`);
        grad.addColorStop(0.4, `rgba(254, 243, 199, ${a})`);
        grad.addColorStop(1, 'rgba(254, 243, 199, 0)');
      } else {
        grad.addColorStop(0, `rgba(210, 230, 250, ${a * 0.35})`);
        grad.addColorStop(0.4, `rgba(220, 240, 255, ${a})`);
        grad.addColorStop(1, 'rgba(210, 230, 250, 0)');
      }

      ctx.strokeStyle = grad;
      ctx.lineWidth = this.width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.quadraticCurveTo(midX, midY, endX, endY);
      ctx.stroke();
      ctx.restore();
    }
  }

  function initRain() {
    // Elegant storm density: increased slightly for clearer presence, smoothly blended
    const count = Math.min(Math.floor((width * height) / 1550), 520);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new NaturalRaindrop());
    }
  }

  // ==========================================================================
  // 3. SOFT MOVING WAVES & BLENDED FOAM BREATHING (Harmonized with Painting)
  // ==========================================================================
  function renderSoftMovingWaves(time, boost) {
    ctx.save();
    ctx.globalCompositeOperation = 'screen';

    // ------------------------------------------------------------------------
    // A. Cliff Base Foam Surge (Where the breaker crashes at the lighthouse rock)
    // Coords in painting: x ~ 30% to 39%, y ~ 50% to 58%
    // ------------------------------------------------------------------------
    const cliffSwell = (Math.sin(time * 1.4) * 0.5 + 0.5) * 0.14;
    const cliffGrad = ctx.createRadialGradient(
      width * 0.34, height * 0.535, width * 0.01,
      width * 0.34, height * 0.535, width * 0.095
    );
    cliffGrad.addColorStop(0, `rgba(235, 248, 255, ${(0.13 + cliffSwell) * boost})`);
    cliffGrad.addColorStop(0.5, `rgba(190, 228, 252, ${(0.06 + cliffSwell * 0.5) * boost})`);
    cliffGrad.addColorStop(1, 'rgba(180, 220, 245, 0)');
    ctx.fillStyle = cliffGrad;
    ctx.beginPath();
    ctx.ellipse(width * 0.34, height * 0.535, width * 0.095, height * 0.048, 0.03, 0, Math.PI * 2);
    ctx.fill();

    // ------------------------------------------------------------------------
    // B. Midground Breaker Wave Rolling Crest (Flows across the center ocean)
    // Coords in painting: x ~ 15% to 85%, y ~ 58% to 68%
    // ------------------------------------------------------------------------
    const wavePhase = time * 0.95;
    ctx.beginPath();
    const startX = width * 0.15;
    const endX = width * 0.88;
    const step = 20;

    for (let x = startX; x <= endX; x += step) {
      // Harmonic rolling undulation matching the wave angle in painting
      const undulation = Math.sin(x * 0.007 - wavePhase) * 4.5 + Math.cos(x * 0.015 + time * 0.6) * 2.5;
      const y = height * 0.625 + undulation;
      if (x === startX) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }

    const waveAlpha = (0.07 + Math.sin(time * 0.8) * 0.025) * boost;
    ctx.strokeStyle = `rgba(225, 244, 255, ${waveAlpha})`;
    ctx.lineWidth = 6.0;
    ctx.lineCap = 'round';
    ctx.filter = 'blur(3px)';
    ctx.stroke();
    ctx.filter = 'none';

    // ------------------------------------------------------------------------
    // C. Foreground Shoreline Reef Wash (Ebbs & flows over the dark boulders)
    // Coords in painting: x ~ 10% to 92%, y ~ 75% to 86%
    // ------------------------------------------------------------------------
    const reefPhase = time * 0.75;
    ctx.beginPath();
    const reefStartX = width * 0.08;
    const reefEndX = width * 0.94;

    for (let x = reefStartX; x <= reefEndX; x += step) {
      const surfShift = Math.sin(x * 0.006 + reefPhase) * 5.0 + Math.cos(x * 0.012 - time * 0.5) * 3.0;
      const y = height * 0.79 + surfShift;
      if (x === reefStartX) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }

    const reefAlpha = (0.055 + Math.cos(time * 0.7) * 0.02) * boost;
    ctx.strokeStyle = `rgba(215, 238, 255, ${reefAlpha})`;
    ctx.lineWidth = 7.5;
    ctx.lineCap = 'round';
    ctx.filter = 'blur(4px)';
    ctx.stroke();
    ctx.filter = 'none';

    ctx.restore();
  }

  // ==========================================================================
  // 4. SOFT, REALISTIC CLIFF BREAKER SPLASH & SEASPRAY MIST
  // ==========================================================================
  class SoftSplashDrop {
    constructor(originX, originY, power = 1.0) {
      this.x = originX + (Math.random() - 0.5) * 12;
      this.y = originY + (Math.random() - 0.5) * 6;
      // Arcs gently upward and rightward with coastal wind
      const angle = -(Math.PI * 0.28 + Math.random() * Math.PI * 0.44);
      const speed = (Math.random() * 2.2 + 1.0) * power;
      this.vx = Math.cos(angle) * speed + (Math.random() * 0.6 + 0.4);
      this.vy = Math.sin(angle) * speed;
      this.size = Math.random() * 0.5 + 0.55; // fine: 0.55px to 1.05px
      this.alpha = Math.random() * 0.28 + 0.24;
      this.decay = Math.random() * 0.008 + 0.006;
      this.gravity = 0.042;
      this.life = Math.random() * 45 + 35;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.vy += this.gravity;
      this.vx *= 0.99;
      this.alpha -= this.decay;
      this.life--;
    }

    draw(boost) {
      if (this.alpha <= 0 || this.life <= 0) return;
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      const a = Math.min(this.alpha * boost, 0.65);
      ctx.fillStyle = `rgba(235, 248, 255, ${a})`;
      ctx.beginPath();
      const speed = Math.hypot(this.vx, this.vy);
      const angle = Math.atan2(this.vy, this.vx);
      ctx.ellipse(this.x, this.y, this.size + speed * 0.25, this.size * 0.8, angle, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  class SheerMistPuff {
    constructor(x, y, maxRadius = 34) {
      this.x = x;
      this.y = y;
      this.radius = Math.random() * 6 + 6;
      this.maxRadius = maxRadius;
      this.growth = (maxRadius - this.radius) / (Math.random() * 35 + 45);
      this.vx = Math.random() * 0.7 + 0.35; // drifts softly right with wind
      this.vy = -(Math.random() * 0.4 + 0.15); // gentle lift
      this.alpha = Math.random() * 0.14 + 0.08; // sheer and delicate
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.radius += this.growth;
      this.alpha *= 0.968;
    }

    draw(boost) {
      if (this.alpha <= 0.004) return;
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      const a = Math.min(this.alpha * boost, 0.28);
      const grad = ctx.createRadialGradient(
        this.x, this.y, 0,
        this.x, this.y, Math.max(this.radius, 1)
      );
      grad.addColorStop(0, `rgba(235, 248, 255, ${a})`);
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
      this.vx = Math.random() * 3.8 + 2.5;
      this.vy = -(Math.random() * 0.45 + 0.12);
      this.alpha = Math.random() * 0.18 + 0.08;
      this.length = Math.random() * 9 + 6;
      this.width = Math.random() * 0.6 + 0.5;
      this.life = Math.random() * 28 + 18;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.alpha -= 0.014;
      this.life--;
    }

    draw(boost) {
      if (this.alpha <= 0 || this.life <= 0) return;
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      const a = Math.min(this.alpha * boost, 0.45);
      ctx.strokeStyle = `rgba(225, 242, 255, ${a})`;
      ctx.lineWidth = this.width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(this.x + this.length, this.y + this.vy * 1.5);
      ctx.stroke();
      ctx.restore();
    }
  }

  function triggerCliffBreakerSplash() {
    const originX = width * 0.335 + (Math.random() * 14 - 7);
    const originY = height * 0.53 + (Math.random() * 7 - 3.5);

    // 16 to 24 fine, graceful splash droplets
    const count = Math.floor(Math.random() * 9 + 16);
    for (let i = 0; i < count; i++) {
      splashParticles.push(new SoftSplashDrop(originX, originY, Math.random() * 0.5 + 0.75));
    }

    // 2 soft radial sea spray mist puffs
    for (let i = 0; i < 2; i++) {
      const ox = originX + (Math.random() * 12 - 6);
      const oy = originY + (Math.random() * 7 - 5);
      mistClouds.push(new SheerMistPuff(ox, oy, Math.random() * 14 + 20));
    }
  }

  // ==========================================================================
  // 5. MAIN TIMING & RENDER LOOP
  // ==========================================================================
  function updateStormEvents() {
    const now = Date.now();

    // Soft Ambient Lightning (gentle distant cloud illumination)
    if (now - lastFlashTime > (Math.random() * 5000 + 7000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.16 + 0.07;
    }

    // Gentle rhythmic breaker collision at lighthouse cliff (every 2.8s - 3.8s)
    if (now > nextCliffBreaker) {
      triggerCliffBreakerSplash();
      nextCliffBreaker = now + (Math.random() * 1000 + 2800);
    }

    // Occasional continuous micro-mist from wave crests
    if (Math.random() < 0.18) {
      const sprayX = width * 0.33 + (Math.random() * 16 - 8);
      const sprayY = height * 0.535 + (Math.random() * 5 - 2.5);
      splashParticles.push(new SoftSplashDrop(sprayX, sprayY, 0.6));
    }

    // Occasional windblown spindrift wisp along mid breaker
    if (Math.random() < 0.05) {
      const sx = Math.random() * (width * 0.6) + (width * 0.22);
      const sy = height * (Math.random() * 0.14 + 0.58);
      spindriftWisps.push(new SpindriftWisp(sx, sy));
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);
    simTime += 0.020;

    updateStormEvents();
    beacon.update();

    // Ambient Lightning calculation
    ambientFlashAlpha += (targetFlash - ambientFlashAlpha) * 0.08;
    if (targetFlash > 0 && Math.abs(targetFlash - ambientFlashAlpha) < 0.01) {
      targetFlash = 0;
    }
    const flashBoost = 1 + ambientFlashAlpha * 2.0;

    // Distant ambient thunder sky flash
    if (ambientFlashAlpha > 0.005) {
      ctx.fillStyle = `rgba(205, 222, 255, ${ambientFlashAlpha * 0.7})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 1. Soft Moving Waves & Blended Foam Surges (Layered over real painting)
    renderSoftMovingWaves(simTime, flashBoost);

    // 2. Sheer Sea Spray Mist Puffs
    for (let i = mistClouds.length - 1; i >= 0; i--) {
      mistClouds[i].update();
      mistClouds[i].draw(flashBoost);
      if (mistClouds[i].alpha <= 0.004) {
        mistClouds.splice(i, 1);
      }
    }

    // 3. Soft Splash Droplets at Lighthouse Base
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

    // 5. Rotating Lighthouse Beacon & Eye-Splash Bloom
    beacon.draw(flashBoost);

    // 6. Natural Storm Wind-Field Rain (Curved, non-single-angle, following the storm)
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flashBoost);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
