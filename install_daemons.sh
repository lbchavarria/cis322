#!/bin/bash
git clone https://github.com/postgres/postgres.git
./configure
make
make install
adduser osnapdev
curl -O http://www.trieuvan.com/apache//httpd/httpd-2.4.25.tar.gz
gunzip httpd-2.4.25.tar.gz
tar -xvf httpd-2.4.25.tar
./configure --prefix=$HOME/installed
make
make install
