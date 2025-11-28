// Gestion des paramètres utilisateur

// Charger le profil au démarrage
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadNavigationMenu();
    loadUserProfile();
    loadPreferences();
});

// Charger le menu de navigation selon le rôle
function loadNavigationMenu() {
    const user = JSON.parse(localStorage.getItem('user'));
    const navMenu = document.getElementById('navMenu');
    
    if (!user) return;
    
    let menuHTML = '';
    
    if (user.role === 'student') {
        menuHTML = `
            <li><a href="dashboard-student.html">Tableau de bord</a></li>
            <li><a href="grades.html">Notes</a></li>
            <li><a href="recommendations.html">Recommandations</a></li>
            <li><a href="chatbot.html">Assistant IA</a></li>
            <li><a href="settings.html" class="active">Paramètres</a></li>
            <li><a href="#" onclick="logout()">Déconnexion</a></li>
        `;
    } else if (user.role === 'teacher') {
        menuHTML = `
            <li><a href="dashboard-teacher.html">Tableau de bord</a></li>
            <li><a href="add-grade.html">Ajouter une Note</a></li>
            <li><a href="chatbot.html">Assistant IA</a></li>
            <li><a href="settings.html" class="active">Paramètres</a></li>
            <li><a href="#" onclick="logout()">Déconnexion</a></li>
        `;
    }
    
    navMenu.innerHTML = menuHTML;
}

// Basculer entre les onglets
function switchTab(tabName) {
    // Désactiver tous les onglets
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    // Activer l'onglet sélectionné
    event.target.classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Charger le profil utilisateur
async function loadUserProfile() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/auth/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            const user = data.user;

            // Remplir les champs du formulaire
            document.getElementById('firstName').value = user.first_name || '';
            document.getElementById('lastName').value = user.last_name || '';
            document.getElementById('email').value = user.email || '';

            // Afficher les initiales
            const initials = (user.first_name?.[0] || '') + (user.last_name?.[0] || '');
            document.getElementById('avatar-initials').textContent = initials.toUpperCase();

            // Afficher le rôle
            const roleText = user.role === 'student' ? 'Étudiant' : 
                           user.role === 'teacher' ? 'Enseignant' : 'Administrateur';
            document.getElementById('user-role-display').textContent = roleText;

            // Si étudiant, charger le profil étudiant
            if (user.role === 'student') {
                document.getElementById('student-fields').style.display = 'block';
                await loadStudentProfile(user.id);
            } else {
                // Masquer les champs étudiants pour les enseignants
                document.getElementById('student-fields').style.display = 'none';
            }
        }
    } catch (error) {
        console.error('Erreur chargement profil:', error);
        showAlert('Erreur lors du chargement du profil', 'danger');
    }
}

// Charger le profil étudiant
async function loadStudentProfile(userId) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/students/${userId}/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            const profile = data.profile;

            if (profile) {
                document.getElementById('studentId').value = profile.student_id || '';
                document.getElementById('department').value = profile.department || '';
                document.getElementById('level').value = profile.level || '';
                document.getElementById('academicYear').value = profile.academic_year || '';
            }
        }
    } catch (error) {
        console.error('Erreur chargement profil étudiant:', error);
    }
}

// Soumettre le formulaire de profil
document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('token');
    const userData = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value
    };

    // Si étudiant, ajouter les infos du profil
    const studentFields = document.getElementById('student-fields');
    if (studentFields.style.display !== 'none') {
        userData.student_profile = {
            student_id: document.getElementById('studentId').value,
            department: document.getElementById('department').value,
            level: document.getElementById('level').value,
            academic_year: document.getElementById('academicYear').value
        };
    }

    try {
        const response = await fetch(`${API_URL}/auth/profile`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (response.ok) {
            showAlert('✅ Profil mis à jour avec succès !', 'success');
            loadUserProfile(); // Recharger le profil
        } else {
            showAlert(data.message || 'Erreur lors de la mise à jour', 'danger');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showAlert('Erreur lors de la mise à jour du profil', 'danger');
    }
});

// Soumettre le formulaire de changement de mot de passe
document.getElementById('passwordForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Vérifier que les mots de passe correspondent
    if (newPassword !== confirmPassword) {
        showAlert('Les mots de passe ne correspondent pas', 'danger');
        return;
    }

    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`${API_URL}/auth/change-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert('✅ Mot de passe changé avec succès !', 'success');
            document.getElementById('passwordForm').reset();
        } else {
            showAlert(data.message || 'Erreur lors du changement de mot de passe', 'danger');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showAlert('Erreur lors du changement de mot de passe', 'danger');
    }
});

// Charger les préférences
function loadPreferences() {
    const darkMode = localStorage.getItem('darkMode') === 'true';
    const language = localStorage.getItem('language') || 'fr';
    const emailNotifications = localStorage.getItem('emailNotifications') !== 'false';
    const gradeAlerts = localStorage.getItem('gradeAlerts') !== 'false';
    const recommendationAlerts = localStorage.getItem('recommendationAlerts') !== 'false';

    document.getElementById('darkMode').checked = darkMode;
    document.getElementById('language').value = language;
    document.getElementById('emailNotifications').checked = emailNotifications;
    document.getElementById('gradeAlerts').checked = gradeAlerts;
    document.getElementById('recommendationAlerts').checked = recommendationAlerts;

    // Appliquer le mode sombre si activé
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }
}

// Sauvegarder les préférences
function savePreferences() {
    const darkMode = document.getElementById('darkMode').checked;
    const language = document.getElementById('language').value;
    const emailNotifications = document.getElementById('emailNotifications').checked;
    const gradeAlerts = document.getElementById('gradeAlerts').checked;
    const recommendationAlerts = document.getElementById('recommendationAlerts').checked;

    localStorage.setItem('darkMode', darkMode);
    localStorage.setItem('language', language);
    localStorage.setItem('emailNotifications', emailNotifications);
    localStorage.setItem('gradeAlerts', gradeAlerts);
    localStorage.setItem('recommendationAlerts', recommendationAlerts);

    // Appliquer le mode sombre
    if (darkMode) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }

    showAlert('✅ Préférences enregistrées !', 'success');
}

// Confirmer la suppression du compte
function confirmDeleteAccount() {
    const confirmed = confirm(
        '⚠️ ATTENTION !\n\n' +
        'Êtes-vous sûr de vouloir supprimer votre compte ?\n' +
        'Cette action est IRRÉVERSIBLE et toutes vos données seront perdues.\n\n' +
        'Cliquez sur OK pour confirmer la suppression.'
    );

    if (confirmed) {
        deleteAccount();
    }
}

// Supprimer le compte
async function deleteAccount() {
    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`${API_URL}/auth/delete-account`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            alert('Votre compte a été supprimé.');
            logout();
        } else {
            const data = await response.json();
            showAlert(data.message || 'Erreur lors de la suppression', 'danger');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showAlert('Erreur lors de la suppression du compte', 'danger');
    }
}

// Afficher une alerte
function showAlert(message, type) {
    const alertContainer = document.getElementById('alert-container');
    alertContainer.innerHTML = `
        <div class="alert alert-${type}" style="margin-bottom: 20px;">
            ${message}
        </div>
    `;

    // Faire disparaître après 5 secondes
    setTimeout(() => {
        alertContainer.innerHTML = '';
    }, 5000);
}

