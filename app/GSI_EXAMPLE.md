# Ajout d'un GSI à DynamoDB - Comportement Terraform

## Scénario : Ajouter un GSI

### Avant (état actuel)
```hcl
resource "aws_dynamodb_table" "config" {
  name         = "borne-appetit-config"
  hash_key     = "PK"
  range_key    = "SK"
  
  global_secondary_index {
    name            = "SK-index"
    hash_key        = "SK"
    projection_type = "ALL"
  }
  
  global_secondary_index {
    name            = "uri_name-index"
    hash_key        = "uri_name"
    projection_type = "ALL"
  }
}
```

### Après (ajout d'un nouveau GSI)
```hcl
resource "aws_dynamodb_table" "config" {
  name         = "borne-appetit-config"
  hash_key     = "PK"
  range_key    = "SK"
  
  # GSI existants (inchangés)
  global_secondary_index {
    name            = "SK-index"
    hash_key        = "SK"
    projection_type = "ALL"
  }
  
  global_secondary_index {
    name            = "uri_name-index"
    hash_key        = "uri_name"
    projection_type = "ALL"
  }
  
  # NOUVEAU GSI
  global_secondary_index {
    name            = "email-index"
    hash_key        = "email"
    projection_type = "ALL"
  }
  
  # Nouvel attribut nécessaire
  attribute {
    name = "email"
    type = "S"
  }
}
```

## Résultat du `terraform apply`

```
Terraform will perform the following actions:

  # module.database.aws_dynamodb_table.config will be updated in-place
  ~ resource "aws_dynamodb_table" "config" {
      + attribute {
          + name = "email"
          + type = "S"
        }
      
      + global_secondary_index {
          + name            = "email-index"
          + hash_key        = "email"
          + projection_type = "ALL"
        }
      
      # (autres attributs inchangés)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

## Ce qui se passe

1. ✅ **Table conservée** : Pas de suppression
2. ✅ **Données conservées** : Toutes les données restent
3. 🔄 **GSI ajouté** : AWS crée l'index en arrière-plan
4. ⏱️ **Temps** : Quelques minutes (selon la taille de la table)
5. ✅ **Disponibilité** : La table reste accessible pendant la création du GSI

## Opérations qui FORCENT une recréation

Certaines modifications **obligent** Terraform à détruire/recréer :

❌ **Changement de `hash_key`** (PK)
❌ **Changement de `range_key`** (SK)
❌ **Changement de `name`** (nom de la table)

Pour ces cas, Terraform affichera :
```
-/+ destroy and then create replacement
```

Et le `prevent_destroy = true` **bloquera** l'opération.

## Opérations sûres (mise à jour in-place)

✅ Ajouter un GSI
✅ Supprimer un GSI
✅ Modifier les tags
✅ Changer le billing mode (PROVISIONED ↔ PAY_PER_REQUEST)
✅ Activer/désactiver Point-in-Time Recovery
✅ Modifier TTL

## Vérification avant apply

Toujours faire :
```bash
terraform plan
```

Chercher ces symboles :
- `~` = mise à jour (safe)
- `+` = création (safe)
- `-` = suppression (attention)
- `-/+` = remplacement (DANGER - données perdues)
