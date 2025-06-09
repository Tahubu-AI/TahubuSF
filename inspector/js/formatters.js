/**
 * Formatting functions for specific tool results
 */

// Format blog post error
function formatBlogPostError(errorMessage) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Create formatted HTML output
        let html = '<div class="formatted-results">';
        html += `<div class="alert error"><strong>Error!</strong> Blog post creation failed.</div>`;
        
        html += '<div class="result-item">';
        html += `<h3>Blog Post Creation Error</h3>`;
        
        // Extract details from the error message
        let errorDetails = errorMessage;
        
        // Try to parse and format the error message if it's more complex
        if (errorMessage.includes("Failed to create blog post draft:")) {
            // The error might contain multiple lines or details
            const lines = errorMessage.split('\n');
            errorDetails = '';
            
            lines.forEach(line => {
                // Format each line as a separate detail
                errorDetails += `<div class="result-property">
                    <span class="property-value">${line}</span>
                </div>`;
            });
        } else {
            // Simple error message
            errorDetails = `<div class="result-property">
                <span class="property-value">${errorMessage}</span>
            </div>`;
        }
        
        html += errorDetails;
        html += '</div>';
        
        // Add possible solutions
        html += `<div class="result-item">
            <h3>Possible Solutions</h3>
            <div class="result-property">
                <p>1. Make sure you've provided a valid parent blog ID</p>
                <p>2. Check that your blog post title and content are valid</p>
                <p>3. Verify that Sitefinity is accessible and working correctly</p>
            </div>
        </div>`;
        
        html += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error formatting blog post error:', error);
        // Fallback to showing the raw error
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = errorMessage;
    }
}

// Format created blog post
function formatCreatedBlogPost(blogPost) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Create formatted HTML output
        let html = '<div class="formatted-results">';
        html += '<div class="alert success"><strong>Success!</strong> Blog post draft created successfully.</div>';
        
        html += '<div class="result-item">';
        html += `<h3>${blogPost.Title || 'New Blog Post'}</h3>`;
        
        // Add post URL if available
        if (blogPost.ItemDefaultUrl) {
            html += `<div class="result-property">
                <span class="property-name">URL:</span>
                <span class="property-value">${blogPost.ItemDefaultUrl}</span>
            </div>`;
        }
        
        // Add ID - Use correct property case, Sitefinity uses "Id" not "ID"
        html += `<div class="result-property">
            <span class="property-name">ID:</span>
            <span class="property-value">${blogPost.Id || blogPost.ID || 'Unknown'}</span>
        </div>`;
        
        // Add Status
        html += `<div class="result-property">
            <span class="property-name">Status:</span>
            <span class="property-value">Draft</span>
        </div>`;
        
        // Add Publication Date
        if (blogPost.PublicationDate) {
            const date = new Date(blogPost.PublicationDate).toLocaleString();
            html += `<div class="result-property">
                <span class="property-name">Created:</span>
                <span class="property-value">${date}</span>
            </div>`;
        }
        
        // Add Summary if available
        if (blogPost.Summary) {
            html += `<div class="result-property">
                <span class="property-name">Summary:</span>
                <span class="property-value">${blogPost.Summary}</span>
            </div>`;
        }
        
        // Preview of content (truncated)
        if (blogPost.Content) {
            // Strip HTML tags for preview
            const contentText = blogPost.Content.replace(/<[^>]*>/g, ' ').substring(0, 100);
            html += `<div class="result-property">
                <span class="property-name">Content:</span>
                <span class="property-value">${contentText}${blogPost.Content.length > 100 ? '...' : ''}</span>
            </div>`;
        }
        
        html += '</div>';
        
        // Add note about Sitefinity
        html += `<div class="result-item">
            <div class="result-property">
                <p>The blog post has been created as a draft. You can now edit, review, and publish it in the Sitefinity admin panel.</p>
            </div>
        </div>`;
        
        html += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error formatting created blog post:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = JSON.stringify(blogPost, null, 2);
    }
}

