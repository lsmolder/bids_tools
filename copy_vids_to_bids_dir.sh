#!/bin/bash

# navigate to the videos dir
cd /Users/aeed/Dropbox/Amr_MR_camera_videos/amr || exit
bids_dir="/Users/aeed/Documents/Work/BIDS/Menon^AS-MBN"
for folder in *;do
  if [ -d "$folder" ]; then
  # change subj name from "44_393072_F" to be "sub-44393072F" to match bids dir

    subj="sub-${folder//_}";
    echo "$subj"
    cd "$folder" || exit
    for ses in ses*;do
      # ses in vid "ses-s1", in bids "ses-01"
      ses_no=$(zeropad "${ses//ses-s}" 2)
      ses_no="ses-${ses_no}"
      echo "$ses"

      # only transfer videos if the subject exists in bids folder
      if [ -d  ${bids_dir}/${subj} ];then
        mkdir -p -- "${bids_dir}/${subj}/${ses_no}/videos"
        cp "$ses"/* "${bids_dir}/${subj}/${ses_no}/videos"

        python \
        /Users/aeed/Documents/Work/bids_tools/bids_tools/rename_videos.py \
        "${bids_dir}/${subj}/${ses_no}"
      fi



    done

    cd ..
  fi
done



