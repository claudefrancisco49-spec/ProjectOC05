#!/bin/sh

echo "---------------------------------"
echo "Running unit tests csv ..."
echo "---------------------------------"
#echo $(pwd)
#echo $(ls /usr/local/bin)

python test_csv.py

if [ $? -ne 0 ]; then
    echo "X Tests failed. Stopping."
    exit 1
fi

echo "---------------------------------"
echo "Tests passed V"
echo "Running main program..."
echo "---------------------------------"

python main.py

echo "---------------------------------"
echo "Running unit tests mongodb ..."
echo "---------------------------------"
# echo "To do ..."
python test_mongodb.py
