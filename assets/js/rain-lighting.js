/**
 * Cinematic Slow-Motion Atmospheric Rain & Rotating Lighthouse Beacon Engine
 * For Dr. Zaid Amin (zaidamin.org)
 * 
 * Aesthetic Philosophy:
 * - Soft, dreamy slow-motion rainfall: raindrops float and drift gracefully like cinema slow-mo.
 * - Perfectly blended: sheer, luminous opacities (0.18 - 0.38) that harmonize with the painting.
 * - Gentle, elegant wind drift (~12 deg angle) without aggressive chaos or harsh gusts.
 * - Hypnotic 3D rotating lighthouse beacon with warm, soft eye-splash bloom.
 * - Silky smooth 60 FPS performance, clean, serene, prestigious.
 */

(function() {
  const canvas = document.getElementById('rain-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = 0;
  let height = 0;
  let simTime = 0;

  // Rain Pool
  let raindrops = [];

  // Gentle, Elegant Wind Angle (~12 degrees)
  let windAngle = 0.20;

  // Ambient Lighting
  let ambientFlashAlpha = 0;
  let targetFlash = 0;
  let lastFlashTime = Date.now();

  function resize() {
    const parent = canvas.parentElement;
    width = canvas.width = parent.clientWidth;
    height = canvas.height = parent.clientHeight;
    initRain();
  }

  window.addEventListener('resize', resize);

  // ==========================================================================
  // 1. MAJESTIC ROTATING LIGHTHOUSE BEACON & SOFT EYE-SPLASH BLOOM
  // ==========================================================================
  const beacon = {
    get lx() { return width * 0.318; },
    get ly() { return height * 0.262; },
    angle: 0.2,
    speed: 0.0105, // slow, majestic ~9.5s per revolution

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
  // 2. SLOW-MOTION, SOFT, BLENDED STORM RAIN ENGINE
  // ==========================================================================
  class SlowMotionRaindrop {
    constructor() {
      // 3 Gentle Depth Tiers:
      // Tier 0: Soft background mist droplets (slow floating, sheer)
      // Tier 1: Midground cinematic rain (slender, graceful, visible)
      // Tier 2: Foreground slow-motion streaks (gentle drift, soft sheen)
      const r = Math.random();
      if (r < 0.45) {
        this.tier = 0;
        this.baseSpeed = Math.random() * 1.8 + 3.2; // slow motion: 3.2 - 5.0 px/frame
        this.length = Math.random() * 4 + 10;      // 10px - 14px
        this.width = 0.65;
        this.baseAlpha = Math.random() * 0.08 + 0.18; // soft, beautifully visible
        this.drift = (Math.random() - 0.5) * 0.03;
      } else if (r < 0.82) {
        this.tier = 1;
        this.baseSpeed = Math.random() * 2.2 + 4.8; // 4.8 - 7.0 px/frame
        this.length = Math.random() * 6 + 14;      // 14px - 20px
        this.width = 0.80;
        this.baseAlpha = Math.random() * 0.10 + 0.26; // 0.26 - 0.36
        this.drift = (Math.random() - 0.5) * 0.025;
      } else {
        this.tier = 2;
        this.baseSpeed = Math.random() * 2.5 + 6.5; // 6.5 - 9.0 px/frame
        this.length = Math.random() * 8 + 18;      // 18px - 26px
        this.width = 0.95;
        this.baseAlpha = Math.random() * 0.12 + 0.35; // 0.35 - 0.47
        this.drift = (Math.random() - 0.5) * 0.02;
      }

      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 300) - 150;
      this.y = initial ? Math.random() * height : -30;
      this.speed = this.baseSpeed * (0.94 + Math.random() * 0.12);
      this.alpha = this.baseAlpha;
    }

    update() {
      // Gentle, harmonic wind drift
      const dropAngle = windAngle + this.drift;
      const vx = Math.sin(dropAngle) * this.speed;
      const vy = Math.cos(dropAngle) * this.speed;

      this.x += vx;
      this.y += vy;

      // Clean, seamless reset at boundaries (zero splash)
      if (this.y > height + 30 || this.x > width + 200) {
        this.reset();
      }
    }

    draw(flashBoost) {
      const dropAngle = windAngle + this.drift;
      ctx.save();

      // Check if illuminated by rotating lighthouse beam
      let beamGlint = 1.0;
      const lx = beacon.lx;
      const ly = beacon.ly;
      if (this.x > lx && Math.abs(this.y - ly) < 42) {
        const facingOcean = Math.max(0, Math.cos(beacon.angle));
        beamGlint = 1.0 + facingOcean * 1.5;
      }

      const a = Math.min(this.alpha * flashBoost * beamGlint, 0.70);

      // Ethereal silver rain, catching warm gold in lighthouse beam
      if (beamGlint > 1.2) {
        ctx.strokeStyle = `rgba(254, 243, 199, ${a})`;
      } else {
        ctx.strokeStyle = `rgba(220, 238, 255, ${a})`;
      }

      ctx.lineWidth = this.width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(
        this.x + Math.sin(dropAngle) * this.length,
        this.y + Math.cos(dropAngle) * this.length
      );
      ctx.stroke();
      ctx.restore();
    }
  }

  function initRain() {
    // Elegant, uncluttered density: 280-320 graceful slow-motion raindrops
    const count = Math.min(Math.floor((width * height) / 2400), 320);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new SlowMotionRaindrop());
    }
  }

  // ==========================================================================
  // 3. MAIN STORM TIMING & RENDER LOOP
  // ==========================================================================
  function updateAtmosphere() {
    const now = Date.now();

    // Gentle, slow breathing wind angle (~11 deg to 14 deg)
    windAngle = 0.20 + Math.sin(simTime * 0.35) * 0.035;

    // Soft Ambient Lightning (gentle distant cloud illumination)
    if (now - lastFlashTime > (Math.random() * 5000 + 7000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.16 + 0.07;
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);
    simTime += 0.020;

    updateAtmosphere();
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

    // 1. Rotating Lighthouse Beacon & Eye-Splash Bloom
    beacon.draw(flashBoost);

    // 2. Slow-Motion, Soft, Harmoniously Blended Rain
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flashBoost);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
