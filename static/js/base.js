// Add your base JavaScript here
document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById('chatToggle');
    const chatPanel = document.getElementById('chatPanel');
    const closeChatBtn = document.getElementById('closeChatBtn');

    chatToggle.addEventListener('click', function() {
        chatPanel.classList.toggle('open');
    });

    closeChatBtn.addEventListener('click', function() {
        chatPanel.classList.remove('open');
    });

    // Add more functionality as needed
});
