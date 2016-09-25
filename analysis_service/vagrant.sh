#!/usr/bin/env bash
sudo apt-get install -y expat libexpat1-dev unzip build-essential python-dev python-pip

#Setup flawfinder
wget http://www.dwheeler.com/flawfinder/flawfinder-1.31.tar.gz
tar -xvf flawfinder-*
cd flawfinder-*
sudo make prefix=/usr install
cd ..

#Setup rats
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/rough-auditing-tool-for-security/rats-2.4.tgz
tar -xvf rats-*
cd rats-*
./configure
make
sudo make install

#Setup the analysis service
cd /vagrant
sudo pip install virtualenv
virtualenv .env --always-copy --no-site-packages
source .env/bin/activate
pip install -r requirements.txt
python server.py
