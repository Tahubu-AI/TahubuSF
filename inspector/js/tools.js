/**
 * Tool functions for communicating with the API
 */

// Run a tool with the given name
async function runTool(toolName) {
    // Show loading indicator
    const loaderId = toolName.toLowerCase().replace('get', '').replace('create', '') + "-loading";
    const loaderElement = document.getElementById(loaderId);
    if (loaderElement) {
        loaderElement.classList.remove('hidden');
    }
    
    // Set results to loading if this is a direct user action (not a background fetch)
    if (loaderElement) {
        // Reset the results container to its initial state with the pre element
        document.getElementById('results-container').innerHTML = '<pre id="results">Loading...</pre>';
    }
    
    try {
        // Call the MCP tool
        const response = await fetch('/api/run-tool', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: toolName,
                params: {}
            }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display the results if this is a direct user action
        if (loaderElement) {
            const result = data.result;
            
            // Pass the raw result to the appropriate formatter based on tool name
            // Each formatter is responsible for parsing its own data format
            if (toolName === 'getParentBlogs' && result) {
                // Format parent blogs results in a more readable way
                displayParentBlogs(result);
            } else if (toolName === 'getParentLists' && result) {
                // Format parent Lists in a more readable way
                displayParentLists(result);
            } else if (toolName === 'getAlbums' && result) {
                // Format Albums in a more readable way
                displayAlbums(result);
            } else if (toolName === 'getCalendars' && result) {
                // Format Calendars in a more readable way
                displayCalendars(result);
            } else if (toolName === 'getDocumentLibraries' && result) {
                // Format parent Document Libraries in a more readable way
                displayDocumentLibraries(result);
            } else if (toolName === 'getVideoLibraries' && result) {
                // Format parent Video Libraries in a more readable way
                displayVideoLibraries(result);
            } else if (toolName === 'getPageTemplates' && result) {
                // Format page templates in a more readable way
                formatPageTemplatesResults(result);
            } else if (toolName === 'getNews' && result) {
                // Format news items in a more readable way
                formatNewsResults(result);
            } else if (toolName === 'getBlogPosts' && result) {
                // Format blog posts in a more readable way
                formatBlogPostsResults(result);
            } else if (toolName === 'getListItems' && result) {
                // Format list Items in a more readable way
                formatListItemsResults(result);
            } else if (toolName === 'getSites' && result) {
                // Format sites in a more readable way
                formatSitesResults(result);
            } else if (toolName === 'getForms' && result) {
                // Format Forms in a more readable way
                formatFormsResults(result);
            } else if (toolName === 'getSearchIndexes' && result) {
                // Format Search Indexes in a more readable way
                formatSearchIndexesResults(result);  
            } else if (toolName === 'getTaxonomies' && result) {
                // Format taxonomies in a more readable way
                formatTaxonomiesResults(result);  
            } else if (toolName === 'getSectionPresets' && result) {
                // Format Section Presets in a more readable way
                formatSectionPresetsResults(result);  
            } else if (toolName === 'getPages' && result) {
                // Format pages in a more readable way
                formatPagesResults(result);
            } else if (toolName === 'getEvents' && result) {
                // Format events in a more readable way
                formatEventsResults(result);
            } else if (toolName === 'getSharedContent' && result) {
                // Format Shared Content in a more readable way
                formatSharedContentResults(result);
            } else if (toolName === 'getImages' && result) {
                // Format images in a more readable way
                formatImagesResults(result);
            } else if(toolName === 'getDocuments' && result) {
               formatDocumentsResults(result); 
            } else if(toolName === 'getVideos' && result) {
               formatVideosResults(result); 
            } else if (result && typeof result === 'string') {
                // If result is a string, display it directly
                document.getElementById('results').textContent = result;
            } else {
                // Display regular JSON results - ensure pre element exists
                document.getElementById('results-container').innerHTML = '<pre id="results"></pre>';
                document.getElementById('results').textContent = JSON.stringify(result, null, 2);
            }
        }
        
        return data.result;
    } catch (error) {
        console.error('Error running tool:', error);
        if (loaderElement) {
            // Ensure the pre element exists
            document.getElementById('results-container').innerHTML = '<pre id="results"></pre>';
            document.getElementById('results').textContent = `Error: ${error.message}`;
        }
        return null;
    } finally {
        // Hide loading indicator
        if (loaderElement) {
            loaderElement.classList.add('hidden');
        }
    }
}

