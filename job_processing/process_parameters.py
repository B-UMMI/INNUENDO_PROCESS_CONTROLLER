import json
import os

def get_protocol_parameters(parameters):

	key_value_args = []

	for key, value in parameters.iteritems():
		key_value_args.append(str(key))

		if len(value.split(' ')) > 1:
			key_value_args.append("'" + str(value) + "'")
		else:
			key_value_args.append(str(value))

	return key_value_args


def process_innuca(key_value_args, parameters, user_folder):

	prev_application_steps = ''

	key_value_args.append('-i')
	key_value_args.append(os.path.join(str(user_folder),'$SLURM_ARRAY_JOB_ID'))

	key_value_args.append('-o')
	key_value_args.append(os.path.join(str(user_folder),'$SLURM_ARRAY_JOB_ID'))

	return key_value_args, prev_application_steps


def process_chewbbaca(key_value_args, parameters, user_folder):
	#list of genomes
	#list of genes
	prev_application_steps = 'find ' + user_folder + '/$SLURM_ARRAY_JOB_ID/*.fasta > ' + user_folder + '/$SLURM_ARRAY_JOB_ID/listGenomes.txt;'
	prev_application_steps = 'find ' + user_folder + '/*.fasta > ' + user_folder + '/$SLURM_ARRAY_JOB_ID/listGenes.txt;'

	key_value_args.append('-i')
	key_value_args.append(os.path.join(str(user_folder),'$SLURM_ARRAY_JOB_ID', 'listGenomes.txt'))

	key_value_args.append('-o')
	key_value_args.append(os.path.join(str(user_folder),'$SLURM_ARRAY_JOB_ID'))

	key_value_args.append('-g')
	key_value_args.append(os.path.join(str(user_folder),'$SLURM_ARRAY_JOB_ID','listGenes.txt'))


	return key_value_args, prev_application_steps
	


def process_parameters(parameters, user_folder, workflow):

	#READ CONFIG FILE
	config = {}
	execfile("config.py", config)

	options = {'INNUca':process_innuca, 'chewBBACA':process_chewbbaca}

	wf_params = json.loads(workflow['parameters'])
	if wf_params['used Software'] in config['APPLICATIONS_ARRAY']:
		software = wf_params['used Software']


	options = {'INNUca':process_innuca, 'chewBBACA':process_chewbbaca}

	key_value_args = get_protocol_parameters(parameters)
	key_value_args, prev_application_steps = options[software](key_value_args, parameters, user_folder)


	return key_value_args, prev_application_steps