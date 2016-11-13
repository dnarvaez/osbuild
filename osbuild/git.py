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
import subprocess
import urlparse

from osbuild import command
from osbuild import config
from osbuild import utils


def _chdir(func):
    def wrapped(*args, **kwargs):
        orig_cwd = os.getcwd()

        os.chdir(args[0].local)
        result = func(*args, **kwargs)
        os.chdir(orig_cwd)

        return result

    return wrapped


class Module:
    def __init__(self, path=None, name=None, remote=None,
                 branch="master", tag=None, retry=10):
        if path is None or name is None or remote is None:
            raise RuntimeError("path, name and remote are required")

        self._compute_remotes(remote)

        self.local = os.path.join(path, name)
        self.tag = tag

        self._path = path
        self._name = name
        self._branch = branch
        self._retry = 10

    def _compute_remotes(self, remote):
        parsed_url = urlparse.urlparse(remote)

        self._remotes = {"origin": remote}

        if parsed_url.netloc != "github.com":
            return

        prefs = config.get_prefs().get("github", {})

        name = os.path.basename(parsed_url.path)

        if parsed_url.path[1:] in prefs.get("ssh", []):
            self._remotes["origin"] = "git@github.com:%s" % parsed_url.path

        for fork in prefs.get("forks", []):
            if name == os.path.basename(fork):
                self._remotes["upstream"] = self._remotes["origin"]
                self._remotes["origin"] = "git@github.com:/%s" % fork

    def _clone(self):
        os.chdir(self._path)

        command.run(["git", "clone", "--progress", self._remotes["origin"],
                     self._name], retry=self._retry)

        os.chdir(self.local)

        command.run(["git", "submodule", "init"])
        command.run(["git", "submodule", "update"])

        for name, remote in self._remotes.items():
            if name != "origin":
                command.run(["git", "remote", "add", name, remote])

        if config.git_user_name:
            command.run(["git", "config", "user.name", config.git_user_name])

        if config.git_email:
            command.run(["git", "config", "user.email", config.git_email])

        if self.tag:
            command.run(["git", "checkout", self.tag])
        else:
            command.run(["git", "checkout", self._branch])

    def exists(self):
        return os.path.exists(os.path.join(self.local, ".git"))

    def update(self, source={}):
        if not self.exists():
            self._clone()
            return

        os.chdir(self.local)

        remote = source.get("repository", self._remotes["origin"])
        revision = source.get("revision", self.tag)

        command.run(["git", "remote", "set-url", "origin", remote])
        command.run(["git", "fetch"], retry=self._retry)
        command.run(["git", "submodule", "update"])

        if revision:
            command.run(["git", "checkout", revision])
        else:
            command.run(["git", "checkout", self._branch])
            command.run(["git", "merge", "--ff-only",
                         "origin/%s" % self._branch])

    @_chdir
    def checkout(self, revision=None):
        if revision is None:
            revision = self.tag
            if revision is None:
                revision = self._branch

        command.run(["git", "checkout", revision])

    @_chdir
    def clean(self):
        result = True

        if not config.interactive:
            command.run(["git", "clean", "-fdx"])
            command.run(["git", "reset", "--hard"])
            return result

        command.run(["git", "clean", "-fdX"])

        files = subprocess.check_output(["git", "ls-files",
                                         "--others"]).strip()
        if files:
            print("\n# The repository contains files which have not been "
                  "added to the index:\n")
            print(files)
            print("\nPress d to delete them, k to keep them.\n")

            while True:
                key = utils.getch()
                if key == "d":
                    command.run(["git", "clean", "-fdx"])
                    break
                elif key == "k":
                    result = False
                    break

        added = subprocess.check_output(["git", "diff", "--cached",
                                         "--name-only"]).strip()
        modified = subprocess.check_output(["git", "ls-files",
                                            "--modified"]).strip()
        deleted = subprocess.check_output(["git", "ls-files",
                                           "--deleted"]).strip()

        if added or modified or deleted:
            print("\n# The repository content has been modified.")

            if added:
                print("\nAdded files:")
                print(added)

            if modified:
                print("\nModified files:")
                print(modified)

            if deleted:
                print("\nDeleted files")
                print(deleted)

            print("\nPress r to reset the changes, k to keep them.\n")

            while True:
                key = utils.getch()
                if key == "r":
                    command.run(["git", "reset", "--hard"])
                    break
                elif key == "k":
                    result = False
                    break

        return result

    @_chdir
    def get_head(self):
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()


def get_module(module):
    return Module(path=config.get_source_dir(),
                  name=module.name,
                  remote=module.repo,
                  branch=module.branch,
                  tag=module.tag,
                  retry=10)