// Fetch parent blogs and populate the parent_id field
async function fetchAndPopulateBlogParentId() {
    try {
        // Show loading in the editor
        const jsonEditor = document.getElementById('blogPostJson');
        const currentData = getCurrentEditorData(jsonEditor.id);
        
        // Show temporary loading message in the JSON editor
        jsonEditor.value = "/* Fetching parent blogs... */\n" + JSON.stringify(currentData, null, 2);
        
        // Fetch parent blogs
        const parentBlogs = await runTool('getParentBlogs');
        
        if (parentBlogs && Object.keys(parentBlogs).length > 0) {
            // Get the first parent blog ID
            const firstParentId = Object.keys(parentBlogs)[0];
            const firstName = parentBlogs[firstParentId];
            
            // Update the parent_id in the current data
            currentData.parent_id = firstParentId;
            
            // Create comment with all available parent blogs
            let blogComment = "/* Available parent blogs:\n";
            for (const [id, title] of Object.entries(parentBlogs)) {
                const isSelected = (id === firstParentId) ? " (SELECTED)" : "";
                blogComment += `${title}${isSelected}: ${id}\n`;
            }
            blogComment += "*/\n";
            
            // Update the JSON editor with the comment and updated data
            jsonEditor.value = blogComment + JSON.stringify(currentData, null, 2);
        } else {
            // No parent blogs found, show warning
            jsonEditor.value = "/* WARNING: No parent blogs found. You need a parent blog to create a post. */\n" + 
                               JSON.stringify(currentData, null, 2);
        }
    } catch (error) {
        console.error("Error fetching parent blogs:", error);
    }
}

// Fetch parent list and populate the parent_id field
async function fetchAndPopulateListParentId() {
    try {
        // Show loading in the editor
        const jsonEditor = document.getElementById('listItemPostJson');
        const currentData = getCurrentEditorData(jsonEditor.id);
        
        // Show temporary loading message in the JSON editor
        jsonEditor.value = "/* Fetching parent lists... */\n" + JSON.stringify(currentData, null, 2);
        
        // Fetch parent Lists
        const parentLists = await runTool('getParentLists');
        
        if (parentLists && Object.keys(parentLists).length > 0) {
            // Get the first parent blog ID
            const firstParentId = Object.keys(parentLists)[0];
            const firstName = parentLists[firstParentId];
            
            // Update the parent_id in the current data
            currentData.parent_id = firstParentId;
            
            // Create comment with all available parent blogs
            let listComment = "/* Available parent Lists:\n";
            for (const [id, title] of Object.entries(parentLists)) {
                const isSelected = (id === firstParentId) ? " (SELECTED)" : "";
                listComment += `${title}${isSelected}: ${id}\n`;
            }
            listComment += "*/\n";
            
            // Update the JSON editor with the comment and updated data
            jsonEditor.value = listComment + JSON.stringify(currentData, null, 2);
        } else {
            // No parent blogs found, show warning
            jsonEditor.value = "/* WARNING: No parent lists found. You need a parent list to create a List Item. */\n" + 
                               JSON.stringify(currentData, null, 2);
        }
    } catch (error) {
        console.error("Error fetching parent lists:", error);
    }
}

