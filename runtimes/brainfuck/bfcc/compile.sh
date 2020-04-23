#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ruby $DIR/bfcc.rb $1 < $2 > $DIR/out.c
gcc $DIR/out.c -o $(dirname $2)/submission -Ofast
rm $DIR/out.c
