// Voting Application JavaScript

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeVotingApp();
});

function initializeVotingApp() {
    console.log('Voting Blockchain Application Initialized');
    
    // Initialize tooltips if available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

// Email validation function
function validateUniversityEmail(email) {
    const uniPattern = /^[a-zA-Z0-9._%+-]+@uni\.(pe|edu\.pe)$/;
    return uniPattern.test(email);
}

// Format verification code input
function formatVerificationCode(input) {
    // Remove non-digits
    let value = input.value.replace(/\D/g, '');
    
    // Limit to 6 digits
    if (value.length > 6) {
        value = value.substring(0, 6);
    }
    
    input.value = value;
}

// Voting form validation
function validateVotingForm() {
    const codeInput = document.getElementById('code');
    const selectedOption = document.querySelector('input[name="option"]:checked');
    
    if (!codeInput || codeInput.value.length !== 6) {
        showAlert('El código de verificación debe tener 6 dígitos.', 'error');
        return false;
    }
    
    if (!selectedOption) {
        showAlert('Por favor selecciona una opción de voto.', 'error');
        return false;
    }
    
    return true;
}

// Show alert messages
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    alertContainer.role = 'alert';
    
    alertContainer.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertContainer, container.firstChild);
    }
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Copy blockchain hash to clipboard
function copyToClipboard(text, elementId) {
    navigator.clipboard.writeText(text).then(function() {
        const element = document.getElementById(elementId);
        if (element) {
            const originalText = element.innerHTML;
            element.innerHTML = '<i class="fas fa-check text-success"></i> Copiado!';
            setTimeout(function() {
                element.innerHTML = originalText;
            }, 2000);
        }
    }).catch(function(err) {
        console.error('Error copying to clipboard: ', err);
        showAlert('Error al copiar al portapapeles', 'error');
    });
}

// Real-time results updates
function updateResults(electionId) {
    fetch(`/api/results/${electionId}`)
        .then(response => response.json())
        .then(data => {
            updateResultsChart(data);
            updateResultsTable(data);
        })
        .catch(error => {
            console.error('Error updating results:', error);
        });
}

// Update chart with new data
function updateResultsChart(data) {
    if (window.resultsChart) {
        window.resultsChart.data.datasets[0].data = Object.values(data);
        window.resultsChart.update();
    }
}

// Update results table
function updateResultsTable(data) {
    const total = Object.values(data).reduce((sum, count) => sum + count, 0);
    
    Object.entries(data).forEach(([option, count]) => {
        const percentage = total > 0 ? (count / total * 100).toFixed(1) : 0;
        
        // Update progress bars and counts
        const progressBar = document.querySelector(`[data-option="${option}"] .progress-bar`);
        const countBadge = document.querySelector(`[data-option="${option}"] .badge`);
        const percentageSpan = document.querySelector(`[data-option="${option}"] .percentage`);
        
        if (progressBar) progressBar.style.width = `${percentage}%`;
        if (countBadge) countBadge.textContent = `${count} votos`;
        if (percentageSpan) percentageSpan.textContent = `${percentage}%`;
    });
}

// Admin panel functions
function confirmElectionToggle(electionTitle, isActive) {
    const action = isActive ? 'desactivar' : 'activar';
    return confirm(`¿Estás seguro de que quieres ${action} la elección "${electionTitle}"?`);
}

function validateElectionForm() {
    const title = document.getElementById('title').value.trim();
    const options = document.getElementById('options').value.trim();
    
    if (!title) {
        showAlert('El título de la elección es requerido.', 'error');
        return false;
    }
    
    const optionsArray = options.split('\n').filter(opt => opt.trim().length > 0);
    if (optionsArray.length < 2) {
        showAlert('Se requieren al menos 2 opciones de votación.', 'error');
        return false;
    }
    
    return true;
}

// Blockchain visualization functions
function expandBlockDetails(blockIndex) {
    const detailsElement = document.getElementById(`block-details-${blockIndex}`);
    if (detailsElement) {
        detailsElement.style.display = detailsElement.style.display === 'none' ? 'block' : 'none';
    }
}

// Security functions
function hashString(str) {
    let hash = 0;
    if (str.length === 0) return hash;
    
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32-bit integer
    }
    
    return Math.abs(hash).toString(16);
}

// Form helpers
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

// Loading states
function setLoadingState(buttonId, isLoading) {
    const button = document.getElementById(buttonId);
    if (button) {
        if (isLoading) {
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
        } else {
            button.disabled = false;
            // Restore original button text would need to be stored separately
        }
    }
}

// Confirmation dialogs
function confirmVote(option) {
    return confirm(
        `¿Estás seguro de que quieres votar por "${option}"?\n\n` +
        'Una vez confirmado, tu voto será registrado permanentemente en la blockchain y no podrá ser cambiado.'
    );
}

// Auto-refresh functionality
function startAutoRefresh(intervalSeconds = 30) {
    setInterval(function() {
        // Only refresh if we're on a results or blockchain page
        if (window.location.pathname.includes('/results/') || 
            window.location.pathname.includes('/blockchain')) {
            location.reload();
        }
    }, intervalSeconds * 1000);
}

// Initialize auto-refresh on appropriate pages
if (window.location.pathname.includes('/results/') || 
    window.location.pathname.includes('/blockchain')) {
    startAutoRefresh(30);
}

// Accessibility improvements
function improveAccessibility() {
    // Add ARIA labels to form controls
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(control => {
        if (!control.getAttribute('aria-label') && control.previousElementSibling) {
            const label = control.previousElementSibling.textContent;
            control.setAttribute('aria-label', label);
        }
    });
    
    // Add keyboard navigation for cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.setAttribute('tabindex', '0');
    });
}

// Initialize accessibility improvements
improveAccessibility();

// Export functions for global use
window.VotingApp = {
    validateUniversityEmail,
    formatVerificationCode,
    validateVotingForm,
    showAlert,
    copyToClipboard,
    updateResults,
    confirmElectionToggle,
    validateElectionForm,
    confirmVote,
    setLoadingState
};
