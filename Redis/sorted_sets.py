import redis

r = redis.Redis(
    host='redis-12103.c281.us-east-1-2.ec2.cloud.redislabs.com',
    port=12103,
    decode_responses=True,
    username="default",
    password="qtaRSKe6YrtJs8MRRlaXLwif6X9ByRC3",
)

# Name of the Redis sorted set
teams = 'Teams'
 
# Add elements to the Redis sorted set
r.zadd(teams, {'Team1': 291})
r.zadd(teams, {'Team2': 142})
r.zadd(teams, {'Team3': 256, 'Team4': 197, 'Team5': 220})
 
# Print the sorted set
print('Contents of the sorted set:')
print(r.zrange(teams, 0, -1, desc=True, withscores=True))
 
# Remove some of the elements
print('Removing few elements (Team3, Team4) from the Redis sorted set:')
print(r.zrem(teams, 'Team3', 'Team4'))
 
print('Remaining elements of the sorted set:')
print(r.zrange(teams, 0, -1, desc=True, withscores=True))
 
# Remove some of the elements by score
print('Removing the range (200 ~ 250) of elements by score:')
print(r.zremrangebyscore(teams, 200, 250))
 
print('Remaining elements of the sorted set:')
print(r.zrange(teams, 0, -1, desc=True, withscores=True))
 
# Print the remaining elements after removal
print('Remaining elements of the sorted set after removals:')
print(r.zrevrange(teams, 0, -1, withscores=True))