class HealthMateChat {
    constructor() {
        this.isTyping = false;
        this.recognition = null;
        this.isRecording = false;
        this.soundEnabled = true;
        this.darkMode = false;
        this.autoSuggestions = true;
        this.fontSize = 'medium';
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadSettings();
        this.initSpeechRecognition();
        this.scrollToBottom();
        this.playNotificationSound();
    }

    bindEvents() {
        // Message input events
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        messageInput.addEventListener('input', () => {
            this.updateSendButton();
            this.showInputSuggestions();
        });

        sendBtn.addEventListener('click', () => this.sendMessage());

        // Header action buttons
        document.getElementById('exportBtn').addEventListener('click', () => this.exportChat());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearChat());
        document.getElementById('settingsBtn').addEventListener('click', () => this.openSettings());

        // Settings modal
        document.getElementById('closeSettings').addEventListener('click', () => this.closeSettings());
        document.getElementById('settingsModal').addEventListener('click', (e) => {
            if (e.target.id === 'settingsModal') {
                this.closeSettings();
            }
        });

        // Settings controls
        document.getElementById('soundEnabled').addEventListener('change', (e) => {
            this.soundEnabled = e.target.checked;
            this.saveSettings();
        });

        document.getElementById('darkMode').addEventListener('change', (e) => {
            this.darkMode = e.target.checked;
            this.toggleDarkMode();
            this.saveSettings();
        });

        document.getElementById('autoSuggestions').addEventListener('change', (e) => {
            this.autoSuggestions = e.target.checked;
            this.saveSettings();
        });

        document.getElementById('fontSize').addEventListener('change', (e) => {
            this.fontSize = e.target.value;
            this.updateFontSize();
            this.saveSettings();
        });

        // Quick actions
        document.querySelectorAll('.quick-action').forEach(action => {
            action.addEventListener('click', (e) => {
                const actionText = e.currentTarget.dataset.action;
                this.handleQuickAction(actionText);
            });
        });

        // Voice recording
        document.getElementById('voiceBtn').addEventListener('click', () => this.toggleVoiceRecording());

