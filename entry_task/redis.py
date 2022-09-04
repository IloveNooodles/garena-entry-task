import redis
from django.conf import settings

# Instance
redisInstance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
