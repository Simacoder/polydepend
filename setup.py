from setuptools import setup, find_packages

setup(
    name='polydepend',
    version='1.3.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    # Dependencies
    install_requires=[
        'requests>=2.25.0',
        'packaging',  # Handles version parsing
    ],

    # Development dependencies
    extras_require={
        'dev': [
            'pytest',
            'coverage',
            'black',
            'mypy'
        ]
    },

    # CLI and GUI entry points
    entry_points={
        'console_scripts': [
            'polydepend-cli=cli:main',
            'polydepend-gui=gui:main'
        ]
    },

    # Metadata
    author='Simanga Mchunu',
    author_email='datawithsima@gmail.com',
    description='Multi-language Dependency Management Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Simacoder/polydepend',

    # Classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Software Distribution'
    ],

    # Requirements
    python_requires='>=3.7',

    # Include additional files specified in MANIFEST.in
    include_package_data=True,
)
