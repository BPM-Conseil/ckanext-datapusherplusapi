# CKAN Extension: Datapusher Plus API

Extension CKAN qui fournit une API REST pour soumettre des fichiers au service datapusher plus.

## Compatibilité

- CKAN 2.9.x
- Python 3.7+

## Installation

1. Cloner ou copier l'extension dans votre environnement CKAN :
```bash
cd /usr/lib/ckan/default/src/
git clone https://github.com/your-org/ckanext-datapusherplusapi.git
```

2. Installer l'extension :
```bash
cd ckanext-datapusherplusapi
pip install -e .
```

3. Ajouter `datapusherplusapi` à la liste des plugins dans votre fichier de configuration CKAN :
```ini
ckan.plugins = ... datapusherplusapi
```

4. Redémarrer CKAN

## Configuration

Ajoutez ces paramètres à votre fichier de configuration CKAN :

```ini
# URL du service datapusher plus (obligatoire)
ckanext.datapusher_plus.url = http://datapusher-plus:8000

# Timeout pour les requêtes en secondes (optionnel, défaut: 30)
ckanext.datapusher_plus.timeout = 30

# Nombre maximum de tentatives (optionnel, défaut: 3)
ckanext.datapusher_plus.max_retries = 3

# Taille maximum des fichiers en MB (optionnel, défaut: 100)
ckanext.datapusher_plus.max_file_size = 100

# Activer les logs détaillés (optionnel, défaut: False)
ckanext.datapusher_plus.debug = True
```

## Utilisation de l'API

### Soumettre un fichier au datapusher plus

**Endpoint :** `POST /api/3/action/datapusher_plus_submit`

**Paramètres :**
- `resource_id` (obligatoire) : ID de la ressource CKAN
- `package_id` (optionnel) : ID du package CKAN
- `force` (optionnel) : Forcer la soumission même si déjà en cours (défaut: false)

**Exemple de requête :**
```bash
curl -X POST "http://your-ckan-site/api/3/action/datapusher_plus_submit" \
  -H "Content-Type: application/json" \
  -H "Authorization: your-api-key" \
  -d '{
    "resource_id": "12345678-1234-1234-1234-123456789012",
    "force": false
  }'
```

**Réponse en cas de succès :**
```json
{
  "success": true,
  "message": "Fichier soumis avec succès au datapusher plus",
  "job_id": "job-12345",
  "resource_id": "12345678-1234-1234-1234-123456789012"
}
```

**Réponse en cas d'erreur :**
```json
{
  "success": false,
  "error": "Description de l'erreur"
}
```

### Récupérer le statut de traitement

**Endpoint :** `GET /api/3/action/datapusher_plus_status/{resource_id}`

**Exemple de requête :**
```bash
curl "http://your-ckan-site/api/3/action/datapusher_plus_status/12345678-1234-1234-1234-123456789012" \
  -H "Authorization: your-api-key"
```

**Réponse :**
```json
{
  "success": true,
  "resource_id": "12345678-1234-1234-1234-123456789012",
  "status": "submitted",
  "submitted": "2024-01-15T10:30:00",
  "resource_url": "http://example.com/data.csv"
}
```

## Formats de fichiers supportés

Par défaut, les formats suivants sont supportés :
- CSV
- TSV
- XLS
- XLSX
- ODS
- JSON
- XML

## Authentification

L'API utilise le système d'authentification CKAN standard. Vous devez :
1. Être connecté en tant qu'utilisateur autorisé
2. Ou fournir une clé API valide dans l'en-tête `Authorization`

## Gestion des erreurs

L'API retourne les codes d'erreur HTTP standard :
- `200` : Succès
- `400` : Paramètres invalides
- `403` : Non autorisé
- `404` : Ressource non trouvée
- `500` : Erreur interne du serveur

## Développement

### Tests

Pour exécuter les tests :
```bash
pytest ckanext/datapusherplusapi/tests/
```

### Structure du projet

```
ckanext-datapusherplusapi/
├── ckanext/
│   └── datapusherplusapi/
│       ├── __init__.py
│       ├── plugin.py          # Plugin principal
│       ├── views.py           # Endpoints API
│       ├── config.py          # Configuration
│       ├── helpers.py         # Fonctions utilitaires
│       └── tests/
│           ├── __init__.py
│           └── test_api.py    # Tests unitaires
├── setup.py
└── README.md
```

## Dépendances

- CKAN >= 2.9.0
- requests
- flask

## Licence

AGPL v3

## Support

Pour signaler des bugs ou demander des fonctionnalités, veuillez créer une issue sur le dépôt GitHub du projet.
