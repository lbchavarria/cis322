#!/bin/bash
git clone https://github.com/postgres/postgres.git
cd postgres/
./configure
make
make install
cd ..
curl -O http://www.trieuvan.com/apache//httpd/httpd-2.4.25.tar.gz
gunzip httpd-2.4.25.tar.gz
tar -xvf httpd-2.4.25.tar
cd httpd-2.4.25/
./configure 
make
make install
cd ..
