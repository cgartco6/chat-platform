// Open chat with a contact
function openChat(contactId) {
    const contact = contacts.find(c => c.id == contactId);
    if (!contact) return;
    
    chatName.textContent = contact.name;
    renderMessages(contactId);
    
    // Mark messages as read
    contact.unread = 0;
    renderContacts();
}

// Render messages for a contact
function renderMessages(contactId) {
    const chatMessages = messages[contactId] || [];
    messagesContainer.innerHTML = '';
    
    chatMessages.forEach(msg => {
        let messageEl;
        
        if (msg.type === 'image') {
            messageEl = createImageMessage(msg);
        } else if (msg.type === 'audio') {
            messageEl = createAudioMessage(msg);
        } else {
            messageEl = createTextMessage(msg);
        }
        
        messagesContainer.appendChild(messageEl);
    });
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Create text message element
function createTextMessage(msg) {
    const messageEl = document.createElement('div');
    messageEl.classList.add('message');
    messageEl.classList.add(msg.sender === 'user' ? 'sent' : 'received');
    
    messageEl.innerHTML = `
        <div class="message-text">${msg.text}</div>
        <div class="message-time-stamp">${msg.time}</div>
    `;
    
    return messageEl;
}

// Create image message element
function createImageMessage(msg) {
    const messageEl = document.createElement('div');
    messageEl.classList.add('message');
    messageEl.classList.add(msg.sender === 'user' ? 'sent' : 'received');
    messageEl.classList.add('media-message');
    
    messageEl.innerHTML = `
        <div class="message-text">${msg.text}</div>
        <img src="${msg.content}" class="media-content" style="max-width: 250px; margin-top: 5px;">
        <div class="message-time-stamp">${msg.time}</div>
    `;
    
    return messageEl;
}

// Create audio message element
function createAudioMessage(msg) {
    const messageEl = document.createElement('div');
    messageEl.classList.add('message');
    messageEl.classList.add(msg.sender === 'user' ? 'sent' : 'received');
    messageEl.classList.add('audio-message');
    
    messageEl.innerHTML = `
        <div class="play-button">
            <i class="fas fa-play"></i>
        </div>
        <div class="audio-player">
            <div class="progress-bar">
                <div class="progress"></div>
            </div>
            <span>${msg.duration}</span>
        </div>
        <div class="message-time-stamp">${msg.time}</div>
    `;
    
    return messageEl;
}

// Send a new message
function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
    
    // Get current time
    const now = new Date();
    const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    // Create new message
    const newMessage = {
        text,
        time,
        sender: 'user'
    };
    
    // Add to messages for active contact
    const activeContactId = document.querySelector('.contact.active').dataset.id;
    if (!messages[activeContactId]) {
        messages[activeContactId] = [];
    }
    messages[activeContactId].push(newMessage);
    
    // Update UI
    renderMessages(activeContactId);
    messageInput.value = '';
    
    // Simulate AI content moderation
    simulateAIContentModeration(text);
    
    // Simulate reply after a delay
    setTimeout(() => {
        simulateReply(activeContactId);
    }, 1000);
}

// Simulate a reply from the contact
function simulateReply(contactId) {
    const replies = [
        "That's interesting!",
        "I see what you mean.",
        "Tell me more about that.",
        "I agree with you.",
        "Thanks for letting me know!",
        "I'll get back to you on that.",
        "Can we talk about this later?",
        "I appreciate your thoughts on this."
    ];
    
    const randomReply = replies[Math.floor(Math.random() * replies.length)];
    
    const now = new Date();
    const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    const replyMessage = {
        text: randomReply,
        time,
        sender: 'contact'
    };
    
    messages[contactId].push(replyMessage);
    renderMessages(contactId);
    
    // Update contact list to show new message
    const contact = contacts.find(c => c.id == contactId);
    if (contact) {
        contact.lastMessage = randomReply;
        contact.time = time;
        contact.unread = (contact.unread || 0) + 1;
        renderContacts();
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
