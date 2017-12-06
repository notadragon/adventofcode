#!/bin/bash

echo $(( $(cat input | sed -e "s/(/+1/g" -e "s/)/-1/g") ))
