# coding: utf-8

from __future__ import with_statement

import os

from fabric.api import *
from fabric.contrib import files

#output['debug'] = True

env.hosts = ['semcomp.icmc.usp.br']

env.settings = 'semcomp.settings.prod'

env.base_path = '/home/www/docker-applications/vm'
env.app_path = os.path.join(env.base_path, 'semcomp/17')
env.repository_path = os.path.join(env.app_path, 'semcomp/code')
env.fig_yml = os.path.join(env.base_path, 'fig.yml')

env.repository_url = 'https://github.com/fcoelho/semcomp-next'

env.fig = '/opt/fig/bin/fig'


@task
def pull():
	if not files.exists(env.repository_path):
		run('git clone {repository_url} {repository_path}'.format(**env))
	with cd(env.repository_path):
		run('git pull && git reset --hard && git clean -fdx')

@task
def fig(cmd):
	# "sudo" customizado pra entrar no diretório que precisa antes
	return run('cd {base_path} && sudo {fig} {cmd}'.format(cmd=cmd, **env), shell=False)

@task
def run_django_command(command, opts):
	# primeiro garante que tem um uwsgi rodando já
	result = fig('ps -q semcomp17uwsgi')
	if not result.strip():
		fig('up -d --no-deps semcomp17uwsgi')
	
	# tem que enfiar o settings *depois* do comando
	cmd = '{python} {manage} {cmd} --settings {settings} {opts}'.format(
		python='/env/bin/python',
		manage='/code/manage.py',
		settings='semcomp.settings.prod',
		cmd=command,
		opts=opts,
	)

	fig('run --rm semcomp17uwsgi {cmd}'.format(cmd=cmd))

@task
def deploy():
	pull()

	fig('up -d --no-deps semcomp17uwsgi')
	fig('up -d --no-deps frontend')

@task
def full_deploy():
	pull()

	run_django_command('syncdb', '--noinput')
	run_django_command('migrate', '--noinput')
	run_django_command('collectstatic', '--noinput')

	fig('up -d --no-deps semcomp17uwsgi')
	fig('up -d --no-deps frontend')
