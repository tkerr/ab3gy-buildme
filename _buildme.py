###############################################################################
# _buildme.py
# Author: Tom Kerr AB3GY
#
# A script used to build my personal package directory.  Does not adhere
# to any python package build conventions.  Copies files from other 
# repositories.
#
# Uniquely named to avoid conflict with standard package build scripts 
# e.g., setup.py
#
# Designed for personal use by the author, but available to anyone under the
# license terms below.
###############################################################################

###############################################################################
# License
# Copyright (c) 2023 Tom Kerr AB3GY (ab3gy@arrl.net).
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,   
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,  
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
###############################################################################

import git     # pip install GitPython
import getopt
import os
import shutil
import sys


###########################################################################
# Globals.
########################################################################### 

# The list of top-level repo directories.
# You MUST use the path separator specified by os.path.sep.
# DO NOT add the path separator to the end of the string.
REPO_LIST = [
    r'D:\dev\AB3GY\python-repos\ab3gy-adif',
    r'D:\dev\AB3GY\python-repos\ab3gy-dxentity',
    r'D:\dev\AB3GY\python-repos\ab3gy-PyRigCat',
    r'D:\dev\AB3GY\python-repos\ab3gy-pyutils',
    r'D:\dev\AB3GY\python-repos\ab3gy-wsjtx',
]


###########################################################################
# Functions.
########################################################################### 

# ------------------------------------------------------------------------
def remove(object, target):
    if object in target:
        target.remove(object)
    return target

# ------------------------------------------------------------------------
def get_repo_files(repo):
    repo_files = []
    for root, dirs, files in os.walk(repo):
        remove('.git', dirs)
        remove('.gitignore', files)
        remove('license.txt', files)
        remove('README.md', files)
        for file in files:
            filespec = os.path.join(root, file)
            repo_files.append(filespec)
    return repo_files

# ------------------------------------------------------------------------
def create_init_file(filespec):
    try:
        file = open(filespec, 'w')
        file.write('"""Empty __init__.py module to identify this directory as a package directory"""\n')
    except Exception as err:
        print(str(err))
    try:
        file.close()
    except Exception:
        pass


###########################################################################
# Main program.
########################################################################### 
if __name__ == "__main__":

    # Usage: _buildme.py [-fv] [pkg_dir]
    
    git_fetch = False
    verbose = False
    
    # Get command line options.
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'fv')
    except (getopt.GetoptError) as err:
        print(str(err))
        sys.exit(1)
    
    for (o, a) in opts:
        if (o == '-f'):
            git_fetch = True
        elif (o == '-v'):
            verbose = True
    
    # Get optional destination root path.
    dst_root = os.path.abspath('.')
    if (len(args) > 0):
        dst_root = os.path.abspath(args[0])
    if verbose: print('Package directory: {}'.format(dst_root))
    
    # Copy files from each repository.
    for repo_name in REPO_LIST:
    
        # Fetch files from the repo to ensure it is up to date.
        if git_fetch:
            my_repo = git.Repo(repo_name)
            for remote in my_repo.remotes:
                if verbose:
                    print('Fetching from {} {}'.format(repo_name, remote))
                remote.fetch()
            
        repo_files = get_repo_files(repo_name)
        for src_file in repo_files:
            # Remove the top-level repo directory.
            (prefix, match, suffix) = src_file.partition(repo_name + os.path.sep)
            
            # Create the local directory and copy the file.
            dst_file = os.path.join(dst_root, suffix)
            dst_dir = os.path.dirname(dst_file)
            if verbose: print(dst_file)
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(src_file, dst_file)
    
    # Create an empty __init__.py file if it does not exist.
    initfile = os.path.join(dst_root, '__init__.py')
    if not os.path.isfile(initfile):
        if verbose: print('Creating {}'.format(initfile))
        create_init_file(initfile)