// Format created news item
function formatCreatedNewsItem(newsitem) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Create formatted HTML output
        let html = '<div class="formatted-results">';
        html += '<div class="alert success"><strong>Success!</strong> News Item draft created successfully.</div>';
        
        html += '<div class="result-item">';
        html += `<h3>${newsitem.Title || 'New Press Releaset'}</h3>`;
        
        // Add post URL if available
        if (newsitem.ItemDefaultUrl) {
            html += `<div class="result-property">
                <span class="property-name">URL:</span>
                <span class="property-value">${newsitem.ItemDefaultUrl}</span>
            </div>`;
        }
        
        // Add ID - Use correct property case, Sitefinity uses "Id" not "ID"
        html += `<div class="result-property">
            <span class="property-name">ID:</span>
            <span class="property-value">${newsitem.Id || newsitem.ID || 'Unknown'}</span>
        </div>`;
        
        // Add Status
        html += `<div class="result-property">
            <span class="property-name">Status:</span>
            <span class="property-value">Draft</span>
        </div>`;
        
        // Add Publication Date
        if (newsitem.PublicationDate) {
            const date = new Date(newsitem.PublicationDate).toLocaleString();
            html += `<div class="result-property">
                <span class="property-name">Created:</span>
                <span class="property-value">${date}</span>
            </div>`;
        }
        
        // Add Summary if available
        if (newsitem.Summary) {
            html += `<div class="result-property">
                <span class="property-name">Summary:</span>
                <span class="property-value">${newsitem.Summary}</span>
            </div>`;
        }
        
        // Preview of content (truncated)
        if (newsitem.Content) {
            // Strip HTML tags for preview
            const contentText = newsitem.Content.replace(/<[^>]*>/g, ' ').substring(0, 100);
            html += `<div class="result-property">
                <span class="property-name">Content:</span>
                <span class="property-value">${contentText}${newsitem.Content.length > 100 ? '...' : ''}</span>
            </div>`;
        }
        
        html += '</div>';
        
        // Add note about Sitefinity
        html += `<div class="result-item">
            <div class="result-property">
                <p>The News Item has been created as a draft. You can now edit, review, and publish it in the Sitefinity admin panel.</p>
            </div>
        </div>`;
        
        html += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error formatting created news item:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = JSON.stringify(newsitem, null, 2);
    }
}

