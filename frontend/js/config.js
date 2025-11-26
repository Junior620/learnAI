// Configuration de l'API
const API_CONFIG = {
    // URL de production sur Render
    PRODUCTION_URL: 'https://learnai-2dnf.onrender.com/api',
    
    // URL de développement local
    DEVELOPMENT_URL: 'http://localhost:5000/api',
    
    // Détection automatique de l'environnement
    get BASE_URL() {
        // TEMPORAIRE: Forcer l'URL de production pour tester
        // Décommenter les lignes ci-dessous pour revenir au mode auto
        return this.PRODUCTION_URL;
        
        // Si on est sur localhost, utiliser l'URL de développement
        // if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        //     return this.DEVELOPMENT_URL;
        // }
        // // Sinon, utiliser l'URL de production
        // return this.PRODUCTION_URL;
    }
};

// Export de l'URL de base pour utilisation dans les autres fichiers
const API_URL = API_CONFIG.BASE_URL;
