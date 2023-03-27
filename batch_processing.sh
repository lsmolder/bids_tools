#!/bin/bash

# incase you downlaoded a compressed dicom with many folders
# just uncompress,
# awakeMice_dicom/20221226>
# 04_393073_M^^^^ 06_393073_M^^^^ 41_393072_F^^^^ 44_393072_F^^^^
# 05_393073_M^^^^ 07_393073_M^^^^ 43_393072_F^^^^
for folder in *; do
  name=$(echo "${folder}" | sed 's/\^\^\^\^//g')
  echo "${name}"
  heudiconv \
  --files "${PWD}"/"${folder}" \
  --outdir /Users/aeed/Documents/Work/awakeMice_Grandjean/bids \
  --subjects $(zeropad "$name" 12) \
  --ses s1 \
  --heuristic /Users/aeed/Documents/Work/bids_tools/bids_tools/heuristic_9T_rest_awake.py \
  --converter dcm2niix \
  --bids \
  --overwrite
done
