/**
 * WebSocket Connection Management
 */

let socket = null;
let sessionId = null;

function initializeSocket() {
    console.log('initializeSocket() called');
    socket = io();
    
    socket.on('connect', () => {
        console.log('✓ Connected to server');
    });
    
    socket.on('session_created', (data) => {
        sessionId = data.session_id;
        console.log('✓ Session created:', sessionId);
    });
    
    socket.on('game_state', (state) => {
        console.log('✓ Game state received:', state);
        if (typeof updateGameUI === 'function') {
            updateGameUI(state);
        } else {
            console.error('updateGameUI function not found');
        }
    });
    
    socket.on('action_result', (result) => {
        console.log('✓ Action result:', result);
        if (!result.success) {
            showNotification(result.message, 'error');
        }
    });
    
    socket.on('error', (error) => {
        console.error('✗ Server error:', error.message);
        showNotification(error.message, 'error');
    });
    
    socket.on('disconnect', () => {
        console.log('✗ Disconnected from server');
    });
}

function emitEvent(eventName, data) {
    if (socket && socket.connected) {
        console.log(`→ Emitting event: ${eventName}`, data);
        data.session_id = sessionId;
        socket.emit(eventName, data);
    } else {
        console.error('✗ Socket not connected or not initialized');
    }
}

function showNotification(message, type = 'info') {
    console.log(`Notification (${type}): ${message}`);
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.background = type === 'error' ? '#e74c5c' : '#57a639';
    notification.style.color = 'white';
    notification.style.padding = '10px 20px';
    notification.style.borderRadius = '4px';
    notification.style.zIndex = '9999';
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
