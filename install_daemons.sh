#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: ./install_daemons.sh <prefix>"
	exit;
fi

git clone https://github.com/postgres/postgres.git pg_build
cd pg_build
git checkout REL9_6_STABLE
./configure --prefix=$1
make install
cd ..

curl https://archive.apache.org/dist/httpd/httpd-2.4.12.tar.gz > httpd-2.4.12.tar.gz
tar -zxf httpd-2.4.12.tar.gz
cd httpd-2.4.12
./configure --prefix=$1
make install
cd ..

rm -rf pg_build httpd=2.4.12.tar.gz httpd-2.4.12
