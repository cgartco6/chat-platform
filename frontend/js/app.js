// Sample data for contacts and messages
const contacts = [
    { id: 1, name: "John Doe", avatar: "JD", lastMessage: "Hey, how are you?", time: "10:30 AM", unread: 3 },
    { id: 2, name: "Jane Smith", avatar: "JS", lastMessage: "See you tomorrow!", time: "Yesterday", unread: 0 },
    { id: 3, name: "Alice Johnson", avatar: "AJ", lastMessage: "Did you finish the project?", time: "Yesterday", unread: 1 },
    { id: 4, name: "Bob Williams", avatar: "BW", lastMessage: "Let's meet for coffee", time: "Wednesday", unread: 0 },
    { id: 5, name: "Eva Davis", avatar: "ED", lastMessage: "The meeting is canceled", time: "Tuesday", unread: 0 },
    { id: 6, name: "Mike Wilson", avatar: "MW", lastMessage: "Check this out!", time: "Monday", unread: 5 },
    { id: 7, name: "Sarah Brown", avatar: "SB", lastMessage: "Happy birthday! 🎉", time: "Sunday", unread: 0 },
    { id: 8, name: "Tom Taylor", avatar: "TT", lastMessage: "Call me when you're free", time: "Saturday", unread: 0 }
];

const messages = {
    1: [
        { text: "Hey there!", time: "10:15 AM", sender: "contact" },
        { text: "Hi! How are you?", time: "10:16 AM", sender: "user" },
        { text: "I'm good, thanks! How about you?", time: "10:20 AM", sender: "contact" },
        { text: "I'm doing great. What are you up to today?", time: "10:22 AM", sender: "user" },
        { text: "Just working on some projects. How about you?", time: "10:25 AM", sender: "contact" },
        { text: "Same here, just coding away! 😊", time: "10:26 AM", sender: "user" },
        { text: "That's cool! What are you working on?", time: "10:30 AM", sender: "contact" }
    ],
    2: [
        { text: "Hi Jane!", time: "09:15 AM", sender: "user" },
        { text: "Hello! How's it going?", time: "09:20 AM", sender: "contact" },
        { text: "All good. Are we still meeting tomorrow?", time: "09:22 AM", sender: "user" },
        { text: "Yes, definitely! See you at 3 PM.", time: "09:25 AM", sender: "contact" },
        { text: "Perfect! Looking forward to it.", time: "09:26 AM", sender: "user" },
        { text: "See you tomorrow!", time: "09:30 AM", sender: "contact" }
    ],
    6: [
        { text: "Check out this photo I took!", time: "09:15 AM", sender: "contact", type: "image", content: "https://picsum.photos/200/300" },
        { text: "Wow, that's beautiful! Where was this taken?", time: "09:20 AM", sender: "user" },
        { text: "At the beach last weekend. Here's another one.", time: "09:25 AM", sender: "contact", type: "image", content: "https://picsum.photos/250/300" },
        { text: "Nice! I also have a voice note for you", time: "09:30 AM", sender: "user", type: "audio", content: "voice_note.mp3", duration: "0:45" }
    ]
};

// DOM elements
const contactsContainer = document.querySelector('.contacts');
const messagesContainer = document.querySelector('.messages');
const messageInput = document.querySelector('.message-input');
const sendButton = document.querySelector('.send-button');
const attachButton = document.getElementById('attach-button');
const chatHeader = document.querySelector('.chat-header');
const chatName = document.querySelector('.chat-name');
const paymentModal = document.getElementById('payment-modal');
const closeModal = document.querySelector('.close-modal');
const creditPackages = document.querySelectorAll('.credit-package');
const paymentButton = document.querySelector('.payment-button');
const countrySelect = document.getElementById('country-select');
const appDownload = document.querySelector('.app-download');
const statusIndicators = document.querySelectorAll('.status-indicator');
const aiIndicators = document.querySelectorAll('.ai-panel .status-indicator');

// Render contacts
function renderContacts() {
    contactsContainer.innerHTML = '';
    contacts.forEach(contact => {
        const contactEl = document.createElement('div');
        contactEl.classList.add('contact');
        contactEl.dataset.id = contact.id;
        
        contactEl.innerHTML = `
            <div class="contact-avatar">${contact.avatar}</div>
            <div class="contact-info">
                <div class="contact-name">${contact.name}</div>
                <div class="contact-message">${contact.lastMessage}</div>
            </div>
            <div class="message-info">
                <div class="message-time">${contact.time}</div>
                ${contact.unread > 0 ? `<div class="message-count">${contact.unread}</div>` : ''}
            </div>
        `;
        
        contactEl.addEventListener('click', () => {
            document.querySelectorAll('.contact').forEach(c => c.classList.remove('active'));
            contactEl.classList.add('active');
            openChat(contact.id);
        });
        
        contactsContainer.appendChild(contactEl);
    });
    
    // Activate first contact by default
    if (contacts.length > 0) {
        document.querySelector(`.contact[data-id="1"]`).classList.add('active');
        openChat(1);
    }
}

// Simulate backend status changes
function simulateBackendStatus() {
    setInterval(() => {
        statusIndicators.forEach(indicator => {
            if (Math.random() > 0.8) {
                indicator.classList.toggle('offline');
            } else if (Math.random() > 0.6) {
                indicator.classList.toggle('processing');
            } else {
                indicator.classList.remove('offline', 'processing');
            }
        });
        
        // Simulate AI status
        aiIndicators.forEach(indicator => {
            if (Math.random() > 0.9) {
                indicator.classList.toggle('offline');
            } else if (Math.random() > 0.7) {
                indicator.classList.toggle('processing');
            } else {
                indicator.classList.remove('offline', 'processing');
            }
        });
    }, 5000);
}

// Event listeners
appDownload.addEventListener('click', () => {
    alert('Mobile app download starting... (simulated)');
});

// Close modal if clicked outside
window.addEventListener('click', (e) => {
    if (e.target === paymentModal) {
        paymentModal.style.display = 'none';
    }
});

// Simulate real-time updates
setInterval(() => {
    // Randomly update status of contacts
    const randomContact = contacts[Math.floor(Math.random() * contacts.length)];
    if (randomContact && Math.random() > 0.7) {
        const statuses = ['online', 'typing...', 'last seen recently'];
        const statusElement = document.querySelector('.status');
        if (statusElement) {
            statusElement.textContent = statuses[Math.floor(Math.random() * statuses.length)];
            
            // Reset after a delay
            setTimeout(() => {
                statusElement.textContent = 'online';
            }, 3000);
        }
    }
}, 8000);

// Initialize the app
renderContacts();
simulateBackendStatus();
