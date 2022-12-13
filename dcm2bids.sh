#!/bin/bash

# take the animal number, dicom directory, and task and convert them to bids format

#
# TODO: take in the name
# TODO: the task
# TODO: cut the videos to match the name
# TODO: phase or magnitude
# TODO: normal phase or reverse phase
# TODO: how the dicom should be organized
# TODO: zeropad the earpunch number to 3 places
# TODO: list of possible answers for task
# TODO: take the TTL file as well
# TODO: take the videos if the task matches whatever you define as video task
# TODO: add extra desription to the script does

function Usage {
    cat <<USAGE

Usage:

`basename $0` -d DICOM_DIR -i Animal_ID -t Task

Compulsory arguments:


     -h:  display help message

     -d:  the directory that contains the dicom files

     -i:  animal ID, should be in this format EarPunchNo_CageNo_Gender

     -t:  type of task (or lack of)



Example:

`basename $0` \
-d /Users/aeed/Documents/Work/Menon^AS-MBN/01_389630_M/20221119/DICOM \
-i 01_389630_M \
-t whisker_stimulation

USAGE
    exit 1
}


if [[ "$1" == "-h" || $# -eq 0 ]];
  then
    Usage >&2
  fi

while getopts "h:d:i:t:" OPT
  do
  case $OPT in
      h) #help
   Usage
   exit 0
   ;;
      d)  # template
   DICOM_DIR=$OPTARG
   ;;
      i)  # input image
   ANIMAL_ID=$OPTARG
   ;;
      t)  # output dir
   TASK=$OPTARG
   ;;
     \?) # getopts issues an error message
   echo "$Usage" >&2
   exit 1
   ;;
  esac
done
