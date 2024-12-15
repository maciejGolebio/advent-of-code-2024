#!bin/bash

# Create a directory for the current day

# Get the current day of December
day=$(date +%d)
day='14'

mkdir -p day$day
mkdir -p day$day/part1
mkdir -p day$day/part2

touch day$day/part1/input.txt
touch day$day/part2/input.txt
touch day$day/part1/main.py
touch day$day/part2/main.py