        // Emoji picker
        document.getElementById('emojiBtn').addEventListener('click', () => this.toggleEmojiPicker());
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.emoji-picker') && !e.target.closest('#emojiBtn')) {
                this.hideEmojiPicker();
            }
        });

        // Emoji selection
        document.querySelectorAll('.emoji').forEach(emoji => {
            emoji.addEventListener('click', (e) => {
                this.insertEmoji(e.target.dataset.emoji);
            });
        });

        // Attachment button
        document.getElementById('attachmentBtn').addEventListener('click', () => this.handleAttachment());

        // Escape key to close modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeSettings();
                this.hideEmojiPicker();
            }
        });
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message || this.isTyping) return;

        messageInput.value = '';
        this.updateSendButton();
        this.hideSuggestions();
        
        this.showTypingIndicator();
        this.isTyping = true;

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            
            if (data.success) {
                this.addMessage(data.user_message);
                this.addMessage(data.bot_message);
                this.showSuggestions(data.suggestions);
                this.playNotificationSound();
            } else {
                this.showError('Failed to get response. Please try again.');
            }
        } catch (error) {
            this.showError('Connection error. Please check your internet connection.');
        } finally {
            this.hideTypingIndicator();
            this.isTyping = false;
            messageInput.focus();
        }
    }

    addMessage(messageData) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${messageData.sender === 'You' ? 'user-message' : 'bot-message'}`;
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-${messageData.sender === 'You' ? 'user' : 'user-md'}"></i>
            </div>
            <div class="message-content">
                <div class="message-header">
                    <span class="sender">${messageData.sender}</span>
                    <span class="timestamp">${messageData.timestamp}</span>
                </div>
                <div class="message-text">${messageData.message}</div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        document.getElementById('typingIndicator').style.display = 'block';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        document.getElementById('typingIndicator').style.display = 'none';
    }

    showSuggestions(suggestions) {
        if (!this.autoSuggestions || !suggestions || suggestions.length === 0) return;

        const suggestionsContainer = document.getElementById('suggestions');
        const suggestionsList = document.getElementById('suggestionsList');
        
        suggestionsList.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = 'suggestion-item';
            suggestionItem.textContent = suggestion;
            suggestionItem.addEventListener('click', () => {
                document.getElementById('messageInput').value = suggestion;
                this.hideSuggestions();
                this.updateSendButton();
            });
            suggestionsList.appendChild(suggestionItem);
        });
        
        suggestionsContainer.style.display = 'block';
    }

    hideSuggestions() {
        document.getElementById('suggestions').style.display = 'none';
    }

    updateSendButton() {
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        const hasText = messageInput.value.trim().length > 0;
        
        sendBtn.disabled = !hasText || this.isTyping;
        sendBtn.style.opacity = hasText && !this.isTyping ? '1' : '0.5';
    }

    scrollToBottom() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async exportChat() {
        try {
            const response = await fetch('/export_chat');
            const data = await response.json();
            
            const blob = new Blob([data.export_text], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            a.click();
            URL.revokeObjectURL(url);
            
            this.showToast('Chat exported successfully!', 'success');
        } catch (error) {
            this.showError('Failed to export chat.');
        }
    }

    async clearChat() {
        if (!confirm('Are you sure you want to clear the chat history?')) return;
        
        try {
            const response = await fetch('/clear_chat', { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('chatMessages').innerHTML = '';
                this.hideSuggestions();
                this.showToast('Chat cleared successfully!', 'success');
            }
        } catch (error) {
            this.showError('Failed to clear chat.');
        }
    }

    openSettings() {
        document.getElementById('settingsModal').style.display = 'flex';
    }

    closeSettings() {
        document.getElementById('settingsModal').style.display = 'none';
    }

    toggleDarkMode() {
        if (this.darkMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }

    updateFontSize() {
        document.body.className = document.body.className.replace(/font-\w+/g, '');
        document.body.classList.add(`font-${this.fontSize}`);
    }

    handleQuickAction(actionText) {
        document.getElementById('messageInput').value = actionText;
        this.updateSendButton();
        this.sendMessage();
    }

    toggleVoiceRecording() {
        if (!this.recognition) {
            this.showError('Voice recognition is not supported in your browser.');
            return;
        }

        const voiceBtn = document.getElementById('voiceBtn');
        
        if (this.isRecording) {
            this.recognition.stop();
            voiceBtn.classList.remove('recording');
            this.isRecording = false;
        } else {
            this.recognition.start();
            voiceBtn.classList.add('recording');
            this.isRecording = true;
        }
    }

    initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
        } else if ('SpeechRecognition' in window) {
            this.recognition = new SpeechRecognition();
        } else {
            return; // Speech recognition not supported
        }

        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('messageInput').value = transcript;
            this.updateSendButton();
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.showError('Speech recognition error. Please try again.');
        };

        this.recognition.onend = () => {
            document.getElementById('voiceBtn').classList.remove('recording');
            this.isRecording = false;
        };
    }

    toggleEmojiPicker() {
        const emojiPicker = document.getElementById('emojiPicker');
        const isVisible = emojiPicker.style.display === 'block';
        emojiPicker.style.display = isVisible ? 'none' : 'block';
    }

    hideEmojiPicker() {
        document.getElementById('emojiPicker').style.display = 'none';
    }

    insertEmoji(emoji) {
        const messageInput = document.getElementById('messageInput');
        const cursorPos = messageInput.selectionStart;
        const textBefore = messageInput.value.substring(0, cursorPos);
        const textAfter = messageInput.value.substring(cursorPos);
        
        messageInput.value = textBefore + emoji + textAfter;
        messageInput.focus();
        messageInput.setSelectionRange(cursorPos + emoji.length, cursorPos + emoji.length);
        
        this.updateSendButton();
        this.hideEmojiPicker();
    }

    handleAttachment() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.txt,.pdf,.doc,.docx,image/*';
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                this.showToast(`File "${file.name}" selected. This feature is coming soon!`, 'info');
            }
        };
        input.click();
    }

    showInputSuggestions() {
        // This would show real-time suggestions as user types
        // Implementation depends on your backend API
    }

    showError(message) {
        this.showToast(message, 'error');
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            animation: slideInRight 0.3s ease;
        `;
        
        switch (type) {
            case 'success':
                toast.style.background = 'var(--success-color)';
                break;
            case 'error':
                toast.style.background = 'var(--error-color)';
                break;
            case 'warning':
                toast.style.background = 'var(--warning-color)';
                break;
            default:
                toast.style.background = 'var(--primary-color)';
        }
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    playNotificationSound() {
        if (!this.soundEnabled) return;
        
        // Create a simple beep sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    }

    saveSettings() {
        const settings = {
            soundEnabled: this.soundEnabled,
            darkMode: this.darkMode,
            autoSuggestions: this.autoSuggestions,
            fontSize: this.fontSize
        };
        localStorage.setItem('healthmate_settings', JSON.stringify(settings));
    }

    loadSettings() {
        const savedSettings = localStorage.getItem('healthmate_settings');
        if (savedSettings) {
            const settings = JSON.parse(savedSettings);
            this.soundEnabled = settings.soundEnabled !== undefined ? settings.soundEnabled : true;
            this.darkMode = settings.darkMode || false;
            this.autoSuggestions = settings.autoSuggestions !== undefined ? settings.autoSuggestions : true;
            this.fontSize = settings.fontSize || 'medium';
            
            // Apply settings
            document.getElementById('soundEnabled').checked = this.soundEnabled;
            document.getElementById('darkMode').checked = this.darkMode;
            document.getElementById('autoSuggestions').checked = this.autoSuggestions;
            document.getElementById('fontSize').value = this.fontSize;
            
            this.toggleDarkMode();
            this.updateFontSize();
        }
    }
}

// Initialize the chat application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new HealthMateChat();
});

// Add CSS for toast animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);