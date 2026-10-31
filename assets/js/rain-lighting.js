/**
 * Photorealistic Ocean Wave Storm, Lighthouse Splash & Atmospheric Rain Engine
 * For Dr. Zaid Amin (zaidamin.org)
 * 
 * Architecture:
 * 1. WebGL Ocean Wave Simulation:
 *    - GPU-accelerated displacement on the actual painting (assets/images/lighthouse-banner.jpg)
 *    - Sky, clouds, and lighthouse tower remain 100% stationary, sharp, and undisturbed
 *    - Ocean surface (y > 45%) undulates, rolls, surges, and breathes with real fluid mathematics
 * 2. Canvas 2D Atmospheric Storm Particle System:
 *    - Realistic crashing breaker spray and billowing mist puffs at the lighthouse base
 *    - Fine windblown spindrift wisps whipping across wave crests
 *    - Slanted storm rain with wind drift and water collision
 *    - Soft ambient thunder flashes with realistic water surface reflection
 */

(function() {
  // ==========================================================================
  // PART 1: WEBGL FLUID OCEAN WAVE ENGINE (Displaces the Painting's Water)
  // ==========================================================================
  const oceanCanvas = document.getElementById('ocean-canvas');
  let gl = null;
  let oceanProgram = null;
  let oceanTexture = null;
  let isTextureLoaded = false;
  let uTimeLoc, uResLoc, uLightningLoc;
  let globalLightningAlpha = 0;

  if (oceanCanvas) {
    try {
      gl = oceanCanvas.getContext('webgl', { alpha: true, antialias: true }) ||
           oceanCanvas.getContext('experimental-webgl', { alpha: true });
    } catch (e) {
      gl = null;
    }
  }

  const VERTEX_SHADER_SOURCE = `
    attribute vec2 a_position;
    varying vec2 v_uv;
    void main() {
      v_uv = (a_position + 1.0) * 0.5;
      gl_Position = vec4(a_position, 0.0, 1.0);
    }
  `;

  const FRAGMENT_SHADER_SOURCE = `
    precision highp float;
    uniform sampler2D u_texture;
    uniform vec2 u_resolution;
    uniform float u_time;
    uniform float u_lightning;
    varying vec2 v_uv;

    void main() {
      vec2 uv = v_uv;

      // In WebGL texture space:
      // v_uv.y = 1.0 is the top (sky), v_uv.y = 0.0 is the bottom (rocky shore).
      // Ocean begins below the lighthouse cliff / horizon (v_uv.y < 0.55).
      // Sky & lighthouse tower remain 100% stationary and sharp!
      float waterMask = smoothstep(0.56, 0.47, v_uv.y);

      if (waterMask > 0.001) {
        // Multi-frequency harmonic wave displacement
        // 1. Primary rolling ocean swell (drifting leftward into the wind)
        float w1 = sin(v_uv.x * 22.0 - u_time * 2.2 + v_uv.y * 10.0) * 0.0055;

        // 2. Secondary breaker wave (peaked crests with trochoidal sharpening)
        float w2_raw = sin(v_uv.x * 38.0 - u_time * 3.4 - v_uv.y * 14.0);
        float w2 = sign(w2_raw) * pow(abs(w2_raw), 1.5) * 0.004;

        // 3. High-frequency ocean surface chop
        float w3 = cos(v_uv.x * 58.0 + u_time * 1.9 + v_uv.y * 24.0) * 0.0025;

        // 4. Cliff collision surge near lighthouse base (x ~ 0.318, y ~ 0.495 in texture space)
        float distToCliff = length(vec2(v_uv.x - 0.318, v_uv.y - 0.495));
        float cliffSurge = exp(-distToCliff * 9.0) * sin(u_time * 3.8) * 0.007;

        // Combined organic displacement vector scaled by water depth
        float depthFactor = smoothstep(0.56, 0.20, v_uv.y);
        vec2 displacement = vec2(
          (w2 * 1.3 - w1 * 0.6 + w3) * waterMask * depthFactor,
          (w1 + w2 + w3 + cliffSurge) * waterMask * depthFactor
        );

        uv += displacement;
      }

      vec4 color = texture2D(u_texture, uv);

      // Subtle dynamic froth / specular illumination along moving wave crests
      if (waterMask > 0.01) {
        float crest = pow(max(0.0, sin(uv.x * 24.0 - u_time * 2.6 + uv.y * 12.0)), 4.0);
        vec3 foamGlint = vec3(0.92, 0.97, 1.0);
        color.rgb += foamGlint * crest * 0.075 * waterMask;

        // Ambient lightning reflection on turbulent wet water
        if (u_lightning > 0.005) {
          float wetSheen = pow(max(0.0, sin(uv.x * 30.0 - u_time * 2.0)), 2.5) * 0.4 + 0.6;
          color.rgb += vec3(0.20, 0.28, 0.45) * u_lightning * wetSheen * waterMask;
        }
      }

      // Atmospheric ambient lightning across entire banner
      if (u_lightning > 0.005) {
        color.rgb += vec3(0.10, 0.14, 0.20) * u_lightning;
      }

      gl_FragColor = color;
    }
  `;

  function initWebGL() {
    if (!gl) return;

    function createShader(type, source) {
      const shader = gl.createShader(type);
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error('Shader compilation error:', gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
      }
      return shader;
    }

    const vertexShader = createShader(gl.VERTEX_SHADER, VERTEX_SHADER_SOURCE);
    const fragmentShader = createShader(gl.FRAGMENT_SHADER, FRAGMENT_SHADER_SOURCE);
    if (!vertexShader || !fragmentShader) return;

    oceanProgram = gl.createProgram();
    gl.attachShader(oceanProgram, vertexShader);
    gl.attachShader(oceanProgram, fragmentShader);
    gl.linkProgram(oceanProgram);

    if (!gl.getProgramParameter(oceanProgram, gl.LINK_STATUS)) {
      console.error('Program link error:', gl.getProgramInfoLog(oceanProgram));
      return;
    }

    gl.useProgram(oceanProgram);

    // Quad geometry (2 triangles covering [-1, -1] to [1, 1])
    const quadBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, quadBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
      -1, -1,
       1, -1,
      -1,  1,
      -1,  1,
       1, -1,
       1,  1
    ]), gl.STATIC_DRAW);

    const aPosLoc = gl.getAttribLocation(oceanProgram, 'a_position');
    gl.enableVertexAttribArray(aPosLoc);
    gl.vertexAttribPointer(aPosLoc, 2, gl.FLOAT, false, 0, 0);

    uTimeLoc = gl.getUniformLocation(oceanProgram, 'u_time');
    uResLoc = gl.getUniformLocation(oceanProgram, 'u_resolution');
    uLightningLoc = gl.getUniformLocation(oceanProgram, 'u_lightning');

    // Load Painting Texture
    oceanTexture = gl.createTexture();
    const image = new Image();
    image.crossOrigin = 'anonymous';
    image.onload = function() {
      gl.bindTexture(gl.TEXTURE_2D, oceanTexture);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      isTextureLoaded = true;
    };
    image.src = 'assets/images/lighthouse-banner.jpg';
  }

  initWebGL();

  // ==========================================================================
  // PART 2: CANVAS 2D REALISTIC CRASHING SPLASHES, MIST & RAIN ENGINE
  // ==========================================================================
  const rainCanvas = document.getElementById('rain-canvas');
  if (!rainCanvas) return;
  const ctx = rainCanvas.getContext('2d');

  let width = 0;
  let height = 0;
  let simTime = 0;

  let raindrops = [];
  let splashDroplets = [];
  let mistClouds = [];
  let spindriftWisps = [];
  let ripples = [];

  let ambientFlashAlpha = 0;
  let targetFlash = 0;
  let lastFlashTime = Date.now();
  let nextLighthouseSplash = 0;

  function resizeAll() {
    const parent = rainCanvas.parentElement;
    width = parent.clientWidth;
    height = parent.clientHeight;

    rainCanvas.width = width;
    rainCanvas.height = height;

    if (oceanCanvas) {
      oceanCanvas.width = width;
      oceanCanvas.height = height;
      if (gl) {
        gl.viewport(0, 0, width, height);
      }
    }

    initRain();
  }

  window.addEventListener('resize', resizeAll);

  // --------------------------------------------------------------------------
  // Splashing Droplets & Vapor Mist (No cartoon shapes—pure organic water)
  // --------------------------------------------------------------------------
  class SplashDrop {
    constructor(x, y, vx, vy, size, alpha = 0.85) {
      this.x = x;
      this.y = y;
      this.vx = vx;
      this.vy = vy;
      this.size = size;
      this.alpha = alpha;
      this.decay = Math.random() * 0.02 + 0.012;
      this.gravity = 0.22;
      this.wind = 0.07;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.vy += this.gravity;
      this.vx += this.wind; // storm wind blows spray rightward
      this.vx *= 0.985;     // air drag
      this.alpha -= this.decay;
    }

    draw(boost) {
      if (this.alpha <= 0) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.95);
      ctx.fillStyle = `rgba(240, 248, 255, ${a})`;
      ctx.beginPath();
      // Ellipse in direction of motion (natural water droplet teardrop)
      const speed = Math.hypot(this.vx, this.vy);
      const angle = Math.atan2(this.vy, this.vx);
      ctx.ellipse(this.x, this.y, this.size + speed * 0.4, this.size * 0.85, angle, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  class MistVapor {
    constructor(x, y, radius, maxRadius, alpha = 0.32) {
      this.x = x;
      this.y = y;
      this.radius = radius;
      this.maxRadius = maxRadius;
      this.alpha = alpha;
      this.growth = (maxRadius - radius) / (Math.random() * 20 + 25);
      this.vx = Math.random() * 1.8 + 0.9;  // drifts right with wind
      this.vy = -(Math.random() * 0.7 + 0.3); // floats upward
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.radius += this.growth;
      this.alpha *= 0.958;
    }

    draw(boost) {
      if (this.alpha <= 0.01) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.55);
      const grad = ctx.createRadialGradient(
        this.x, this.y, 0,
        this.x, this.y, Math.max(this.radius, 1)
      );
      grad.addColorStop(0, `rgba(245, 250, 255, ${a})`);
      grad.addColorStop(0.45, `rgba(220, 238, 252, ${a * 0.45})`);
      grad.addColorStop(1, 'rgba(200, 230, 250, 0)');

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
      this.vx = Math.random() * 5 + 4; // fast gale drift
      this.vy = -(Math.random() * 0.8 + 0.2);
      this.alpha = Math.random() * 0.35 + 0.15;
      this.length = Math.random() * 12 + 8;
      this.width = Math.random() * 1.2 + 0.6;
      this.life = Math.random() * 25 + 18;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.alpha -= 0.018;
      this.life--;
    }

    draw(boost) {
      if (this.alpha <= 0 || this.life <= 0) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.7);
      ctx.strokeStyle = `rgba(230, 244, 255, ${a})`;
      ctx.lineWidth = this.width;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(this.x, this.y);
      ctx.lineTo(this.x + this.length, this.y + this.vy * 2);
      ctx.stroke();
      ctx.restore();
    }
  }

  // --------------------------------------------------------------------------
  // Crashing Wave Trigger at Lighthouse Base
  // --------------------------------------------------------------------------
  function triggerLighthouseBreakerCrash() {
    // Exact cliff base in the painting: ~31.8% width, ~50.5% height
    const impactX = width * 0.318 + (Math.random() * 18 - 9);
    const impactY = height * 0.505 + (Math.random() * 10 - 5);

    // 1. Upward explosive water droplets (40-65 droplets)
    const count = Math.floor(Math.random() * 25 + 45);
    for (let i = 0; i < count; i++) {
      const angle = -(Math.PI * 0.22 + Math.random() * Math.PI * 0.58);
      const speed = Math.random() * 8.5 + 3.5;
      const vx = Math.cos(angle) * speed + (Math.random() * 2.0 + 0.8);
      const vy = Math.sin(angle) * speed;
      const size = Math.random() * 1.8 + 1.0;
      splashDroplets.push(new SplashDrop(impactX, impactY, vx, vy, size, 0.9));
    }

    // 2. Billowing Sea Mist Clouds (4 clouds per impact)
    for (let i = 0; i < 4; i++) {
      const ox = impactX + (Math.random() * 20 - 10);
      const oy = impactY + (Math.random() * 12 - 8);
      const initR = Math.random() * 8 + 8;
      const maxR = Math.random() * 26 + 32;
      mistClouds.push(new MistVapor(ox, oy, initR, maxR, 0.38));
    }
  }

  function triggerRockSplash(x, y) {
    const count = Math.floor(Math.random() * 8 + 6);
    for (let i = 0; i < count; i++) {
      const angle = -(Math.PI * 0.25 + Math.random() * Math.PI * 0.5);
      const speed = Math.random() * 4.5 + 2.0;
      const vx = Math.cos(angle) * speed + 0.6;
      const vy = Math.sin(angle) * speed;
      splashDroplets.push(new SplashDrop(x, y, vx, vy, Math.random() * 1.3 + 0.8, 0.7));
    }
  }

  // --------------------------------------------------------------------------
  // Raindrop System
  // --------------------------------------------------------------------------
  class Raindrop {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * (width + 250) - 100;
      this.y = initial ? Math.random() * height : -20;
      this.speed = Math.random() * 8 + 12;
      this.length = Math.random() * 16 + 14;
      this.angle = 0.22; // subtle wind slant to the right
      this.alpha = Math.random() * 0.32 + 0.16;
      this.width = Math.random() * 1.0 + 0.6;
    }

    update() {
      this.x += Math.sin(this.angle) * this.speed;
      this.y += Math.cos(this.angle) * this.speed;

      // When reaching ocean zone (y > height * 0.52)
      if (this.y > height * 0.52 + Math.random() * (height * 0.45)) {
        if (Math.random() < 0.12) {
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
      const a = Math.min(this.alpha * boost, 0.85);
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
      this.maxRadius = Math.random() * 7 + 4;
      this.alpha = 0.4;
      this.growth = Math.random() * 0.4 + 0.3;
    }

    update() {
      this.radius += this.growth;
      this.alpha -= 0.022;
    }

    draw(boost) {
      if (this.alpha <= 0) return;
      ctx.save();
      const a = Math.min(this.alpha * boost, 0.7);
      ctx.strokeStyle = `rgba(186, 230, 253, ${a})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.ellipse(this.x, this.y, this.radius * 2.2, this.radius * 0.65, 0, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }
  }

  function initRain() {
    const count = Math.min(Math.floor((width * height) / 4800), 150);
    raindrops = [];
    for (let i = 0; i < count; i++) {
      raindrops.push(new Raindrop());
    }
  }

  // --------------------------------------------------------------------------
  // Main Animation Loop
  // --------------------------------------------------------------------------
  function updateLightingAndEvents() {
    const now = Date.now();

    // Soft Ambient Lightning
    if (now - lastFlashTime > (Math.random() * 5000 + 6000)) {
      lastFlashTime = now;
      targetFlash = Math.random() * 0.20 + 0.08;
    }

    // Periodic Lighthouse Cliff Breaker Collision (every 2.6 - 3.8 seconds)
    if (now > nextLighthouseSplash) {
      triggerLighthouseBreakerCrash();
      nextLighthouseSplash = now + (Math.random() * 1200 + 2600);
    }

    // Occasional windblown spindrift across mid-ocean crest
    if (Math.random() < 0.08) {
      const sx = Math.random() * (width * 0.7) + (width * 0.2);
      const sy = height * (Math.random() * 0.25 + 0.55);
      spindriftWisps.push(new SpindriftWisp(sx, sy));
    }

    // Occasional minor rock splash in foreground
    if (Math.random() < 0.03) {
      const rx = Math.random() * width;
      const ry = height * (Math.random() * 0.15 + 0.80);
      triggerRockSplash(rx, ry);
    }
  }

  function render() {
    simTime += 0.024;
    updateLightingAndEvents();

    // Compute Ambient Flash
    ambientFlashAlpha += (targetFlash - ambientFlashAlpha) * 0.08;
    if (targetFlash > 0 && Math.abs(targetFlash - ambientFlashAlpha) < 0.01) {
      targetFlash = 0;
    }
    globalLightningAlpha = ambientFlashAlpha;
    const flashBoost = 1 + ambientFlashAlpha * 2.5;

    // 1. Render WebGL Fluid Ocean Waves
    if (gl && oceanProgram && isTextureLoaded) {
      gl.useProgram(oceanProgram);
      gl.uniform1f(uTimeLoc, simTime);
      gl.uniform2f(uResLoc, width, height);
      gl.uniform1f(uLightningLoc, globalLightningAlpha);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }

    // 2. Render 2D Canvas Overlays (Rain, Splashes, Spindrift, Mist)
    ctx.clearRect(0, 0, width, height);

    // Ambient Lightning sky flash (if WebGL inactive)
    if (!gl && ambientFlashAlpha > 0.005) {
      ctx.fillStyle = `rgba(192, 210, 245, ${ambientFlashAlpha})`;
      ctx.fillRect(0, 0, width, height);
    }

    // Draw Spindrift Wisps
    for (let i = spindriftWisps.length - 1; i >= 0; i--) {
      spindriftWisps[i].update();
      spindriftWisps[i].draw(flashBoost);
      if (spindriftWisps[i].alpha <= 0 || spindriftWisps[i].life <= 0) {
        spindriftWisps.splice(i, 1);
      }
    }

    // Draw Mist Clouds
    for (let i = mistClouds.length - 1; i >= 0; i--) {
      mistClouds[i].update();
      mistClouds[i].draw(flashBoost);
      if (mistClouds[i].alpha <= 0.01) {
        mistClouds.splice(i, 1);
      }
    }

    // Draw Splash Droplets
    for (let i = splashDroplets.length - 1; i >= 0; i--) {
      splashDroplets[i].update();
      splashDroplets[i].draw(flashBoost);
      if (splashDroplets[i].alpha <= 0 || splashDroplets[i].y > height + 20) {
        splashDroplets.splice(i, 1);
      }
    }

    // Draw Ripples
    for (let i = ripples.length - 1; i >= 0; i--) {
      ripples[i].update();
      ripples[i].draw(flashBoost);
      if (ripples[i].alpha <= 0) {
        ripples.splice(i, 1);
      }
    }

    // Draw Raindrops
    for (let drop of raindrops) {
      drop.update();
      drop.draw(flashBoost);
    }

    requestAnimationFrame(render);
  }

  resizeAll();
  requestAnimationFrame(render);
})();
