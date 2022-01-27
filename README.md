# PythonMicroservices

## Instructions to Run the Microservices
The code contains 3 microservices - userService, contentService, UserInteractionService.</br>
To run the 3 microservices, download the repository, navigate to the downloaded repository and run teh following command in terminal:</br>
**`./start`**</br>
This command will start all the docker containers, set up the db and run all the microservices. If the program appears to be stuck, wait for progress. It might take  a minute or so for the docker-containers to build the first time.
</br>


## Testing & Documentation of the APIs
The repository contains a file named **`TestCollection.postman_collection.json`**.</br>
Import this collection into postman to see details about the APIs and their documentation.</br>
This file contains all the API requests for populating the database. When building the code for the 1st time, run all the requests in this collection to populate the database before making any request.</br>
Apart from that it has 3 more collections:</br>
1) UserCollection: This collection contains samples for all the USER API along with the documentation, request and response structures for all the user APIs. The story1.csv file present in the repository can be used to make request to upload content from .csv file to the server. The request has been saved by the name `Get content from csv file`.
2) ContentCollection: This collection contains example requests along with request and response structures for all the content realated APIs.</br>
3) UserInteractionCollection: This collection contains the request, response structure along with sample requests for all the APIs related to userInteraction Service.

## Architecture Diagram
![alt text](https://github.com/rakshit-singh/PythonMicroservices/blob/main/ArchitectureDiagram.svg)</br>

Each of the 3 services have their own Databases. A RabbitMQ message queue is used to pass messages between the microservices to coordinate and ensure data consistency.

## Database Schema
## Database Schema for User Service
![alt text](https://github.com/rakshit-singh/PythonMicroservices/blob/main/userService/UserDBSchema.png)

### DataBase Schema for Content Service
![alt text](https://github.com/rakshit-singh/PythonMicroservices/blob/main/contentService/ContentDBSchema.png)</br>
The user_id field contains the id of the user that has uploaded/contributed the content.

### Database Schema for UserInteraction Service
![alt text](https://github.com/rakshit-singh/PythonMicroservices/blob/main/userInteractionService/userInteractionDBSchema.png)
The Database Schema for the user Interaction service has been designed keep in mind the fact that the service might need to support events like fetching all the content user has read in the past (use those to recommend new content), content that the user has liked whith minimal changes to the db and the service.


