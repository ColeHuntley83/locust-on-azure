from locust import HttpLocust, TaskSet, task, between
from faker import Faker
fake = Faker()

class APIUser(HttpLocust):
    wait_time = between(5, 10) # seconds
    
    @task(8)
    def getpost(self):
        post_id = fake.random_int(min=1, max=100, step=1)
        self.client.get("/posts/%i" % post_id, name="/posts/[id]")

    @task()
    def postpost(self):        
        self.client.post("/posts", {"title": "foo", "body": "bar", "userId": 1}, name="/posts")

