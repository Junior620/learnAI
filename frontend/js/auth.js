// Gestion de l'authentification
const API_URL = 'http://localhost:5000/api';

// Fonction de connexion
async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Sauvegarder le token et les infos utilisateur
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            return { success: true, user: data.user };
        } else {
            return { success: false, message: data.error || 'Erreur de connexion' };
        }
    } catch (error) {
        console.error('Erreur:', error);
        return { success: false, message: 'Erreur de connexion au serveur' };
    }
}

// Fonction d'inscription
async function register(formData) {
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            return { success: true, message: 'Inscription réussie' };
        } else {
            return { success: false, message: data.error || 'Erreur d\'inscription' };
        }
    } catch (error) {
        console.error('Erreur:', error);
        return { success: false, message: 'Erreur de connexion au serveur' };
    }
}

// Fonction de déconnexion
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

// Vérifier si l'utilisateur est connecté
function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

// Récupérer le token
function getToken() {
    return localStorage.getItem('token');
}

// Récupérer l'utilisateur
function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

// Faire une requête authentifiée
async function authenticatedFetch(url, options = {}) {
    const token = getToken();
    
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };

    try {
        const response = await fetch(url, { ...options, headers });
        
        if (response.status === 401) {
            logout();
            return;
        }

        return response;
    } catch (error) {
        console.error('Erreur:', error);
        throw error;
    }
}

// Vérifier l'authentification et rediriger si nécessaire
function checkAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}
