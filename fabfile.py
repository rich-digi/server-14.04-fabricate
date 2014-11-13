from fabric.api import env, run

env.user  = 'root'
env.hosts = ['linode-a.apewave.com']
# env.password = 'oolongT42'

"""
THESE LOOK USEFUL...
fabric.contrib.files.append
fabric.contrib.files.comment
fabric.contrib.files.uncomment
fabric.contrib.files.sed
fabric.contrib.files.upload_template
"""

def set_hostname():
	# Set machine hostname
	run('hostname %s' % machine_name)
	run('echo %s > /etc/hostname' % machine_name)
	run('echo 127.0.0.1 %s >> /etc/hosts' % machine_name)
	run('uname -n')

def set_timezone():
	# Set timezone to Europe/London
	run('export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true')
	run('echo %s > /etc/timezone' % 'Europe/London')
	run('dpkg-reconfigure -f noninteractive tzdata')

def create_groups_and_users():
	run('addgroup www')
	run('useradd -g www www')

def add_source_repos():
	# Add any additional source repositories required for the build
	run('echo deb http://download.webmin.com/download/repository sarge contrib >> /etc/apt/sources.list')
	run('echo deb http://webmin.mirror.somersettechsolutions.co.uk/repository sarge contrib >> /etc/apt/sources.list')
	run('mkdir -p /home/oev/generic/install')
	run('cd /home/oev/generic/install')
	run('wget http://www.webmin.com/jcameron-key.asc')
	run('apt-key add jcameron-key.asc')

def update_sources():
	run('apt-get update && apt-get upgrade')
	
def install_ftp_clients():
	run('apt-get install ftp ncftp')
	
def install_ftp_server():
	run('apt-get install vsftpd')
	
