#!/bin/bash

while getopts 'u:' flag; do
  case "${flag}" in
    u) url="${OPTARG}" ;;
    *) exit 1 ;;
  esac
done

python anagram_palyndrom_finder.py -url ${url}