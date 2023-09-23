#!/bin/bash

source ./docker/sdk_version.sh

docker run --net host --rm -v $PWD:/bank_account_monitor/ -w /bank_account_monitor/ -it bank_account_monitor_sdk:$SDK_VERSION  /bin/bash