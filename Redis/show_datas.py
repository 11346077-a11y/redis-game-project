
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

'''
上面是client1.py的code
'''

# 字符串 Strings
print('[STRING] foo:', r.get('foo'))
print('[STRING] test:', r.get('test'))
 
# 列表 Lists
print('[LIST] list:', r.lrange('list', '0', '10'))
 
# 雜湊 Hashes
print('[HASH] hash_test:', r.hgetall('hash_test'))
 
# 集合 Sets
print('[SET] set_test:', r.smembers('set_test'))
 
# 有序集 Sorted sets
print('[Sorted SET] zset_test:', r.zrange('zset_test', 0, 10))