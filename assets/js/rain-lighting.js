/**
 * Cinematic Realistic Living Storm Atmosphere for zaidamin.org:
 * 1. Procedural Volumetric Storm Clouds: multi-lobed organic cloud puffs that billow, churn, and drift smoothly
 * 2. High-Altitude Scud & Atmospheric Air Currents: fast windblown storm vapor tearing across the sky
 * 3. Sea-Level Storm Haze: soft atmospheric rain mist at the ocean horizon
 * 4. Realistic Intra-Cloud Lightning Engine: multi-stroke flash illuminating the cloud bodies and rain glints
 * 5. Heavy Driving Storm Rain: high-velocity wind-field rainfall with dynamic gale squalls & gusts
 * 6. 3D Rotating Lighthouse Beacon: oceanic sweeping volumetric beam and soft eye-splash bloom
 * 7. Clean, pristine ocean: 100% natural, fused seamlessly over the real classical painting
 */

(function() {
  const canvas = document.getElementById('rain-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = 0;
  let height = 0;
  let simTime = 0;

  // ==========================================================================
  // PROCEDURAL PRE-RENDERED SPRITES (Organic, Seamless, GPU-Accelerated)
  // ==========================================================================
  // 1. Organic Cumulus Storm Cloud Puff
  const cloudSprite = (function() {
    const c = document.createElement('canvas');
    c.width = 256;
    c.height = 256;
    const sctx = c.getContext('2d');

    const lobes = [
      { x: 128, y: 128, r: 85, a: 0.65 },
      { x: 96,  y: 118, r: 70, a: 0.50 },
      { x: 160, y: 118, r: 70, a: 0.50 },
      { x: 110, y: 148, r: 60, a: 0.45 },
      { x: 148, y: 148, r: 60, a: 0.45 },
      { x: 74,  y: 132, r: 48, a: 0.35 },
      { x: 182, y: 132, r: 48, a: 0.35 },
      { x: 128, y: 92,  r: 58, a: 0.55 }
    ];

    for (let lobe of lobes) {
      const grad = sctx.createRadialGradient(lobe.x, lobe.y, 0, lobe.x, lobe.y, lobe.r);
      grad.addColorStop(0, `rgba(205, 225, 250, ${lobe.a})`);
      grad.addColorStop(0.4, `rgba(165, 195, 230, ${lobe.a * 0.6})`);
      grad.addColorStop(0.75, `rgba(125, 155, 195, ${lobe.a * 0.2})`);
      grad.addColorStop(1, 'rgba(95, 125, 165, 0)');

      sctx.fillStyle = grad;
      sctx.beginPath();
      sctx.arc(lobe.x, lobe.y, lobe.r, 0, Math.PI * 2);
      sctx.fill();
    }
    return c;
  })();

  // 2. Wispy Gale Scud (Torn Low-Altitude Storm Vapor)
  const scudSprite = (function() {
    const c = document.createElement('canvas');
    c.width = 340;
    c.height = 120;
    const sctx = c.getContext('2d');

    sctx.save();
    sctx.scale(1.0, 0.35);
    const grad = sctx.createRadialGradient(170, 60 / 0.35, 0, 170, 60 / 0.35, 150);
    grad.addColorStop(0, 'rgba(215, 235, 255, 0.60)');
    grad.addColorStop(0.35, 'rgba(175, 205, 240, 0.35)');
    grad.addColorStop(0.70, 'rgba(130, 165, 205, 0.10)');
    grad.addColorStop(1, 'rgba(95, 130, 175, 0)');

    sctx.fillStyle = grad;
    sctx.beginPath();
    sctx.arc(170, 60 / 0.35, 150, 0, Math.PI * 2);
    sctx.fill();
    sctx.restore();
    return c;
  })();

  // 3. Horizon Storm Rain Haze Band
  const hazeSprite = (function() {
    const c = document.createElement('canvas');
    c.width = 600;
    c.height = 140;
    const sctx = c.getContext('2d');

    const grad = sctx.createLinearGradient(0, 0, 0, 140);
    grad.addColorStop(0, 'rgba(170, 200, 235, 0)');
    grad.addColorStop(0.5, 'rgba(195, 220, 248, 0.32)');
    grad.addColorStop(1, 'rgba(170, 200, 235, 0)');

    sctx.fillStyle = grad;
    sctx.fillRect(0, 0, 600, 140);
    return c;
  })();

  // Pools
  let cloudClusters = [];
  let scudWisps = [];
  let hazeBands = [];
  let raindrops = [];

  // ==========================================================================
  // REALISTIC INTRA-CLOUD LIGHTNING SYSTEM
  // ==========================================================================
  const stormLightning = {
    state: 0, // 0: idle, 1: leader, 2: main stroke, 3: secondary stroke, 4: decay
    intensity: 0,
    nextTime: Date.now() + 5000,
    stateTimer: 0,

    update() {
      const now = Date.now();

      if (this.state === 0) {
        if (now > this.nextTime) {
          this.state = 1; // trigger leader flash
          this.stateTimer = 0;
          this.intensity = Math.random() * 0.35 + 0.25;
          this.nextTime = now + (Math.random() * 8000 + 7000);
        }
      } else if (this.state === 1) {
        // Leader flash (quick preliminary flicker)
        this.stateTimer++;
        if (this.stateTimer > 2) {
          this.state = 2; // main brilliant return stroke
          this.stateTimer = 0;
          this.intensity = Math.random() * 0.45 + 0.55; // 0.55 to 1.0
        }
      } else if (this.state === 2) {
        // Main stroke
        this.stateTimer++;
        if (this.stateTimer > 3) {
          this.state = 3; // second strike / re-strike
          this.stateTimer = 0;
          this.intensity = Math.random() * 0.30 + 0.40;
        }
      } else if (this.state === 3) {
        // Re-strike
        this.stateTimer++;
        if (this.stateTimer > 3) {
          this.state = 4; // exponential decay
          this.stateTimer = 0;
        }
      } else if (this.state === 4) {
        // Exponential decay
        this.intensity *= 0.82;
        if (this.intensity < 0.01) {
          this.intensity = 0;
          this.state = 0;
        }
      }
    }
  };

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
  // 2. DYNAMIC STORM WIND & GALE GUST SYSTEM
  // ==========================================================================
  function getStormWind(t) {
    // Dynamic gust factor: surges every 4 to 6 seconds
    const gust = Math.max(0, Math.sin(t * 0.45) * 0.16) + Math.max(0, Math.cos(t * 0.95) * 0.09);
    return {
      baseAngle: 0.36 + gust, // ~21 to 32 degrees slanting down-right
      gustSpeedMultiplier: 1.0 + gust * 1.4,
      gustFactor: gust
    };
  }

  function getLocalRainAngle(x, y, t, bias) {
    const wind = getStormWind(t);
    const altitudeShear = (y / Math.max(height, 1)) * 0.10;
    const wave = Math.sin(x * 0.003 - t * 0.7 + y * 0.002) * 0.05;
    return wind.baseAngle + altitudeShear + wave + bias;
  }

  // ==========================================================================
  // 3. LIVING PROCEDURAL STORM CLOUD MASSES (Organic Billowing Puffs)
  // ==========================================================================
  class CloudCluster {
    constructor(x, y, particleCount = 10) {
      this.x = x;
      this.y = y;
      this.speed = Math.random() * 0.22 + 0.26; // stately storm drift
      this.particles = [];

      for (let i = 0; i < particleCount; i++) {
        this.particles.push({
          ox: (Math.random() - 0.5) * 260,
          oy: (Math.random() - 0.5) * 85,
          scale: Math.random() * 0.65 + 0.85,
          rotation: Math.random() * Math.PI * 2,
          rotSpeed: (Math.random() - 0.5) * 0.0018,
          churnSpeed: Math.random() * 0.3 + 0.2,
          seed: Math.random() * 100,
          baseAlpha: Math.random() * 0.035 + 0.045
        });
      }
    }

    update() {
      this.x += this.speed;
      // Wrap seamlessly
      if (this.x - 300 > width) {
        this.x = -350;
        this.y = height * (Math.random() * 0.32 + 0.04);
      }
    }

    draw(lightningBoost) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      for (let p of this.particles) {
        p.rotation += p.rotSpeed;

        // Organic harmonic churn within the cloud mass
        const churnX = Math.sin(simTime * p.churnSpeed + p.seed) * 14;
        const churnY = Math.cos(simTime * (p.churnSpeed * 0.8) + p.seed) * 8;
        const scalePulse = 1.0 + Math.sin(simTime * 0.25 + p.seed) * 0.08;

        const px = this.x + p.ox + churnX;
        const py = this.y + p.oy + churnY;
        const s = p.scale * scalePulse;
        const w = 256 * s;
        const h = 256 * s;

        // Cloud illumination from ambient lightning
        const alpha = Math.min(p.baseAlpha * (1 + lightningBoost * 2.8), 0.28);

        ctx.save();
        ctx.translate(px, py);
        ctx.rotate(p.rotation);
        ctx.globalAlpha = alpha;
        ctx.drawImage(cloudSprite, -w * 0.5, -h * 0.5, w, h);
        ctx.restore();
      }

      ctx.restore();
    }
  }

  // ==========================================================================
  // 4. HIGH-ALTITUDE SCUD & TORN STORM VAPOR (Atmospheric Air Motion)
  // ==========================================================================
  class ScudWisp {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = initial ? Math.random() * (width + 400) - 200 : -350;
      this.y = height * (Math.random() * 0.44 + 0.06);
      this.scale = Math.random() * 0.55 + 0.75;
      this.baseSpeed = Math.random() * 1.4 + 1.8; // swift gale speed
      this.baseAlpha = Math.random() * 0.035 + 0.030;
      this.seed = Math.random() * 100;
    }

    update() {
      const wind = getStormWind(simTime);
      this.x += this.baseSpeed * wind.gustSpeedMultiplier;
      this.y += Math.sin(simTime * 0.7 + this.seed) * 0.22;

      if (this.x - 300 > width) {
        this.reset();
      }
    }

    draw(lightningBoost) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      const wind = getStormWind(simTime);
      const angle = wind.baseAngle - 0.22; // aligned with storm air
      const alpha = Math.min(this.baseAlpha * (1 + lightningBoost * 2.0), 0.18);

      const w = 340 * this.scale;
      const h = 120 * this.scale;

      ctx.translate(this.x, this.y);
      ctx.rotate(angle);
      ctx.globalAlpha = alpha;
      ctx.drawImage(scudSprite, -w * 0.5, -h * 0.5, w, h);
      ctx.restore();
    }
  }

  // ==========================================================================
  // 5. SEA-LEVEL STORM HAZE (Drifting Atmospheric Spray Band at Horizon)
  // ==========================================================================
  class HorizonHaze {
    constructor(x, y, speed, alpha) {
      this.x = x;
      this.y = y;
      this.speed = speed;
      this.baseAlpha = alpha;
      this.seed = Math.random() * 100;
    }

    update() {
      this.x += this.speed;
      if (this.x - 400 > width) {
        this.x = -600;
      }
    }

    draw(lightningBoost) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      const pulse = Math.sin(simTime * 0.4 + this.seed) * 0.012;
      const alpha = Math.min((this.baseAlpha + pulse) * (1 + lightningBoost * 1.5), 0.15);

      ctx.globalAlpha = alpha;
      ctx.drawImage(hazeSprite, this.x, this.y, 600, 140);
      ctx.restore();
    }
  }

  // ==========================================================================
  // 6. HEAVY DRIVING STORM RAIN (High-Speed Multi-Tier Gale Streaks)
  // ==========================================================================
  class HeavyStormRaindrop {
    constructor() {
      const r = Math.random();
      if (r < 0.42) {
        this.tier = 0; // distant dense mist sheets & drizzle
        this.baseSpeed = Math.random() * 3.5 + 13.0;
        this.baseLength = Math.random() * 6 + 15;
        this.width = 0.55;
        this.baseAlpha = Math.random() * 0.07 + 0.14;
        this.bias = (Math.random() - 0.5) * 0.08;
      } else if (r < 0.82) {
        this.tier = 1; // midground driving gale downpour
        this.baseSpeed = Math.random() * 4.5 + 18.0;
        this.baseLength = Math.random() * 8 + 22;
        this.width = 0.75;
        this.baseAlpha = Math.random() * 0.09 + 0.22;
        this.bias = (Math.random() - 0.5) * 0.06;
      } else {
        this.tier = 2; // foreground heavy storm streaks
        this.baseSpeed = Math.random() * 5.5 + 24.0;
        this.baseLength = Math.random() * 12 + 30;
        this.width = 0.95;
        this.baseAlpha = Math.random() * 0.12 + 0.30;
        this.bias = (Math.random() - 0.5) * 0.04;
      }

      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 500) - 250;
      this.y = initial ? Math.random() * height : -45;
      this.speed = this.baseSpeed * (0.95 + Math.random() * 0.10);
      this.alpha = this.baseAlpha;
    }

    update() {
      const wind = getStormWind(simTime);
      const angle = getLocalRainAngle(this.x, this.y, simTime, this.bias);
      const totalSpeed = this.speed * wind.gustSpeedMultiplier;

      const vx = Math.sin(angle) * totalSpeed;
      const vy = Math.cos(angle) * totalSpeed;

      this.x += vx;
      this.y += vy;

      if (this.y > height + 45 || this.x > width + 300) {
        this.reset();
      }
    }

    draw(lightningBoost) {
      const angle = getLocalRainAngle(this.x, this.y, simTime, this.bias);
      const wind = getStormWind(simTime);
      const currentLength = this.baseLength * wind.gustSpeedMultiplier;

      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      // Check if illuminated by rotating lighthouse beam
      let beamGlint = 1.0;
      const lx = beacon.lx;
      const ly = beacon.ly;
      if (this.x > lx && Math.abs(this.y - ly) < 48) {
        const facingOcean = Math.max(0, Math.cos(beacon.angle));
        beamGlint = 1.0 + facingOcean * 1.6;
      }

      // Lightning glint boost
      const a = Math.min(this.alpha * (1 + lightningBoost * 2.2) * beamGlint, 0.62);

      const endX = this.x + Math.sin(angle) * currentLength;
      const endY = this.y + Math.cos(angle) * currentLength;

      const grad = ctx.createLinearGradient(this.x, this.y, endX, endY);
      if (beamGlint > 1.15) {
        grad.addColorStop(0, `rgba(254, 243, 199, ${a * 0.35})`);
        grad.addColorStop(0.4, `rgba(254, 243, 199, ${a})`);
        grad.addColorStop(1, 'rgba(254, 243, 199, 0)');
      } else {
        grad.addColorStop(0, `rgba(210, 235, 255, ${a * 0.35})`);
        grad.addColorStop(0.4, `rgba(228, 244, 255, ${a})`);
        grad.addColorStop(1, 'rgba(210, 235, 255, 0)');
      }

      ctx.strokeStyle = grad;
      ctx.lineWidth = this.width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(endX, endY);
      ctx.stroke();
      ctx.restore();
    }
  }

  // ==========================================================================
  // 7. INITIALIZE STORM SYSTEM
  // ==========================================================================
  function initStormAtmosphere() {
    // A. 4 Major Volumetric Storm Cloud Clusters across the sky
    cloudClusters = [];
    const clusterPositions = [
      { x: width * 0.15, y: height * 0.18, count: 11 },
      { x: width * 0.42, y: height * 0.14, count: 12 },
      { x: width * 0.72, y: height * 0.20, count: 11 },
      { x: width * 0.96, y: height * 0.15, count: 10 }
    ];
    for (let c of clusterPositions) {
      cloudClusters.push(new CloudCluster(c.x, c.y, c.count));
    }

    // B. Low Scud Wisps (Torn Gale Vapor)
    scudWisps = [];
    const scudCount = 8;
    for (let i = 0; i < scudCount; i++) {
      scudWisps.push(new ScudWisp());
    }

    // C. Sea-Level Horizon Storm Spray Haze
    hazeBands = [];
    hazeBands.push(new HorizonHaze(0, height * 0.46, 0.35, 0.055));
    hazeBands.push(new HorizonHaze(width * 0.55, height * 0.50, 0.42, 0.050));

    // D. Heavy Driving Storm Rain (~720 drops on desktop)
    const count = Math.min(Math.floor((width * height) / 1050), 750);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new HeavyStormRaindrop());
    }
  }

  function resize() {
    const parent = canvas.parentElement;
    width = canvas.width = parent.clientWidth;
    height = canvas.height = parent.clientHeight;
    initStormAtmosphere();
  }

  window.addEventListener('resize', resize);

  // ==========================================================================
  // 8. MAIN ANIMATION & RENDERING LOOP
  // ==========================================================================
  function render() {
    ctx.clearRect(0, 0, width, height);
    simTime += 0.020;

    stormLightning.update();
    beacon.update();

    const flash = stormLightning.intensity;

    // Distant ambient thunder sky flash
    if (flash > 0.02) {
      ctx.fillStyle = `rgba(215, 230, 255, ${flash * 0.22})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 1. Procedural Living Volumetric Storm Clouds (Screen blend, billows & churns)
    for (let cluster of cloudClusters) {
      cluster.update();
      cluster.draw(flash);
    }

    // 2. High-Altitude Scud & Atmospheric Gale Currents
    for (let scud of scudWisps) {
      scud.update();
      scud.draw(flash);
    }

    // 3. Sea-Level Horizon Storm Spray Haze
    for (let haze of hazeBands) {
      haze.update();
      haze.draw(flash);
    }

    // 4. Rotating Lighthouse Beacon & Eye-Splash Bloom
    beacon.draw(1 + flash * 0.8);

    // 5. Heavy Driving Storm Rain (High-velocity, gust-reactive)
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flash);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
