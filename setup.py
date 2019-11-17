from setuptools import find_packages
from setuptools import setup

setup(
    name='hx711_scale',
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    py_modules=[],
    install_requires=['setuptools'],
    author='Alex Rössler',
    author_email='alex@machinekoder.com',
    maintainer='Alex Rössler',
    maintainer_email='alex@machinekoder.com',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='HX711 based scale for ROS2.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'scale_node = hx711_scale.scale_node:main',
        ],
    },
)
