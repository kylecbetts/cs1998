Name: Kyle Betts
NetID: kcb82

Working Endpoint: GET /api/courses/
Your Server Address: 34.130.59.69

Questions:
Explain the concept of deployment in your own words.

Deployment is the act of setting up and running your code on 
a production server. 

What are environment variables?

Environment variables are values that you would like to keep hidden. 
These typically live in a .env file, and that file is included in 
the .gitignore and .dockerignore files so that they are never uploaded 
to the internet where they could be seen by someone else. Typical environment 
variables include API keys. 

What is the filename of the file where environment variables are traditionally stored?

.env

What is the network protocol we use to access servers?

http (hypertext transfer protocol)

Explain the concept of clustering in your own words.

Clustering is the use of multiple servers all connected together. 
Typically this is used to break the application into various roles, 
such as web server, database, and file storage. This increases modularity, 
allowing for certain parts of the application to be replaced with different 
versions when needed. Also having each server specialize in one task can 
lead to performance increases.

Explain the concept of load balancing in your own words.

Load balancing allows you to spin up multiple servers, each running your 
application. When traffic comes in, the load balancing server then divides 
up the requests amongst the running servers. This improves performance by 
spreading the work out across each running server.
