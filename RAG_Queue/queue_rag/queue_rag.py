# we are using rq to create a queue for our tasks. RQ is a simple Python library for queueing jobs and processing them in the background with workers. It is backed by Redis, which is a fast in-memory data store.
#using valkey to store queue data
from redis import Redis
from rq import Queue

queue = Queue(connection=Redis(host='localhost', port=6379))

