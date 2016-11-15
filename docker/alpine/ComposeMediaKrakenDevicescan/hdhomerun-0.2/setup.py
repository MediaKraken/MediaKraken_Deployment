from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='hdhomerun',
      version='0.2',
      description='Python bindings for libhdhomerun',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia :: Video :: Capture',
        'Topic :: Software Development :: Libraries',
      ],
      keywords='libhdhomerun hdhomerun',
      url='http://github.com/s-clark/python-hdhomerun',
      author='Stuart Clark',
      author_email='stuart.clark@Jahingo.com',
      license='MIT',
      packages=['hdhomerun'],
      include_package_data=True,
      zip_safe=False)
