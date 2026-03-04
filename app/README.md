# Borne Appétit - Infrastructure Backend

Infrastructure AWS avec Clean Architecture pour la borne de commande interactive.

## Architecture

### Infrastructure AWS
- **API Gateway** : HTTP API avec CORS
- **Lambda** : 3 fonctions serverless
- **DynamoDB** : Table de configuration
- **S3 + CloudFront** : Distribution des assets statiques

### Clean Architecture

```
src/
├── domain/              # Entités et interfaces métier
│   ├── entities.py      # Restaurant, Terminal
│   └── repositories.py  # Interfaces des repositories
├── application/         # Cas d'usage
│   └── use_cases.py     # GetRestaurantConfig, GetTerminalConfig
└── infrastructure/      # Implémentations techniques
    ├── dynamodb_repositories.py  # Implémentation DynamoDB
    ├── health_handler.py
    ├── terminal_handler.py
    └── restaurant_handler.py
```

## Endpoints API

### Health Check
```
GET /health
```

### Configuration Terminal
```
GET /terminal/config/{uuid}
```

### Configuration Restaurant
```
GET /restaurant/{uri}/config
```

## Structure Terraform

```
tf/
├── main.tf              # Configuration principale
├── modules.tf           # Déclaration des modules
├── variables.tf         # Variables globales
├── outputs.tf           # Outputs
├── iam.tf              # Rôles et permissions
└── modules/
    ├── api/            # API Gateway et routes
    │   ├── gateway.tf
    │   ├── routes_health.tf
    │   ├── routes_terminal.tf
    │   └── routes_restaurant.tf
    ├── lambda/         # Fonctions Lambda
    │   ├── health.tf
    │   ├── terminal_config.tf
    │   └── restaurant_config.tf
    ├── database/       # DynamoDB
    │   └── dynamodb.tf
    └── storage/        # S3 et CloudFront
        ├── s3.tf
        └── cloudfront.tf
```

## Déploiement

```bash
cd tf
terraform init
terraform plan
terraform apply
```

## Principes Clean Architecture

1. **Domain** : Logique métier pure, indépendante de toute technologie
2. **Application** : Orchestration des cas d'usage
3. **Infrastructure** : Implémentations techniques (DynamoDB, Lambda handlers)

Les dépendances pointent toujours vers l'intérieur (Infrastructure → Application → Domain).