// Fetch calendar and populate the parent_id field
async function fetchAndPopulateCalendarParentId() {
    try {
        // Show loading in the editor
        const jsonEditor = document.getElementById('eventPostJson');
        const currentData = getCurrentEditorData(jsonEditor.id);
        
        // Show temporary loading message in the JSON editor
        jsonEditor.value = "/* Fetching Calendars... */\n" + JSON.stringify(currentData, null, 2);
        
        // Fetch parent Calendars
        const parentCalendars = await runTool('getCalendars');
        
        if (parentCalendars && Object.keys(parentCalendars).length > 0) {
            // Get the first parent Calendar ID
            const firstParentId = Object.keys(parentCalendars)[0];
            const firstName = parentCalendars[firstParentId];
            
            // Update the parent_id in the current data
            currentData.parent_id = firstParentId;
            
            // Create comment with all available calendars
            let calendarComment = "/* Available Calenders:\n";
            for (const [id, title] of Object.entries(parentCalendars)) {
                const isSelected = (id === firstParentId) ? " (SELECTED)" : "";
                calendarComment += `${title}${isSelected}: ${id}\n`;
            }
            calendarComment += "*/\n";
            
            // Update the JSON editor with the comment and updated data
            jsonEditor.value = calendarComment + JSON.stringify(currentData, null, 2);
        } else {
            // No parent blogs found, show warning
            jsonEditor.value = "/* WARNING: No Calendars found. You need a Calendar to create an event. */\n" + 
                               JSON.stringify(currentData, null, 2);
        }
    } catch (error) {
        console.error("Error fetching calendars:", error);
    }
}
// Create a blog post
async function createBlogPost() {
    // Show loading indicator
    document.getElementById('createblogpost-loading').classList.remove('hidden');
    
    try {
        // Get the JSON data from the editor
        const jsonEditor = document.getElementById('blogPostJson');
        let blogPostData;
        
        try {
            // Remove any comments from the JSON before parsing
            const jsonWithoutComments = jsonEditor.value.replace(/\/\*[\s\S]*?\*\/|\/\/.*/g, '');
            blogPostData = JSON.parse(jsonWithoutComments);
        } catch (e) {
            throw new Error(`Invalid JSON: ${e.message}`);
        }
        
        // Validate required fields
        if (!blogPostData.parent_id || blogPostData.parent_id === "REQUIRED - Use the Parent Blogs tool to get a valid ID") {
            throw new Error("Parent blog ID (parent_id) is required. Please use the Parent Blogs tool to get a valid ID.");
        }
        
        // Call the MCP tool
        const response = await fetch('/api/run-tool', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: 'createBlogPostDraft',
                params: blogPostData
            }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Show notification
        if (data.result && data.result.Id) {
            showNotification("Blog post created successfully!", "success");
            formatCreatedBlogPost(data.result);
            
            // Close the modal after successful creation
            closeBlogEditor();
        } else {
            throw new Error("Blog post created but no ID was returned. Check results for details.");
        }
        
        return data.result;
    } catch (error) {
        console.error('Error creating blog post:', error);
        showNotification(error.message, "error");
        formatBlogPostError(error.message);
        return null;
    } finally {
        // Hide loading indicator
        document.getElementById('createblogpost-loading').classList.add('hidden');
    }
}

// Create a List Item
async function createListItem() {
    // Show loading indicator
    document.getElementById('createlistitem-loading').classList.remove('hidden');
    
    try {
        // Get the JSON data from the editor
        const jsonEditor = document.getElementById('listItemPostJson');
        let listItemPostData;
        
        try {
            // Remove any comments from the JSON before parsing
            const jsonWithoutComments = jsonEditor.value.replace(/\/\*[\s\S]*?\*\/|\/\/.*/g, '');
            listItemPostData = JSON.parse(jsonWithoutComments);
        } catch (e) {
            throw new Error(`Invalid JSON: ${e.message}`);
        }
        
        // Validate required fields
        if (!listItemPostData.parent_id || listItemPostData.parent_id === "REQUIRED - Use the Parent List tool to get a valid ID") {
            throw new Error("Parent list ID (parent_id) is required. Please use the Parent List tool to get a valid ID.");
        }
        
        // Call the MCP tool
        const response = await fetch('/api/run-tool', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: 'createListItemDraft',
                params: listItemPostData
            }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Show notification
        if (data.result && data.result.Id) {
            showNotification("List Item created successfully!", "success");
            formatCreatedListItem(data.result);
            
            // Close the modal after successful creation
            closeListsEditor();
        } else {
            throw new Error("List Item created but no ID was returned. Check results for details.");
        }
        
        return data.result;
    } catch (error) {
        console.error('Error creating List Item:', error);
        showNotification(error.message, "error");
        formatListItemError(error.message);
        return null;
    } finally {
        // Hide loading indicator
        document.getElementById('createlistitem-loading').classList.add('hidden');
    }
}

