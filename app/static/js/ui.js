/**
 * Game UI Management
 */

let currentGameState = null;

function showScreen(screenId) {
    try {
        console.log('Showing screen:', screenId);
        
        // Hide all screens
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        
        // Show selected screen
        const targetScreen = document.getElementById(screenId);
        if (!targetScreen) {
            console.error('Screen not found:', screenId);
            return;
        }
        targetScreen.classList.add('active');
        console.log('Screen displayed:', screenId);
    } catch (error) {
        console.error('Error showing screen:', error);
    }
}

function startNewRun() {
    console.log('startNewRun() called');
    showScreen('character-screen');
}

function selectCharacter(character) {
    console.log('selectCharacter() called with:', character);
    window.selectedCharacter = character;
    showScreen('ascension-screen');
}

function showAscension() {
    console.log('showAscension() called');
    showScreen('ascension-screen');
}

function showSettings() {
    // TODO: Implement settings
    alert('Settings coming soon!');
}

function backToMenu() {
    console.log('backToMenu() called');
    showScreen('menu-screen');
}

function returnToMenu() {
    console.log('returnToMenu() called');
    showScreen('menu-screen');
}

function startRunWithAscension(ascension) {
    console.log('startRunWithAscension() called with ascension:', ascension);
    
    if (!window.selectedCharacter) {
        console.error('No character selected');
        alert('Please select a character first');
        return;
    }
    
    // Show game screen first
    showScreen('game-screen');
    
    // Then send start run event
    emitEvent('start_run', {
        character: window.selectedCharacter,
        ascension: ascension
    });
}

function updateGameUI(state) {
    currentGameState = state;
    
    console.log('updateGameUI called with state:', state);
    console.log('  phase:', state.phase);
    console.log('  game_over:', state.game_over);
    console.log('  player_won:', state.player_won);
    console.log('  current_combat:', state.current_combat ? 'yes' : 'no');
    
    try {
        // Update player stats
        const hpElement = document.getElementById('player-hp');
        const goldElement = document.getElementById('player-gold');
        const actElement = document.getElementById('current-act');
        
        if (hpElement) hpElement.textContent = state.player.hp + ' / ' + state.player.max_hp;
        if (goldElement) goldElement.textContent = state.player.gold;
        if (actElement) actElement.textContent = state.act;
        
        // Make sure game screen is visible
        const gameScreen = document.getElementById('game-screen');
        if (gameScreen && !gameScreen.classList.contains('active')) {
            gameScreen.classList.add('active');
        }
        
        // Check for game over/victory first
        if (state.game_over || state.player_won || state.phase === 'game_over' || state.phase === 'won') {
            console.log('Showing game over screen - game_over:', state.game_over, 'player_won:', state.player_won);
            showGameOverScreen(state);
        }
        // Update based on game phase
        else if (state.phase === 'map') {
            showMapView(state);
        } else if (state.phase === 'player_turn' || state.phase === 'enemy_turn' || state.phase === 'player_action' || state.phase === 'combat_end') {
            showCombatView(state);
        }
    } catch (error) {
        console.error('Error in updateGameUI:', error);
    }
}

function showMapView(state) {
    console.log('showMapView called');
    
    try {
        // Show map view, hide combat view
        const mapView = document.getElementById('map-view');
        const combatView = document.getElementById('combat-view');
        
        if (mapView) {
            mapView.classList.remove('hidden');
            mapView.classList.add('active');
        }
        if (combatView) {
            combatView.classList.add('hidden');
            combatView.classList.remove('active');
        }
        
        // Draw map
        if (state.current_map) {
            drawMap(state.current_map);
            
            // Update available nodes
            if (state.current_map.available_next) {
                updateMapNodesList(state.current_map.available_next);
            }
        }
    } catch (error) {
        console.error('Error in showMapView:', error);
    }
}

