# Comportement Terraform

## Déploiement Normal (après le premier apply)

Terraform compare l'état actuel (state) avec le code :
- ✅ **Aucun changement** → Rien ne se passe
- 🔄 **Modification** → Met à jour la ressource (sans la détruire si possible)
- ➕ **Nouvelle ressource** → Crée uniquement la nouvelle
- ➖ **Ressource supprimée du code** → Supprime uniquement celle-là

## Exemple : Modifier une Lambda

```bash
# Tu modifies le code Python dans src/infrastructure/health_handler.py
terraform apply
```

**Résultat :**
- ✅ Lambda health : **mise à jour** (nouveau code)
- ✅ Lambda terminal : **inchangée**
- ✅ Lambda restaurant : **inchangée**
- ✅ API Gateway : **inchangé**
- ✅ DynamoDB : **inchangée**

## Protection contre la suppression

Dans `dynamodb.tf`, il y a :
```hcl
lifecycle {
  prevent_destroy = true
}
```

Cela **empêche** Terraform de supprimer la table DynamoDB, même si tu fais `terraform destroy`.

## Ce qui s'est passé aujourd'hui

1. Ancien code : ressources à la racine (`aws_s3_bucket.assets`)
2. Nouveau code : ressources dans modules (`module.storage.aws_s3_bucket.assets`)
3. Terraform ne reconnaît pas que c'est la même ressource
4. Solution : Migration du state avec `terraform state mv`

## Prochains déploiements

Maintenant que le state est à jour, les prochains `terraform apply` seront **incrémentaux** :
- Seules les ressources modifiées seront touchées
- Pas de suppression/recréation inutile
