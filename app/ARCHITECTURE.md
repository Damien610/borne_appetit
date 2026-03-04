# Borne Appétit - Clean Architecture

## Structure du Projet

```
.
├── src/
│   ├── domain/                          # Couche Domaine (Entités + Interfaces)
│   │   ├── entities.py                  # Restaurant, Terminal
│   │   └── repositories.py              # Interfaces RestaurantRepository, TerminalRepository
│   │
│   ├── application/                     # Couche Application (Use Cases)
│   │   └── use_cases.py                 # GetRestaurantConfig, GetTerminalConfig
│   │
│   └── infrastructure/                  # Couche Infrastructure (Implémentations)
│       ├── dynamodb_repositories.py     # Implémentation DynamoDB des repositories
│       ├── health_handler.py            # Handler Lambda health check
│       ├── terminal_handler.py          # Handler Lambda terminal config
│       └── restaurant_handler.py        # Handler Lambda restaurant config
│
├── tf/                                  # Infrastructure as Code
│   ├── main.tf                          # Configuration Terraform principale
│   ├── modules.tf                       # Déclaration des modules
│   ├── variables.tf                     # Variables globales
│   ├── outputs.tf                       # Outputs
│   ├── iam.tf                          # Rôles et permissions IAM
│   │
│   └── modules/                         # Modules Terraform
│       ├── api/                         # API Gateway
│       │   ├── gateway.tf               # Configuration API Gateway
│       │   ├── routes_health.tf         # Route /health
│       │   ├── routes_terminal.tf       # Route /terminal/config/{uuid}
│       │   ├── routes_restaurant.tf     # Route /restaurant/{uri}/config
│       │   └── variables.tf
│       │
│       ├── lambda/                      # Fonctions Lambda
│       │   ├── health.tf                # Lambda health
│       │   ├── terminal_config.tf       # Lambda terminal config
│       │   ├── restaurant_config.tf     # Lambda restaurant config
│       │   └── variables.tf
│       │
│       ├── database/                    # Base de données
│       │   ├── dynamodb.tf              # Table DynamoDB config
│       │   └── outputs.tf
│       │
│       └── storage/                     # Stockage statique
│           ├── s3.tf                    # Bucket S3
│           ├── cloudfront.tf            # Distribution CloudFront
│           ├── variables.tf
│           └── outputs.tf
│
└── static/                              # Assets statiques
    └── index.html
```

## Flux de Dépendances (Clean Architecture)

```
Infrastructure → Application → Domain
     ↓               ↓            ↓
  Handlers      Use Cases    Entities
  DynamoDB      Business     Interfaces
  Repos         Logic
```

### Règles :
- **Domain** : Aucune dépendance externe (pure Python)
- **Application** : Dépend uniquement du Domain
- **Infrastructure** : Dépend de Application et Domain, implémente les détails techniques

## Endpoints API

| Endpoint | Méthode | Handler | Use Case |
|----------|---------|---------|----------|
| `/health` | GET | `health_handler.py` | - |
| `/terminal/config/{uuid}` | GET | `terminal_handler.py` | `GetTerminalConfigUseCase` |
| `/restaurant/{uri}/config` | GET | `restaurant_handler.py` | `GetRestaurantConfigUseCase` |

## Déploiement

```bash
cd tf
terraform init
terraform plan
terraform apply
```

## Avantages de cette Architecture

1. **Testabilité** : Les use cases peuvent être testés sans infrastructure
2. **Maintenabilité** : Séparation claire des responsabilités
3. **Évolutivité** : Facile d'ajouter de nouveaux use cases ou repositories
4. **Indépendance** : Le domaine ne dépend d'aucune technologie
