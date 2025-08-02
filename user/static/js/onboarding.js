document.addEventListener('DOMContentLoaded', () => {
    const slideIllustration = document.getElementById('slideIllustration');
    const slideTitle = document.getElementById('slideTitle');
    const slideDescription = document.getElementById('slideDescription');
    const paginationDots = document.getElementById('paginationDots');
    const nextButton = document.getElementById('nextButton');
    const backArrow = document.getElementById('backArrow');
    // Removed const featureBubbles = document.getElementById('featureBubbles');

    // Define the content for each slide
    const slidesData = [
        {
            image: '/static/images/ilust1.jpg',
            title: 'Lorem ipsum dolor sit amet',
            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'
            
        },
        {
            image: '/static/images/raise-hand.jpg',
            title: 'Lorem ipsum dolor sit amet',
            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'
            // Removed showBubbles: false
        },
        {
            image: '/static/images/happy-family.jpg',
            title: 'Lorem ipsum dolor sit amet',
            description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'
            // Removed showBubbles: true
        }
    ];

    let currentSlideIndex = 0;
    const totalSlides = slidesData.length;

    // Function to update the displayed slide content
    function updateSlideContent(index) {
        // Fade out current content
        slideIllustration.style.opacity = '0';
        slideTitle.style.opacity = '0';
        slideDescription.style.opacity = '0';

        setTimeout(() => {
            const data = slidesData[index];

            // Update image
            slideIllustration.innerHTML = `<img src="${data.image}" alt="Onboarding Illustration ${index + 1}">`;

            // Update text
            slideTitle.textContent = data.title;
            slideDescription.textContent = data.description;

            // Removed show/hide feature bubbles logic

            // Update dots
            dots.forEach((dot, idx) => {
                dot.classList.remove('active');
                if (idx === index) {
                    dot.classList.add('active');
                }
            });

            // Handle back arrow visibility
            if (currentSlideIndex === 0) {
                backArrow.style.visibility = 'hidden'; // Hide on first slide
            } else {
                backArrow.style.visibility = 'visible'; // Show on subsequent slides
            }

            // Fade in new content
            slideIllustration.style.opacity = '1';
            slideTitle.style.opacity = '1';
            slideDescription.style.opacity = '1';
        }, 300); // Wait for fade out to complete before changing content
    }

    // Initialize pagination dots
    const dots = Array.from(paginationDots.children); // Get actual dot elements

    // Event Listeners
    nextButton.addEventListener('click', () => {
        if (currentSlideIndex < totalSlides - 1) {
            currentSlideIndex++;
            updateSlideContent(currentSlideIndex);
        } else {
            // Last slide - action complete or redirect
            window.location.href = '/login-signup/';
        }
    });

    backArrow.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent default link behavior
        if (currentSlideIndex > 0) {
            currentSlideIndex--;
            updateSlideContent(currentSlideIndex);
        }
    });

    dots.forEach(dot => {
        dot.addEventListener('click', (event) => {
            const index = parseInt(event.target.dataset.slide);
            currentSlideIndex = index;
            updateSlideContent(currentSlideIndex);
        });
    });

    // Initialize the first slide
    updateSlideContent(currentSlideIndex);
});