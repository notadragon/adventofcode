#!/bin/bash

echo $(( $(cat input2 | sed -e "s/(/+1/g" -e "s/)/-1/g") ))
