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
        
        // Add ID
        html += `<div class="result-property">
            <span class="property-name">ID:</span>
            <span class="property-value">${blogPost.Id || 'Unknown'}</span>
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

// Format parent blogs
function displayParentBlogs(parentBlogs) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
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
        document.getElementById('results').textContent = JSON.stringify(parentBlogs, null, 2);
    }
}

// Format parent lists
function displayParentLists(parentLists) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
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
        document.getElementById('results').textContent = JSON.stringify(parentLists, null, 2);
    }
}

// Format albums
function displayAlbums(albums) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
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
        document.getElementById('results').textContent = JSON.stringify(albums, null, 2);
    }
}

// Format calendars
function displayCalendars(calendars) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
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
        document.getElementById('results').textContent = JSON.stringify(calendars, null, 2);
    }
}

// Format document libraries
function displayDocumentLibraries(documentlibraries) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
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
        document.getElementById('results').textContent = JSON.stringify(documentlibraries, null, 2);
    }
}

// Format video libraries
function displayVideoLibraries(videolibraries) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
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
        document.getElementById('results').textContent = JSON.stringify(videolibraries, null, 2);
    }
}

// Format news results
function formatNewsResults(news) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!news || !news.value || news.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No news items found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>News Items (${news.value.length} found)</h3>`;
        
        news.value.forEach(item => {
            formattedOutput += `<div class="result-item">
                <h3>${item.Title || 'Untitled News'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${item.Id || 'Unknown'}</span>
                </div>`;
                
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
        document.getElementById('results').textContent = JSON.stringify(news, null, 2);
    }
}

// Format blog posts results
function formatBlogPostsResults(posts) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!posts || !posts.value || posts.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No blog posts found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Blog Posts (${posts.value.length} found)</h3>`;
        
        posts.value.forEach(post => {
            formattedOutput += `<div class="result-item">
                <h3>${post.Title || 'Untitled Post'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${post.Id || 'Unknown'}</span>
                </div>`;
                
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
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting blog post results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = JSON.stringify(posts, null, 2);
    }
}

// Format list items results
function formatListItemsResults(items) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!items || !items.value || items.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No list items found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>List Items (${items.value.length} found)</h3>`;
        
        items.value.forEach(item => {
            formattedOutput += `<div class="result-item">
                <h3>${item.Title || 'Untitled Item'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${item.Id || 'Unknown'}</span>
                </div>`;
                
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
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting list item results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = JSON.stringify(items, null, 2);
    }
}

// Format sites results
function formatSitesResults(sites) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!sites || !sites.value || sites.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No sites found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Sites (${sites.value.length} found)</h3>`;
        
        sites.value.forEach(site => {
            formattedOutput += `<div class="result-item">
                <h3>${site.Name || 'Unnamed Site'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${site.Id || 'Unknown'}</span>
                </div>`;
                
            if (site.IsDefault) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Default Site:</span>
                    <span class="property-value">Yes</span>
                </div>`;
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
        document.getElementById('results').textContent = JSON.stringify(sites, null, 2);
    }
}

