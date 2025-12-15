document.addEventListener("DOMContentLoaded", function () {
    // Hamburger menu toggle
    const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");

    hamburger.addEventListener("click", () => {
      hamburger.classList.toggle("active");
      navLinks.classList.toggle("active");
    });

    // Smooth scrolling for internal navigation links on aboutus.html
    document.querySelectorAll('.nav-links a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Only prevent default if it's an internal hash link on the same page
            if (href.startsWith('#') && window.location.pathname.endsWith('aboutus.html')) {
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


    // Timeline animation on scroll
    function animateTimeline() {
        const timelineItems = document.querySelectorAll('.ab-timeline-item');

        timelineItems.forEach(item => {
            const itemTop = item.getBoundingClientRect().top;
            const triggerBottom = window.innerHeight * 0.8;

            if (itemTop < triggerBottom) {
                item.classList.add('ab-animate');
            }
        });
    }

    // Scroll event listener for timeline
    window.addEventListener('scroll', animateTimeline);

    // Initialize animations on DOM content loaded
    animateTimeline();

    // Intersection Observer for general scroll animations (re-using 'visible' class from style.css)
    const animateOnScrollElements = document.querySelectorAll('.animate-on-scroll');

    const observerOptions = {
        threshold: 0.1, // Trigger when 10% of the element is visible
        rootMargin: '0px 0px -50px 0px' // Trigger 50px above the bottom of the viewport
    };

    const generalObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible'); // Use 'visible' from style.css
                generalObserver.unobserve(entry.target); // Unobserve after animation (to run once)
            }
        });
    }, observerOptions);

    animateOnScrollElements.forEach(el => {
        generalObserver.observe(el);
    });
});
