#!/bin/bash

HERE=$(pwd)
INSTALLDIR='/tmp/pyropossum-install/'
mkdir -p $INSTALLDIR
cd $INSTALLDIR
wget https://github.com/stevenorum/pyropossum/archive/master.zip -O $INSTALLDIR/pyropossum-master.zip
unzip $INSTALLDIR/pyropossum-master.zip
cd ${INSTALLDIR}/pyropossum-master
pip3 install -r ${INSTALLDIR}/pyropossum-master/requirements.txt
python3 ${INSTALLDIR}/pyropossum-master/setup.py install
cp ${INSTALLDIR}/pyropossum-master/etc/init.d/pyropossum /etc/init.d/pyropossum
mkdir -p /etc/pyropossum
cp ${INSTALLDIR}/pyropossum-master/config.json /etc/pyropossum/config.json
chmod +x /etc/init.d/pyropossum
# For some reason this isn't currently working through /usr/sbin/service, so make the raw call instead.
/etc/init.d/pyropossum start
cd $HERE
rm -rf $INSTALLDIR
