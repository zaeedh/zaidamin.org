/**
 * Cinematic Realistic Storm Atmosphere for zaidamin.org:
 * 1. Rolling Storm Clouds: soft, layered atmospheric cloud masses drifting smoothly across the background sky
 * 2. Moving Atmospheric Air Currents & Scud Wisps: fast-drifting storm vapor torn by maritime gales
 * 3. Atmospheric Squall Curtains: sweeping sheets of downpour billowing across the atmosphere
 * 4. Heavy Wind-Field Rain: dense, organic multi-tier rainfall with feathered linear gradients
 * 5. 3D Rotating Lighthouse Beacon: oceanic sweeping beam and soft eye-splash lens bloom
 * 6. Completely clean ocean: no artificial splash waves; pure natural storm blended over the original painting
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
  let cloudBanks = [];
  let airWisps = [];
  let squallCurtains = [];

  // Ambient Lightning
  let ambientFlashAlpha = 0;
  let targetFlash = 0;
  let lastFlashTime = Date.now();

  function resize() {
    const parent = canvas.parentElement;
    width = canvas.width = parent.clientWidth;
    height = canvas.height = parent.clientHeight;
    initStormAtmosphere();
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
  // 2. DYNAMIC STORM WIND FIELD & GUST CALCULATOR
  // ==========================================================================
  function getStormWindAngle(x, y, t, individualBias) {
    const base = 0.31; // ~18 degrees standard storm tilt
    const gust = Math.sin(t * 0.55 + x * 0.002) * 0.08 + Math.cos(t * 1.1) * 0.03;
    const altitudeShear = (y / Math.max(height, 1)) * 0.12;
    const wave = Math.sin(x * 0.003 - t * 0.8 + y * 0.002) * 0.06;
    return base + gust + altitudeShear + wave + individualBias;
  }

  // ==========================================================================
  // 3. ROLLING STORM CLOUDS IN BACKGROUND (Soft, Realistic Atmospheric Drift)
  // ==========================================================================
  class StormCloudBank {
    constructor(x, y, rx, ry, speed, baseAlpha) {
      this.x = x;
      this.y = y;
      this.rx = rx;
      this.ry = ry;
      this.speed = speed;
      this.baseAlpha = baseAlpha;
      this.seed = Math.random() * 100;
    }

    update() {
      this.x += this.speed;
      this.currentY = this.y + Math.sin(simTime * 0.35 + this.seed) * 5;
      if (this.x - this.rx > width + 100) {
        this.x = -this.rx - 80;
        this.y = height * (Math.random() * 0.38 + 0.05);
      }
    }

    draw(flashBoost) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      const pulse = Math.sin(simTime * 0.28 + this.seed) * 0.015;
      const alpha = Math.min((this.baseAlpha + pulse) * flashBoost, 0.20);

      ctx.translate(this.x, this.currentY);
      ctx.scale(this.rx / Math.max(this.ry, 1), 1.0);

      const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, this.ry);
      grad.addColorStop(0, `rgba(175, 205, 235, ${alpha * 0.95})`);
      grad.addColorStop(0.35, `rgba(140, 175, 215, ${alpha * 0.65})`);
      grad.addColorStop(0.70, `rgba(105, 140, 185, ${alpha * 0.25})`);
      grad.addColorStop(1, 'rgba(80, 110, 150, 0)');

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(0, 0, this.ry, 0, Math.PI * 2);
      ctx.fill();

      ctx.restore();
    }
  }

  // ==========================================================================
  // 4. ATMOSPHERIC STORM AIR CURRENTS & SCUD WISPS (Torn Vapor in Gale)
  // ==========================================================================
  class StormAirWisp {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = initial ? Math.random() * (width + 300) - 150 : -250;
      this.y = height * (Math.random() * 0.46 + 0.06);
      this.length = Math.random() * 140 + 90;
      this.height = Math.random() * 16 + 10;
      this.speed = Math.random() * 1.1 + 1.4; // swift drifting gale motion
      this.baseAlpha = Math.random() * 0.045 + 0.035; // sheer vapor
      this.seed = Math.random() * 50;
    }

    update() {
      this.x += this.speed;
      this.y += Math.sin(simTime * 0.75 + this.seed) * 0.3;
      if (this.x - this.length > width + 80) {
        this.reset();
      }
    }

    draw(flashBoost) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      const angle = getStormWindAngle(this.x, this.y, simTime, 0) - 0.20;
      const alpha = Math.min(this.baseAlpha * flashBoost, 0.15);

      ctx.translate(this.x, this.y);
      ctx.rotate(angle);

      const grad = ctx.createLinearGradient(-this.length * 0.5, 0, this.length * 0.5, 0);
      grad.addColorStop(0, 'rgba(195, 225, 255, 0)');
      grad.addColorStop(0.25, `rgba(205, 230, 255, ${alpha * 0.65})`);
      grad.addColorStop(0.5, `rgba(225, 242, 255, ${alpha})`);
      grad.addColorStop(0.75, `rgba(205, 230, 255, ${alpha * 0.65})`);
      grad.addColorStop(1, 'rgba(195, 225, 255, 0)');

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.ellipse(0, 0, this.length * 0.5, this.height * 0.5, 0, 0, Math.PI * 2);
      ctx.fill();

      ctx.restore();
    }
  }

  // ==========================================================================
  // 5. ATMOSPHERIC SQUALL CURTAINS (Blowing Sheets of Heavy Rain)
  // ==========================================================================
  class SquallCurtain {
    constructor(index) {
      this.index = index;
      this.reset(true);
    }

    reset(initial = false) {
      this.x = initial ? Math.random() * (width + 500) - 250 : -width * 0.40;
      this.widthSpan = width * (Math.random() * 0.18 + 0.30);
      this.speed = Math.random() * 0.8 + 1.5;
      this.baseAlpha = Math.random() * 0.038 + 0.032;
      this.seed = Math.random() * 100;
    }

    update() {
      this.x += this.speed;
      if (this.x > width + 300) {
        this.reset();
      }
    }

    draw(flashBoost) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      const gust = Math.sin(simTime * 0.55 + this.seed) * 0.012;
      const alpha = Math.min((this.baseAlpha + gust) * flashBoost, 0.13);

      const slant = height * 0.34;
      const grad = ctx.createLinearGradient(this.x, 0, this.x + this.widthSpan, 0);
      grad.addColorStop(0, 'rgba(195, 225, 255, 0)');
      grad.addColorStop(0.35, `rgba(210, 235, 255, ${alpha * 0.7})`);
      grad.addColorStop(0.5, `rgba(225, 245, 255, ${alpha})`);
      grad.addColorStop(0.65, `rgba(210, 235, 255, ${alpha * 0.7})`);
      grad.addColorStop(1, 'rgba(195, 225, 255, 0)');

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.moveTo(this.x, 0);
      ctx.lineTo(this.x + this.widthSpan, 0);
      ctx.lineTo(this.x + this.widthSpan + slant, height);
      ctx.lineTo(this.x + slant, height);
      ctx.closePath();
      ctx.fill();

      ctx.restore();
    }
  }

  // ==========================================================================
  // 6. HEAVY WIND-FIELD RAINDROP SIMULATION (Multi-tier Downpour)
  // ==========================================================================
  class HeavyRaindrop {
    constructor() {
      const r = Math.random();
      if (r < 0.44) {
        this.tier = 0; // distant dense mist-rain & gale drizzle
        this.baseSpeed = Math.random() * 2.4 + 5.0;
        this.baseLength = Math.random() * 5 + 12;
        this.width = 0.50;
        this.baseAlpha = Math.random() * 0.07 + 0.14;
        this.bias = (Math.random() - 0.5) * 0.08;
      } else if (r < 0.82) {
        this.tier = 1; // midground driving gale downpour
        this.baseSpeed = Math.random() * 3.0 + 7.5;
        this.baseLength = Math.random() * 6 + 17;
        this.width = 0.72;
        this.baseAlpha = Math.random() * 0.09 + 0.21;
        this.bias = (Math.random() - 0.5) * 0.06;
      } else {
        this.tier = 2; // foreground heavy storm streaks
        this.baseSpeed = Math.random() * 3.5 + 10.5;
        this.baseLength = Math.random() * 8 + 23;
        this.width = 0.95;
        this.baseAlpha = Math.random() * 0.12 + 0.28;
        this.bias = (Math.random() - 0.5) * 0.04;
      }

      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 450) - 225;
      this.y = initial ? Math.random() * height : -35;
      this.speed = this.baseSpeed * (0.94 + Math.random() * 0.12);
      this.alpha = this.baseAlpha;
    }

    update() {
      const currentAngle = getStormWindAngle(this.x, this.y, simTime, this.bias);
      const vx = Math.sin(currentAngle) * this.speed;
      const vy = Math.cos(currentAngle) * this.speed;

      this.x += vx;
      this.y += vy;

      if (this.y > height + 35 || this.x > width + 260) {
        this.reset();
      }
    }

    draw(flashBoost) {
      const currentAngle = getStormWindAngle(this.x, this.y, simTime, this.bias);
      const tailAngle = getStormWindAngle(this.x, this.y - this.baseLength * 0.5, simTime, this.bias);

      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      // Check if illuminated by rotating lighthouse beam
      let beamGlint = 1.0;
      const lx = beacon.lx;
      const ly = beacon.ly;
      if (this.x > lx && Math.abs(this.y - ly) < 46) {
        const facingOcean = Math.max(0, Math.cos(beacon.angle));
        beamGlint = 1.0 + facingOcean * 1.5;
      }

      const a = Math.min(this.alpha * flashBoost * beamGlint, 0.58);

      const endX = this.x + Math.sin(currentAngle) * this.baseLength;
      const endY = this.y + Math.cos(currentAngle) * this.baseLength;
      const midX = this.x + Math.sin((currentAngle + tailAngle) * 0.5) * (this.baseLength * 0.5);
      const midY = this.y + Math.cos((currentAngle + tailAngle) * 0.5) * (this.baseLength * 0.5);

      const grad = ctx.createLinearGradient(this.x, this.y, endX, endY);
      if (beamGlint > 1.15) {
        grad.addColorStop(0, `rgba(254, 243, 199, ${a * 0.35})`);
        grad.addColorStop(0.4, `rgba(254, 243, 199, ${a})`);
        grad.addColorStop(1, 'rgba(254, 243, 199, 0)');
      } else {
        grad.addColorStop(0, `rgba(210, 232, 252, ${a * 0.35})`);
        grad.addColorStop(0.4, `rgba(225, 242, 255, ${a})`);
        grad.addColorStop(1, 'rgba(210, 232, 252, 0)');
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

  // ==========================================================================
  // 7. INITIALIZE STORM ATMOSPHERE
  // ==========================================================================
  function initStormAtmosphere() {
    // A. Rolling Storm Clouds
    cloudBanks = [];
    const cloudCount = 5;
    for (let i = 0; i < cloudCount; i++) {
      const cx = (width / cloudCount) * i + Math.random() * 80;
      const cy = height * (Math.random() * 0.35 + 0.05);
      const rx = width * (Math.random() * 0.15 + 0.24);
      const ry = height * (Math.random() * 0.10 + 0.16);
      const speed = Math.random() * 0.22 + 0.22;
      const alpha = Math.random() * 0.035 + 0.055;
      cloudBanks.push(new StormCloudBank(cx, cy, rx, ry, speed, alpha));
    }

    // B. Low Atmospheric Storm Air Wisps
    airWisps = [];
    const wispCount = 10;
    for (let i = 0; i < wispCount; i++) {
      airWisps.push(new StormAirWisp());
    }

    // C. Squall Curtains (Heavy rain sheets)
    squallCurtains = [];
    const squallCount = 3;
    for (let i = 0; i < squallCount; i++) {
      squallCurtains.push(new SquallCurtain(i));
    }

    // D. Heavy Raindrop Simulation (~750 drops on desktop)
    const rainCount = Math.min(Math.floor((width * height) / 1050), 780);
    raindrops = [];
    for (let i = 0; i < rainCount; i++) {
      raindrops.push(new HeavyRaindrop());
    }
  }

  // ==========================================================================
  // 8. MAIN ANIMATION & RENDERING LOOP
  // ==========================================================================
  function updateStormLighting() {
    const now = Date.now();
    // Gentle distant thunder illumination across storm clouds
    if (now - lastFlashTime > (Math.random() * 5000 + 7000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.16 + 0.07;
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);
    simTime += 0.020;

    updateStormLighting();
    beacon.update();

    // Ambient Lightning calculation
    ambientFlashAlpha += (targetFlash - ambientFlashAlpha) * 0.08;
    if (targetFlash > 0 && Math.abs(targetFlash - ambientFlashAlpha) < 0.01) {
      targetFlash = 0;
    }
    const flashBoost = 1 + ambientFlashAlpha * 2.0;

    // Distant ambient thunder sky flash
    if (ambientFlashAlpha > 0.005) {
      ctx.fillStyle = `rgba(205, 222, 255, ${ambientFlashAlpha * 0.65})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 1. Rolling Storm Clouds in Background
    for (let cloud of cloudBanks) {
      cloud.update();
      cloud.draw(flashBoost);
    }

    // 2. Moving Atmospheric Air Currents & Scud Wisps
    for (let wisp of airWisps) {
      wisp.update();
      wisp.draw(flashBoost);
    }

    // 3. Atmospheric Squall Curtains (Blowing heavy downpour sheets)
    for (let squall of squallCurtains) {
      squall.update();
      squall.draw(flashBoost);
    }

    // 4. Rotating Lighthouse Beacon & Eye-Splash Bloom
    beacon.draw(flashBoost);

    // 5. Heavy Wind-Field Raindrops (Multi-tier downpour)
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flashBoost);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
