/**
 * Global function for toggling named mob visibility
 * Called from the checkbox in named mob popups
 */
window.toggleMobVisibility = function(mobId, isHidden) {
    console.log(`Toggling visibility for mob ${mobId} to ${isHidden}`);
    
    fetch(`/named-mobs/visibility`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + btoa('invicta:invicta')
        },
        body: JSON.stringify({ mob_id: mobId, is_hidden: isHidden ? 1 : 0 })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(`Mob ${mobId} visibility updated: ${data.message}`);
            alert(`Mob ${mobId} is now ${isHidden ? 'hidden' : 'shown'}. Please refresh the page.`);
        } else {
            console.error('Failed to update mob visibility:', data.error);
            alert('Failed to update mob visibility: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error updating mob visibility:', error);
        alert('Error updating mob visibility: ' + error);
    });
};