// Format forms results
function formatFormsResults(forms) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!forms || !forms.value || forms.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No forms found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Forms (${forms.value.length} found)</h3>`;
        
        forms.value.forEach(form => {
            formattedOutput += `<div class="result-item">
                <h3>${form.Title || 'Untitled Form'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${form.Id || 'Unknown'}</span>
                </div>`;
                
            if (form.UrlName) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">URL Name:</span>
                    <span class="property-value">${form.UrlName}</span>
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
        document.getElementById('results').textContent = JSON.stringify(forms, null, 2);
    }
}

// Format search indexes results
function formatSearchIndexesResults(indexes) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!indexes || !indexes.value || indexes.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No search indexes found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Search Indexes (${indexes.value.length} found)</h3>`;
        
        indexes.value.forEach(index => {
            formattedOutput += `<div class="result-item">
                <h3>${index.Name || 'Unnamed Index'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${index.Id || 'Unknown'}</span>
                </div>`;
                
            if (index.Description) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Description:</span>
                    <span class="property-value">${index.Description}</span>
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
        document.getElementById('results').textContent = JSON.stringify(indexes, null, 2);
    }
}

// Format taxonomies results
function formatTaxonomiesResults(taxonomies) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!taxonomies || !taxonomies.value || taxonomies.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No taxonomies found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Taxonomies (${taxonomies.value.length} found)</h3>`;
        
        taxonomies.value.forEach(taxonomy => {
            formattedOutput += `<div class="result-item">
                <h3>${taxonomy.Title || 'Untitled Taxonomy'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${taxonomy.Id || 'Unknown'}</span>
                </div>`;
                
            if (taxonomy.TaxonomyType) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Type:</span>
                    <span class="property-value">${taxonomy.TaxonomyType}</span>
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
        document.getElementById('results').textContent = JSON.stringify(taxonomies, null, 2);
    }
}

// Format section presets results
function formatSectionPresetsResults(presets) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!presets || !presets.value || presets.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No section presets found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Section Presets (${presets.value.length} found)</h3>`;
        
        presets.value.forEach(preset => {
            formattedOutput += `<div class="result-item">
                <h3>${preset.Title || 'Untitled Preset'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${preset.Id || 'Unknown'}</span>
                </div>`;
                
            if (preset.SectionName) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Section Name:</span>
                    <span class="property-value">${preset.SectionName}</span>
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
        document.getElementById('results').textContent = JSON.stringify(presets, null, 2);
    }
}

// Format pages results
function formatPagesResults(pages) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!pages || !pages.value || pages.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No pages found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Pages (${pages.value.length} found)</h3>`;
        
        pages.value.forEach(page => {
            formattedOutput += `<div class="result-item">
                <h3>${page.Title || 'Untitled Page'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${page.Id || 'Unknown'}</span>
                </div>`;
                
            if (page.ParentId) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Parent ID:</span>
                    <span class="property-value">${page.ParentId}</span>
                </div>`;
            }
            
            if (page.UrlName) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">URL Name:</span>
                    <span class="property-value">${page.UrlName}</span>
                </div>`;
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
        document.getElementById('results').textContent = JSON.stringify(pages, null, 2);
    }
}

// Format events results
function formatEventsResults(events) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!events || !events.value || events.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No events found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Events (${events.value.length} found)</h3>`;
        
        events.value.forEach(event => {
            formattedOutput += `<div class="result-item">
                <h3>${event.Title || 'Untitled Event'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${event.Id || 'Unknown'}</span>
                </div>`;
                
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
        document.getElementById('results').textContent = JSON.stringify(events, null, 2);
    }
}

// Format shared content results
function formatSharedContentResults(content) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!content || !content.value || content.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No shared content found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Shared Content (${content.value.length} found)</h3>`;
        
        content.value.forEach(item => {
            formattedOutput += `<div class="result-item">
                <h3>${item.Title || 'Untitled Content'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${item.Id || 'Unknown'}</span>
                </div>`;
                
            if (item.PublicationDate) {
                const date = new Date(item.PublicationDate).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Published:</span>
                    <span class="property-value">${date}</span>
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
        document.getElementById('results').textContent = JSON.stringify(content, null, 2);
    }
}

// Format images results
function formatImagesResults(images) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!images || !images.value || images.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No images found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Images (${images.value.length} found)</h3>`;
        
        images.value.forEach(image => {
            formattedOutput += `<div class="result-item">
                <h3>${image.Title || 'Untitled Image'}</h3>`;
                
            if (image.ThumbnailUrl) {
                formattedOutput += `<div class="result-property">
                    <img src="${image.ThumbnailUrl}" alt="${image.Title || 'Image thumbnail'}" style="max-width: 200px; max-height: 150px;">
                </div>`;
            }
                
            formattedOutput += `<div class="result-property">
                <span class="property-name">ID:</span>
                <span class="property-value">${image.Id || 'Unknown'}</span>
            </div>`;
                
            if (image.UrlName) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">URL Name:</span>
                    <span class="property-value">${image.UrlName}</span>
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
        document.getElementById('results').textContent = JSON.stringify(images, null, 2);
    }
}

// Format documents results
function formatDocumentsResults(documents) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!documents || !documents.value || documents.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No documents found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Documents (${documents.value.length} found)</h3>`;
        
        documents.value.forEach(doc => {
            formattedOutput += `<div class="result-item">
                <h3>${doc.Title || 'Untitled Document'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${doc.Id || 'Unknown'}</span>
                </div>`;
                
            if (doc.Extension) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Type:</span>
                    <span class="property-value">${doc.Extension.toUpperCase()}</span>
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
        document.getElementById('results').textContent = JSON.stringify(documents, null, 2);
    }
}

// Format videos results
function formatVideosResults(videos) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!videos || !videos.value || videos.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No videos found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Videos (${videos.value.length} found)</h3>`;
        
        videos.value.forEach(video => {
            formattedOutput += `<div class="result-item">
                <h3>${video.Title || 'Untitled Video'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${video.Id || 'Unknown'}</span>
                </div>`;
                
            if (video.PublicationDate) {
                const date = new Date(video.PublicationDate).toLocaleString();
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Published:</span>
                    <span class="property-value">${date}</span>
                </div>`;
            }
            
            if (video.UrlName) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">URL Name:</span>
                    <span class="property-value">${video.UrlName}</span>
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
        document.getElementById('results').textContent = JSON.stringify(videos, null, 2);
    }
}

// Format page templates results
function formatPageTemplatesResults(templates) {
    const resultsContainer = document.getElementById('results-container');
    
    try {
        if (!templates || !templates.value || templates.value.length === 0) {
            resultsContainer.innerHTML = '<pre id="results">No page templates found.</pre>';
            return;
        }
        
        let formattedOutput = '<div class="formatted-results">';
        formattedOutput += `<h3>Page Templates (${templates.value.length} found)</h3>`;
        
        templates.value.forEach(template => {
            formattedOutput += `<div class="result-item">
                <h3>${template.Name || 'Unnamed Template'}</h3>
                <div class="result-property">
                    <span class="property-name">ID:</span>
                    <span class="property-value">${template.Id || 'Unknown'}</span>
                </div>`;
                
            if (template.Title) {
                formattedOutput += `<div class="result-property">
                    <span class="property-name">Title:</span>
                    <span class="property-value">${template.Title}</span>
                </div>`;
            }
                
            formattedOutput += '</div>';
        });
        
        formattedOutput += '</div>';
        
        // Update the results container
        resultsContainer.innerHTML = formattedOutput;
    } catch (error) {
        console.error('Error formatting page templates results:', error);
        // Fallback to showing the raw data
        resultsContainer.innerHTML = '<pre id="results"></pre>';
        document.getElementById('results').textContent = JSON.stringify(templates, null, 2);
    }
} 