### Api exercise


How to run the Api endpoint container


1.] git clone https://github.com/misua/api.git


2.] cd to _api_ dir, and do a docker/podman-compose up -d 


### Additional info & facts with the api endpoint
   - i am just using a Dict to store the counters, and not a datastore like redis,memcache.
   - i did NOT use ratelimiter library, i was considering Flask-limiter as its easier to integrate with redis if the needs would come up.
   - filebeat is installed on the same container where the rest python app is, it would recieve the flask_app.log(as configured in filebeat.yml) and
     later on send to a different docker container that runs kibana and elasticsearch.
   - Dockerfileelastic is the Dockerfile for kibana and elasticsearch.(just rename it to Dockerfile if you need to build and run it)



     
3.] Access the api at http://127.0.0.1:5000/api/resource - by default you are allowed to request 2 times in 60 seconds

4.] To Change the rate limit call http://127.0.0.1/api/limit by using curl(in cli) or postman e.g 


    curl -X POST -H "Content-Type: application/json" -d '{"limit": 10, "window": 120}' http://localhost:5000/api/limit

   > this changes the rate limit to be 10 requests on a 2 minutes window.

![Flow](https://raw.githubusercontent.com/misua/gmay_eggs/main/accelbyte.png)

