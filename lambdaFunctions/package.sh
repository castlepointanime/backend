#!/bin/bash

set -e

if [ "$#" != "1" ]; then
    >&2 echo "Usage: $0 [directory of lambda function]"
    exit 1
fi
directory=$1
rm -rf package
mkdir package
cp -r ./${directory} ./package 
cd package
pip install -r $directory/requirements.txt --target ${directory}
zip -r deployment.zip docusignLambda
mv deployment.zip ../
cd ..
chmod 755 deployment.zip
rm -rf package
echo "Done!"
exit 0