/**
 * Auto-dismiss messages after 6 seconds
 * Improves UX by automatically hiding success/info messages
 */
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        // Auto-dismiss after 6 seconds (6000ms)
        const timeoutId = setTimeout(function() {
            // Add fade-out class for smooth transition
            alert.classList.add('alert-fade-out');
            
            // Remove from DOM after animation completes
            setTimeout(function() {
                alert.remove();
                
                // If this was the last alert in a container, remove the container too
                const container = alert.parentElement;
                if (container && container.classList.contains('alert-container') && container.children.length === 0) {
                    container.remove();
                }
            }, 400); // Match transition duration
        }, 6000); // 6 seconds
        
        // Store timeout ID on the element for potential manual cancellation
        alert.dataset.timeoutId = timeoutId;
        
        // Optional: Allow manual dismissal on click
        alert.style.cursor = 'pointer';
        alert.addEventListener('click', function() {
            clearTimeout(timeoutId);
            alert.classList.add('alert-fade-out');
            setTimeout(function() {
                alert.remove();
                const container = alert.parentElement;
                if (container && container.classList.contains('alert-container') && container.children.length === 0) {
                    container.remove();
                }
            }, 400);
        });
        
        // Add hover effect to pause auto-dismiss (optional enhancement)
        let isHovered = false;
        alert.addEventListener('mouseenter', function() {
            isHovered = true;
        });
        alert.addEventListener('mouseleave', function() {
            isHovered = false;
        });
    });
});













