/**
 * Cinematic Realistic Living Storm Atmosphere for zaidamin.org:
 * 1. Procedural Volumetric Storm Clouds: multi-lobed organic cloud puffs that billow, churn, and drift smoothly
 * 2. High-Altitude Scud & Atmospheric Air Currents: fast windblown storm vapor tearing across the sky
 * 3. Sea-Level Storm Haze: soft atmospheric rain mist at the ocean horizon
 * 4. Soft Distant Lightning Strikes at Behind: procedural branching lightning bolts deep in the sky
 * 5. Distant Village Lamps & Secondary Lighthouse: warm cottage lights twinkling across the bay & rhythmic distant beacon
 * 6. Soft Feathered Volumetric Lighthouse Beam: zero cut edges, silky Gaussian atmospheric diffusion & eye-splash bloom
 * 7. Soft, Small & Smooth Rain with Depth of Field: delicate heterogeneous micro-streaks with 3 optical depth layers
 * 8. Clean, borderless presentation: seamlessly integrated with the page layout
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
  // 1. SOFT RANDOM DISTANT LIGHTNING STRIKES (Behind Clouds)
  // ==========================================================================
  let activeLightningStrike = null;
  let nextLightningStrikeTime = Date.now() + 4000;
  let ambientFlashIntensity = 0;

  function createLightningBolt(x1, y1, x2, y2, displace, branchProb = 0.38) {
    const branches = [];
    function subdivide(p1, p2, disp, curDepth) {
      if (disp < 3.5 || curDepth > 5) {
        return [p1, p2];
      }
      const midX = (p1.x + p2.x) * 0.5 + (Math.random() - 0.5) * disp;
      const midY = (p1.y + p2.y) * 0.5 + (Math.random() - 0.5) * (disp * 0.25);
      const mid = { x: midX, y: midY };

      if (curDepth < 3 && Math.random() < branchProb) {
        const branchEnd = {
          x: midX + (Math.random() - 0.3) * (disp * 2.8),
          y: midY + (Math.random() * 0.6 + 0.4) * (disp * 2.2)
        };
        branches.push(subdivide(mid, branchEnd, disp * 0.5, curDepth + 1));
      }

      const left = subdivide(p1, mid, disp * 0.52, curDepth + 1);
      const right = subdivide(mid, p2, disp * 0.52, curDepth + 1);
      return left.slice(0, -1).concat(right);
    }

    const mainPath = subdivide({ x: x1, y: y1 }, { x: x2, y: y2 }, displace, 0);
    return { mainPath, branches };
  }

  function triggerRandomLightningStrike() {
    const startX = width * (Math.random() * 0.65 + 0.18);
    const startY = height * (Math.random() * 0.08 + 0.01);
    const endX = startX + (Math.random() - 0.5) * (width * 0.16);
    const endY = height * (Math.random() * 0.14 + 0.42);
    const displace = Math.min(width * 0.045, 46);

    const bolt = createLightningBolt(startX, startY, endX, endY, displace);
    activeLightningStrike = {
      bolt: bolt,
      frame: 0,
      maxFrames: Math.floor(Math.random() * 5 + 9),
      alpha: 0
    };
  }

  function updateAndDrawLightningStrike() {
    const now = Date.now();
    if (!activeLightningStrike && now > nextLightningStrikeTime) {
      triggerRandomLightningStrike();
      nextLightningStrikeTime = now + (Math.random() * 9000 + 7000);
    }

    if (!activeLightningStrike) {
      ambientFlashIntensity *= 0.88;
      return;
    }

    activeLightningStrike.frame++;
    const f = activeLightningStrike.frame;
    const mf = activeLightningStrike.maxFrames;

    let strikeAlpha = 0;
    if (f <= 2) strikeAlpha = 0.28;
    else if (f <= 5) strikeAlpha = 0.54;
    else if (f <= 8) strikeAlpha = 0.32;
    else strikeAlpha = Math.max(0, 0.32 * (1 - (f - 8) / (mf - 8)));

    ambientFlashIntensity = strikeAlpha * 0.35;

    if (f > mf || strikeAlpha <= 0.01) {
      activeLightningStrike = null;
      return;
    }

    ctx.save();
    ctx.globalCompositeOperation = 'screen';
    ctx.shadowColor = 'rgba(186, 230, 253, 0.65)';
    ctx.shadowBlur = 8;

    // Draw main soft bolt path
    ctx.strokeStyle = `rgba(230, 244, 255, ${strikeAlpha * 0.72})`;
    ctx.lineWidth = 1.0;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.beginPath();
    const main = activeLightningStrike.bolt.mainPath;
    for (let i = 0; i < main.length; i++) {
      if (i === 0) ctx.moveTo(main[i].x, main[i].y);
      else ctx.lineTo(main[i].x, main[i].y);
    }
    ctx.stroke();

    // Secondary sub-branches (whisper thin & soft)
    ctx.strokeStyle = `rgba(200, 230, 255, ${strikeAlpha * 0.40})`;
    ctx.lineWidth = 0.60;
    for (let b of activeLightningStrike.bolt.branches) {
      ctx.beginPath();
      for (let i = 0; i < b.length; i++) {
        if (i === 0) ctx.moveTo(b[i].x, b[i].y);
        else ctx.lineTo(b[i].x, b[i].y);
      }
      ctx.stroke();
    }

    // Soft atmospheric cloud illumination around strike origin
    const origin = main[0];
    const cloudGlow = ctx.createRadialGradient(origin.x, origin.y, 10, origin.x, origin.y, width * 0.22);
    cloudGlow.addColorStop(0, `rgba(215, 235, 255, ${strikeAlpha * 0.22})`);
    cloudGlow.addColorStop(0.5, `rgba(180, 215, 255, ${strikeAlpha * 0.08})`);
    cloudGlow.addColorStop(1, 'rgba(180, 215, 255, 0)');
    ctx.fillStyle = cloudGlow;
    ctx.fillRect(0, 0, width, height);

    ctx.restore();
  }

  // ==========================================================================
  // 2. DISTANT VILLAGE HOUSE LAMPS & SECONDARY LIGHTHOUSE AMBIENCE
  // ==========================================================================
  const distantVillageLamps = [
    // A. Cliffside Hill Village Cottages (on the cliff left of the lighthouse)
    { nx: 0.082, ny: 0.258, size: 1.0, baseA: 0.85, seed: 1.2 },
    { nx: 0.104, ny: 0.278, size: 1.2, baseA: 0.90, seed: 3.4 },
    { nx: 0.122, ny: 0.298, size: 0.9, baseA: 0.80, seed: 5.7 },
    { nx: 0.144, ny: 0.312, size: 1.1, baseA: 0.85, seed: 8.1 },
    { nx: 0.168, ny: 0.324, size: 0.9, baseA: 0.75, seed: 10.6 },
    { nx: 0.185, ny: 0.334, size: 1.0, baseA: 0.80, seed: 13.2 },
    // B. Distant Shoreline Cottages Across the Bay (Horizon right)
    { nx: 0.672, ny: 0.518, size: 0.85, baseA: 0.75, seed: 2.5 },
    { nx: 0.694, ny: 0.522, size: 1.05, baseA: 0.85, seed: 4.8 },
    { nx: 0.715, ny: 0.516, size: 0.80, baseA: 0.70, seed: 6.9 },
    { nx: 0.732, ny: 0.524, size: 1.15, baseA: 0.90, seed: 9.3 },
    { nx: 0.758, ny: 0.519, size: 0.95, baseA: 0.80, seed: 11.7 },
    { nx: 0.776, ny: 0.526, size: 0.85, baseA: 0.75, seed: 14.1 },
    { nx: 0.802, ny: 0.521, size: 1.05, baseA: 0.85, seed: 16.5 }
  ];

  function drawDistantVillageLamps(boost) {
    ctx.save();
    ctx.globalCompositeOperation = 'screen';

    for (let lamp of distantVillageLamps) {
      const x = width * lamp.nx;
      const y = height * lamp.ny;

      // Realistic warm storm twinkle: distant cottage lights flickering through rain & sea haze
      const twinkle = 0.70 + Math.sin(simTime * 2.8 + lamp.seed) * 0.20 + Math.cos(simTime * 5.5 + lamp.seed) * 0.10;
      const a = Math.min(lamp.baseA * twinkle * boost, 1.0);

      // Soft warm golden hearth halo
      const haloGrad = ctx.createRadialGradient(x, y, 0, x, y, lamp.size * 4.5);
      haloGrad.addColorStop(0, `rgba(254, 240, 138, ${a * 0.75})`);
      haloGrad.addColorStop(0.4, `rgba(245, 158, 11, ${a * 0.35})`);
      haloGrad.addColorStop(1, 'rgba(217, 119, 6, 0)');

      ctx.fillStyle = haloGrad;
      ctx.beginPath();
      ctx.arc(x, y, lamp.size * 4.5, 0, Math.PI * 2);
      ctx.fill();

      // Sharp warm lamp pinprick core
      ctx.fillStyle = `rgba(255, 255, 245, ${a * 0.95})`;
      ctx.beginPath();
      ctx.arc(x, y, lamp.size * 0.85, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  // Distant secondary lighthouse far behind across the bay
  const distantSecondaryLighthouse = {
    nx: 0.865,
    ny: 0.496,
    angle: 1.5,
    speed: 0.016, // distinct ~6s revolution

    update() {
      this.angle += this.speed;
      if (this.angle > Math.PI * 2) this.angle -= Math.PI * 2;
    },

    draw(boost) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      const x = width * this.nx;
      const y = height * this.ny;

      const facingViewer = Math.max(0, Math.sin(this.angle));
      const facingAcross = Math.max(0, Math.cos(this.angle));

      // Periodic maritime pulse / flash when facing viewer
      const pulse = Math.pow(facingViewer, 5.0);
      const pulseAlpha = Math.min((0.25 + pulse * 0.75) * boost, 1.0);

      // Faint sweeping miniature horizon beam
      if (facingAcross > 0.1) {
        const beamLen = width * 0.11;
        const bAlpha = Math.pow(facingAcross, 1.5) * 0.16 * boost;
        const grad = ctx.createLinearGradient(x, y, x - beamLen, y + 2);
        grad.addColorStop(0, `rgba(254, 240, 138, ${bAlpha * 1.4})`);
        grad.addColorStop(0.5, `rgba(254, 240, 138, ${bAlpha * 0.5})`);
        grad.addColorStop(1, 'rgba(254, 240, 138, 0)');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.moveTo(x, y - 0.8);
        ctx.lineTo(x - beamLen, y - 4);
        ctx.lineTo(x - beamLen, y + 6);
        ctx.lineTo(x, y + 0.8);
        ctx.closePath();
        ctx.fill();
      }

      // Distant beacon pinprick & soft aura
      const halo = ctx.createRadialGradient(x, y, 0, x, y, 6.0);
      halo.addColorStop(0, `rgba(255, 255, 240, ${pulseAlpha * 0.9})`);
      halo.addColorStop(0.3, `rgba(253, 224, 71, ${pulseAlpha * 0.5})`);
      halo.addColorStop(1, 'rgba(253, 224, 71, 0)');

      ctx.fillStyle = halo;
      ctx.beginPath();
      ctx.arc(x, y, 6.0, 0, Math.PI * 2);
      ctx.fill();

      // Core point
      ctx.fillStyle = `rgba(255, 255, 255, ${pulseAlpha})`;
      ctx.beginPath();
      ctx.arc(x, y, 1.1, 0, Math.PI * 2);
      ctx.fill();

      ctx.restore();
    }
  };

  // ==========================================================================
  // 3. PRIMARY ROTATING LIGHTHOUSE BEACON (Ultra-Soft Natural Warm Light & Zero Hard Edges)
  // ==========================================================================
  const beacon = {
    get lx() { return width * 0.321; },
    get ly() { return height * 0.267; },
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

      // A. Steady Ultra-Soft Natural Warm Lantern Glow (Zero Cutting Edges, Silky Atmospheric Feather)
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      ctx.filter = 'blur(6px)';

      const baseCoreGrad = ctx.createRadialGradient(lx, ly, 0, lx, ly, 24);
      baseCoreGrad.addColorStop(0, 'rgba(255, 255, 250, 0.95)');
      baseCoreGrad.addColorStop(0.20, 'rgba(255, 238, 170, 0.75)');
      baseCoreGrad.addColorStop(0.48, 'rgba(250, 195, 80, 0.35)');
      baseCoreGrad.addColorStop(0.78, 'rgba(225, 145, 40, 0.08)');
      baseCoreGrad.addColorStop(1, 'rgba(200, 110, 20, 0)');

      ctx.fillStyle = baseCoreGrad;
      ctx.beginPath();
      ctx.arc(lx, ly, 36, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // B. Volumetric Sweeping Beam with Soft Feathering & Natural Warm Light (Zero Cutting Edges)
      if (facingOcean > 0.02) {
        const beamIntensity = Math.pow(facingOcean, 1.25) * flashBoost;
        const beamLength = width * 0.72;
        const beamPitch = 0.015 + Math.sin(this.angle * 2) * 0.010;
        const baseHalfWidth = 28 + facingOcean * 16;

        ctx.save();
        ctx.globalCompositeOperation = 'screen';
        ctx.filter = 'blur(14px)'; // True optical Gaussian feathering dissolving all cutting edges

        // 3-pass warm light volumetric beam
        const beamLayers = [
          { widthScale: 1.30, alphaScale: 0.18, lenScale: 0.96 },
          { widthScale: 0.90, alphaScale: 0.38, lenScale: 0.90 },
          { widthScale: 0.50, alphaScale: 0.65, lenScale: 0.82 }
        ];

        for (let layer of beamLayers) {
          const halfW = baseHalfWidth * layer.widthScale;
          const curLen = beamLength * layer.lenScale;
          const layerEndY = ly + Math.sin(beamPitch) * curLen;

          const p1x = lx - 2.0;
          const p1y = ly - 1.5;
          const p2x = lx - 2.0;
          const p2y = ly + 1.5;
          const p3x = lx + curLen;
          const p3y = layerEndY + halfW;
          const p4x = lx + curLen;
          const p4y = layerEndY - halfW;

          const beamGrad = ctx.createLinearGradient(lx, ly, lx + curLen, layerEndY);
          beamGrad.addColorStop(0, `rgba(255, 252, 238, ${0.85 * beamIntensity * layer.alphaScale})`);
          beamGrad.addColorStop(0.15, `rgba(255, 230, 140, ${0.60 * beamIntensity * layer.alphaScale})`);
          beamGrad.addColorStop(0.40, `rgba(248, 192, 75, ${0.30 * beamIntensity * layer.alphaScale})`);
          beamGrad.addColorStop(0.70, `rgba(225, 145, 40, ${0.10 * beamIntensity * layer.alphaScale})`);
          beamGrad.addColorStop(0.95, 'rgba(195, 115, 25, 0)');
          beamGrad.addColorStop(1, 'rgba(195, 115, 25, 0)');

          ctx.fillStyle = beamGrad;
          ctx.beginPath();
          ctx.moveTo(p1x, p1y);
          ctx.lineTo(p4x, p4y);
          ctx.quadraticCurveTo(lx + curLen + 25, layerEndY, p3x, p3y);
          ctx.lineTo(p2x, p2y);
          ctx.closePath();
          ctx.fill();
        }

        ctx.restore();
      }

      // C. Soft Natural Warm Lens Flare Corona & Anamorphic Glare when Sweeping toward Viewer
      if (facingViewer > 0.05) {
        const eyeSplash = Math.pow(facingViewer, 3.2);
        const flareAlpha = Math.min(eyeSplash * flashBoost, 1.0);

        ctx.save();
        ctx.globalCompositeOperation = 'screen';
        ctx.filter = 'blur(8px)';

        // Soft warm atmospheric wash over viewer
        const eyeWashGrad = ctx.createRadialGradient(lx, ly, 10, lx, ly, Math.max(width, height) * 0.75);
        eyeWashGrad.addColorStop(0, `rgba(255, 248, 225, ${0.16 * flareAlpha})`);
        eyeWashGrad.addColorStop(0.35, `rgba(255, 220, 110, ${0.06 * flareAlpha})`);
        eyeWashGrad.addColorStop(0.7, `rgba(240, 175, 60, ${0.015 * flareAlpha})`);
        eyeWashGrad.addColorStop(1, 'rgba(240, 175, 60, 0)');

        ctx.fillStyle = eyeWashGrad;
        ctx.fillRect(0, 0, width, height);

        // Radiant Soft Lens Flare Corona
        const flareRadius = 55 + eyeSplash * 45;
        const coronaGrad = ctx.createRadialGradient(lx, ly, 0, lx, ly, flareRadius);
        coronaGrad.addColorStop(0, `rgba(255, 255, 250, ${0.95 * flareAlpha})`);
        coronaGrad.addColorStop(0.20, `rgba(255, 235, 160, ${0.75 * flareAlpha})`);
        coronaGrad.addColorStop(0.50, `rgba(245, 185, 65, ${0.40 * flareAlpha})`);
        coronaGrad.addColorStop(0.80, `rgba(215, 130, 30, ${0.10 * flareAlpha})`);
        coronaGrad.addColorStop(1, 'rgba(200, 110, 20, 0)');

        ctx.fillStyle = coronaGrad;
        ctx.beginPath();
        ctx.arc(lx, ly, flareRadius + 15, 0, Math.PI * 2);
        ctx.fill();

        // Warm Anamorphic Horizontal Glare Streak
        const streakLength = 100 + eyeSplash * 140;
        const streakHeight = 2.0 + eyeSplash * 1.8;
        const streakGrad = ctx.createLinearGradient(lx - streakLength, ly, lx + streakLength, ly);
        streakGrad.addColorStop(0, 'rgba(255, 245, 210, 0)');
        streakGrad.addColorStop(0.35, `rgba(255, 225, 130, ${0.28 * flareAlpha})`);
        streakGrad.addColorStop(0.5, `rgba(255, 255, 250, ${0.85 * flareAlpha})`);
        streakGrad.addColorStop(0.65, `rgba(255, 225, 130, ${0.28 * flareAlpha})`);
        streakGrad.addColorStop(1, 'rgba(255, 245, 210, 0)');

        ctx.fillStyle = streakGrad;
        ctx.beginPath();
        ctx.ellipse(lx, ly, streakLength, streakHeight, 0, 0, Math.PI * 2);
        ctx.fill();

        // Brilliant Soft Filament Core
        ctx.fillStyle = `rgba(255, 255, 255, ${0.92 * flareAlpha})`;
        ctx.beginPath();
        ctx.arc(lx, ly, 3.5 + eyeSplash * 2.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
      }

      ctx.restore();
    }
  };

    // 4. DYNAMIC STORM WIND & GALE GUST SYSTEM
  // ==========================================================================
  function getStormWind(t) {
    const gust = Math.max(0, Math.sin(t * 0.45) * 0.14) + Math.max(0, Math.cos(t * 0.95) * 0.08);
    return {
      baseAngle: 0.34 + gust,
      gustSpeedMultiplier: 1.0 + gust * 1.25,
      gustFactor: gust
    };
  }

  function getLocalRainAngle(x, y, t, bias) {
    const wind = getStormWind(t);
    const altitudeShear = (y / Math.max(height, 1)) * 0.08;
    const wave = Math.sin(x * 0.003 - t * 0.7 + y * 0.002) * 0.04;
    return wind.baseAngle + altitudeShear + wave + bias;
  }

  // ==========================================================================
  // 5. LIVING PROCEDURAL STORM CLOUD MASSES (Organic Billowing Puffs)
  // ==========================================================================
  class CloudCluster {
    constructor(x, y, particleCount = 10) {
      this.x = x;
      this.y = y;
      this.speed = Math.random() * 0.18 + 0.22;
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

        const churnX = Math.sin(simTime * p.churnSpeed + p.seed) * 14;
        const churnY = Math.cos(simTime * (p.churnSpeed * 0.8) + p.seed) * 8;
        const scalePulse = 1.0 + Math.sin(simTime * 0.25 + p.seed) * 0.08;

        const px = this.x + p.ox + churnX;
        const py = this.y + p.oy + churnY;
        const s = p.scale * scalePulse;
        const w = 256 * s;
        const h = 256 * s;

        const alpha = Math.min(p.baseAlpha * (1 + lightningBoost * 2.5), 0.25);

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
  // 6. HIGH-ALTITUDE SCUD & TORN STORM VAPOR (Atmospheric Air Motion)
  // ==========================================================================
  class ScudWisp {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = initial ? Math.random() * (width + 400) - 200 : -350;
      this.y = height * (Math.random() * 0.44 + 0.06);
      this.scale = Math.random() * 0.55 + 0.75;
      this.baseSpeed = Math.random() * 1.2 + 1.5;
      this.baseAlpha = Math.random() * 0.030 + 0.025;
      this.seed = Math.random() * 100;
    }

    update() {
      const wind = getStormWind(simTime);
      this.x += this.baseSpeed * wind.gustSpeedMultiplier;
      this.y += Math.sin(simTime * 0.7 + this.seed) * 0.20;

      if (this.x - 300 > width) {
        this.reset();
      }
    }

    draw(lightningBoost) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      const wind = getStormWind(simTime);
      const angle = wind.baseAngle - 0.22;
      const alpha = Math.min(this.baseAlpha * (1 + lightningBoost * 2.0), 0.16);

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
  // 7. SEA-LEVEL STORM HAZE (Drifting Atmospheric Spray Band at Horizon)
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
      const alpha = Math.min((this.baseAlpha + pulse) * (1 + lightningBoost * 1.4), 0.14);

      ctx.globalAlpha = alpha;
      ctx.drawImage(hazeSprite, this.x, this.y, 600, 140);
      ctx.restore();
    }
  }

  // ==========================================================================
  // 8. NATURAL STORM RAIN WITH DEPTH OF FIELD (DOF BLUR & FOCUS) & SILKY SMOOTHNESS
  // ==========================================================================
  class RealisticDOFRaindrop {
    constructor() {
      // 3 Optical Depth Layers:
      // - Far layer (44%): Distant atmospheric blur, fine mist & soft drizzle
      // - Focal layer (45%): Midground focal plane (in-focus), smooth, delicate driving drops
      // - Near layer (11%): Immediate foreground (out-of-focus bokeh blur), soft & translucent
      const r = Math.random();

      if (r < 0.44) {
        // LAYER 1: Distant Background (Atmospheric Far Blur)
        this.layer = 0;
        this.baseLength = Math.random() * 4.0 + 4.5; // 4.5px to 8.5px
        this.width = 0.35; // delicate, smooth
        this.baseSpeed = Math.random() * 2.0 + 5.5;
        this.baseAlpha = Math.random() * 0.03 + 0.055; // 0.055 - 0.085 (soft atmospheric mist)
        this.blur = 0;
      } else if (r < 0.89) {
        // LAYER 2: Midground Focal Plane (Sharp & Crisp IN-FOCUS, Silky Smooth)
        this.layer = 1;
        const subSize = Math.random();
        if (subSize < 0.38) {
          this.baseLength = Math.random() * 4.0 + 8.0; // 8 - 12px fine drops
          this.width = 0.46;
          this.baseAlpha = Math.random() * 0.03 + 0.10; // 0.10 - 0.13
        } else if (subSize < 0.82) {
          this.baseLength = Math.random() * 5.0 + 12.0; // 12 - 17px standard drops
          this.width = 0.54;
          this.baseAlpha = Math.random() * 0.04 + 0.125; // 0.125 - 0.165
        } else {
          this.baseLength = Math.random() * 6.0 + 16.0; // 16 - 22px driving drops
          this.width = 0.62;
          this.baseAlpha = Math.random() * 0.04 + 0.155; // 0.155 - 0.195
        }
        this.baseSpeed = Math.random() * 2.8 + 8.8;
        this.blur = 0;
      } else {
        // LAYER 3: Immediate Camera Foreground (Out-of-Focus BOKEH Blur)
        this.layer = 2;
        this.baseLength = Math.random() * 12 + 20; // 20px to 32px (gentle motion blur)
        this.width = Math.random() * 0.35 + 1.25; // 1.25px to 1.60px (soft defocused bokeh)
        this.baseSpeed = Math.random() * 3.5 + 13.5;
        this.baseAlpha = Math.random() * 0.025 + 0.050; // 0.050 - 0.075 (ghostly optical blur)
        this.blur = 2.0;
      }

      this.bias = (Math.random() - 0.5) * 0.05;
      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 500) - 250;
      this.y = initial ? Math.random() * height : -40;
      this.speed = this.baseSpeed * (0.96 + Math.random() * 0.08);
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

      if (this.y > height + 40 || this.x > width + 300) {
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
        beamGlint = 1.0 + facingOcean * 1.4;
      }

      // Soft ceiling
      const a = Math.min(this.alpha * (1 + lightningBoost * 1.6) * beamGlint, 0.44);

      const endX = this.x + Math.sin(angle) * currentLength;
      const endY = this.y + Math.cos(angle) * currentLength;

      if (this.layer === 2) {
        // LAYER 3: Out-of-Focus Foreground Bokeh Blur
        ctx.shadowColor = beamGlint > 1.15 ? 'rgba(254, 240, 138, 0.40)' : 'rgba(215, 235, 255, 0.35)';
        ctx.shadowBlur = this.blur;

        const grad = ctx.createLinearGradient(this.x, this.y, endX, endY);
        if (beamGlint > 1.15) {
          grad.addColorStop(0, 'rgba(254, 243, 199, 0)');
          grad.addColorStop(0.35, `rgba(254, 243, 199, ${a * 0.70})`);
          grad.addColorStop(1, 'rgba(254, 243, 199, 0)');
        } else {
          grad.addColorStop(0, 'rgba(210, 235, 255, 0)');
          grad.addColorStop(0.35, `rgba(225, 242, 255, ${a * 0.70})`);
          grad.addColorStop(1, 'rgba(200, 225, 250, 0)');
        }

        ctx.strokeStyle = grad;
        ctx.lineWidth = this.width;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(endX, endY);
        ctx.stroke();

      } else if (this.layer === 1) {
        // LAYER 2: In-Focus Focal Plane (5-stop feathered gradient for silky smoothness)
        const grad = ctx.createLinearGradient(this.x, this.y, endX, endY);
        if (beamGlint > 1.15) {
          grad.addColorStop(0, 'rgba(254, 243, 199, 0)');
          grad.addColorStop(0.25, `rgba(254, 243, 199, ${a * 0.45})`);
          grad.addColorStop(0.50, `rgba(254, 243, 199, ${a})`);
          grad.addColorStop(0.80, `rgba(254, 243, 199, ${a * 0.35})`);
          grad.addColorStop(1, 'rgba(254, 243, 199, 0)');
        } else {
          grad.addColorStop(0, 'rgba(215, 238, 255, 0)');
          grad.addColorStop(0.25, `rgba(225, 242, 255, ${a * 0.45})`);
          grad.addColorStop(0.50, `rgba(235, 248, 255, ${a})`);
          grad.addColorStop(0.80, `rgba(220, 240, 255, ${a * 0.35})`);
          grad.addColorStop(1, 'rgba(200, 225, 250, 0)');
        }

        ctx.strokeStyle = grad;
        ctx.lineWidth = this.width;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(endX, endY);
        ctx.stroke();

      } else {
        // LAYER 1: Distant Background (Atmospheric Far Blur, whisper soft)
        const grad = ctx.createLinearGradient(this.x, this.y, endX, endY);
        grad.addColorStop(0, 'rgba(200, 225, 250, 0)');
        grad.addColorStop(0.4, `rgba(210, 232, 252, ${a})`);
        grad.addColorStop(1, 'rgba(200, 225, 250, 0)');

        ctx.strokeStyle = grad;
        ctx.lineWidth = this.width;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(endX, endY);
        ctx.stroke();
      }

      ctx.restore();
    }
  }

  // ==========================================================================
  // 9. INITIALIZE STORM SYSTEM
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

    // D. Soft Natural Realistic Rain Storm (~540 drops on desktop)
    const count = Math.min(Math.floor((width * height) / 1450), 540);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new RealisticDOFRaindrop());
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
  // 10. MAIN ANIMATION & RENDERING LOOP
  // ==========================================================================
  function render() {
    ctx.clearRect(0, 0, width, height);
    simTime += 0.020;

    beacon.update();
    distantSecondaryLighthouse.update();

    // 1. Soft Random Distant Lightning Strikes (Behind Clouds)
    updateAndDrawLightningStrike();

    // Ambient flash glow across deep sky
    if (ambientFlashIntensity > 0.01) {
      ctx.fillStyle = `rgba(215, 230, 255, ${ambientFlashIntensity * 0.35})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 2. Procedural Living Volumetric Storm Clouds (Screen blend, billows & churns)
    for (let cluster of cloudClusters) {
      cluster.update();
      cluster.draw(ambientFlashIntensity);
    }

    // 3. High-Altitude Scud & Atmospheric Gale Currents
    for (let scud of scudWisps) {
      scud.update();
      scud.draw(ambientFlashIntensity);
    }

    // 4. Sea-Level Horizon Storm Spray Haze
    for (let haze of hazeBands) {
      haze.update();
      haze.draw(ambientFlashIntensity);
    }

    // 5. Distant Village House Lamps & Secondary Lighthouse Ambience
    drawDistantVillageLamps(1 + ambientFlashIntensity * 0.8);
    distantSecondaryLighthouse.draw(1 + ambientFlashIntensity * 0.8);

    // 6. Rotating Lighthouse Beacon with Feathered Soft Edges & Eye Bloom
    beacon.draw(1 + ambientFlashIntensity * 0.8);

    // 7. Soft, Small & Smooth Heterogeneous DOF Rain
    for (let drop of raindrops) {
      drop.update();
      drop.draw(ambientFlashIntensity);
    }

    requestAnimationFrame(render);
  }

  resize();
  requestAnimationFrame(render);
})();
