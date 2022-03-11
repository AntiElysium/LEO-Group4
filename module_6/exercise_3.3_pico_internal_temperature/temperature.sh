#!/bin/bash

# You need to do this shit first:
# screen /dev/ttyACM0
# ctrl A \


read data < /dev/ttyACM0
echo $data
