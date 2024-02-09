

## routes with OpenAPI spec


routes can be found here in the openAPI spec  [Created Routes](./radpair/openapi/openapi.yaml)
## these routes are important to be added to if any other API endpoints are to be created as we can quickly share these and understand 
## the routes better


# How To Run


1. First thing run cp docker-compose-dist.yaml docker-compose.yaml and input your chatgpt key in the correct key in the ENV section
    without this key the openapi will throw an error
    Whey did I do this? it would not be good security practices to leave a api key in the docker compose n any situation, trying to do this on
    the frontend is not really real world since everybody could see your token, it would go more than likeley in a prod environment be added in the CI/CD
    pipeline with the docker container is build and pushed to the ECR.

to get started you need to inside the backend-app/flask-application director and then you will need to run ./scripts/build_container.sh
You will now see output being logged out while the container is being built, keep in mind I did not put hot loading in so if you make a modification you
will need to rebuild ( if you're doing something with the envs)


2. After doing the above still inside the directory where you ran the shell file you need to run docker-compose up -d if you want to see all the output in  real time then you just remove the "-d" when shutting the container down you need to run docker-compose down

3. you should have a running container! if not reach out to me travishaycock92@gmail.com



# Design patterns

The code I used here is a boiler plate that I used for my health application that is currently running on app runner AWS: https://cxmape9yrk.us-east-1.awsapprunner.com/status  you can see it here if you paste that in a browser. I was trying to deploy this on either railway.app or on App runner but I am running out of time as I really could have hoped to decouple this from the app so you could only focus on the front end but my logic is, instead of writing a frontend only app which is not really realistic considering the context I wanted to demonstrate a backend server and full stack competence as well as just making something shiny in react. At the time of writing this I do not have tests but will come back for a second pass.

I like keeping a scripts folder in this application because it allows us to run the same commands and when the container is running I can also access these scripts as well and do operations.

The applications design patterns are fairly straightforward using the Flask library we have the blueprints pattern that allows us to not step on eachothers toes when creating new endpoints or working in different areas. We also employ a division with responsibilities handlers, queries a handlder in this context would be a direction or a control where the code should go, it's a place to do preprocessing call other classes before executing a query, or perhaps call a query in another class as well before calling the next, the reason I do this is because it's easier to test, it's abstract but also clear what it's doing.

In the queries classes we have raw queries or what would be there, this is subjective but I sometimes find the ORM is too abstract I have worked on projects that are both big and small that use the ORM and that's fine in most cases.

For authentication you see there is none here because for that to make sense I would need spin up a pg database to check the hash but also I would need to worry in the frontend using a Context for axios to store the JWT in which would take some more time, I am mentioning this because neglecting this in the real world is ofcourse in short horrible for many reasons.


## Context Manager
 Ok what is this? I implemented the context manager out of past project experiences, countless P.R's that 
 had to be re-done because people import os and common sys libs into all their classes here and there, it made a lot of import statements that were not really nessisary, we can centralize the calls in the util_helper that way when soemone want sot use a comoon import they call the utilhelper instead of doing something like i.e os. environ['USER']  everywhere and we kick this up a notch by making sure the registered callers are registered and legal, otherwise they raise an error and have to go back and implement it properly


 ## Error handling
  There are try and excepts in here, I would not be confident with this level of try and excepts to be honest unless I had tests to support that confidence most times with the tests I can get specifically the 
  exceptions that would be raised in a specific scenario but taking a more TDD approach to this.


# How to make this better

 1. First tests, we should always try to have our tests caught up with our features and created during development perhaps Test driven development or perhaps after - different places have different standars and developers have their own way. In this application I had to sacrifice getting something out the door rather than add tests unfortunatley like I noted above.

 2. Implement JWT this goes without saying the JWT should be an actual secret and be a very difficult set of chars and verify all private endpoints to make sure it was signed by out server and not somebody elses.

 3. Create some queries! we have a login route we should use it!

 4. that db directory contains a db change log in yaml, I would use liquibase to manage my DB changes so
    it has scope of history too

 5. introduce flake8 and black to standardize the codebase, make it run in the CircleCI so we can be sure   no unformatted code reached the main branch


Extras, I attempted to add in things that would be there if this were a real project thinking ahead like circleci config and pull request template