#!/bin/sh
# this will install everything as root, so take that into account before you run it

# avoid "cannot open shared object file" ImportErrors; make sure the libraries are accessible in LD_LIBRARY_PATH
# if you want a more permanent solution, try echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH` >> ~/.bashrc
# here we are attempting to head the problem off by exporting it first.  it should be added to the path inside the binary
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH


# need cmake, python development headers, ZLib and OpenSSL
sudo apt-get install cmake python2.7-dev zlib1g-dev libssl-dev python3.3-dev

mkdir libgit && cd libgit

git clone git://github.com/libgit2/libgit2.git

cd libgit2

# instructions from http://libgit2.github.com/#install
mkdir build && cd build
cmake ..
cmake --build .
sudo cmake --build . --target install

cd ../../

# instructions from https://github.com/libgit2/pygit2/blob/master/README.rst
git clone git://github.com/libgit2/pygit2.git
cd pygit2
sudo python setup.py install
sudo python3.3 setup.py install



# clean up after ourselves
cd ../../
rm -rf libgit/

# now, from the python interpreter:
# >>> from pygit2 import Repository
# if you don't get any errors, you're done!

sudo ldconfig
