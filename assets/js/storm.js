/**
 * Royal Blue Storm & Cybernetic Lightning Canvas Engine
 * Atmospheric background for Dr. Zaid Amin's Academic Portal
 * Features:
 * - Dynamic royal blue storm clouds with ambient lightning flashes
 * - Neural lightning arcs connecting drifting cybernetic storm particles
 * - Occasional realistic branching lightning strikes
 * - Cursor magnetic interactivity
 */

(function() {
  const canvas = document.getElementById('storm-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = 0;
  let height = 0;
  let particles = [];
  let lightningBolts = [];
  let flashAlpha = 0;
  let targetFlash = 0;
  let mouse = { x: -1000, y: -1000, active: false };

  function resize() {
    const parent = canvas.parentElement;
    width = canvas.width = parent.clientWidth;
    height = canvas.height = parent.clientHeight;
    initParticles();
  }

  window.addEventListener('resize', resize);
  parentEl = canvas.parentElement;
  parentEl.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
    mouse.active = true;
  });
  parentEl.addEventListener('mouseleave', () => {
    mouse.active = false;
  });

  // Particle Class
  class StormParticle {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * width;
      this.y = initial ? Math.random() * height : height + 10;
      this.vx = (Math.random() - 0.5) * 0.8;
      this.vy = -Math.random() * 1.2 - 0.4;
      this.size = Math.random() * 2.2 + 0.8;
      this.alpha = Math.random() * 0.6 + 0.3;
      this.color = Math.random() > 0.4 ? '#38bdf8' : (Math.random() > 0.5 ? '#60a5fa' : '#ffffff');
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      // Magnetic pull to mouse
      if (mouse.active) {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 180) {
          this.x += (dx / dist) * 1.5;
          this.y += (dy / dist) * 1.5;
        }
      }

      if (this.y < -10 || this.x < -10 || this.x > width + 10) {
        this.reset();
      }
    }

    draw() {
      ctx.save();
      ctx.globalAlpha = this.alpha;
      ctx.fillStyle = this.color;
      ctx.shadowBlur = 10;
      ctx.shadowColor = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  // Branching Lightning Strike Generator
  class LightningStrike {
    constructor(startX, startY) {
      this.path = [];
      this.alpha = 1.0;
      this.decay = Math.random() * 0.05 + 0.04;
      this.buildPath(startX, startY);
    }

    buildPath(x, y) {
      this.path.push({ x, y });
      let currentX = x;
      let currentY = y;
      const targetY = height * (Math.random() * 0.5 + 0.4);

      while (currentY < targetY) {
        currentX += (Math.random() - 0.5) * 45;
        currentY += Math.random() * 25 + 10;
        this.path.push({ x: currentX, y: currentY });

        // Occasional fork
        if (Math.random() < 0.25 && this.path.length < 8) {
          this.path.push({ x: currentX + (Math.random() - 0.5) * 40, y: currentY + 20, isFork: true });
        }
      }
    }

    update() {
      this.alpha -= this.decay;
    }

    draw() {
      if (this.alpha <= 0) return;
      ctx.save();
      ctx.strokeStyle = `rgba(186, 230, 253, ${this.alpha})`;
      ctx.shadowColor = '#38bdf8';
      ctx.shadowBlur = 20;
      ctx.lineWidth = 2.5;

      ctx.beginPath();
      for (let i = 0; i < this.path.length; i++) {
        const pt = this.path[i];
        if (pt.isFork) {
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(this.path[i - 1].x, this.path[i - 1].y);
          ctx.lineTo(pt.x, pt.y);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(this.path[i - 1].x, this.path[i - 1].y);
        } else if (i === 0) {
          ctx.moveTo(pt.x, pt.y);
        } else {
          ctx.lineTo(pt.x, pt.y);
        }
      }
      ctx.stroke();
      ctx.restore();
    }
  }

  function initParticles() {
    const count = Math.min(Math.floor((width * height) / 9000), 100);
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push(new StormParticle());
    }
  }

  // Random Lightning trigger
  let lastLightningTime = Date.now();
  function checkLightning() {
    const now = Date.now();
    if (now - lastLightningTime > (Math.random() * 4000 + 3500)) {
      lastLightningTime = now;
      const startX = Math.random() * (width * 0.8) + (width * 0.1);
      lightningBolts.push(new LightningStrike(startX, 0));
      targetFlash = Math.random() * 0.35 + 0.15;
    }
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    // 1. Deep Royal Blue Atmospheric Gradient Base
    const bgGrad = ctx.createLinearGradient(0, 0, 0, height);
    bgGrad.addColorStop(0, '#030712');
    bgGrad.addColorStop(0.3, '#071330');
    bgGrad.addColorStop(0.7, '#0b1e4a');
    bgGrad.addColorStop(1, '#050b1a');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, width, height);

    // 2. Rolling Storm Nebula / Atmospheric Clouds
    const time = Date.now() * 0.0005;
    const radial = ctx.createRadialGradient(
      width * 0.5 + Math.sin(time) * 120, height * 0.3, 20,
      width * 0.5, height * 0.4, width * 0.6
    );
    radial.addColorStop(0, 'rgba(30, 64, 175, 0.4)');
    radial.addColorStop(0.5, 'rgba(14, 165, 233, 0.15)');
    radial.addColorStop(1, 'transparent');
    ctx.fillStyle = radial;
    ctx.fillRect(0, 0, width, height);

    // 3. Ambient Lightning Flash
    flashAlpha += (targetFlash - flashAlpha) * 0.12;
    if (targetFlash > 0 && Math.abs(targetFlash - flashAlpha) < 0.02) {
      targetFlash = 0;
    }
    if (flashAlpha > 0.01) {
      ctx.fillStyle = `rgba(96, 165, 250, ${flashAlpha})`;
      ctx.fillRect(0, 0, width, height);
    }

    // 4. Update & Draw Lightning Bolts
    for (let i = lightningBolts.length - 1; i >= 0; i--) {
      lightningBolts[i].update();
      lightningBolts[i].draw();
      if (lightningBolts[i].alpha <= 0) {
        lightningBolts.splice(i, 1);
      }
    }

    // 5. Connect close particles with electric neural threads
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 110) {
          ctx.strokeStyle = `rgba(56, 189, 248, ${(1 - dist / 110) * 0.25})`;
          ctx.lineWidth = 0.8;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }

    // 6. Draw particles
    for (let p of particles) {
      p.update();
      p.draw();
    }

    checkLightning();
    requestAnimationFrame(render);
  }

  // Initialize
  resize();
  requestAnimationFrame(render);
})();
