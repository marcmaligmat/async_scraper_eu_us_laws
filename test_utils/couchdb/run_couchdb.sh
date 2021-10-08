#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
docker run -v $SCRIPT_DIR/local.ini:/opt/couchdb/etc/local.ini -p 5984:5984 --rm -it couchdb
