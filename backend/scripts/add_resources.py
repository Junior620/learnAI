#!/usr/bin/env python3
"""
Script pour ajouter des ressources pédagogiques dans la base de données
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import Database

def add_resources():
    """Ajoute des ressources pédagogiques pour chaque matière"""
    
    # Récupérer les matières
    subjects_query = "SELECT id, name, code FROM subjects ORDER BY id"
    subjects = Database.execute_query(subjects_query, fetch=True)
    
    if not subjects:
        print("❌ Aucune matière trouvée dans la base de données")
        return
    
    resources_data = []
    
    for subject in subjects:
        subject_id = subject['id']
        subject_name = subject['name']
        
        # Ressources pour chaque matière
        resources_data.extend([
            # Niveau Débutant
            {
                'title': f'Introduction à {subject_name}',
                'description': f'Cours complet pour débuter en {subject_name}. Couvre tous les concepts de base avec des exemples pratiques.',
                'resource_type': 'pdf',
                'url': f'https://example.com/cours/{subject_name.lower().replace(" ", "-")}-debutant.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'beginner'
            },
            {
                'title': f'Tutoriel vidéo {subject_name} - Les bases',
                'description': f'Série de vidéos pour comprendre les fondamentaux de {subject_name}. Durée: 2h30.',
                'resource_type': 'video',
                'url': f'https://youtube.com/watch?v={subject_name[:5]}',
                'subject_id': subject_id,
                'difficulty_level': 'beginner'
            },
            {
                'title': f'Exercices de base en {subject_name}',
                'description': f'50 exercices corrigés pour maîtriser les bases de {subject_name}.',
                'resource_type': 'exercise',
                'url': f'https://example.com/exercices/{subject_name.lower().replace(" ", "-")}-base.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'beginner'
            },
            
            # Niveau Intermédiaire
            {
                'title': f'{subject_name} - Niveau intermédiaire',
                'description': f'Approfondissez vos connaissances en {subject_name} avec ce cours avancé.',
                'resource_type': 'pdf',
                'url': f'https://example.com/cours/{subject_name.lower().replace(" ", "-")}-intermediaire.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'intermediate'
            },
            {
                'title': f'Problèmes résolus en {subject_name}',
                'description': f'Collection de problèmes types avec solutions détaillées en {subject_name}.',
                'resource_type': 'exercise',
                'url': f'https://example.com/exercices/{subject_name.lower().replace(" ", "-")}-intermediaire.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'intermediate'
            },
            
            # Niveau Avancé
            {
                'title': f'{subject_name} avancé - Préparation examens',
                'description': f'Ressources avancées pour exceller en {subject_name}. Sujets d\'examens corrigés.',
                'resource_type': 'pdf',
                'url': f'https://example.com/cours/{subject_name.lower().replace(" ", "-")}-avance.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'advanced'
            },
            {
                'title': f'Projet pratique en {subject_name}',
                'description': f'Projet complet pour mettre en pratique vos compétences en {subject_name}.',
                'resource_type': 'exercise',
                'url': f'https://example.com/projets/{subject_name.lower().replace(" ", "-")}-projet.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'advanced'
            }
        ])
    
    # Ajouter des ressources générales
    resources_data.extend([
        {
            'title': 'Méthodes de travail efficaces',
            'description': 'Guide complet pour améliorer vos méthodes de travail et votre organisation.',
            'resource_type': 'article',
            'url': 'https://example.com/methodes-travail.html',
            'subject_id': None,
            'difficulty_level': None
        },
        {
            'title': 'Gestion du stress aux examens',
            'description': 'Techniques pour gérer le stress et optimiser vos performances aux examens.',
            'resource_type': 'article',
            'url': 'https://example.com/gestion-stress.html',
            'subject_id': None,
            'difficulty_level': None
        },
        {
            'title': 'Techniques de mémorisation',
            'description': 'Méthodes scientifiquement prouvées pour améliorer votre mémoire.',
            'resource_type': 'video',
            'url': 'https://youtube.com/watch?v=memorisation',
            'subject_id': None,
            'difficulty_level': None
        }
    ])
    
    # Insérer les ressources
    insert_query = """
        INSERT INTO resources (title, description, resource_type, url, subject_id, difficulty_level)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """
    
    count = 0
    for resource in resources_data:
        try:
            Database.execute_query(
                insert_query,
                (
                    resource['title'],
                    resource['description'],
                    resource['resource_type'],
                    resource['url'],
                    resource['subject_id'],
                    resource['difficulty_level']
                )
            )
            count += 1
        except Exception as e:
            print(f"⚠️ Erreur lors de l'ajout de '{resource['title']}': {e}")
    
    print(f"✅ {count} ressources ajoutées avec succès !")
    print(f"📚 Total de ressources par matière: {len(subjects) * 7}")
    print(f"📚 Ressources générales: 3")
    print(f"📚 Total: {count}")

if __name__ == '__main__':
    print("🚀 Ajout des ressources pédagogiques...")
    add_resources()
    print("✅ Terminé !")
