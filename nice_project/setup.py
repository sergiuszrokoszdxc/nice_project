from setuptools import setup

setup(
   name='nice_project',
   version='0.1.1',
   description='A module for being nice',
   author='Sergiusz Rokosz',
   author_email='sergiusz.rokosz@dxc.com',
   packages=['nice_project', "nice_project.utils"],
   include_package_data=True,
   install_requires=["Flask==1.1.2",
                     "uwsgi==2.0.18"]
)
