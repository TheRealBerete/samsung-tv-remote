/**
 * Samsung TV Remote Pro - Frontend JavaScript
 * Gère les interactions avec l'API du backend
 */

const API_BASE = '';

/**
 * Envoyer une touche de télécommande
 * @param {string} key - Code de la touche (ex: KEY_UP)
 */
async function sendKey(key) {
    try {
        const response = await fetch(`${API_BASE}/key/${key}`);
        const data = await response.json();

        if (data.success) {
            // Vibration haptique si disponible
            if (navigator.vibrate) {
                navigator.vibrate(15);
            }
            console.log(`✅ Touche envoyée : ${key}`);
        } else {
            console.error(`❌ Échec : ${key}`);
        }
    } catch (error) {
        console.error('Erreur lors de l\'envoi de la touche:', error);
    }
}

/**
 * Lancer une application sur la TV
 * @param {string} appName - Nom de l'application (ex: NETFLIX)
 */
async function launchApp(appName) {
    try {
        const response = await fetch(`${API_BASE}/app/${appName}`);
        const data = await response.json();

        if (data.success) {
            // Vibration plus longue pour la confirmation
            if (navigator.vibrate) {
                navigator.vibrate([15, 10, 15]);
            }
            console.log(`✅ Lancement de ${appName} (${data.app_id})`);
        } else {
            console.error(`❌ Échec : ${data.error}`);
        }
    } catch (error) {
        console.error('Erreur lors du lancement de l\'app:', error);
    }
}

/**
 * Mettre à jour le statut de la TV
 */
async function updateStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        console.log('État de la TV:', data);
        
        // Mettre à jour l'interface selon le statut
        const statusEl = document.querySelector('.status');
        if (data.status === 'online') {
            statusEl.style.opacity = '1';
        } else {
            statusEl.style.opacity = '0.5';
        }
    } catch (error) {
        console.warn('Impossible de vérifier le statut:', error);
    }
}

/**
 * Initialiser l'application
 */
function init() {
    // Enregistrer les événements click sur les boutons de navigation
    document.querySelectorAll('[data-key]').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const key = button.getAttribute('data-key');
            sendKey(key);
        });
    });

    // Enregistrer les événements click sur les boutons d'applications
    document.querySelectorAll('[data-app]').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const appName = button.getAttribute('data-app');
            launchApp(appName);
        });
    });

    // Mettre à jour le statut au démarrage et périodiquement
    updateStatus();
    setInterval(updateStatus, 30000); // Toutes les 30 secondes

    console.log('🎮 Samsung TV Remote Pro - Initialisée');
}

// Initialiser quand le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
