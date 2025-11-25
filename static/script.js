class ChatBot {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.messagesContainer = document.getElementById('messages');
        this.statusBtn = document.getElementById('statusBtn');
        this.settingsBtn = document.getElementById('settingsBtn');
        this.historyBtn = document.getElementById('historyBtn');
        this.welcomeMessage = document.getElementById('welcomeMessage');
        this.chatContainer = document.getElementById('chatContainer');
        this.roleSelectWelcome = document.getElementById('roleSelectWelcome');
        this.selectedRole = 'assistant';
        this.roleConfig = {};
        this.isLoading = false;
        this.init();
    }

    async init() {
        // Parallel loading
        await Promise.all([
            this.loadRoleConfig(),
            this.loadConversationHistory()
        ]);
        
        this.setupEventListeners();
        this.checkStatus();
        setInterval(() => this.checkStatus(), 10000);
    }

    setupEventListeners() {
        this.sendBtn.addEventListener('click', (e) => this.sendMessage(e));
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage(e);
            }
        });
        
        this.settingsBtn.addEventListener('click', () => this.showSettings());
        this.historyBtn.addEventListener('click', () => this.loadHistory());
        this.statusBtn.addEventListener('click', () => this.checkStatus());
        document.getElementById('changeRoleBtn').addEventListener('click', () => this.changeRole());
        
        this.roleSelectWelcome.addEventListener('change', (e) => {
            this.selectedRole = e.target.value;
        });

        document.getElementById('continueBtn').addEventListener('click', () => {
            if (this.selectedRole) this.setRole(this.selectedRole);
        });

        window.addEventListener('click', (e) => {
            ['settingsModal', 'historyModal', 'confirmationModal'].forEach(modal => {
                if (e.target.id === modal) {
                    document.getElementById(modal).style.display = 'none';
                }
            });
        });
    }

    async loadRoleConfig() {
        try {
            const response = await fetch('/api/roles');
            const data = await response.json();
            this.roleConfig = data.config || {};
        } catch (error) {
            console.error('Role config error:', error);
        }
    }

    async loadConversationHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            const messages = data.messages || [];
            
            this.messagesContainer.innerHTML = '';
            
            for (const msg of messages) {
                this.addMessage(msg.role, msg.content);
            }
            
            if (messages.length > 0) {
                this.welcomeMessage.style.display = 'none';
            }
        } catch (error) {
            console.error('History error:', error);
        }
    }

    async checkStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            const indicator = this.statusBtn.querySelector('.status-indicator');
            const statusText = this.statusBtn.querySelector('.status-text');
            
            if (data.status === 'connected') {
                indicator.classList.remove('disconnected');
                indicator.classList.add('connected');
                statusText.textContent = 'Connected';
                this.messageInput.disabled = false;
                this.sendBtn.disabled = false;
            } else {
                indicator.classList.add('disconnected');
                statusText.textContent = 'Disconnected';
                this.messageInput.disabled = true;
                this.sendBtn.disabled = true;
            }
        } catch (error) {
            console.error('Status error:', error);
            this.messageInput.disabled = true;
            this.sendBtn.disabled = true;
        }
    }

    async sendMessage(event) {
        event.preventDefault();

        if (this.isLoading) return;
        
        const message = this.messageInput.value.trim();
        if (!message) return;

        this.isLoading = true;
        this.sendBtn.disabled = true;

        this.addMessage('user', message);
        this.messageInput.value = '';
        this.welcomeMessage.style.display = 'none';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            if (response.ok) {
                const preparedMessage = String(data.message || '');
                const model = String(data.model || 'google/gemini-2.5-flash');
                
                this.addMessage('assistant', '⏳ Thinking...');
                
                try {
                    if (!preparedMessage || preparedMessage.length === 0) {
                        throw new Error('Empty message');
                    }
                    
                    const aiResponse = await puter.ai.chat(preparedMessage, { model: model });
                    
                    const lastMsg = this.messagesContainer.lastChild;
                    if (lastMsg) this.messagesContainer.removeChild(lastMsg);
                    
                    this.addMessage('assistant', aiResponse);
                    
                    fetch('/api/save-response', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ response: aiResponse })
                    }).catch(e => console.error('Save error:', e));
                    
                } catch (puterError) {
                    const lastMsg = this.messagesContainer.lastChild;
                    if (lastMsg) this.messagesContainer.removeChild(lastMsg);
                    this.addMessage('assistant', `⚠️ Error: ${puterError.message}`);
                }
            } else {
                this.addMessage('assistant', `⚠️ Error: ${data.error}`);
            }
        } catch (error) {
            this.addMessage('assistant', `⚠️ Error: ${error.message}`);
        } finally {
            this.isLoading = false;
            this.sendBtn.disabled = false;
            this.messageInput.focus();
        }
    }

    addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const roleConfig = this.roleConfig[this.selectedRole] || { emoji: '🤖', color: '#667eea' };
        
        const wrapper = document.createElement('div');
        wrapper.className = 'message-wrapper';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = role === 'user' ? '👤' : roleConfig.emoji;
        avatar.style.fontSize = role === 'user' ? '18px' : '24px';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const header = document.createElement('div');
        header.className = 'message-header';
        const roleDisplay = role === 'user' ? 'You' : this.selectedRole.replace(/_/g, ' ').toUpperCase();
        header.textContent = roleDisplay;

        const bubble = document.createElement('div');
        bubble.className = `message-bubble role-${this.selectedRole}`;
        const contentStr = String(content || '');
        bubble.innerHTML = contentStr.replace(/\n/g, '<br/>');

        const timestamp = document.createElement('div');
        timestamp.className = 'message-time';
        timestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        contentDiv.appendChild(header);
        contentDiv.appendChild(bubble);
        contentDiv.appendChild(timestamp);

        wrapper.appendChild(avatar);
        wrapper.appendChild(contentDiv);
        messageDiv.appendChild(wrapper);
        this.messagesContainer.appendChild(messageDiv);

        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    async showSettings() {
        try {
            const context = await (await fetch('/api/get-context')).json();
            document.getElementById('locationInput').value = context.location || '';
            document.getElementById('timezoneInput').value = context.timezone || '';
            document.getElementById('expertiseLevel').value = context.expertise_level || 'general';
        } catch (error) {
            console.error('Settings error:', error);
        }
        document.getElementById('settingsModal').style.display = 'block';
    }

    async saveSettings() {
        const location = document.getElementById('locationInput').value;
        const timezone = document.getElementById('timezoneInput').value;
        const expertiseLevel = document.getElementById('expertiseLevel').value;

        try {
            await fetch('/api/set-context', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    location: location,
                    timezone: timezone,
                    expertise_level: expertiseLevel
                })
            });

            alert('Settings saved!');
            document.getElementById('settingsModal').style.display = 'none';
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }

    async setRole(role) {
        try {
            await fetch('/api/set-role', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ role: role })
            });
            
            this.welcomeMessage.style.display = 'none';
        } catch (error) {
            console.error('Role error:', error);
        }
    }

    changeRole() {
        this.messagesContainer.innerHTML = '';
        this.welcomeMessage.style.display = 'block';
        this.roleSelectWelcome.focus();
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            const messages = data.messages || [];
            
            const historyDiv = document.getElementById('historyList');
            historyDiv.innerHTML = '';
            
            if (messages.length === 0) {
                historyDiv.innerHTML = '<p>No messages yet</p>';
            } else {
                for (const msg of messages) {
                    const msgEl = document.createElement('div');
                    msgEl.className = 'history-item';
                    msgEl.textContent = `${msg.role.toUpperCase()}: ${msg.content.substring(0, 50)}...`;
                    historyDiv.appendChild(msgEl);
                }
            }
            
            document.getElementById('historyModal').style.display = 'block';
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }

    async confirmClear() {
        try {
            await fetch('/api/clear', { method: 'POST' });
            this.messagesContainer.innerHTML = '';
            this.welcomeMessage.style.display = 'block';
            document.getElementById('confirmationModal').style.display = 'none';
            document.getElementById('historyModal').style.display = 'none';
            alert('History cleared!');
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new ChatBot();
});
