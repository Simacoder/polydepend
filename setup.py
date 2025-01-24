from setuptools import setup, find_packages

setup(
    name="polydepend",
    version="1.0.0",
    author="Simanga Mchunu",
    author_email="datawithsima@gmail.com",
    description="A cross-language dependency resolver and manager.",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'polydepend=cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
