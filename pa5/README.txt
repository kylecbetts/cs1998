Name: Kyle Betts
NetID: kcb82

Challenges Attempted (Tier I/II/III):
Working Endpoint: GET /api/courses/
Your Docker Hub Repository Link: https://hub.docker.com/repository/docker/kylebetts/cs1998pa5

Questions:
Explain the concept of containerization in your own words.

Containerization is the ability to package an applications environment 
into a single entity, so that is can be easily distributed and run on 
different devices. The application environment contains the code, config 
files, environment variables, and the dependent libraries. 

What is the difference between a Docker image and a Docker container?

A docker image is a blueprint for running an application. An image is 
like a Class, while the container is like an Object. Each container 
of the image follows the same blueprint, but you can spin up numerous 
containers of the same image. Images are executed as containers.

What is the command to list all Docker images?

`docker images`

What is the command to list all Docker containers?

`docker ps`

What is a Docker tag and what is it used for?

A Docker tag is a name for an image.

What is Docker Hub and what is it used for?

Docker Hub is a remote location to store and retrieve Docker 
images. It works in a similar way to GitHub where you can 
push your images to the server, pull your images to a 
different device, have your images public or private, etc.

What is Docker compose used for?

Docker Compose simplifies the steps to running a container(s). Running 
a container can contain lots of flags, which can be specified in the 
docker-compose.yml file so you don't have to remember them. Also, numerous 
containers of the same or different images can be spun up in this file, 
so is simplifies starting up all the containers needed.

What is the difference between the RUN and CMD commands?

The CMD command can only be called once, and it should be used to start 
up the application. The RUN command is used to issue terminal commands, 
and can be used numerous times. It can be used to create directories, 
install dependencies etc.
