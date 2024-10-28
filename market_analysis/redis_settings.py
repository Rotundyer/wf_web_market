from redis import asyncio as aioredis

redis_client = aioredis.from_url('redis://192.168.0.214:6379',
                                 encoding='utf8',
                                 decode_responses=True)
