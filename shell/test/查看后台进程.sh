#!/bin/bash
status=$(ps -ef |grep docker |grep -v 'grep'|wc -l)

if test $status -gt 0;then
    echo "有"；
else
    echo "无:""$status";
fi;
