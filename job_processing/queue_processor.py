from rq import Queue #Queue
from redis import Redis
import subprocess

#READ CONFIG FILE
config = {}
execfile("config.py", config)

redis_conn = Redis()
q = Queue('innuendo_jobs', connection=redis_conn)

class Queue_Processor:

	def process_job(self, **kwargs):
		key_value_args = []
		parameters = kwargs['parameters']['used Parameter']
		for key, value in parameters.iteritems():
			key_value_args.append(str(key))
			
			if len(value.split(' ')) > 1:
				key_value_args.append('"' + str(value) + '"')
			else:
				key_value_args.append(str(value))

		key_value_args.append("--spadesMaxMemory")
		key_value_args.append("4")

		#print key_value_args
		key_value_args = [config['INNUCA_PATH']] + key_value_args
		print key_value_args
		subprocess.call(key_value_args)
		
		return True

	def insert_job(self, **kwargs):
		#Insert jobs in queue
		job = q.enqueue_call(func=self.process_job, kwargs=kwargs)