// Format parent blogs
function displayParentBlogs(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string or object format
        let parentBlogs = data;
        if (typeof data === 'string') {
            // Try to convert from a structured format to a dictionary
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array of objects to dictionary format
                const blogsDict = {};
                parsedData.forEach(item => {
                    if (item.Id && item.Title) {
                        blogsDict[item.Id] = item.Title;
                    }
                });
                if (Object.keys(blogsDict).length > 0) {
                    parentBlogs = blogsDict;
                }
            }
        }
        
        if (!parentBlogs || Object.keys(parentBlogs).length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No parent blogs found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += '<h3>Available Parent Blogs</h3>';
        
        for (const [id, title] of Object.entries(parentBlogs)) {
            formattedOutput += `<div class="result-item">
                <h3>${title}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${id}</span>
                </div>
            </div>`;
        }
        
        // Add a note about usage
        formattedOutput += '<div class="result-item">'+
            '<div class="result-property">'+
            '<p>Use one of these IDs in the \'parent_id\' field when creating a blog post.</p>'+
            '</div></div>';
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error displaying parent blogs:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format parent lists
function displayParentLists(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string or object format
        let parentLists = data;
        if (typeof data === 'string') {
            // Try to convert from a structured format to a dictionary
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array of objects to dictionary format
                const listsDict = {};
                parsedData.forEach(item => {
                    if (item.Id && item.Title) {
                        listsDict[item.Id] = item.Title;
                    }
                });
                if (Object.keys(listsDict).length > 0) {
                    parentLists = listsDict;
                }
            }
        }
        
        if (!parentLists || Object.keys(parentLists).length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No parent Lists found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += '<h3>Available Parent Lists</h3>';
        
        for (const [id, title] of Object.entries(parentLists)) {
            formattedOutput += `<div class="result-item">
                <h3>${title}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${id}</span>
                </div>
            </div>`;
        }
        
        // Add a note about usage
        formattedOutput += '<div class="result-item">'+
            '<div class="result-property">'+
            '<p>Use one of these IDs in the \'parent_id\' field when creating a List Item.</p>'+
            '</div></div>';
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error displaying parent lists:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format albums
function displayAlbums(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string or object format
        let albums = data;
        if (typeof data === 'string') {
            // Try to convert from a structured format to a dictionary
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array of objects to dictionary format
                const albumsDict = {};
                parsedData.forEach(item => {
                    if (item.Id && item.Title) {
                        albumsDict[item.Id] = item.Title;
                    }
                });
                if (Object.keys(albumsDict).length > 0) {
                    albums = albumsDict;
                }
            }
        }
        
        if (!albums || Object.keys(albums).length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No albums found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += '<h3>Available Albums</h3>';
        
        for (const [id, title] of Object.entries(albums)) {
            formattedOutput += `<div class="result-item">
                <h3>${title}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${id}</span>
                </div>
            </div>`;
        }
        
        // Add a note about usage
        formattedOutput += '<div class="result-item">'+
            '<div class="result-property">'+
            '<p>Use one of these IDs in the \'parent_id\' field when creating an image.</p>'+
            '</div></div>';
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error displaying Albums:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format calendars
function displayCalendars(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string or object format
        let calendars = data;
        if (typeof data === 'string') {
            // Try to convert from a structured format to a dictionary
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array of objects to dictionary format
                const calendarsDict = {};
                parsedData.forEach(item => {
                    if (item.Id && item.Title) {
                        calendarsDict[item.Id] = item.Title;
                    }
                });
                if (Object.keys(calendarsDict).length > 0) {
                    calendars = calendarsDict;
                }
            }
        }
        
        if (!calendars || Object.keys(calendars).length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No calendars found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += '<h3>Available Calendars</h3>';
        
        for (const [id, title] of Object.entries(calendars)) {
            formattedOutput += `<div class="result-item">
                <h3>${title}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${id}</span>
                </div>
            </div>`;
        }
        
        // Add a note about usage
        formattedOutput += '<div class="result-item">'+
            '<div class="result-property">'+
            '<p>Use one of these IDs in the \'parent_id\' field when creating an event.</p>'+
            '</div></div>';
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error displaying calendars:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format document libraries
function displayDocumentLibraries(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string or object format
        let documentlibraries = data;
        if (typeof data === 'string') {
            // Try to convert from a structured format to a dictionary
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array of objects to dictionary format
                const librariesDict = {};
                parsedData.forEach(item => {
                    if (item.Id && item.Title) {
                        librariesDict[item.Id] = item.Title;
                    }
                });
                if (Object.keys(librariesDict).length > 0) {
                    documentlibraries = librariesDict;
                }
            }
        }
        
        if (!documentlibraries || Object.keys(documentlibraries).length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No document libraries found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += '<h3>Available document libraries</h3>';
        
        for (const [id, title] of Object.entries(documentlibraries)) {
            formattedOutput += `<div class="result-item">
                <h3>${title}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${id}</span>
                </div>
            </div>`;
        }
        
        // Add a note about usage
        formattedOutput += '<div class="result-item">'+
            '<div class="result-property">'+
            '<p>Use one of these IDs in the \'parent_id\' field when creating a document.</p>'+
            '</div></div>';
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error displaying document libraries:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format video libraries
function displayVideoLibraries(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string or object format
        let videolibraries = data;
        if (typeof data === 'string') {
            // Try to convert from a structured format to a dictionary
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array of objects to dictionary format
                const librariesDict = {};
                parsedData.forEach(item => {
                    if (item.Id && item.Title) {
                        librariesDict[item.Id] = item.Title;
                    }
                });
                if (Object.keys(librariesDict).length > 0) {
                    videolibraries = librariesDict;
                }
            }
        }
        
        if (!videolibraries || Object.keys(videolibraries).length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No video libraries found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += '<h3>Available video libraries</h3>';
        
        for (const [id, title] of Object.entries(videolibraries)) {
            formattedOutput += `<div class="result-item">
                <h3>${title}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${id}</span>
                </div>
            </div>`;
        }
        
        // Add a note about usage
        formattedOutput += '<div class="result-item">'+
            '<div class="result-property">'+
            '<p>Use one of these IDs in the \'parent_id\' field when creating a video.</p>'+
            '</div></div>';
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error displaying video libraries:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format news results
function formatNewsResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let news = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                news = { value: parsedData };
            }
        }
        
        if (!news || !news.value || news.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No news items found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>News Items (${news.value.length} found)</h3>`;
        
        news.value.forEach(item => {
            formattedOutput += `<div class="result-item">
                <h3>${item.Title || 'Untitled News'}</h3>`;
                
            if (item.PublicationDate) {
                const date = new Date(item.PublicationDate).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Published:</span>
                    <span class="property-value">${date}</span>
                </div>`;
            }
            
            if (item.Author) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Author:</span>
                    <span class="property-value">${item.Author}</span>
                </div>`;
            }
            
            if (item.Summary) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Summary:</span>
                    <span class="property-value">${item.Summary}</span>
                </div>`;
            }
            
            if (item.UrlName) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">URL Name:</span>
                    <span class="property-value">${item.UrlName}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting news results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format blog posts results
function formatBlogPostsResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let posts = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                posts = { value: parsedData };
            }
        }
        
        if (!posts || !posts.value || posts.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No blog posts found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Blog Posts (${posts.value.length} found)</h3>`;
        
        posts.value.forEach(post => {
            formattedOutput += `<div class="result-item">
                <h3>${post.Title || 'Untitled Post'}</h3>`;
                
            if (post.PublicationDate) {
                const date = new Date(post.PublicationDate).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Published:</span>
                    <span class="property-value">${date}</span>
                </div>`;
            }
            
            if (post.UrlName) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">URL Name:</span>
                    <span class="property-value">${post.UrlName}</span>
                </div>`;
            }
            
            if (post.Summary) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Summary:</span>
                    <span class="property-value">${post.Summary}</span>
                </div>`;
            }

            if (post.Id) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${post.Id}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting blog post results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format list items results
function formatListItemsResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let items = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                items = { value: parsedData };
            }
        }
        
        if (!items || !items.value || items.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No list items found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>List Items (${items.value.length} found)</h3>`;
        
        items.value.forEach(item => {
            formattedOutput += `<div class="result-item">
                <h3>${item.Title || 'Untitled Item'}</h3>`;
                
            if (item.PublicationDate) {
                const date = new Date(item.PublicationDate).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Published:</span>
                    <span class="property-value">${date}</span>
                </div>`;
            }
            
            if (item.Content) {
                // Show a truncated version of the content
                const truncatedContent = item.Content.length > 100 ? 
                    item.Content.substring(0, 100) + '...' : 
                    item.Content;
                
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Content:</span>
                    <span class="property-value">${truncatedContent}</span>
                </div>`;
            }

            if (item.Id) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${item.Id}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting list item results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format sites results
function formatSitesResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let sites = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                sites = { value: parsedData };
            }
        }
        
        if (!sites || !sites.value || sites.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No sites found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Sites (${sites.value.length} found)</h3>`;
        
        sites.value.forEach(site => {
            formattedOutput += `<div class="result-item">
                <h3>${site.Name || 'Unnamed Site'}</h3>`;
                
            // Add all site properties except Title/Name
            for (const [key, value] of Object.entries(site)) {
                if (key !== 'Title' && key !== 'Name') {
                    formattedOutput += `<div class="result-property">
                        <span class="property-name">${key}:</span>
                        <span class="property-value">${value}</span>
                    </div>`;
                }
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting sites results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format forms results
function formatFormsResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let forms = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                forms = { value: parsedData };
            }
        }
        
        if (!forms || !forms.value || forms.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No forms found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Forms (${forms.value.length} found)</h3>`;
        
        forms.value.forEach(form => {
            formattedOutput += `<div class="result-item">
                <h3>${form.Title || 'Untitled Form'}</h3>`;
                
            // Add common form properties
            if (form.SuccessMessage) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Success Message:</span>
                    <span class="property-value">${form.SuccessMessage}</span>
                </div>`;
            }
            if (form.Renderer) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Renderer:</span>
                    <span class="property-value">${form.Renderer}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting forms results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format search indexes results
function formatSearchIndexesResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let indexes = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                indexes = { value: parsedData };
            }
        }
        
        if (!indexes || !indexes.value || indexes.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No search indexes found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Search Indexes (${indexes.value.length} found)</h3>`;
        
        indexes.value.forEach(index => {
            formattedOutput += `<div class="result-item">
                <h3>${index.Name || 'Unnamed Index'}</h3>`;
                
            if (index.IsActive) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">IsActive:</span>
                    <span class="property-value">${index.IsActive}</span>
                </div>`;
            }
            
            if (index.IsBackend) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">IsBackend:</span>
                    <span class="property-value">${index.IsBackend}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting search indexes results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format taxonomies results
function formatTaxonomiesResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let taxonomies = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                taxonomies = { value: parsedData };
            }
        }
        
        if (!taxonomies || !taxonomies.value || taxonomies.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No taxonomies found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Taxonomies (${taxonomies.value.length} found)</h3>`;
        
        taxonomies.value.forEach(taxonomy => {
            formattedOutput += `<div class="result-item">
                <h3>${taxonomy.Title || 'Untitled Taxonomy'}</h3>`;
                
            if (taxonomy.TaxonName) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Taxon Name:</span>
                    <span class="property-value">${taxonomy.TaxonName}</span>
                </div>`;
            }
            
            if (taxonomy.Type) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Type:</span>
                    <span class="property-value">${taxonomy.Type}</span>
                </div>`;
            }

            if (taxonomy.UseCount) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Use Count:</span>
                    <span class="property-value">${taxonomy.UseCount}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting taxonomies results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format section presets results
function formatSectionPresetsResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let presets = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                presets = { value: parsedData };
            }
        }
        
        if (!presets || !presets.value || presets.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No section presets found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Section Presets (${presets.value.length} found)</h3>`;
        
        presets.value.forEach(preset => {
            formattedOutput += `<div class="result-item">
                <h3>${preset.Title || 'Untitled Preset'}</h3>`;
                
            if (preset.Thumbnail) {
                formattedOutput += `<div class="result-item">
                    <img src=${preset.Thumbnail} width=800px/>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting section presets results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format pages results
function formatPagesResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let pages = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                pages = { value: parsedData };
            }
        }
        
        if (!pages || !pages.value || pages.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No pages found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Pages (${pages.value.length} found)</h3>`;
        
        pages.value.forEach(page => {
            formattedOutput += `<div class="result-item">
                <h3>${page.Title || 'Untitled Page'}</h3>`;
                
            // Add common page properties
            for (const [key, value] of Object.entries(page)) {
                if (key !== 'Title') {
                    formattedOutput += `<div class="result-property">
                        <span class="property-name">${key}:</span>
                        <span class="property-value">${value}</span>
                    </div>`;
                }
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting pages results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format events results
function formatEventsResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let events = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                events = { value: parsedData };
            }
        }
        
        if (!events || !events.value || events.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No events found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Events (${events.value.length} found)</h3>`;
        
        events.value.forEach(event => {
            formattedOutput += `<div class="result-item">
                <h3>${event.Title || 'Untitled Event'}</h3>`;
                
            if (event.EventStart) {
                const startDate = new Date(event.EventStart).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Start:</span>
                    <span class="property-value">${startDate}</span>
                </div>`;
            }
            
            if (event.EventEnd) {
                const endDate = new Date(event.EventEnd).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">End:</span>
                    <span class="property-value">${endDate}</span>
                </div>`;
            }
            
            if (event.Summary) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Summary:</span>
                    <span class="property-value">${event.Summary}</span>
                </div>`;
            }
            
            if (event.Content) {
                // Show a truncated version of the content
                const truncatedContent = event.Content.length > 100 ? 
                    event.Content.substring(0, 100) + '...' : 
                    event.Content;
                
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Content:</span>
                    <span class="property-value">${truncatedContent}</span>
                </div>`;
            }
            
            if (event.UrlName) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">URL Name:</span>
                    <span class="property-value">${event.UrlName}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting events results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format videos results
function formatVideosResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let videos = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                videos = { value: parsedData };
            }
        }
        
        if (!videos || !videos.value || videos.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No videos found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Videos (${videos.value.length} found)</h3>`;
        
        videos.value.forEach(video => {
            formattedOutput += `<div class="result-item">
                <h3>${video.Title || 'Untitled Video'}</h3>`;
                
            if (video.PublicationDate) {
                const date = new Date(video.PublicationDate).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Published:</span>
                    <span class="property-value">${date}</span>
                </div>`;
            }
            
            if (video.Url) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">URL:</span>
                    <span class="property-value">${video.Url}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting videos results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format shared content results
function formatSharedContentResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let content = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                content = { value: parsedData };
            }
        }
        
        if (!content || !content.value || content.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No shared content found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Shared Content (${content.value.length} found)</h3>`;
        
        content.value.forEach(item => {
            formattedOutput += `<div class="result-item">
                <h3>${item.Title || 'Untitled Content'}</h3>`;
                
            if (item.PublicationDate) {
                const date = new Date(item.PublicationDate).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Published:</span>
                    <span class="property-value">${date}</span>
                </div>`;
            }
            
            if (item.Content) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Content:</span>
                    <span class="property-value">${item.Content}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting shared content results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format images results
function formatImagesResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let images = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                images = { value: parsedData };
            }
        }
        
        if (!images || !images.value || images.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No images found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Images (${images.value.length} found)</h3>`;
        
        images.value.forEach(image => {
            formattedOutput += `<div class="result-item">
                <h3>${image.Title || 'Untitled Image'}</h3>`;
                
            if (image.EmbedUrl) {
                formattedOutput += `<div class="result-property">
                    <img src="${image.EmbedUrl}" alt="${image.AlternativeText || 'Image thumbnail'}" style="max-width: 200px; max-height: 150px;">
                </div>`;
            }
            
            if (image.PublicationDate) {
                const date = new Date(image.PublicationDate).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Published:</span>
                    <span class="property-value">${date}</span>
                </div>`;
            }

            if (image.Extension) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Extension:</span>
                    <span class="property-value">${image.Extension}</span>
                </div>`;
            }
                
            if (image.TotalSize) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Total Size:</span>
                    <span class="property-value">${image.TotalSize}</span>
                </div>`;
            }

            if (image.Height) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Height:</span>
                    <span class="property-value">${image.Height}</span>
                </div>`;
            }
                
            if (image.Width) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Width:</span>
                    <span class="property-value">${image.Width}</span>
                </div>`;
            }

            if (image.AlternativeText) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Alternative Text:</span>
                    <span class="property-value">${image.AlternativeText}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting images results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format documents results
function formatDocumentsResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string
        let documents = data;
        if (typeof data === 'string') {
            const parsedData = parseStructuredString(data);
            if (Array.isArray(parsedData)) {
                // Convert array to expected format with 'value' property
                documents = { value: parsedData };
            }
        }
        
        if (!documents || !documents.value || documents.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No documents found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Documents (${documents.value.length} found)</h3>`;
        
        documents.value.forEach(doc => {
            formattedOutput += `<div class="result-item">
                <h3>${doc.Title || 'Untitled Document'}</h3>`;
                
            if (doc.Extension) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Type:</span>
                    <span class="property-value">${doc.Extension.toUpperCase()}</span>
                </div>`;
            }

            if (doc.PublicationDate) {
                const date = new Date(doc.PublicationDate).toLocaleDateString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Published:</span>
                    <span class="property-value">${date}</span>
                </div>`;
            }
            
            if (doc.TotalSize) {
                const sizeInKB = Math.round(doc.TotalSize / 1024);
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Size:</span>
                    <span class="property-value">${sizeInKB} KB</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting documents results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}

// Format page templates results
function formatPageTemplatesResults(data) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        // Parse the data if it's a string (sometimes it might be pre-parsed)
        let templates = data;
        if (typeof data === 'string') {
            // Try to identify and parse structured data in the string
            templates = parseStructuredString(data);
        }
        
        // Create formatted HTML output
        let html = '<div class="formatted-results">';
        
        if (Array.isArray(templates)) {
            // It's an array of template objects
            html += '<h3>Page Templates</h3>';
            html += '<div class="result-table-container">';
            html += '<table class="result-table">';
            html += '<thead><tr><th>Title</th><th>Framework</th><th>Renderer</th></tr></thead>';
            html += '<tbody>';
            
            templates.forEach(template => {
                html += `<tr>
                    <td>${template.Title || ''}</td>
                    <td>${template.Framework || ''}</td>
                    <td>${template.Renderer || 'None'}</td>
                </tr>`;
            });
            
            html += '</tbody></table></div>';
        } else {
            // It's a string-based format or unknown format
            const items = data.split('\n\n').filter(item => item.trim());
            
            items.forEach(item => {
                html += '<div class="result-item">';
                
                const lines = item.split('\n');
                let title = 'Unknown Template';
                
                // Extract properties
                lines.forEach(line => {
                    if (line.startsWith('Title:')) {
                        title = line.replace('Title:', '').trim();
                        html += `<h3>${title}</h3>`;
                    } else if (line.includes(':')) {
                        const [name, value] = line.split(':').map(s => s.trim());
                        html += `<div class="result-property">
                            <span class="property-name">${name}:</span>
                            <span class="property-value">${value}</span>
                        </div>`;
                    } else if (line.trim()) {
                        html += `<div class="result-property">${line}</div>`;
                    }
                });
                
                html += '</div>';
            });
        }
        
        html += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error formatting page templates:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    }
}
