from setuptools import setup

requirements = ['domonic',
     'html5lib',
     'plotly',
     'pandas',
     'numpy',
     'entsoe-py'
     ]

setup(
    name='opendc-eesr',
    version='0.0.1',    
    description='An OpenDC extension for reporting energy efficiency and sustanability.',
    url='https://github.com/philippsommer27/opendc-eesr',
    author='Philipp Sommerhalter',
    author_email='philippsommerhalter@gmail.com',
    license='Apache Software License 2.0',
    packages=['opendc-eesr'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research/Developers',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)