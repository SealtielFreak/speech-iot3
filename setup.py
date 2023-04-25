import setuptools


setuptools.setup(name="speech-iot3",
      version="1.0",
      description="",

      author="Diego Sealtiel Valderrama Garcia",
      license="MIT",
      url="https://github.com/SealtielFreak/speech-iot3",

      scripts=['user_register.py'],

      packages=['iot3'],
      install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)