function showCombatView(state) {
    console.log('showCombatView called');
    
    try {
        // Show combat view, hide map view
        const mapView = document.getElementById('map-view');
        const combatView = document.getElementById('combat-view');
        
        if (mapView) {
            mapView.classList.add('hidden');
            mapView.classList.remove('active');
        }
        if (combatView) {
            combatView.classList.remove('hidden');
            combatView.classList.add('active');
        }
        
        // Update combat display
        if (state.current_combat) {
            updateEnemiesDisplay(state.current_combat.monsters);
            updatePlayerHand(state.current_combat.hand);
            updateCombatInfo(state.current_combat);
        }
    } catch (error) {
        console.error('Error in showCombatView:', error);
    }
}

function showGameOverScreen(state) {
    showScreen('game-over-screen');
    
    const title = state.player_won ? 'VICTORY!' : 'DEFEATED!';
    const titleColor = state.player_won ? 'green' : 'red';
    
    document.getElementById('game-over-title').textContent = title;
    document.getElementById('game-over-title').style.color = titleColor;
    
    const stats = document.getElementById('game-over-stats');
    stats.innerHTML = `
        <div><strong>Act:</strong> ${state.act}</div>
        <div><strong>Turns:</strong> ${state.run_stats.turns_taken}</div>
        <div><strong>Enemies Defeated:</strong> ${state.run_stats.enemies_defeated}</div>
        <div><strong>Gold Earned:</strong> ${state.run_stats.gold_earned}</div>
        <div><strong>Final HP:</strong> ${state.player.hp}</div>
    `;
}

function drawMap(mapState) {
    const canvas = document.getElementById('map-canvas');
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.fillStyle = '#0a0e27';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;
    const cellWidth = canvas.width / 20;
    const cellHeight = canvas.height / 15;
    
    for (let x = 0; x < canvas.width; x += cellWidth) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    
    for (let y = 0; y < canvas.height; y += cellHeight) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
    
    // Draw nodes
    if (mapState && mapState.nodes) {
        mapState.nodes.forEach(node => {
            const x = node.x * cellWidth + cellWidth / 2;
            const y = node.y * cellHeight + cellHeight / 2;
            const radius = 15;
            
            // Choose color based on type
            let color = '#d4a574'; // gold default
            if (node.type === 'combat') color = '#999';
            else if (node.type === 'elite') color = '#cc3333';
            else if (node.type === 'merchant') color = '#57a639';
            else if (node.type === 'rest') color = '#4da6ff';
            else if (node.type === 'boss') color = '#ff6600';
            
            // Draw node
            ctx.fillStyle = node.visited ? '#333' : color;
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fill();
            
            // Draw border
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.stroke();
        });
    }
}

function updateMapNodesList(availableNodes) {
    try {
        const list = document.getElementById('map-nodes-list');
        if (!list) {
            console.error('map-nodes-list element not found');
            return;
        }
        
        list.innerHTML = '';
        
        if (!availableNodes || availableNodes.length === 0) {
            list.innerHTML = '<div style="color: #999;">No nodes available</div>';
            return;
        }
        
        availableNodes.forEach(node => {
            const nodeEl = document.createElement('div');
            nodeEl.className = 'map-node-item';
            nodeEl.innerHTML = `
                <div class="map-node-type">${node.type || 'unknown'}</div>
                <div>Floor ${node.y || '?'}</div>
            `;
            nodeEl.onclick = () => moveToNode(node.id);
            list.appendChild(nodeEl);
        });
    } catch (error) {
        console.error('Error in updateMapNodesList:', error);
    }
}

function moveToNode(nodeId) {
    emitEvent('move_to_node', { node_id: nodeId });
}

