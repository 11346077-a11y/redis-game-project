"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='redis-12103.c281.us-east-1-2.ec2.cloud.redislabs.com',
    port=12103,
    decode_responses=True,
    username="default",
    password="qtaRSKe6YrtJs8MRRlaXLwif6X9ByRC3",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar