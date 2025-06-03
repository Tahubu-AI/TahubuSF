/**
 * Utility functions for the TahubuSF Inspector
 */

// Accordion functionality
function toggleAccordion(header) {
    header.classList.toggle('active');
    
    const content = header.nextElementSibling;
    
    // Toggle active class on content
    content.classList.toggle('active');
    
    // Recalculate scrollHeight to account for dynamic content
    // This is important when the collapse button at the bottom is clicked
    if (content.classList.contains('active')) {
        // First set maxHeight to none to get the true scrollHeight
        content.style.maxHeight = 'none';
        // Then get the scrollHeight and set it as the maxHeight
        const scrollHeight = content.scrollHeight;
        content.style.maxHeight = scrollHeight + "px";
    } else {
        content.style.maxHeight = 0;
    }
    
    // Initialize the content div max-height for other active sections
    document.querySelectorAll('.accordion-content.active').forEach(element => {
        if (element !== content) {
            // Do the same recalculation for other active sections
            element.style.maxHeight = 'none';
            const scrollHeight = element.scrollHeight;
            element.style.maxHeight = scrollHeight + "px";
        }
    });
}

// Toggle mobile results visibility
function toggleMobileResults() {
    const resultsColumn = document.querySelector('.results-column');
    const toggleBtn = document.getElementById('toggle-results-btn');
    const toggleText = toggleBtn.querySelector('.toggle-text');
    const toggleIcon = toggleBtn.querySelector('.toggle-icon');
    
    // Check current state
    const isVisible = resultsColumn.classList.contains('mobile-visible');
    
    // Toggle visibility class
    if (isVisible) {
        resultsColumn.classList.remove('mobile-visible');
        toggleText.textContent = 'Show Results';
        toggleIcon.textContent = '↑';
    } else {
        resultsColumn.classList.add('mobile-visible');
        toggleText.textContent = 'Hide Results';
        toggleIcon.textContent = '↓';
        
        // Scroll to the top of results when showing
        const resultsContainer = document.getElementById('results-container');
        if (resultsContainer) {
            resultsContainer.scrollTop = 0;
        }
    }
}

// Show notification
function showNotification(message, type = "success") {
    const notification = document.getElementById('notification');
    const messageElement = notification.querySelector('.message');
    const iconElement = notification.querySelector('.icon');
    
    // Set the message text
    messageElement.textContent = message;
    
    // Update the icon based on type using decimal HTML entities
    // &#10004; = checkmark, &#10060; = X mark
    iconElement.innerHTML = type === "success" ? "&#10004;" : "&#10060;";
    
    // Reset classes
    notification.className = "notification";
    if (type === "error") {
        notification.classList.add("error");
    }
    
    notification.classList.add('show');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
    }, 5000);
}

// Parse a structured string into an array of objects
function parseStructuredString(str) {
    // Try to identify and parse a string with structured data
    try {
        // First check if it's JSON
        return JSON.parse(str);
    } catch (e) {
        // Not JSON, might be another structured format
        const items = [];
        
        // Split by double newlines which typically separate items
        const chunks = str.split('\n\n').filter(chunk => chunk.trim());
        
        chunks.forEach(chunk => {
            const item = {};
            const lines = chunk.split('\n');
            
            lines.forEach(line => {
                    if (line.includes(':')) {
                        // Only split on the first colon, and do not split if the value part contains 'https://'
                        const colonIndex = line.indexOf(':');
                        if (colonIndex !== -1) {
                            let key = line.substring(0, colonIndex).trim();
                            // Remove spaces inside the key
                            key = key.replace(/\s+/g, '');
                            const value = line.substring(colonIndex + 1).trim();
                            // If value contains 'https://', do not split further
                            if (value.includes('https://')) {
                                item[key] = value;
                            } else {
                                // If value does not contain 'https://', assign as usual
                                item[key] = value;
                            }
                        }
                    }
                });
            
            if (Object.keys(item).length > 0) {
                items.push(item);
            }
        });
        
        return items.length > 0 ? items : str;
    }
}

// Format generic result
function formatGenericResult(data) {
    if (typeof data === 'object' && data !== null) {
        let html = '';
        
        // For objects, create a property list
        for (const [key, value] of Object.entries(data)) {
            if (typeof value === 'object' && value !== null) {
                html += `<div class="result-property">
                    <span class="property-name">${key}:</span>
                    <span class="property-value">${JSON.stringify(value)}</span>
                </div>`;
            } else {
                html += `<div class="result-property">
                    <span class="property-name">${key}:</span>
                    <span class="property-value">${value}</span>
                </div>`;
            }
        }
        
        return html;
    } else if (typeof data === 'string') {
        return `<div class="result-property">${data}</div>`;
    } else {
        return `<div class="result-property">${JSON.stringify(data)}</div>`;
    }
}

// Get the current data from the JSON editor
function getCurrentEditorData() {
    const jsonEditor = document.getElementById('blogPostJson');
    
    try {
        // Remove any comments from the JSON before parsing
        const jsonWithoutComments = jsonEditor.value.replace(/\/\*[\s\S]*?\*\/|\/\/.*/g, '');
        return JSON.parse(jsonWithoutComments);
    } catch (e) {
        // Return a default structure if there's an error
        return {
            title: '',
            content: '',
            summary: '',
            parent_id: 'REQUIRED - Use the Parent Blogs tool to get a valid ID',
            draft: true
        };
    }
} 