function updateEnemiesDisplay(enemies) {
    try {
        const container = document.getElementById('enemies-container');
        if (!container) {
            console.error('enemies-container element not found');
            return;
        }
        
        container.innerHTML = '';
        
        if (!enemies || enemies.length === 0) {
            container.innerHTML = '<div style="color: #999;">No enemies</div>';
            return;
        }
        
        enemies.forEach(enemy => {
            const enemyEl = document.createElement('div');
            enemyEl.className = 'enemy-card';
            
            const hpPercent = Math.round((enemy.hp / enemy.max_hp) * 100);
            const hpBarWidth = Math.max(0, hpPercent);
            
            enemyEl.innerHTML = `
                <div class="enemy-name">${enemy.name || 'Unknown'}</div>
                <div class="enemy-hp">
                    <div>HP: ${enemy.hp}/${enemy.max_hp}</div>
                    <div class="enemy-hp-bar">
                        <div class="enemy-hp-fill" style="width: ${hpBarWidth}%"></div>
                    </div>
                </div>
                ${enemy.block > 0 ? `<div style="color: #4da6ff;">🛡️ Block: ${enemy.block}</div>` : ''}
                <div class="enemy-intent">
                    <div class="enemy-intent-label">Next Action:</div>
                    <div class="enemy-intent-value">${enemy.intent || '?'}</div>
                </div>
            `;
            
            container.appendChild(enemyEl);
        });
    } catch (error) {
        console.error('Error in updateEnemiesDisplay:', error);
    }
}

function updatePlayerHand(hand) {
    try {
        const handEl = document.getElementById('player-hand');
        if (!handEl) {
            console.error('player-hand element not found');
            return;
        }
        
        handEl.innerHTML = '';
        
        if (!hand || hand.length === 0) {
            handEl.innerHTML = '<div style="color: #999;">No cards in hand</div>';
            return;
        }
        
        hand.forEach((card, index) => {
            const cardEl = document.createElement('div');
            cardEl.className = 'card-in-hand';
            
            const energyEl = document.getElementById('current-energy');
            const currentEnergy = energyEl ? parseInt(energyEl.textContent) : 0;
            const canPlay = currentEnergy >= card.cost;
            
            let cardType = card.type || 'power';
            let cardTypeColor = '#d4a574';
            if (cardType === 'attack') cardTypeColor = '#e74c5c';
            else if (cardType === 'skill') cardTypeColor = '#57a639';
            else if (cardType === 'power') cardTypeColor = '#9d4edd';
            
            cardEl.innerHTML = `
                <div class="card-name">${card.name || 'Card'}</div>
                <div class="card-type" style="color: ${cardTypeColor};">${cardType}</div>
                <div class="card-cost ${!canPlay ? 'unavailable' : ''}">${card.cost}</div>
            `;
            
            if (!canPlay) {
                cardEl.classList.add('unavailable');
            }
            
            cardEl.onclick = () => {
                if (canPlay) {
                    playCard(index);
                } else {
                    showNotification('Not enough energy', 'error');
                }
            };
            
            handEl.appendChild(cardEl);
        });
    } catch (error) {
        console.error('Error in updatePlayerHand:', error);
    }
}

function updateCombatInfo(combat) {
    try {
        const turnEl = document.getElementById('turn-number');
        const energyEl = document.getElementById('current-energy');
        const maxEnergyEl = document.getElementById('max-energy');
        const drawEl = document.getElementById('draw-pile');
        const discardEl = document.getElementById('discard-pile');
        
        if (turnEl) turnEl.textContent = (combat.turn || 1);
        if (energyEl) energyEl.textContent = (combat.player_energy !== undefined ? combat.player_energy : 0);
        if (maxEnergyEl) maxEnergyEl.textContent = (combat.max_energy || 3);
        if (drawEl) drawEl.textContent = (combat.draw_pile_size || 0);
        if (discardEl) discardEl.textContent = (combat.discard_pile_size || 0);
    } catch (error) {
        console.error('Error in updateCombatInfo:', error);
    }
}

function playCard(cardIndex) {
    emitEvent('play_card', { card_index: cardIndex, target_idx: 0 });
}

function endTurn() {
    emitEvent('end_turn', {});
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired');
    try {
        initializeSocket();
        showScreen('menu-screen');
        console.log('✓ UI Initialized successfully');
    } catch (error) {
        console.error('✗ Error during initialization:', error);
    }
});
