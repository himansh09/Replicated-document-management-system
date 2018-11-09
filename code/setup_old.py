from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call

def read_readme_file():
    with open('README.rst') as readme_file:
        return readme_file.read()

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        print('####################### In develop')
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        print('####################### After Installation')
        check_call("bash ./install_libraries".split())
        install.run(self)

setup(name='replicated_document_management_system',
      version='1.0',
      description='It replicates the database of documents like git into HA server clusters.',
      long_description=read_readme_file(),
      url='http://github.com/himansh09/replicated-document-management-system',
      author='Himanshu Saraiya, Pranhat Nampally, I.G.Prasad',
      author_email='himanshu.saraiya09@gmail.com',
      license='',
      packages=['replicated_document_management_system'],
      scripts=['bin/install_libraries'],
      install_requires=[
          'paramiko','kazoo','flask', 'Flask-SocketIO'
          ],
      zip_safe=False,
      cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
        })

##### debian packages required
##zookeeper , nginx ,uwsgi, openssh-server
