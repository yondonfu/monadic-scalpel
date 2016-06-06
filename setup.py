from setuptools import setup

def read_requirements(filename):
    try:
        with open(filename) as f:
            return f.read().splitlines()
    except IOError:
        import os
        raise IOError(os.getcwd())

setup(name="monadic-scalpel",
      version="0.1",
      description="Python web scraping library using monadic programming",
      url="http://github.com/yondonfu/monadic-scalpel",
      author="Yondon Fu",
      author_email="yondon.fu@gmail.com",
      license="MIT",
      packages=["monadic_scalpel"],
      install_requires=read_requirements("requirements.txt"),
      zip_safe=False)
