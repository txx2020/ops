#!/bin/bash

com1=(
b
c
d
);
for iuser   in "${com1[@]}" ; do
    if test $iuser = "b" ;then
       echo "1";
    else
       echo "  ";
    fi;
done;