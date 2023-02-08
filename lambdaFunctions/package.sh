#!/bin/bash

set -e

if [ "$#" != "1" ]; then
    >&2 echo "Usage: $0 [directory of lambda function]"
    exit 1
fi
directory=$1

cd $directory
rm -rf package deployment.zip .aws-sam
zip -r deployment.zip .
pip install -r requirements.txt --target ./package
cd package
zip -r ../deployment.zip .
cd ..
chmod 755 deployment.zip
rm -rf package
echo "Done!"
exit 0