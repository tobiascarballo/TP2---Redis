

from redis import Redis

r = Redis(host='localhost', port=6379, decode_responses=True)

print(r.ping())

r.set('jedi2', 'Luke Skywalker')

print(r.get('jedi2'))

r.lpush('jedis', 'Yoda', 'Obi-Wan')

print(r.lrange('jedis', 0, -1))