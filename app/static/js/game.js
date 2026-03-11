/**
 * Game Logic and State Management
 */

// Game loop and state management handled primarily on server side
// This file contains client-side game logic and validation

class ClientGameState {
    constructor() {
        this.state = null;
        this.selectedCard = null;
    }
    
    updateState(newState) {
        this.state = newState;
    }
    
    isPlayerTurn() {
        return this.state && this.state.current_combat && 
               this.state.current_combat.phase === 'player_turn';
    }
    
    getAvailableCards() {
        if (!this.state || !this.state.current_combat) return [];
        
        const energy = this.state.current_combat.player_energy;
        return this.state.current_combat.hand.filter(card => card.cost <= energy);
    }
    
    canPlayCard(cardIndex) {
        if (!this.isPlayerTurn()) return false;
        
        const hand = this.state.current_combat.hand;
        if (cardIndex >= hand.length) return false;
        
        const card = hand[cardIndex];
        const energy = this.state.current_combat.player_energy;
        
        return card.cost <= energy;
    }
}

const gameState = new ClientGameState();

// Update game state when receiving from server
function updateGameState(state) {
    gameState.updateState(state);
    updateGameUI(state);
}

// Validation helpers
function validateCardPlay(cardIndex) {
    if (!gameState.canPlayCard(cardIndex)) {
        showNotification('Cannot play this card', 'error');
        return false;
    }
    return true;
}

function validateTurnEnd() {
    if (!gameState.isPlayerTurn()) {
        showNotification('Not your turn', 'error');
        return false;
    }
    return true;
}

// Override the updateGameUI from ui.js to use gameState
const originalUpdateGameUI = window.updateGameUI;
window.updateGameUI = function(state) {
    gameState.updateState(state);
    originalUpdateGameUI(state);
};

// Add keyboard shortcuts
document.addEventListener('keydown', (event) => {
    // Number keys 1-9 for card selection
    if (event.key >= '0' && event.key <= '9') {
        const cardIndex = parseInt(event.key) - 1;
        if (cardIndex < gameState.state?.current_combat?.hand?.length) {
            playCard(cardIndex);
        }
    }
    
    // Space or E for end turn
    if (event.key === ' ' || event.key.toLowerCase() === 'e') {
        event.preventDefault();
        if (validateTurnEnd()) {
            endTurn();
        }
    }
});
