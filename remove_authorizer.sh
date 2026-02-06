#!/bin/bash
# Script temporaire pour retirer l'authorizer de la route
# À exécuter depuis GitHub Actions ou avec credentials AWS

aws apigatewayv2 update-route \
  --api-id x2p1mpmjy1 \
  --route-id $(aws apigatewayv2 get-routes --api-id x2p1mpmjy1 --query "Items[?RouteKey=='GET /restaurant/{uri}/config'].RouteId" --output text) \
  --authorization-type NONE \
  --region eu-west-1

echo "Authorizer retiré de la route. Relancez terraform apply."
