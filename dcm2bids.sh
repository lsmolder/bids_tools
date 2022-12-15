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
# TODO: test on Arthur's Brown data as well
# TODO: delete all unnecessary dirs
# TODOL multiple sessions, maybe add an extra flag or make conditional if subject existed
# TODO: take in session number as well
# TODO: accept field maps as well


function Usage {
    cat <<USAGE

Usage:

Convert the dicom files from the discom server to BIDS format

`basename $0` -d DICOM_ZIP -i Animal_ID -t Task -d BIDS_DIR

Compulsory arguments:


     -h:  display help message

     -z:  the dcm zip file that contains the dicom files from dcm server (abspath)

     -i:  animal ID, should be in this format EarPunchNo_CageNo_Gender

     -s: session number

     -t:  type of task (or lack of)

     -d:  directory where you want to put your nifti BIDS output (abspath)



Example:

`basename $0` \
-z /Users/aeed/Documents/Work/Menon^AS-MBN/01_389630_M/20221119/DICOM \
-i 01_389630_M \
-s s1 \
-t whisker_stimulation \
-d /Users/aeed/Documents/Work/Menon^AS-MBN/01_389630_M/20221119/BIDS

USAGE
    exit 1
}


if [[ "$1" == "-h" || $# -eq 0 ]];
  then
    Usage >&2
  fi

while getopts "h:z:i:s:t:d:" OPT
  do
  case $OPT in
      h) #help
   Usage
   exit 0
   ;;
      z)  # zipped dcm file
   DICOM_ZIP=$OPTARG
   ;;
      i)  # animal id
   ANIMAL_ID=$OPTARG
   ;;
   s)  # animal id
   SESSION_NO=$OPTARG
   ;;
      t)  # task type
   TASK=$OPTARG
   ;;
      d)  # output bids dir
   BIDS_DIR=$OPTARG
   ;;
     \?) # getopts issues an error message
   echo "$Usage" >&2
   exit 1
   ;;
  esac
done


# decompress the dcm file in the zipped file dir
ZIP_DIR=`dirname ${DICOM_ZIP}` # get the parent dir
unzip ${DICOM_ZIP} -d ${ZIP_DIR}


heudiconv \
--files ${ZIP_DIR}  \
--outdir ${BIDS_DIR}  \
--subjects ${ANIMAL_ID}   \
--ses ${SESSION_NO} \
--heuristic heuristic_9T.py  \
--converter dcm2niix \
--bids \
--overwrite
