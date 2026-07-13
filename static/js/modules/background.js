export function initBackground() {
    const canvas = document.getElementById("bgCanvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    let width = 0;
    let height = 0;
    const particles = [];
    const particleCount = window.innerWidth < 768 ? 34 : 72;

    const resize = () => {
        width = canvas.width = window.innerWidth * window.devicePixelRatio;
        height = canvas.height = window.innerHeight * window.devicePixelRatio;
        canvas.style.width = `${window.innerWidth}px`;
        canvas.style.height = `${window.innerHeight}px`;
    };

    class Particle {
        constructor() {
            this.reset(true);
        }

        reset(initial = false) {
            this.x = Math.random() * width;
            this.y = initial ? Math.random() * height : -20 * window.devicePixelRatio;
            this.vx = (Math.random() - 0.5) * 0.18 * window.devicePixelRatio;
            this.vy = (Math.random() * 0.35 + 0.15) * window.devicePixelRatio;
            this.r = (Math.random() * 1.5 + 0.8) * window.devicePixelRatio;
            this.alpha = Math.random() * 0.55 + 0.15;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;
            if (this.y > height + 30) this.reset();
            if (this.x < -40 || this.x > width + 40) this.vx *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.fillStyle = `rgba(255, 62, 165, ${this.alpha})`;
            ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    const init = () => {
        resize();
        particles.length = 0;
        for (let i = 0; i < particleCount; i++) particles.push(new Particle());
    };

    const drawGridGlow = () => {
        ctx.save();
        ctx.globalCompositeOperation = "screen";
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            for (let j = i + 1; j < particles.length; j++) {
                const q = particles[j];
                const dx = p.x - q.x;
                const dy = p.y - q.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 150 * window.devicePixelRatio) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(255, 107, 214, ${(1 - dist / (150 * window.devicePixelRatio)) * 0.09})`;
                    ctx.lineWidth = 1;
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(q.x, q.y);
                    ctx.stroke();
                }
            }
        }
        ctx.restore();
    };

    const animate = () => {
        ctx.clearRect(0, 0, width, height);
        drawGridGlow();
        particles.forEach((p) => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animate);
    };

    window.addEventListener("resize", init);
    init();
    animate();
}
