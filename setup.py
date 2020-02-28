import setuptools

with open('README.md') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='pipreqsnb',
    version='0.1.1',
    description='A pipreqs wrapper that supports notebooks',
    url='https://github.com/ivanlen/pipreqsnb',
    author='Ivan Lengyel',
    author_email='ivalengy@gmail.com',
    entry_points={
        'console_scripts': ['pipreqsnb=pipreqsnb.pipreqsnb:main'],
    },
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['pipreqs'],
    zip_safe=False)
