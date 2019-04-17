from setuptools import setup, find_packages


setup(
    name='lampy',
    version='1.0.0',
    description='Functional Programming for Python',
    url='https://github.com/Lgneous/Lampy',
    author='Julien Chedal-Anglay',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='functional functions lambda',
    packages=find_packages(exclude=['docs', 'tests']),
    python_requires='>=3.5',
    project_urls={
        'Source': 'https://github.com/Lgneous/Lampy',
    },
)
