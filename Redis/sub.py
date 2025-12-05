import redis

r = redis.Redis(
    host='redis-12103.c281.us-east-1-2.ec2.cloud.redislabs.com',
    port=12103,
    decode_responses=True,
    username="default",
    password="qtaRSKe6YrtJs8MRRlaXLwif6X9ByRC3",
)

rps = r.pubsub()
rps.psubscribe('topic_*')  # subscribes the client to the given patterns
rps.subscribe('my_topic')

for message in rps.listen():
    print(message)
    if message.get('data') == 'QUIT':
        quit()