// Create an Event
async function createEventItem() {
    // Show loading indicator
    document.getElementById('createevent-loading').classList.remove('hidden');
    
    try {
        // Get the JSON data from the editor
        const jsonEditor = document.getElementById('eventPostJson');
        let eventPostData;
        
        try {
            // Remove any comments from the JSON before parsing
            const jsonWithoutComments = jsonEditor.value.replace(/\/\*[\s\S]*?\*\/|\/\/.*/g, '');
            eventPostData = JSON.parse(jsonWithoutComments);
        } catch (e) {
            throw new Error(`Invalid JSON: ${e.message}`);
        }
        
        // Validate required fields
        if (!eventPostData.parent_id || eventPostData.parent_id === "REQUIRED - Use the Calendar tool to get a valid ID") {
            throw new Error("Calendar ID (parent_id) is required. Please use the Calendar tool to get a valid ID.");
        }
        
        // Call the MCP tool
        const response = await fetch('/api/run-tool', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: 'createEventDraft',
                params: eventPostData
            }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Show notification
        if (data.result && data.result.Id) {
            showNotification("Event created successfully!", "success");
            formatCreatedEvent(data.result);
            
            // Close the modal after successful creation
            closeEventEditor();
        } else {
            throw new Error("Event created but no ID was returned. Check results for details.");
        }
        
        return data.result;
    } catch (error) {
        console.error('Error creating Event:', error);
        showNotification(error.message, "error");
        formatEventError(error.message);
        return null;
    } finally {
        // Hide loading indicator
        document.getElementById('createevent-loading').classList.add('hidden');
    }
}

// Create a News Item
async function createNewsItem() {
    // Show loading indicator
    document.getElementById('createnewsitem-loading').classList.remove('hidden');
    
    try {
        // Get the JSON data from the editor
        const jsonEditor = document.getElementById('newsPostJson');
        let newsData;
        
        try {
            // Remove any comments from the JSON before parsing
            const jsonWithoutComments = jsonEditor.value.replace(/\/\*[\s\S]*?\*\/|\/\/.*/g, '');
            newsData = JSON.parse(jsonWithoutComments);
        } catch (e) {
            throw new Error(`Invalid JSON: ${e.message}`);
        }
              
        // Call the MCP tool
        const response = await fetch('/api/run-tool', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: 'createNewsItemDraft',
                params: newsData
            }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Show notification
        if (data.result && data.result.Id) {
            showNotification("News Item created successfully!", "success");
            formatCreatedNewsItem(data.result);
            
            // Close the modal after successful creation
            closeNewsEditor();
        } else {
            throw new Error("News Item was created but something went wrong. Check results for details.");
        }
        
        return data.result;
    } catch (error) {
        console.error('Error creating News Item:', error);
        showNotification(error.message, "error");
        formatNewsItemError(error.message);
        return null;
    } finally {
        // Hide loading indicator
        document.getElementById('createnewsitem-loading').classList.add('hidden');
    }
}

// Open the blog editor modal
function openBlogEditor() {
    document.getElementById('blogEditorModal').style.display = 'block';
    fetchAndPopulateBlogParentId();
}

// Open the news editor modal
function openNewsEditor() {
    document.getElementById('newsEditorModal').style.display = 'block';
}

// Open the ListItem editor modal
function openListItemEditor() {
    document.getElementById('listItemEditorModal').style.display = 'block';
    fetchAndPopulateListParentId();
}

// Open the Event editor modal
function openEventEditor() {
    document.getElementById('eventEditorModal').style.display = 'block';
    fetchAndPopulateCalendarParentId();
}

// Close the blog editor modal
function closeBlogEditor() {
    document.getElementById('blogEditorModal').style.display = 'none';
} 

// Close the news editor modal
function closeNewsEditor() {
    document.getElementById('newsEditorModal').style.display = 'none';
} 

// Close the List Item editor modal
function closeListsEditor() {
    document.getElementById('listItemEditorModal').style.display = 'none';
} 
// Close the Event editor modal
function closeEventEditor() {
    document.getElementById('eventEditorModal').style.display = 'none';
} 