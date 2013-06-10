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

import os
import shutil

from osbuild import config
from osbuild import command


def build():
    print("\n= Building docs =\n")

    clean()

    for module in config.load_modules():
        if module.has_docs:
            print("* Generating %s" % module.name)
            os.chdir(module.get_source_dir())
            output_dir = os.path.join(config.docs_dir, module.docs_dir)
            command.run(["docker", "-I", "-c", "default", "-o", output_dir,
                         "--extras" "addHeader"])

    return True


def clean():
    try:
        shutil.rmtree(os.path.join(config.docs_dir))
    except OSError:
        pass
