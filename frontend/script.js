// Global variables
let apiBaseUrl = 'http://localhost:8000/api';
let vectorStoreLoaded = false;
let processingStats = {};
let chatHistory = [];

// DOM elements
const apiKeyInput = document.getElementById('apiKey');
const setApiKeyBtn = document.getElementById('setApiKeyBtn');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const directoryPathInput = document.getElementById('directoryPath');
const processDirectoryBtn = document.getElementById('processDirectoryBtn');
const saveVectorStoreBtn = document.getElementById('saveVectorStoreBtn');
const loadVectorStoreBtn = document.getElementById('loadVectorStoreBtn');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');
const welcomeMessage = document.getElementById('welcomeMessage');
const chatInputContainer = document.getElementById('chatInputContainer');
const loadingSpinner = document.getElementById('loadingSpinner');
const statsSection = document.getElementById('statsSection');
const chartSection = document.getElementById('chartSection');

// Chart instances
let fileTypesChart = null;
let summaryChart = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadInitialState();
});

function initializeEventListeners() {
    // API Key
    setApiKeyBtn.addEventListener('click', setApiKey);
    
    // File upload
    uploadBtn.addEventListener('click', uploadFiles);
    fileInput.addEventListener('change', handleFileSelection);
    
    // Directory processing
    processDirectoryBtn.addEventListener('click', processDirectory);
    
    // Vector store management
    saveVectorStoreBtn.addEventListener('click', saveVectorStore);
    loadVectorStoreBtn.addEventListener('click', loadVectorStore);
    
    // Chat
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Markdown preview functionality
    initializeMarkdownPreview();
    
    // Load initial stats
    loadStats();
}

async function loadInitialState() {
    try {
        await loadStats();
    } catch (error) {
        console.error('Error loading initial state:', error);
    }
}

// API Key Management
async function setApiKey() {
    const apiKey = apiKeyInput.value.trim();
    if (!apiKey) {
        showAlert('Please enter a valid API key', 'danger');
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch(`${apiBaseUrl}/set-api-key`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ api_key: apiKey })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('API key set successfully!', 'success');
        } else {
            throw new Error(data.detail || 'Failed to set API key');
        }
    } catch (error) {
        showAlert(`Error setting API key: ${error.message}`, 'danger');
    } finally {
        showLoading(false);
    }
}

// File Upload Management
function handleFileSelection() {
    const files = fileInput.files;
    if (files.length > 0) {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = `<i class="fas fa-rocket"></i> Process ${files.length} Document(s)`;
    } else {
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-rocket"></i> Process Documents';
    }
}

async function uploadFiles() {
    const files = fileInput.files;
    if (files.length === 0) {
        showAlert('Please select files to upload', 'warning');
        return;
    }
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }
    
    try {
        showProcessingModal('Processing uploaded documents...');
        
        const response = await fetch(`${apiBaseUrl}/upload-files`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            hideProcessingModal();
            processingStats = data.stats;
            vectorStoreLoaded = true;
            updateUI();
            showProcessingSummary(data.stats);
            showAlert(data.message, 'success');
            
            // Clear file input
            fileInput.value = '';
            handleFileSelection();
        } else {
            throw new Error(data.detail || 'Failed to process files');
        }
    } catch (error) {
        hideProcessingModal();
        showAlert(`Error processing files: ${error.message}`, 'danger');
    }
}

// Directory Processing
async function processDirectory() {
    const directoryPath = directoryPathInput.value.trim();
    if (!directoryPath) {
        showAlert('Please enter a directory path', 'warning');
        return;
    }
    
    try {
        showProcessingModal('Processing directory...');
        
        const formData = new FormData();
        formData.append('directory_path', directoryPath);
        
        const response = await fetch(`${apiBaseUrl}/process-directory`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            hideProcessingModal();
            processingStats = data.stats;
            vectorStoreLoaded = true;
            updateUI();
            showProcessingSummary(data.stats);
            showAlert(data.message, 'success');
        } else {
            throw new Error(data.detail || 'Failed to process directory');
        }
    } catch (error) {
        hideProcessingModal();
        showAlert(`Error processing directory: ${error.message}`, 'danger');
    }
}

// Vector Store Management
async function saveVectorStore() {
    try {
        showLoading(true);
        
        const response = await fetch(`${apiBaseUrl}/save-vector-store`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Vector store saved successfully!', 'success');
        } else {
            throw new Error(data.detail || 'Failed to save vector store');
        }
    } catch (error) {
        showAlert(`Error saving vector store: ${error.message}`, 'danger');
    } finally {
        showLoading(false);
    }
}

