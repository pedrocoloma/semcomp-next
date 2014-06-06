from __future__ import with_statement
from fabric.api import *
from fabric.contrib import files

from pathlib import Path
import os

import six

output['debug'] = True

env.hosts = ['semcomp.icmc.usp.br']

env.settings = 'semcomp.settings.prod'

env.base_path = '/home/www/docker-applications/vm'
env.app_path = os.path.join(env.base_path, 'semcomp/17')
env.repository_path = os.path.join(env.app_path, 'code')
env.dockerfile_path = os.path.join(env.repository_path, 'resources')
env.fig_yml = os.path.join(env.base_path, 'fig.yml')

env.repository_url = 'https://github.com/fcoelho/semcomp-next'

env.fig = '/opt/fig/bin/fig'

@task
def teste():
	with prefix('cd {}'.format(env.base_path)):
		sudo('{fig} ps'.format(**env), shell=False)

@task
def pull():
	if not files.exists(env.repository_path):
		run('git clone {repository_url} {repository_path}'.format(**env))
	with cd(env.repository_path):
		run('git pull && git reset --hard')

def get_pypi_address():
	pypi_container_id = sudo(
		'{fig} -f {fig_yml} -p vm ps -q pypi'.format(**env), shell=False)
	
	inspect_format = (
		'{{$ip := .NetworkSettings.IPAddress}}'
		'{{range $p, $conf := .NetworkSettings.Ports}}'
			'{{$ip}}:{{$p}}'
		'{{end}}'
	)

	pypi_address = sudo("docker inspect --format '{format}' {pypi}".format(**{
		'format': inspect_format,
		'pypi': pypi_container_id,
	}), shell=False).replace('/tcp', '')

	return 'http://{0}/root/pypi/'.format(pypi_address)

@task
def build_image():
	index_url = get_pypi_address()

	template_file = os.path.join(env.dockerfile_path, 'Dockerfile.template')
	output_file = os.path.join(env.dockerfile_path, 'Dockerfile')

	with open(template_file) as f:
		dockerfile = f.read()
	with open(output_file, 'w') as f:
		f.write(dockerfile.format(**{
			'REQUIREMENTS_FILE': os.getenv('REQUIREMENTS_FILE', 'requirements.txt'),
			'INDEX_URL': index_url
		}))

