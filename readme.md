# Source from [Langchain](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/#add-examples-in-the-cypher-generation-prompt)

## docker reminder

Une image Docker est un modèle immuable
Un conteneur Docker est une instance en cours d'exécution d'une image. 
Un volume est un espace de stockage externe aux conteneurs où les données peuvent être conservées.

Dockerfile est un fichier de script qui définit comment construire une image 
docker-compose.yaml est un fichier de configuration utilisé pour orchestrer plusieurs services Docker. 

## docker run

Do

    docker-compose up 

instead of running : 

    docker run `
        --name neo4j `
        -p 7474:7474 -p 7687:7687 `
        -d `
        -e NEO4J_AUTH=neo4j/password `
        -e NEO4J_PLUGINS="[\"apoc\"]" `
        neo4j:latest

Pour éviter d'avoir ces noms :

1/ dans mes images :
langchain-neo4j-neo4j

2/ dans mes containers :
langchain-neo4j


    docker-compose -p mon_projet up
