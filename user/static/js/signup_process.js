document.addEventListener('DOMContentLoaded', () => {
    // This value is correctly set from the template
    const currentStepIndex = initialCurrentStep;

    // --- Elements ---
    const signupBackArrow = document.getElementById('signupBackArrow');
    const signupTitle = document.getElementById('signupTitle');
    const passwordToggles = document.querySelectorAll('.toggle-password');
    const profilePictureInput = document.getElementById('id_profile_picture');
    const profilePicPreview = document.getElementById('profilePicPreview');

    // --- UI Updates based on current step ---

    // Update back arrow visibility and title
    if (currentStepIndex === 0) {
        signupBackArrow.style.visibility = 'hidden';
    } else {
        signupBackArrow.style.visibility = 'visible';
    }

    if (currentStepIndex === 2) { // On the success screen
        signupTitle.textContent = '';
        signupBackArrow.style.visibility = 'hidden';
    } else {
        signupTitle.textContent = 'Sign up';
    }


    // --- Event Listeners ---

    // Back arrow click handler
    signupBackArrow.addEventListener('click', (e) => {
        e.preventDefault();
        // The view's GET logic handles which step to show.
        // We just need to go to the previous step number.
        const previousStepNumber = currentStepIndex; // Step index 1 is step 2, so we go back to step 1
        if (previousStepNumber > 0) {
            window.location.href = window.location.pathname + `?step=${previousStepNumber}`;
        }
    });

    // Password visibility toggle
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const targetId = toggle.dataset.target;
            const targetInput = document.getElementById(targetId);
            if (targetInput) {
                const type = targetInput.getAttribute('type') === 'password' ? 'text' : 'password';
                targetInput.setAttribute('type', type);
                // You can add icon toggling logic here
            }
        });
    });

    // Profile picture preview
    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file && profilePicPreview) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    profilePicPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            } else if (profilePicPreview) {
                // Reset to a default placeholder if needed
                profilePicPreview.src = '/static/images/user.png'; 
            }
        });
    }
});
