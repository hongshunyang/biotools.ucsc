#!/bin/bash

## for i in `seq 2 16`;do cp -a 20170611-1 20170611-$i;done
## for i in `seq 2 16`;do rm -rf 20170611-$i;done

./app.py -c ../data/20170611-1 -t 2500 -o 25 -e 3 -f 1
./app.py -c ../data/20170611-2 -t 2500 -o 25 -e 3 -f 5
./app.py -c ../data/20170611-3 -t 2500 -o 25 -e 5 -f 1
./app.py -c ../data/20170611-4 -t 2500 -o 25 -e 5 -f 5

./app.py -c ../data/20170611-5 -t 2500 -o 20 -e 3 -f 1
./app.py -c ../data/20170611-6 -t 2500 -o 20 -e 3 -f 5
./app.py -c ../data/20170611-7 -t 2500 -o 20 -e 5 -f 1
./app.py -c ../data/20170611-8 -t 2500 -o 20 -e 5 -f 5

./app.py -c ../data/20170611-9 -t 500 -o 25 -e 3 -f 1
./app.py -c ../data/20170611-10 -t 500 -o 25 -e 3 -f 5
./app.py -c ../data/20170611-11 -t 500 -o 25 -e 5 -f 1
./app.py -c ../data/20170611-12 -t 500 -o 25 -e 5 -f 5

./app.py -c ../data/20170611-13 -t 500 -o 20 -e 3 -f 1
./app.py -c ../data/20170611-14 -t 500 -o 20 -e 3 -f 5
./app.py -c ../data/20170611-15 -t 500 -o 20 -e 5 -f 1
./app.py -c ../data/20170611-16 -t 500 -o 20 -e 5 -f 5

./app.py -c ../data/20170611-17 -t 100 -o 20 -e 3 -f 1
./app.py -c ../data/20170611-18 -t 100 -o 20 -e 5 -f 1
./app.py -c ../data/20170611-19 -t 100 -o 20 -e 8 -f 1
./app.py -c ../data/20170611-20 -t 100 -o 20 -e 10 -f 1
./app.py -c ../data/20170611-21 -t 50 -o 20 -e 3 -f 1
./app.py -c ../data/20170611-22 -t 50 -o 20 -e 5 -f 1
./app.py -c ../data/20170611-23 -t 50 -o 20 -e 10 -f 1
./app.py -c ../data/20170611-24 -t 20 -o 20 -e 3 -f 1
./app.py -c ../data/20170611-25 -t 20 -o 20 -e 5 -f 1
