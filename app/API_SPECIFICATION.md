# Borne Appétit - Spécification API

## Base URL

```
https://{api-gateway-url}
```

L'URL de l'API Gateway sera fournie après le déploiement Terraform.

---

## Endpoints

### 1. Health Check

Vérifie que l'API est opérationnelle.

**Endpoint**
```
GET /health
```

**Réponse (200 OK)**
```json
{
  "status": "healthy"
}
```

---

### 2. Configuration Terminal

Récupère la configuration complète d'un terminal (terminal + restaurant associé).

**Endpoint**
```
GET /terminal/config/{uuid}
```

**Paramètres**
- `uuid` (path) : UUID du terminal

**Réponse (200 OK)**
```json
{
  "terminal": {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "restaurant_uuid": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Terminal Principal",
    "location": "Entrée"
  },
  "restaurant": {
    "uuid": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Le Gourmet",
    "uri_name": "le-gourmet",
    "logo": "https://cloudfront-url/logos/le-gourmet.png",
    "favicon": "https://cloudfront-url/favicons/le-gourmet.ico",
    "welcome_image": "https://cloudfront-url/welcome/le-gourmet.jpg",
    "primary_color": "#FF6B35",
    "secondary_color": "#004E89"
  }
}
```

**Réponse (404 Not Found)**
```json
{
  "error": "Terminal not found"
}
```

---

### 3. Configuration Restaurant

Récupère la configuration d'un restaurant via son URI.

**Endpoint**
```
GET /restaurant/{uri}/config
```

**Paramètres**
- `uri` (path) : URI du restaurant (ex: "le-gourmet")

**Réponse (200 OK)**
```json
{
  "uuid": "660e8400-e29b-41d4-a716-446655440001",
  "name": "Le Gourmet",
  "uri_name": "le-gourmet",
  "logo": "https://cloudfront-url/logos/le-gourmet.png",
  "favicon": "https://cloudfront-url/favicons/le-gourmet.ico",
  "welcome_image": "https://cloudfront-url/welcome/le-gourmet.jpg",
  "primary_color": "#FF6B35",
  "secondary_color": "#004E89"
}
```

**Réponse (404 Not Found)**
```json
{
  "error": "Restaurant not found"
}
```

---

### 4. Refresh Token Terminal

Génère un token JWT pour authentifier un terminal (valide 24h).

**Endpoint**
```
POST /terminal/refresh-token
```

**Body**
```json
{
  "terminal_uuid": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Réponse (200 OK)**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400
}
```

**Réponses d'erreur**
- `400` : Terminal UUID manquant
- `404` : Terminal non trouvé
- `500` : Configuration JWT manquante

---

### 5. Recherche Client par Code Fidélité

Récupère les informations d'un client via son code de fidélité.

**Endpoint**
```
GET /restaurant/{restaurant_uuid}/customer?loyaltyCode={code}
```

**Paramètres**
- `restaurant_uuid` (path) : UUID du restaurant
- `loyaltyCode` (query) : Code de fidélité du client

**Réponse (200 OK)**
```json
{
  "customer_id": "cust_123456",
  "email": "client@example.com",
  "loyalty_code": "ABC123",
  "points": 150,
  "restaurant_uuid": "660e8400-e29b-41d4-a716-446655440001"
}
```

**Réponses d'erreur**
- `400` : loyaltyCode requis
- `404` : Customer not found

---

### 6. Envoi Carte de Fidélité

Crée un client et envoie sa carte de fidélité Google Wallet par email.

**Endpoint**
```
POST /send-loyalty-card
```

**Headers**
```
Authorization: Bearer {jwt_token}
```

**Body**
```json
{
  "email": "client@example.com"
}
```

**Réponse (200 OK)**
```json
{
  "message": "Email envoyé avec succès",
  "customer_id": "cust_123456",
  "loyalty_code": "ABC123",
  "wallet_url": "https://pay.google.com/gp/v/save/..."
}
```

**Réponses d'erreur**
- `400` : Email requis
- `401` : Token manquant, expiré ou invalide
- `500` : Échec envoi email

---

### 7. Mise à Jour Points Fidélité

Met à jour les points de fidélité d'un client (DynamoDB + Google Wallet).

**Endpoint**
```
PATCH /customer/{customer_id}/points
```

**Headers**
```
Authorization: Bearer {jwt_token}
```

**Paramètres**
- `customer_id` (path) : ID du client

**Body**
```json
{
  "points": 200
}
```

**Réponse (200 OK)**
```json
{
  "message": "Points mis à jour avec succès",
  "customer_id": "cust_123456",
  "points": 200
}
```

**Réponses d'erreur**
- `400` : customer_id et points requis
- `401` : Token invalide
- `404` : Objet Wallet introuvable

---

### 8. Création Classe Google Wallet

Crée ou met à jour une classe de fidélité Google Wallet pour un restaurant.

**Endpoint**
```
POST /wallet/class/{restaurant_id}
```

**Paramètres**
- `restaurant_id` (path) : UUID du restaurant

**Réponse (200 OK)**
```json
{
  "message": "Classe créée avec succès",
  "class_id": "3388000000022345678.le-gourmet_loyalty_v2"
}
```

**Réponses d'erreur**
- `400` : Restaurant ID requis
- `404` : Restaurant introuvable

---

## Types de données

### Terminal
| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| uuid | string | Oui | Identifiant unique du terminal |
| restaurant_uuid | string | Oui | UUID du restaurant associé |
| name | string | Oui | Nom du terminal |
| location | string | Non | Localisation physique du terminal |

### Restaurant
| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| uuid | string | Oui | Identifiant unique du restaurant |
| name | string | Oui | Nom du restaurant |
| uri_name | string | Oui | URI du restaurant (slug) |
| logo | string | Non | URL du logo |
| favicon | string | Non | URL du favicon |
| welcome_image | string | Non | URL de l'image d'accueil |
| primary_color | string | Non | Couleur primaire (hex) |
| secondary_color | string | Non | Couleur secondaire (hex) |

### Customer
| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| customer_id | string | Oui | Identifiant unique du client |
| email | string | Oui | Email du client |
| loyalty_code | string | Oui | Code de fidélité unique |
| points | integer | Oui | Nombre de points de fidélité |
| restaurant_uuid | string | Oui | UUID du restaurant associé |

---

## CORS

L'API est configurée avec CORS pour accepter les requêtes depuis n'importe quelle origine.

**Headers autorisés :**
- `Content-Type`
- `Authorization`

**Méthodes autorisées :**
- `GET`
- `POST`
- `PUT`
- `DELETE`
- `OPTIONS`

---

## Codes d'erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 404 | Ressource non trouvée |
| 500 | Erreur serveur |

---

## Notes d'implémentation

1. **Assets statiques** : Les URLs des images (logo, favicon, welcome_image) pointent vers CloudFront
2. **UUID** : Tous les identifiants sont au format UUID v4
3. **URI** : Les URI de restaurant sont en minuscules avec tirets (ex: "le-gourmet")
4. **Couleurs** : Format hexadécimal avec # (ex: "#FF6B35")
5. **Authentification JWT** : Les endpoints protégés nécessitent un token JWT obtenu via `/terminal/refresh-token`
6. **Google Wallet** : Les cartes de fidélité sont créées et mises à jour automatiquement via l'API Google Wallet
7. **Expiration token** : Les tokens JWT expirent après 24h (86400 secondes)
