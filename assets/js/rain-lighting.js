/**
 * Heavy Ocean Storm Rain & Rotating Lighthouse Beacon Engine
 * For Dr. Zaid Amin (zaidamin.org)
 * 
 * Features:
 * 1. Severe Ocean Storm Rain:
 *    - 720+ needle-fine, whisper-thin, ultra-smooth raindrops.
 *    - Steep squall slant (driven by heavy gale-force storm winds at ~26 deg).
 *    - Small, compact raindrop needles (4px-10px) with high velocity (16-28 px/frame).
 *    - Zero splash on collision (clean, seamless, continuous storm downpour).
 *    - 3 depth tiers (distant squall mist veil, midground driving sheets, foreground fast needles).
 *    - Dynamic wind gusting: rain angle and speed surge in organic storm waves.
 * 2. 3D Rotating Lighthouse Beacon & Eye-Splash Bloom:
 *    - Sweeps across the stormy ocean with a volumetric conical beam.
 *    - Rotates toward the viewer: blooms into a soft, dazzling lens flare & warm eye-flash.
 *    - Rotates away: smoothly dissolves back into the ocean sweep.
 *    - Raindrops catch golden-white glints when cutting through the rotating beam.
 * 3. Soft Distant Thunder Flashes:
 *    - Gentle, natural ambient lightning illuminating the tempest.
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

  // Storm Dynamics (Severe Squall Gale)
  let currentWindAngle = 0.42; // ~24 deg slant
  let windGustFactor = 1.0;

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
        const beamHalfWidth = 24 + facingOcean * 12;

        const p1x = lx;
        const p1y = ly - 3;
        const p2x = lx;
        const p2y = ly + 3;
        const p3x = lx + beamLength;
        const p3y = endY + beamHalfWidth;
        const p4x = lx + beamLength;
        const p4y = endY - beamHalfWidth;

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
  // 2. SEVERE STORM RAIN ENGINE (Smaller, Smooth, Needle-Fine, Heavy Gale)
  // ==========================================================================
  class RainNeedle {
    constructor() {
      // 3 Depth Tiers:
      // 0 = Distant squall mist needles (faint, ultra small, dense haze)
      // 1 = Midground driving storm downpour (steady gale needles)
      // 2 = Foreground fast storm streaks (fast, motion-blurred)
      const r = Math.random();
      if (r < 0.50) {
        this.tier = 0;
        this.baseSpeed = Math.random() * 5 + 13;
        this.baseLength = Math.random() * 3 + 4; // very small: 4px to 7px
        this.width = 0.30; // whisper thin needle
        this.baseAlpha = Math.random() * 0.05 + 0.06;
      } else if (r < 0.85) {
        this.tier = 1;
        this.baseSpeed = Math.random() * 6 + 18;
        this.baseLength = Math.random() * 4 + 6; // 6px to 10px
        this.width = 0.40;
        this.baseAlpha = Math.random() * 0.06 + 0.10;
      } else {
        this.tier = 2;
        this.baseSpeed = Math.random() * 7 + 23;
        this.baseLength = Math.random() * 4 + 9; // 9px to 13px
        this.width = 0.50;
        this.baseAlpha = Math.random() * 0.08 + 0.14;
      }

      this.reset(true);
    }

    reset(initial = false) {
      // Spawn across wider area to account for steep wind angle
      this.x = Math.random() * (width + 500) - 250;
      this.y = initial ? Math.random() * height : -20;
      this.speed = this.baseSpeed * (0.95 + Math.random() * 0.15);
      this.length = this.baseLength;
      this.alpha = this.baseAlpha;
    }

    update() {
      // Driven hard by current storm squall angle and gusting wind
      const vx = Math.sin(currentWindAngle) * this.speed * windGustFactor;
      const vy = Math.cos(currentWindAngle) * this.speed;

      this.x += vx;
      this.y += vy;

      // NO SPLASH ON WATER - Clean, continuous storm downpour passing through
      if (this.y > height + 25 || this.x > width + 300) {
        this.reset();
      }
    }

    draw(flashBoost) {
      ctx.save();

      // Check if illuminated by rotating lighthouse beam
      let beamGlint = 1.0;
      const lx = beacon.lx;
      const ly = beacon.ly;
      if (this.x > lx && Math.abs(this.y - ly) < 40) {
        const facingOcean = Math.max(0, Math.cos(beacon.angle));
        beamGlint = 1.0 + facingOcean * 1.6;
      }

      const a = Math.min(this.alpha * flashBoost * beamGlint, 0.65);

      if (beamGlint > 1.15) {
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

  // Soft atmospheric drifting squall haze (giving the feeling of a raging storm)
  function renderStormSquallHaze(time, flashBoost) {
    ctx.save();
    ctx.globalCompositeOperation = 'screen';

    // Horizontal wind-driven squall mist sheet
    const hazePulse = (Math.sin(time * 0.8) * 0.5 + 0.5) * 0.04;
    const hazeGrad = ctx.createLinearGradient(0, 0, width, height * 0.7);
    hazeGrad.addColorStop(0, 'rgba(180, 210, 240, 0)');
    hazeGrad.addColorStop(0.3, `rgba(195, 220, 245, ${(0.035 + hazePulse) * flashBoost})`);
    hazeGrad.addColorStop(0.7, `rgba(180, 210, 240, ${(0.025 + hazePulse * 0.6) * flashBoost})`);
    hazeGrad.addColorStop(1, 'rgba(180, 210, 240, 0)');

    ctx.fillStyle = hazeGrad;
    ctx.fillRect(0, 0, width, height);
    ctx.restore();
  }

  function initRain() {
    // Dense storm downpour: 650 to 750 small needle raindrops
    const count = Math.min(Math.floor((width * height) / 1000), 720);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new RainNeedle());
    }
  }

  // ==========================================================================
  // 3. MAIN STORM TIMING & RENDER LOOP
  // ==========================================================================
  function updateStormDynamics() {
    const now = Date.now();

    // Severe squall wind gusting: steep storm slant (~25 deg) with breathing surges
    currentWindAngle = 0.42 + Math.sin(simTime * 0.6) * 0.08 + Math.cos(simTime * 1.3) * 0.03;
    windGustFactor = 1.0 + Math.sin(simTime * 0.6) * 0.28;

    // Soft Ambient Lightning
    if (now - lastFlashTime > (Math.random() * 5000 + 6000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.18 + 0.07;
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

    // Distant ambient thunder sky flash
    if (ambientFlashAlpha > 0.005) {
      ctx.fillStyle = `rgba(195, 210, 245, ${ambientFlashAlpha * 0.75})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 1. Drifting Atmospheric Storm Squall Haze
    renderStormSquallHaze(simTime, flashBoost);

    // 2. Rotating Lighthouse Beacon & Eye-Splash Bloom
    beacon.draw(flashBoost);

    // 3. Dense, Needle-Fine, Wind-Swept Bad Storm Rain (Zero Splashes)
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flashBoost);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
