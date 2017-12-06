#!/bin/bash

cat input | sed -e "s/(/+\n/g" -e "s/)/-\n/g" | (
    J=0
    I=0
    while read line ; do
        if [ "${line}" = "" ] ; then
            continue
        fi
        
        J=$((${J}+1))
        case "${line}" in
            +)
                I=$((${I}+1))
                ;;
            -)
                I=$((${I}-1))
                ;;
        esac
        if (( "${I}" < 0 )) ; then
            echo "${J}: change:${line} floor:$I"
            break;
        fi
    done
)

                                                       
                                                      
