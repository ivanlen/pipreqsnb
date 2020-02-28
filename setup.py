import setuptools

setuptools.setup(
    name='pipreqsnb',
    version='0.1',
    description='A pipreqs wrapper that supports notebooks',
    url='https://github.com/ivanlen/pipreqsnb',
    author='Ivan Lengyel',
    author_email='ivalengy@gmail.com',
    entry_points={
        'console_scripts': ['pipreqsnb=pipreqsnb.pipreqsnb:main'],
    },
    # scripts=['pipreqsnb/pipreqsnb.py'],
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['pipreqs'],
    zip_safe=False)
