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
import signal
import string
import random

from osbuild import config
from osbuild import command


def run(cmd, **kwargs):
    args = [cmd]

    prefs = config.get_prefs()

    if "resolution" in prefs:
        args.extend(["--resolution", prefs["resolution"]])

    if "output" in prefs:
        args.extend(["--output", prefs["output"]])

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    command.run(args, **kwargs)


def collect_logs(source_path, log_path):
    logs = {}

    if not os.path.exists(source_path):
        return

    for filename in os.listdir(source_path):
        if filename.endswith(".log"):
            path = os.path.join(source_path, filename)
            with open(path) as f:
                logs[filename] = f.read()

    with open(log_path, "a") as f:
        for filename, log in logs.items():
            f.write("\n===== %s =====\n\n%s" % (filename, log))


def _get_random_id():
    return ''.join(random.choice(string.letters) for i in range(8))
