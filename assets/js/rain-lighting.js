/**
 * Cinematic Chaotic Ocean Tempest & Rotating Lighthouse Beacon Engine
 * For Dr. Zaid Amin (zaidamin.org)
 * 
 * Features:
 * 1. Chaotic, High-Visibility Storm Rain:
 *    - 680+ luminous, sharply visible rain streaks (alpha 0.35 to 0.85).
 *    - True motion-blur physics: streak length scales with velocity (18px to 52px).
 *    - Turbulent wind gusts: severe storm slant (28 deg - 42 deg) with chaotic fluttering eddies.
 *    - Torrential squall sheets: wind gusts surge dynamically in breathing tempest waves.
 *    - Zero water splash/ripples: clean, seamless, continuous storm driving downpour.
 * 2. 3D Rotating Lighthouse Beacon & Eye-Splash Bloom:
 *    - Sweeps across the storm with a volumetric conical beam.
 *    - Rotates toward the viewer: blooms into a soft, radiant lens flare & warm eye-flash.
 *    - Rotates away: smoothly dissolves back into the ocean sweep.
 *    - Rain streaks passing through the beam glint brilliantly in golden-white.
 * 3. Driving Squall Mist Sheets:
 *    - Diagonal wind-driven mist bands sweeping across the sky and sea with the gale.
 * 4. Ambient Distant Thunder Lighting:
 *    - Soft sky flashes that illuminate the entire downpour in silver-blue.
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

  // Wind & Chaos Dynamics
  let baseWindAngle = 0.52; // ~30 deg steep storm slant
  let currentWindAngle = 0.52;
  let gustPower = 1.0;

  // Ambient Lightning
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
  // 1. ROTATING LIGHTHOUSE BEACON & EYE-SPLASH BLOOM ENGINE
  // ==========================================================================
  const beacon = {
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

      const facingOcean = Math.cos(this.angle);
      const facingViewer = Math.sin(this.angle);

      ctx.save();

      // A. Steady Base Lantern Glow
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

      // B. Volumetric Beam Sweeping Across the Ocean
      if (facingOcean > 0.02) {
        const beamIntensity = Math.pow(facingOcean, 1.35) * flashBoost;
        const beamLength = width * 0.75;
        
        const beamPitch = 0.02 + Math.sin(this.angle * 2) * 0.015;
        const endY = ly + Math.sin(beamPitch) * beamLength;
        const beamHalfWidth = 26 + facingOcean * 14;

        const p1x = lx;
        const p1y = ly - 3;
        const p2x = lx;
        const p2y = ly + 3;
        const p3x = lx + beamLength;
        const p3y = endY + beamHalfWidth;
        const p4x = lx + beamLength;
        const p4y = endY - beamHalfWidth;

        const beamGrad = ctx.createLinearGradient(lx, ly, lx + beamLength, endY);
        beamGrad.addColorStop(0, `rgba(255, 250, 225, ${0.80 * beamIntensity})`);
        beamGrad.addColorStop(0.15, `rgba(254, 240, 138, ${0.48 * beamIntensity})`);
        beamGrad.addColorStop(0.55, `rgba(186, 230, 253, ${0.16 * beamIntensity})`);
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

      // C. "Splash into My Eyes" Lens Flare & Eye Bloom
      if (facingViewer > 0.05) {
        const eyeSplash = Math.pow(facingViewer, 3.2);
        const flareAlpha = Math.min(eyeSplash * flashBoost, 1.0);

        // Soft warm atmospheric wash over viewer
        const eyeWashGrad = ctx.createRadialGradient(lx, ly, 10, lx, ly, Math.max(width, height) * 0.75);
        eyeWashGrad.addColorStop(0, `rgba(255, 250, 220, ${0.22 * flareAlpha})`);
        eyeWashGrad.addColorStop(0.35, `rgba(253, 224, 71, ${0.09 * flareAlpha})`);
        eyeWashGrad.addColorStop(0.7, `rgba(186, 230, 253, ${0.03 * flareAlpha})`);
        eyeWashGrad.addColorStop(1, 'rgba(186, 230, 253, 0)');

        ctx.fillStyle = eyeWashGrad;
        ctx.fillRect(0, 0, width, height);

        // Radiant Lens Flare Corona
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

        // Anamorphic Horizontal Glare Streak
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

        // Brilliant White Filament Hotspot
        ctx.fillStyle = `rgba(255, 255, 255, ${0.98 * flareAlpha})`;
        ctx.beginPath();
        ctx.arc(lx, ly, 5 + eyeSplash * 3, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.restore();
    }
  };

  // ==========================================================================
  // 2. CHAOTIC, VISIBLE, HIGH-SPEED STORM RAIN ENGINE
  // ==========================================================================
  class StormStreak {
    constructor() {
      // 3 Atmospheric Depth Tiers:
      // Tier 0: Background heavy squall veil (fast, dense, highly visible)
      // Tier 1: Midground driving storm downpour (sharp, slanted needles)
      // Tier 2: Foreground slashing storm streaks (high-speed, motion-blurred)
      const r = Math.random();
      if (r < 0.45) {
        this.tier = 0;
        this.speedBase = Math.random() * 6 + 18;
        this.width = Math.random() * 0.3 + 0.75;
        this.baseAlpha = Math.random() * 0.15 + 0.32;
        this.lengthFactor = 1.0;
        this.flutter = (Math.random() - 0.5) * 0.12; // individual wind turbulence
      } else if (r < 0.82) {
        this.tier = 1;
        this.speedBase = Math.random() * 8 + 24;
        this.width = Math.random() * 0.4 + 1.0;
        this.baseAlpha = Math.random() * 0.18 + 0.48;
        this.lengthFactor = 1.25;
        this.flutter = (Math.random() - 0.5) * 0.10;
      } else {
        this.tier = 2;
        this.speedBase = Math.random() * 10 + 32;
        this.width = Math.random() * 0.5 + 1.35;
        this.baseAlpha = Math.random() * 0.20 + 0.65;
        this.lengthFactor = 1.5;
        this.flutter = (Math.random() - 0.5) * 0.08;
      }

      this.reset(true);
    }

    reset(initial = false) {
      // Spawn generously across left and top to account for steep sideways slant
      this.x = Math.random() * (width + 600) - 300;
      this.y = initial ? Math.random() * height : -30;
      this.speed = this.speedBase * (0.92 + Math.random() * 0.16);
      this.alpha = this.baseAlpha;
    }

    update() {
      // Individual turbulent angle = global gust angle + drop flutter
      const dropAngle = currentWindAngle + this.flutter;
      const vx = Math.sin(dropAngle) * this.speed * gustPower;
      const vy = Math.cos(dropAngle) * this.speed;

      this.x += vx;
      this.y += vy;

      // Clean, seamless reset without splashes
      if (this.y > height + 40 || this.x > width + 400) {
        this.reset();
      }
    }

    draw(flashBoost) {
      const dropAngle = currentWindAngle + this.flutter;
      // Motion blur streak length directly proportional to velocity
      const streakLength = this.speed * this.lengthFactor;

      ctx.save();

      // Check if cutting through rotating lighthouse beam
      let inBeam = false;
      const lx = beacon.lx;
      const ly = beacon.ly;
      if (this.x > lx && Math.abs(this.y - ly) < 48) {
        const facingOcean = Math.max(0, Math.cos(beacon.angle));
        if (facingOcean > 0.1) {
          inBeam = true;
        }
      }

      const a = Math.min(this.alpha * flashBoost * (inBeam ? 1.6 : 1.0), 0.95);

      // Rain color: bright crystalline silver-white, glowing gold in lighthouse beam
      if (inBeam) {
        ctx.strokeStyle = `rgba(255, 248, 215, ${a})`;
      } else {
        ctx.strokeStyle = `rgba(228, 242, 255, ${a})`;
      }

      ctx.lineWidth = this.width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(
        this.x + Math.sin(dropAngle) * streakLength,
        this.y + Math.cos(dropAngle) * streakLength
      );
      ctx.stroke();
      ctx.restore();
    }
  }

  // ==========================================================================
  // 3. TORRENTIAL SQUALL MIST SHEETS (Atmospheric Storm Gale Veils)
  // ==========================================================================
  function renderSquallMistBands(time, flashBoost) {
    ctx.save();
    ctx.globalCompositeOperation = 'screen';

    // Fast-moving diagonal squall fog sheets that surge across with wind gusts
    const surge1 = (Math.sin(time * 1.2) * 0.5 + 0.5);
    const surge2 = (Math.cos(time * 0.8) * 0.5 + 0.5);

    // Band 1: High-altitude driving squall haze
    const grad1 = ctx.createLinearGradient(0, 0, width * 0.8, height * 0.6);
    grad1.addColorStop(0, 'rgba(195, 225, 255, 0)');
    grad1.addColorStop(0.35, `rgba(210, 235, 255, ${(0.05 + surge1 * 0.04) * flashBoost})`);
    grad1.addColorStop(0.75, 'rgba(195, 225, 255, 0)');
    ctx.fillStyle = grad1;
    ctx.fillRect(0, 0, width, height * 0.7);

    // Band 2: Ocean surface wind-swept spray mist
    const grad2 = ctx.createLinearGradient(0, height * 0.50, width, height);
    grad2.addColorStop(0, 'rgba(180, 220, 255, 0)');
    grad2.addColorStop(0.45, `rgba(205, 235, 255, ${(0.045 + surge2 * 0.035) * flashBoost})`);
    grad2.addColorStop(0.85, 'rgba(180, 220, 255, 0)');
    ctx.fillStyle = grad2;
    ctx.fillRect(0, height * 0.48, width, height * 0.52);

    ctx.restore();
  }

  function initRain() {
    // Dense chaotic tempest: 680 sharply visible, driving storm streaks
    const count = Math.min(Math.floor((width * height) / 1050), 720);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new StormStreak());
    }
  }

  // ==========================================================================
  // 4. MAIN STORM TIMING & RENDER LOOP
  // ==========================================================================
  function updateChaosDynamics() {
    const now = Date.now();

    // Chaotic Storm Squall Wind:
    // Base angle ~30 deg, fluctuating between 26 deg and 42 deg during gust surges
    const gustWave1 = Math.sin(simTime * 0.75) * 0.10;
    const gustWave2 = Math.cos(simTime * 1.6) * 0.04;
    currentWindAngle = baseWindAngle + gustWave1 + gustWave2;
    gustPower = 1.0 + Math.max(0, Math.sin(simTime * 0.75)) * 0.35; // surges up by 35% in gusts

    // Ambient Distant Lightning
    if (now - lastFlashTime > (Math.random() * 5000 + 6000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.22 + 0.09;
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);
    simTime += 0.022;

    updateChaosDynamics();
    beacon.update();

    // Ambient Lightning calculation
    ambientFlashAlpha += (targetFlash - ambientFlashAlpha) * 0.08;
    if (targetFlash > 0 && Math.abs(targetFlash - ambientFlashAlpha) < 0.01) {
      targetFlash = 0;
    }
    const flashBoost = 1 + ambientFlashAlpha * 2.4;

    // Distant ambient thunder sky illumination
    if (ambientFlashAlpha > 0.005) {
      ctx.fillStyle = `rgba(205, 222, 255, ${ambientFlashAlpha * 0.8})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 1. Torrential Squall Mist Bands
    renderSquallMistBands(simTime, flashBoost);

    // 2. Rotating Lighthouse Beacon & Eye-Splash Bloom
    beacon.draw(flashBoost);

    // 3. Dense, Chaotic, Highly-Visible Bad Storm Rain
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flashBoost);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
