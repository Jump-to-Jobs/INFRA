document.addEventListener("DOMContentLoaded", function () {
    // Hamburger menu toggle function - uses existing classes from style.css
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.querySelector(".nav-links"); // Use .nav-links for consistency

    if (hamburger && navLinks) {
        hamburger.addEventListener("click", () => {
            hamburger.classList.toggle("active");
            navLinks.classList.toggle("active");
        });
    }

    // Smooth scrolling for navigation links - uses existing classes from style.css
    document.querySelectorAll('.nav-links a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });


    // Intersection Observer for scroll animations - uses existing classes from style.css
    const animateOnScrollElements = document.querySelectorAll('.animate-on-scroll');

    const observerOptions = {
        threshold: 0.1, // Trigger when 10% of the element is visible
        rootMargin: '0px 0px -50px 0px' // Trigger 50px above the bottom of the viewport
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible'); // Use 'visible' from style.css
                observer.unobserve(entry.target); // Unobserve after animation (to run once)
            }
        });
    }, observerOptions);

    animateOnScrollElements.forEach(el => {
        observer.observe(el);
    });

    // Function to display messages (replaces alert)
    function showMessageBox(message, isError = false) {
        const messageBox = document.getElementById('emp-messageBox');
        messageBox.textContent = message;
        messageBox.classList.remove('emp-error');
        if (isError) {
            messageBox.classList.add('emp-error');
        }
        messageBox.classList.add('emp-show');

        setTimeout(() => {
            messageBox.classList.remove('emp-show');
        }, 3000); // Hide after 3 seconds
    }

    // Form submission handling
    const contactForm = document.getElementById('emp-contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault(); // Prevent default form submission

            const formData = new FormData(contactForm);
            const jsonData = {};
            formData.forEach((value, key) => {
                jsonData[key] = value;
            });

            // Define your backend endpoint URL here
            // IMPORTANT: Replace this with your actual backend API endpoint
            const backendEndpoint = 'YOUR_BACKEND_API_ENDPOINT_HERE'; 

            try {
                const response = await fetch(backendEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(jsonData)
                });

                if (response.ok) {
                    // If the response is successful (status 200-299)
                    showMessageBox('Your inquiry has been successfully submitted. We will contact you shortly!');
                    contactForm.reset(); // Reset form fields
                } else {
                    // If the server responded with an error status
                    const errorData = await response.json(); // Try to parse error message from server
                    showMessageBox(`Submission failed: ${errorData.message || response.statusText}`, true);
                }
            } catch (error) {
                // Handle network errors or other issues
                console.error('Error submitting form:', error);
                showMessageBox('An error occurred during submission. Please try again later.', true);
            }
        });
    }

    // Counter animation for stats
    function animateCounter(element, target) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            // Update text, append + or % based on content
            element.textContent = Math.floor(current) + (element.textContent.includes('%') ? '%' : '+');
        }, 20);
    }

    // Trigger counter animation when stats section is visible
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const numbers = entry.target.querySelectorAll('.emp-stat-number');
                numbers.forEach(num => {
                    // Parse target number from text content
                    const target = parseInt(num.textContent);
                    animateCounter(num, target);
                });
                statsObserver.unobserve(entry.target); // Unobserve after animation
            }
        });
    }, { threshold: 0.5 }); // Trigger when 50% of the section is visible

    const statsSection = document.querySelector('.emp-stats');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
});
