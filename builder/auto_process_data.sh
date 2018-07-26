#!/bin/bash

# source /grid/fermiapp/products/uboone/setup_uboone.sh

source /uboone/app/users/kalousis/setup_larsoft_merger.sh
 
PROCESSES=`ps aux | grep 'Loop.pl' | wc -l`

MAXPROC=8

[[ $HOST = "hermes" ]] && MAXPROC=8

/usr/bin/perl /uboone/app/users/kalousis/MuCS/builder/auto_wrapper.pl $PROCESSES $MAXPROC