async function loadVectorStore() {
    try {
        showLoading(true);
        
        const response = await fetch(`${apiBaseUrl}/load-vector-store`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            vectorStoreLoaded = true;
            processingStats = data.stats || {};
            updateUI();
            showAlert('Vector store loaded successfully!', 'success');
        } else {
            throw new Error(data.detail || 'Failed to load vector store');
        }
    } catch (error) {
        showAlert(`Error loading vector store: ${error.message}`, 'danger');
    } finally {
        showLoading(false);
    }
}

// Chat Management
async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    if (!vectorStoreLoaded) {
        showAlert('Please upload and process documents first', 'warning');
        return;
    }
    
    // Add user message to chat
    addMessageToChat('user', message);
    chatInput.value = '';
    chatInput.disabled = true;
    sendBtn.disabled = true;
    
    try {
        const response = await fetch(`${apiBaseUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            addMessageToChat('assistant', data.response, data.citations, data.themes);
        } else {
            throw new Error(data.detail || 'Failed to get response');
        }
    } catch (error) {
        addMessageToChat('assistant', `Error: ${error.message}`);
    } finally {
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

function addMessageToChat(role, content, citations = null, themes = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.innerHTML = formatMessage(content);
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString();
    
    messageDiv.appendChild(bubbleDiv);
    messageDiv.appendChild(timeDiv);
    
    // Add citations if available
    if (citations && citations.length > 0) {
        const citationsDiv = createCitationsSection(citations);
        messageDiv.appendChild(citationsDiv);
    }
    
    // Add themes if available
    if (themes && themes.themes && themes.themes.length > 0) {
        const themesDiv = createThemesSection(themes);
        messageDiv.appendChild(themesDiv);
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Add copy buttons to code blocks after DOM insertion
    addCopyButtonsToCodeBlocks(messageDiv);
}

function createCitationsSection(citations) {
    const citationsDiv = document.createElement('div');
    citationsDiv.className = 'citations-section';
    citationsDiv.innerHTML = '<h6><i class="fas fa-book"></i> Citations</h6>';
    
    citations.forEach((citation, index) => {
        const citationItem = document.createElement('div');
        citationItem.className = 'citation-item';
        
        const header = document.createElement('div');
        header.className = 'citation-header';
        header.textContent = `Citation ${index + 1}: ${citation.citation}`;
        
        const content = document.createElement('div');
        content.className = 'citation-content';
        const contentPreview = citation.content.substring(0, 300) + (citation.content.length > 300 ? '...' : '');
        content.innerHTML = formatMessage(contentPreview);
        
        const meta = document.createElement('div');
        meta.className = 'citation-meta';
        meta.innerHTML = `
            <strong>Score:</strong> ${citation.score.toFixed(3)} | 
            <strong>Type:</strong> ${citation.type}
            ${citation.page ? ` | <strong>Page:</strong> ${citation.page}` : ''}
        `;
        
        citationItem.appendChild(header);
        citationItem.appendChild(content);
        citationItem.appendChild(meta);
        citationsDiv.appendChild(citationItem);
    });
    
    return citationsDiv;
}

function createThemesSection(themes) {
    const themesDiv = document.createElement('div');
    themesDiv.className = 'themes-section';
    themesDiv.innerHTML = '<h6><i class="fas fa-lightbulb"></i> Common Themes</h6>';
    
    themes.themes.forEach(theme => {
        const themeItem = document.createElement('div');
        themeItem.className = 'theme-item';
        
        themeItem.innerHTML = `
            <div class="theme-name">${theme.name}</div>
            <div class="theme-description">${formatMessage(theme.description)}</div>
            <div class="theme-frequency">Frequency: ${theme.frequency}</div>
        `;
        
        themesDiv.appendChild(themeItem);
    });
    
    if (themes.summary) {
        const summaryDiv = document.createElement('div');
        summaryDiv.innerHTML = `<strong>Summary:</strong> ${formatMessage(themes.summary)}`;
        themesDiv.appendChild(summaryDiv);
    }
    
    if (themes.insights && themes.insights.length > 0) {
        const insightsDiv = document.createElement('div');
        insightsDiv.innerHTML = '<strong>Key Insights:</strong>';
        const insightsList = document.createElement('ul');
        themes.insights.forEach(insight => {
            const li = document.createElement('li');
            li.innerHTML = formatMessage(insight);
            insightsList.appendChild(li);
        });
        insightsDiv.appendChild(insightsList);
        themesDiv.appendChild(insightsDiv);
    }
    
    return themesDiv;
}

// Stats Management
async function loadStats() {
    try {
        const response = await fetch(`${apiBaseUrl}/stats`);
        const data = await response.json();
        
        if (response.ok) {
            vectorStoreLoaded = data.vector_store_loaded;
            processingStats = data.stats || {};
            updateUI();
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function updateUI() {
    // Update welcome message and chat input
    if (vectorStoreLoaded) {
        welcomeMessage.style.display = 'none';
        chatInputContainer.style.display = 'block';
        chatInput.disabled = false;
        sendBtn.disabled = false;
    } else {
        welcomeMessage.style.display = 'block';
        chatInputContainer.style.display = 'none';
        chatInput.disabled = true;
        sendBtn.disabled = true;
    }
    
    // Update stats
    if (processingStats && Object.keys(processingStats).length > 0) {
        updateStatsDisplay();
        statsSection.style.display = 'block';
        chartSection.style.display = 'block';
        updateFileTypesChart();
    } else {
        statsSection.style.display = 'none';
        chartSection.style.display = 'none';
    }
}

function updateStatsDisplay() {
    document.getElementById('totalFiles').textContent = processingStats.total_files || 0;
    document.getElementById('totalDocuments').textContent = processingStats.total_documents || 0;
    document.getElementById('totalChunks').textContent = processingStats.total_chunks || 0;
    document.getElementById('totalFileTypes').textContent = processingStats.file_types ? processingStats.file_types.length : 0;
}

function updateFileTypesChart() {
    const ctx = document.getElementById('fileTypesChart').getContext('2d');
    
    if (fileTypesChart) {
        fileTypesChart.destroy();
    }
    
    if (processingStats.type_counts) {
        const labels = Object.keys(processingStats.type_counts);
        const data = Object.values(processingStats.type_counts);
        
        fileTypesChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Processing Modal Management
function showProcessingModal(message) {
    document.getElementById('processingMessage').textContent = message;
    const modal = new bootstrap.Modal(document.getElementById('processingModal'), {
        backdrop: 'static',
        keyboard: false
    });
    modal.show();
}

function hideProcessingModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('processingModal'));
    if (modal) {
        modal.hide();
    }
}

// Processing Summary Modal
function showProcessingSummary(stats) {
    // Update summary modal data
    document.getElementById('summaryFiles').textContent = stats.total_files || 0;
    document.getElementById('summaryDocuments').textContent = stats.total_documents || 0;
    document.getElementById('summaryChunks').textContent = stats.total_chunks || 0;
    document.getElementById('summaryFileTypes').textContent = stats.file_types ? stats.file_types.length : 0;
    
    // Update summary chart
    const ctx = document.getElementById('summaryChart').getContext('2d');
    
    if (summaryChart) {
        summaryChart.destroy();
    }
    
    if (stats.type_counts) {
        const labels = Object.keys(stats.type_counts);
        const data = Object.values(stats.type_counts);
        
        summaryChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('summaryModal'));
    modal.show();
}

// Initialize markdown preview functionality
function initializeMarkdownPreview() {
    const markdownToggle = document.getElementById('markdownToggle');
    const chatInput = document.getElementById('chatInput');
    const markdownPreview = document.getElementById('markdownPreview');
    let isPreviewMode = false;
    
    if (!markdownToggle || !chatInput || !markdownPreview) return;
    
    // Toggle preview mode
    markdownToggle.addEventListener('click', function() {
        isPreviewMode = !isPreviewMode;
        
        if (isPreviewMode) {
            // Show preview, hide input
            chatInput.style.display = 'none';
            markdownPreview.style.display = 'block';
            markdownPreview.innerHTML = formatMessage(chatInput.value || '');
            markdownToggle.innerHTML = '<i class="fas fa-edit"></i> Edit';
            markdownToggle.classList.remove('btn-outline-secondary');
            markdownToggle.classList.add('btn-outline-primary');
        } else {
            // Show input, hide preview
            chatInput.style.display = 'block';
            markdownPreview.style.display = 'none';
            markdownToggle.innerHTML = '<i class="fas fa-eye"></i> Preview';
            markdownToggle.classList.remove('btn-outline-primary');
            markdownToggle.classList.add('btn-outline-secondary');
            chatInput.focus();
        }
    });
    
    // Update preview on input change
    chatInput.addEventListener('input', function() {
        if (isPreviewMode) {
            markdownPreview.innerHTML = formatMessage(chatInput.value || '');
        }
    });
    
    // Handle keyboard shortcuts
    chatInput.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + P for preview toggle
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            markdownToggle.click();
        }
        
        // Ctrl/Cmd + Enter to send message
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
}

// Test markdown formatting function (for demonstration)
function testMarkdownFormatting() {
    const testMarkdown = `
# Markdown Support Test

This is a **comprehensive test** of markdown support in the RAG application.

## Features Supported:

### Text Formatting
- **Bold text** using \`**bold**\`
- *Italic text* using \`*italic*\`
- \`Inline code\` using backticks

### Lists
1. Numbered lists
2. With multiple items
   - Nested bullet points
   - With proper indentation

### Code Blocks
\`\`\`python
def hello_world():
    print("Hello, World!")
    return "Success"
\`\`\`

\`\`\`javascript
function greet(name) {
    return \`Hello, \${name}!\`;
}
\`\`\`

### Blockquotes
> This is a blockquote example.
> It can span multiple lines.

### Tables
| Feature | Status | Description |
|---------|--------|-------------|
| Headers | ✅ | H1-H6 supported |
| Lists | ✅ | Ordered and unordered |
| Code | ✅ | Inline and blocks |
| Tables | ✅ | With alignment |

### Links and Emphasis
Visit [the documentation](https://example.com) for more info.

---

*This test demonstrates the full markdown capabilities of the application.*
    `;
    
    console.log('Test markdown content:', testMarkdown);
    return testMarkdown;
}

// Make test function available globally for debugging
window.testMarkdownFormatting = testMarkdownFormatting;

// Utility Functions
function showLoading(show) {
    loadingSpinner.style.display = show ? 'block' : 'none';
}

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to top of main content
    const mainContent = document.querySelector('.main-content');
    const header = document.querySelector('.header');
    mainContent.insertBefore(alertDiv, header.nextSibling);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function formatMessage(message) {
    // Check if marked library is loaded
    if (typeof marked !== 'undefined') {
        // Configure marked for safe rendering with custom renderer
        const renderer = new marked.Renderer();
        
        // Custom code block renderer for syntax highlighting
        renderer.code = function(code, language) {
            const validLanguage = language && Prism.languages[language] ? language : 'text';
            const highlightedCode = typeof Prism !== 'undefined' && Prism.languages[validLanguage] 
                ? Prism.highlight(code, Prism.languages[validLanguage], validLanguage)
                : code;
            
            return `<pre class="language-${validLanguage}"><code class="language-${validLanguage}">${highlightedCode}</code></pre>`;
        };
        
        // Configure marked options
        marked.setOptions({
            renderer: renderer,
            breaks: true,
            gfm: true,
            sanitize: false // We'll use DOMPurify for sanitization
        });
        
        // Parse markdown
        let html = marked.parse(message);
        
        // Sanitize HTML if DOMPurify is available
        if (typeof DOMPurify !== 'undefined') {
            html = DOMPurify.sanitize(html, {
                ALLOWED_TAGS: [
                    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'a', 'table', 'thead',
                    'tbody', 'tr', 'td', 'th', 'hr', 'img', 'span'
                ],
                ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class']
            });
        }
        
        return html;
    } else {
        // Fallback to basic formatting if marked is not loaded
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }
}

// Add copy buttons to code blocks
function addCopyButtonsToCodeBlocks(container) {
    const codeBlocks = container.querySelectorAll('pre[class*="language-"]');
    
    codeBlocks.forEach(codeBlock => {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'code-copy-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = 'Copy code';
        
        copyBtn.addEventListener('click', async () => {
            const code = codeBlock.querySelector('code').textContent;
            
            try {
                await navigator.clipboard.writeText(code);
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                copyBtn.style.background = 'rgba(25, 135, 84, 0.1)';
                
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                    copyBtn.style.background = 'rgba(255, 255, 255, 0.8)';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy code:', err);
                copyBtn.innerHTML = '<i class="fas fa-times"></i>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            }
        });
        
        codeBlock.appendChild(copyBtn);
    });
}

// Drag and Drop for File Upload
function initializeDragAndDrop() {
    const fileUploadArea = document.querySelector('.file-upload-area');
    
    if (fileUploadArea) {
        fileUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });
        
        fileUploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        });
        
        fileUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            fileInput.files = files;
            handleFileSelection();
        });
    }
}

// Initialize drag and drop when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeDragAndDrop);
