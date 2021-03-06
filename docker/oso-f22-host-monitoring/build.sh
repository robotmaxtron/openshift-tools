#!/bin/bash

sudo echo -e "\nTesting sudo works...\n"

# We MUST be in the same directory as this script for the build to work properly
cd $(dirname $0)

# Make sure pcp-base is built with latest changes since we depend on it.
if ../pcp-base/build.sh ; then
  # Build ourselves
  echo
  echo "Building oso-f22-host-monitoring..."
  sudo time docker build $@ -t oso-f22-host-monitoring . && \
  sudo docker tag -f oso-f22-host-monitoring docker-registry.ops.rhcloud.com/ops/oso-f22-host-monitoring
fi
