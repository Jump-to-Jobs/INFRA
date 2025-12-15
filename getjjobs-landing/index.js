document.addEventListener("DOMContentLoaded", function () {
    // Hamburger menu toggle
    const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");

    hamburger.addEventListener("click", () => {
      hamburger.classList.toggle("active");
      navLinks.classList.toggle("active");
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-links a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Only prevent default if it's an internal hash link on the same page
            const path = window.location.pathname;
            const isIndexPage = path.endsWith('/') || path.endsWith('/index.html') || path === '/index.html';
            if (href.startsWith('#') && isIndexPage) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Animate on scroll for elements
    const animateOnScrollElements = document.querySelectorAll('.animate-on-scroll');

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Unobserve after animation (to run once)
            }
        });
    }, observerOptions);

    animateOnScrollElements.forEach(el => {
        observer.observe(el);
    });

    // Removed startDemo() as buttons now handle direct navigation or scroll.

    // Add some interactive hover effects for cards
    document.querySelectorAll('.problem-card, .solution-card, .testimonial-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Sticky CTA container visibility
    window.addEventListener('scroll', function() {
        const stickyCTAContainer = document.getElementById('stickyCTAContainer');
        const heroSection = document.querySelector('.hero');
        // Ensure heroSection exists before trying to access its properties
        if (heroSection && stickyCTAContainer) {
            const heroBottom = heroSection.offsetTop + heroSection.offsetHeight;
            if (window.scrollY > heroBottom - 200) {
                stickyCTAContainer.classList.add('visible');
            } else {
                stickyCTAContainer.classList.remove('visible');
            }
        }
    });

    // Phone mockup interaction
    const playIcon = document.querySelector('.play-icon');
    if (playIcon) {
        playIcon.addEventListener('click', function() {
            this.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
                alert('🎬 Video Preview!\n\n"Hi, I\'m Woori! I\'m a creative Final year Designer who loves connecting with people through storytelling. I bring fresh ideas, social media expertise, and endless enthusiasm to every project!"');
            }, 150);
        });
    }
});
