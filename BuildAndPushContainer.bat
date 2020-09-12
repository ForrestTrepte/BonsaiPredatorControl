call az login
call az acr login --subscription 8740a2a4-8576-4eb3-8023-4bf3ef4a7c33 --name bonsailearning
call docker build -t predatorimage .
call docker tag predatorimage bonsailearning.azurecr.io/bonsai/predatorimage
call docker push bonsailearning.azurecr.io/bonsai/predatorimage