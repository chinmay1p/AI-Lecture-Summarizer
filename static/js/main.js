// SlideSense - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('videoFile');
    const uploadForm = document.getElementById('uploadForm');
    const uploadProgress = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('progressFill');

    if (!uploadArea || !fileInput || !uploadForm) {
        return; // Exit if elements don't exist
    }

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection(files[0]);
        }
    });

    // Click to upload
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });

    // Handle file selection
    function handleFileSelection(file) {
        // Validate file type
        if (!file.type.startsWith('video/')) {
            showError('Please select a valid video file.');
            return;
        }

        // Validate file size (max 500MB)
        const maxSize = 500 * 1024 * 1024; // 500MB
        if (file.size > maxSize) {
            showError('File size too large. Please select a video smaller than 500MB.');
            return;
        }

        // Update UI to show selected file
        updateUploadAreaWithFile(file);
        
        // Auto-submit form after a short delay
        setTimeout(() => {
            submitForm();
        }, 1000);
    }

    // Update upload area to show selected file
    function updateUploadAreaWithFile(file) {
        const uploadIcon = uploadArea.querySelector('.upload-icon');
        const uploadTitle = uploadArea.querySelector('.upload-title');
        const uploadSubtitle = uploadArea.querySelector('.upload-subtitle');

        uploadIcon.innerHTML = `
            <svg fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"></path>
            </svg>
        `;
        
        uploadTitle.textContent = file.name;
        uploadSubtitle.textContent = `Size: ${formatFileSize(file.size)} • Click to change`;
        
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.background = '#EFF6FF';
    }

    // Submit the form
    function submitForm() {
        uploadProgress.style.display = 'block';
        uploadArea.style.display = 'none';
        
        // Simulate progress (since we can't track real upload progress easily)
        simulateProgress();
        
        // Submit the form
        uploadForm.submit();
    }

    // Simulate upload progress
    function simulateProgress() {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) {
                progress = 90;
                clearInterval(interval);
            }
            progressFill.style.width = progress + '%';
        }, 200);
    }

    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Show error message
    function showError(message) {
        // Remove existing error messages
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Create new error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <svg class="error-icon" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
            <span>${message}</span>
        `;

        // Insert error message before upload container
        const uploadContainer = document.querySelector('.upload-container');
        uploadContainer.insertBefore(errorDiv, uploadContainer.firstChild);

        // Auto-remove error after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }

    // Prevent default drag behaviors on the entire page
    document.addEventListener('dragover', function(e) {
        e.preventDefault();
    });

    document.addEventListener('drop', function(e) {
        e.preventDefault();
    });
});

// Processing state simulation (for demonstration purposes)
function showProcessingState() {
    const mainContainer = document.querySelector('.main-container');
    if (!mainContainer) return;

    mainContainer.innerHTML = `
        <div class="processing-container">
            <div class="processing-icon">
                <svg fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
                </svg>
            </div>
            <h2 class="processing-title">Processing Your Lecture Video</h2>
            <div class="processing-steps">
                <div class="processing-step">
                    <div class="step-icon active">1</div>
                    <div class="step-text active">Analyzing video & extracting keyframes...</div>
                </div>
                <div class="processing-step">
                    <div class="step-icon pending">2</div>
                    <div class="step-text">Enhancing slide contrast...</div>
                </div>
                <div class="processing-step">
                    <div class="step-icon pending">3</div>
                    <div class="step-text">Recognizing text from slides...</div>
                </div>
                <div class="processing-step">
                    <div class="step-icon pending">4</div>
                    <div class="step-text">Generating your summary...</div>
                </div>
            </div>
        </div>
    `;

    // Simulate step progression
    simulateStepProgression();
}

function simulateStepProgression() {
    const steps = document.querySelectorAll('.processing-step');
    let currentStep = 0;

    const stepInterval = setInterval(() => {
        if (currentStep < steps.length) {
            // Mark current step as completed
            if (currentStep > 0) {
                const prevStep = steps[currentStep - 1];
                const prevIcon = prevStep.querySelector('.step-icon');
                const prevText = prevStep.querySelector('.step-text');
                
                prevIcon.classList.remove('active');
                prevIcon.classList.add('completed');
                prevText.classList.remove('active');
                prevText.classList.add('completed');
            }

            // Mark next step as active
            if (currentStep < steps.length) {
                const currentStepEl = steps[currentStep];
                const currentIcon = currentStepEl.querySelector('.step-icon');
                const currentText = currentStepEl.querySelector('.step-text');
                
                currentIcon.classList.remove('pending');
                currentIcon.classList.add('active');
                currentText.classList.remove('pending');
                currentText.classList.add('active');
            }

            currentStep++;
        } else {
            clearInterval(stepInterval);
        }
    }, 2000); // Change step every 2 seconds
}

// Utility function to show success message
function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `
        <svg class="success-icon" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
        </svg>
        <span>${message}</span>
    `;

    const mainContainer = document.querySelector('.main-container');
    if (mainContainer) {
        mainContainer.insertBefore(successDiv, mainContainer.firstChild);
        
        // Auto-remove success message after 3 seconds
        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.remove();
            }
        }, 3000);
    }
}
