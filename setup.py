# Copyright 2013 Daniel Narvaez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
from setuptools import setup, Extension
from distutils.cmd import Command

classifiers = ["License :: OSI Approved :: Apache Software License",
               "Programming Language :: Python :: 2",
               "Topic :: Software Development :: Build Tools"]


class LintCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.check_call(["pep8", "osbuild"])
        subprocess.check_call(["pyflakes", "osbuild"])


setup(name="osbuild",
      packages=["osbuild"],
      version="0.33",
      description="Pull, build and test multiple source modules",
      author="Daniel Narvaez",
      author_email="dwnarvaez@gmail.com",
      url="http://github.com/dnarvaez/osbuild",
      classifiers=classifiers,
      test_suite="osbuild.tests",
      cmdclass={"lint": LintCommand},
      install_requires=["plog==0.16",
                        "json-format==0.1",
                        "pygments==2.7.4"])
