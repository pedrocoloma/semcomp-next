from __future__ import with_statement

import os

from fabric.api import *
from fabric.contrib import files

output['debug'] = True

env.hosts = ['semcomp.icmc.usp.br']

env.settings = 'semcomp.settings.prod'

env.base_path = '/home/www/docker-applications/vm'
env.app_path = os.path.join(env.base_path, 'semcomp/17')
env.repository_path = os.path.join(env.app_path, 'image/code')
env.dockerfile_path = os.path.join(env.app_path, 'image/Dockerfile')
env.fig_yml = os.path.join(env.base_path, 'fig.yml')

env.repository_url = 'https://github.com/fcoelho/semcomp-next'

env.fig = '/opt/fig/bin/fig'

@task
def pull():
	if not files.exists(env.repository_path):
		run('git clone {repository_url} {repository_path}'.format(**env))
	with cd(env.repository_path):
		run('git pull && git reset --hard')

def fig(cmd):
	return sudo('{fig} -f {fig_yml} -p vm {cmd}'.format(
		cmd=cmd, **env), shell=False)

def get_pypi_address():
	pypi_container_id = fig('ps -q pypi')

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

	with open('resources/Dockerfile.template') as f:
		dockerfile = f.read()
	with open('resources/Dockerfile', 'w') as f:
		f.write(dockerfile.format(**{
			'REQUIREMENTS_FILE': 'requirements/dev.txt',
			'INDEX_URL': index_url
		}))

	put('resources/Dockerfile', env.dockerfile_path)

	fig('up -d semcomp17uwsgi')
