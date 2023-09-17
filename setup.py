from setuptools import setup, find_packages


long_description = """IP2Location Toolkit Allows User To Easily Download IP2Location and IP2Proxy Databases and Helps The User To Easily Find The Right Database based on the database contents, IP type (IPv4 or IPv6) and Database format."""
setup(
    name='ip2location_toolkit',
    version='0.1.0',
    description='IP2Location Toolkit Allows User To Easily Download IP2Location and IP2Proxy Databases.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Abdallah Ragab',
    author_email='abdallahsamehragab1@gmail.com',
    url='https://github.com/Abdallah-Ragab/ip2location_toolkit',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Internet :: Log Analysis',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: System :: Networking',
    ],
    python_requires='>=3.0',
    requires=[
        'requests',
        'tqdm',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'ip2location-toolkit=ip2location_toolkit:run',
        ],
    },
    )
