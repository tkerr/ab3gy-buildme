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
# Copyright (c) 2024 Tom Kerr AB3GY (ab3gy@arrl.net).
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
import os
import sys
import shutil
import yaml
from pathlib import Path


###########################################################################
# Globals.
########################################################################### 
scriptname = os.path.basename(sys.argv[0])


###########################################################################
# Main program.
########################################################################### 
if __name__ == "__main__":
    # Usage: _buildme.py <package-list.yml>
    
    if (len(sys.argv) < 2):
        print('No YAML package list file specified.')
        print('Usage: {} <package-list.yml>'.format(scriptname))
        sys.exit(1)
        
    yml_file = sys.argv[1]
    if os.path.isfile(yml_file):
        try:
            with open(yml_file) as yf:
                yd = yaml.safe_load(yf)
        except Exception as err:
            print('Error reading {}: {}'.format(yml_file, str(err)))
            sys.exit(1)
    else:
        print('File not found: {}'.format(yml_file))
        sys.exit(1)

    for pkg in yd["packages"]:
        print(pkg['name'])
        src_base = os.path.abspath(pkg['src_path'])
        dst_base = os.path.abspath(pkg['dst_path'])
        for file in pkg['files']:
            src_file = os.path.join(src_base, file)
            dst_file = os.path.join(dst_base, file)
            (dirname, filename) = os.path.split(dst_file)
            Path(dirname).mkdir(parents=True, exist_ok=True)
            if os.path.isfile(src_file):
                try:
                    shutil.copy2(src_file, dst_file)
                except Exception as err:
                    print('Error copying {}: {}'.format(src_file, str(err)))
                    sys.exit(1)
            else:
                print('File not found: {}'.format(src_file))
