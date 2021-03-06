# Copyright (c) Microsoft Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import subprocess

folder = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(folder, "build")):
    shutil.rmtree(os.path.join(folder, "build"))
if os.path.exists(os.path.join(folder, "dist")):
    shutil.rmtree(os.path.join(folder, "dist"))
if os.path.exists(os.path.join(folder, "playwright.egg-info")):
    shutil.rmtree(os.path.join(folder, "playwright.egg-info"))

subprocess.run("python setup.py sdist bdist_wheel", shell=True)
