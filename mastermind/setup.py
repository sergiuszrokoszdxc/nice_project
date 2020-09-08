from setuptools import setup

setup(
   name='mastermind',
   version='0.1.1',
   description='A backend service for a mastermind games',
   author='Sergiusz Rokosz',
   author_email='sergiusz.rokosz@dxc.com',
   packages=['mastermind'],
   install_requires=["fastapi",
                     "motor",
                     "gunicorn",
                     "uvicorn"]
)
