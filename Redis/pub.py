import redis

r = redis.Redis(
    host='redis-12103.c281.us-east-1-2.ec2.cloud.redislabs.com',
    port=12103,
    decode_responses=True,
    username="default",
    password="qtaRSKe6YrtJs8MRRlaXLwif6X9ByRC3",
)

myhost = "localhost"
r = redis.Redis(host=myhost, port=6379, db=0, decode_responses=True)

r.publish("topic_1", "Welcome")
r.publish("topic_2", "Hello")

while True:
    message = input("Enter the message to pub: ")
    r.publish("my_topic", message)
    if message == 'QUIT':
        quit()