#!/bin/bash
source ./docker/sdk_version.sh

docker build -t bank_account_monitor_sdk:$SDK_VERSION ./docker/