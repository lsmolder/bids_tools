#!/bin/bash
# use the bids_tools to ocnvert the raw data into bids format
# I downloaded all the subjects in one folder from the dicom server
# TODO: some animals are not converted properly, check for example session-02 sub-AppTauApoe4154M8
# TODO: I think I fixed it, but recheck
# TODO: check orientation after update
# define the bids output dir to stroe all subjects

# define your heuristic python script
heuristic="/Users/aeed/Documents/Work/bids_tools/bids_tools/heuristic_9T_rest_awake.py"
dcm_dir="/Users/aeed/Documents/Work/BIDS/dicom"
output_dir="/Users/aeed/Documents/Work/BIDS/Menon^AS-MBN"

# you have to read the folders organized according to date, otherwise 2nd session will be first
# that's why I commented out find
for folder in ${dcm_dir}/*; do
  if [ -d $folder ];then
        #     folder_base=`basename ${folder}`
        #     subject_ID=`echo ${folder_base} | cut -d '/' -f2 | tr -d '^'`
        # for folder in $(find ${dcm_dir} -name '*App*' -type d); do
        # extract the subject ID from the folder name
        echo "${folder}"
        subject_ID=$(basename "$folder" | awk -F'_' '{print $1}')

        # the heudiconv removes the -, so you need to remove it as well form folder's name
        subject_ID=$(echo "${subject_ID}" | tr -d '-')

        echo "subject_ID: ${subject_ID}"
        # cd DICOM
        session_no=1;
        # if the subject exists count how many sessions then add one to get new session's number
        # if [ -d ${output_dir}/sub-"${subject_ID}" ]; then
        # now, the DICOM folder has all the sessions for each subject
        for session in $(ls -d "${folder}/DICOM"/*/); do
          session_no=$(zeropad ${session_no} 2)
          echo ${session_no} 

          heudiconv \
            --files "${session}" \
            -c dcm2niix \
            -o ${output_dir} \
            -ss "${session_no}" \
            -s "${subject_ID}" \
            -f ${heuristic} \
            --bids 
          session_no=$(echo $((session_no + 1)))
          echo "##########################################################"  
        done  

  fi
done
# just in case you want to run one manually:
# folder="/Users/aeed/Documents/Work/Brown^TBI2AD/DICOM/20221124/AppTauApoe4-15-4M8/20221124_01.DB8FF776/"
# session_no="2"
# subject_ID="AppTauApoe4154M8"
# output_dir="/Users/aeed/Documents/Work/Brown^TBI2AD/bids"
# heuristic="/Users/aeed/Documents/Work/bids_tools/bids_tools/heuristic_9T_Brown^TBI2AD.py"
