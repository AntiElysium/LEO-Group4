#!/bin/bash

# You need to do this shit first:
# screen /dev/ttyACM0
# ctrl A \


read data < /dev/ttyACM0
echo $data

curl "https://api.thingspeak.com/update?api_key=MMW4VLHXUMV3Q980&field1=${data}"
