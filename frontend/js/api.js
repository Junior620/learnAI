// Fonctions API pour l'application
// Note: API_URL est défini dans auth.js

// Dashboard étudiant
async function getStudentDashboard() {
    const response = await authenticatedFetch(`${API_URL}/student/dashboard`);
    return await response.json();
}

// Prédictions
async function getPredictions() {
    const response = await authenticatedFetch(`${API_URL}/student/predictions`);
    return await response.json();
}

// Recommandations
async function getRecommendations() {
    const response = await authenticatedFetch(`${API_URL}/student/recommendations`);
    return await response.json();
}

// Dashboard enseignant
async function getTeacherDashboard() {
    const response = await authenticatedFetch(`${API_URL}/teacher/dashboard`);
    return await response.json();
}

// Liste des étudiants
async function getStudents() {
    const response = await authenticatedFetch(`${API_URL}/teacher/students`);
    return await response.json();
}

// Performance d'un étudiant
async function getStudentPerformance(studentId) {
    const response = await authenticatedFetch(`${API_URL}/teacher/student/${studentId}/performance`);
    return await response.json();
}

// Chatbot
async function sendChatMessage(message) {
    const response = await authenticatedFetch(`${API_URL}/chatbot/message`, {
        method: 'POST',
        body: JSON.stringify({ message })
    });
    return await response.json();
}

// Historique chatbot
async function getChatHistory() {
    const response = await authenticatedFetch(`${API_URL}/chatbot/history`);
    return await response.json();
}

// Matières
async function getSubjects() {
    const response = await authenticatedFetch(`${API_URL}/teacher/subjects`);
    return await response.json();
}

// Ajouter une note
async function addGrade(data) {
    const response = await authenticatedFetch(`${API_URL}/teacher/grade`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    return await response.json();
}
