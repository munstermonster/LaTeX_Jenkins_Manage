# Andrew Gloster
# August 2018
# Python script to compile changed documents on Jenkins

# Copyright 2018 Andrew Gloster

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#------------------------------------
# Import relevant python modules
#------------------------------------

import os
from subprocess import Popen, PIPE
import sys

# ---------------------------------------------------------------------
# Main Program Begin
# ---------------------------------------------------------------------

# Get the current directory as this can be useful later
dirCurrent = os.getcwd()

# List of changed .tex files
listTex = []

# Command to pick up the changed .tex files between this commit and the previous one
cmdChanged = 'git diff --name-only HEAD^ HEAD'

# Run this command and wait to complete
run = Popen([cmdChanged], shell = True, stdout = PIPE, stdin = PIPE)
run.wait()

# Pick out the .tex files returned by the diff
texfiles = [line for line in run.stdout if line.endswith(".tex\n")]

# Check that .tex files exist and aren't in the diff because they were deleted. (There's probably a different diff command that would have presorted this.)
texfiles = [texfile for texfile in texfiles if os.path.exists(texfile)]

# Loop over the standard out to recover the file names
for file in texfiles:

	# Use / to split into file names and add the folder end needed
	path = os.path.split(file)[0] + '/'

	# Add in backslash for cd where there are spaces
	path = path.replace(" ", "\\ ")

	# Pick out tex file name
	tex = os.path.split(file)[1]

	# Change folder from current
	cmdCD = 'cd ' + path + ' \n'

	# Run latexmk on file
	cmdLatex = ' latexmk -pdf -halt-on-error ' + tex

	# Stick together to make one command
	cmdBuikd = cmdCD + cmdLatex

	# Call the subprocess
	latex = Popen([cmdBuikd], shell = True, stdout = PIPE, stdin = PIPE)

	# Use communicate to prevent deadlock
	[latexOutput, latexErr] = latex.communicate()

	# Wait till finish
	latex.wait()

	# Throw an error is unsuccessful
	if latex.returncode is not 0:
		print(latexOutput)
		sys.exit(-1)
