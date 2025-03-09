// DOM Elements
const navItems = document.querySelectorAll('.nav-item');
const themeToggle = document.querySelector('.theme-toggle');
const dashboardSections = document.querySelectorAll('.dashboard-section');

// Charts Elements
const performanceChart = document.getElementById('performanceChart');
const subjectChart = document.getElementById('subjectChart');
const overallChart = document.getElementById('overallChart');
const branchChart = document.getElementById('branchChart');

// Upload Elements
const dropZone = document.querySelector('.upload-box');
const imageUpload = document.getElementById('image-upload');
const imagePreview = document.getElementById('image-preview');
const previewContainer = document.querySelector('.preview-container');
const uploadBox = document.querySelector('.upload-box');
const cancelButton = document.querySelector('.cancel-button');

// Section Navigation
navItems.forEach(item => {
    item.addEventListener('click', function(e) {
        if (this.dataset.section) {
            e.preventDefault();
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            dashboardSections.forEach(s => s.classList.remove('active'));
            document.getElementById(this.dataset.section).classList.add('active');
        }
    });
});

// Theme Toggle
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    const icon = themeToggle.querySelector('i');
    icon.classList.toggle('fa-moon');
    icon.classList.toggle('fa-sun');
    
    // Save theme preference
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
});

// Load saved theme
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-theme');
        themeToggle.querySelector('i').classList.replace('fa-moon', 'fa-sun');
    }
});

// File Upload Handling
if (imageUpload) {
    imageUpload.addEventListener('change', handleFileSelect);
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        previewFile(file);
    }
}

function previewFile(file) {
    if (validateFile(file)) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            uploadBox.style.display = 'none';
            previewContainer.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
}

function validateFile(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!validTypes.includes(file.type)) {
        showMessage('Please upload an image file (JPEG, PNG, GIF)', 'error');
        return false;
    }
    if (file.size > 5 * 1024 * 1024) { // 5MB limit
        showMessage('File size should be less than 5MB', 'error');
        return false;
    }
    return true;
}

// Drag and Drop
if (dropZone) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    dropZone.addEventListener('drop', handleDrop, false);
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    dropZone.classList.add('highlight');
}

function unhighlight(e) {
    dropZone.classList.remove('highlight');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const file = dt.files[0];
    imageUpload.files = dt.files;
    
    if (file) {
        previewFile(file);
    }
}

// Cancel Upload
if (cancelButton) {
    cancelButton.addEventListener('click', () => {
        imageUpload.value = '';
        uploadBox.style.display = 'block';
        previewContainer.style.display = 'none';
    });
}

// Message Display
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        ${message}
    `;
    
    document.querySelector('.upload-container').prepend(messageDiv);
    
    setTimeout(() => messageDiv.remove(), 3000);
}

// Initialize Charts
function initializeCharts(chartData) {
    // Student Dashboard Charts
    if (overallChart) {
        new Chart(overallChart.getContext('2d'), {
            type: 'line',
            data: {
                labels: chartData.performanceDates,
                datasets: [{
                    label: 'Overall Performance',
                    data: chartData.performanceScores,
                    borderColor: '#4a90e2',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    if (subjectChart) {
        new Chart(subjectChart.getContext('2d'), {
            type: 'bar',
            data: {
                labels: chartData.subjects,
                datasets: [{
                    label: 'Subject Performance',
                    data: chartData.subjectScores,
                    backgroundColor: '#4a90e2'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // Teacher Dashboard Charts
    if (performanceChart) {
        new Chart(performanceChart.getContext('2d'), {
            type: 'line',
            data: {
                labels: chartData.performanceLabels,
                datasets: [{
                    label: 'Average Performance',
                    data: chartData.performanceData,
                    borderColor: '#4a90e2',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    if (branchChart) {
        new Chart(branchChart.getContext('2d'), {
            type: 'bar',
            data: {
                labels: chartData.branchLabels,
                datasets: [{
                    label: 'Branch Distribution',
                    data: chartData.branchData,
                    backgroundColor: '#4a90e2'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

// Export functions for use in templates
window.dashboardFunctions = {
    initializeCharts,
    showMessage
};