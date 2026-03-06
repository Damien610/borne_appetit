# Lambda Layer - Shared Dependencies

## 📦 Contenu

Cette layer contient :
- Modules Python partagés : `infrastructure/`, `application/`, `domain/`
- Dépendances pip : PyJWT, requests, google-auth, google-auth-oauthlib, boto3

## 🚀 Utilisation

Le fichier `shared_layer.zip` est **pré-buildé et commité** dans Git.

**Vous n'avez pas besoin de Docker** pour développer ! Terraform utilise directement le zip.

## 🔨 Rebuilder la layer (si nécessaire)

Si vous modifiez les dépendances ou les modules partagés :

```bash
# Prérequis : Docker Desktop doit être démarré
./build_shared_layer.sh
```

Puis commitez le nouveau `shared_layer.zip`.

## ⚙️ Pourquoi Docker ?

Les dépendances Python (notamment `cryptography`) doivent être compilées pour **Linux** (AWS Lambda), pas macOS/Windows.

Docker utilise l'image officielle AWS Lambda pour garantir la compatibilité.

## 📝 Notes

- Taille du zip : ~27MB
- Temps de build : ~30-60 secondes
- Fréquence de rebuild : Rare (seulement si dépendances changent)
