from setuptools import setup

setup(
    name='TimeMachine',
    version='1.0',
    packages=['comparer', 'reporter', 'archiever', 'retriever', 'utilities', 'interactor', 'database_expert'],
    url='https://github.com/eaingaran/TimeMachine',
    license='MIT License',
    author='Aingaran Elango',
    author_email='eaingaran@gmail.com',
    description='A databse testing tool that keeps track of data across releases.'
)
