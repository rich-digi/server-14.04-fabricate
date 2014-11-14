from fabric.api import env, run
import yaml

# Load the YAML configuration file
f = open('linode-a.yaml', 'r')
config = yaml.load(f)
f.close()

env.hosts 		= config['machine']['fqdn']
env.user  		= config['machine']['root_login']
env.password 	= config['machine']['root_pwd']

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
	machine_name = config['machine']['name']
	run('hostname %s' % machine_name)
	run('echo %s > /etc/hostname' % machine_name)
	run('echo 127.0.0.1 %s >> /etc/hosts' % machine_name)
	run('uname -n')

def enable_firewall():
	# Enable Ubuntu Firewall and allow SSH & MySQL Ports
	run('ufw enable')
	for port in config['firewall']:
		run('ufw allow %d' % port)

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
	run('apt-get update && apt-get upgrade -y')

def install_basics():
	run('apt-get install zip curl telnet mailutils')

def install_samba():
	run('apt-get install samba')
	run('echo -ne "%s\n%s\n" | smbpasswd -a -s $LOGIN' % (config['samba_pwd'], config['samba_pwd']))

def install_mysql():
	run('echo "mysql-server mysql-server/root_password password %s" | sudo debconf-set-selections' % config['mysql']['root_pwd'])
	run('echo "mysql-server mysql-server/root_password_again password %s" | sudo debconf-set-selections' % config['mysql']['root_pwd'])
	run('apt-get -y install mysql-server')
	run('mysql_secure_installation')
	run('sed -i s/127.0.0.1/%s/ /etc/mysql/my.cnf' % config['machine']['ip_address'])
	run('mysql --user=root --password=%s' % config['mysql']['root_pwd'])
	run('CREATE USER "%s"@"%" IDENTIFIED BY "%s";' % (config['mysql']['remote_login'], config['mysql']['remote_pwd']))
	run('GRANT ALL ON *.* TO "%s" IDENTIFIED BY "%s";' % (config['mysql']['remote_login'], config['mysql']['remote_pwd']))
	run('FLUSH PRIVILEGES;')
	run('exit;')
	run('service mysql restart')

def install_webmin():
	run('apt-get install webmin')

def install_svn_git():
	run('apt-get install subversion')
	run('apt-get install git-core')

def install_ftp_clients():
	run('apt-get install ftp ncftp')
	
def install_ftp_server():
	run('apt-get install vsftpd')
	
