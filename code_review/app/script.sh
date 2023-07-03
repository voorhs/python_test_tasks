#! /bin/bash

# this srcipt
#   handles case of missing data
#   implements logic that data archive should be prodived separately from image build (via mounted volume for docker container)

if [ -f /data/data.tgz ]; then
    tar zxf /data/data.tgz
else
    echo SIGMA BASED CSV CHECKER: data.tgz is not found in working directory, you should place here data.tgz containing data.csv
    exit 1
fi

python3 csv_sum.py