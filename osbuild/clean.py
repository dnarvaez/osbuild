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

from osbuild import build
from osbuild import state
from osbuild import docs


def clean(continue_on_error=True):
    print("\n= Clean =\n")

    if not build.clean(continue_on_error=continue_on_error):
        if not continue_on_error:
            return False

    docs.clean()
    state.clean()

    return True
