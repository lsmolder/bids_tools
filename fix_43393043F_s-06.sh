#!/bin/bash
#for subject 43393072F_s-06
#it appears that I duplicated some of the runs and did not organize them properly and now there is a duplicate of
#run-01 and run-02
#the mag and phase are not organized as xx0001 and xx0002, instead as 3 and 4
#you have to correct this manually to get it to work properly with heudiconv
dcm_dir="/Users/aeed/Documents/Work/BIDS/dicom/43393072F/DICOM/20230407/43_393072_F^^^^/20230407_01.99535FC2"

rm -rf ${dcm_dir}/150001
rm -rf ${dcm_dir}/310001

mv ${dcm_dir}/150003 ${dcm_dir}/150001
mv ${dcm_dir}/150004 ${dcm_dir}/150002

mv ${dcm_dir}/190003 ${dcm_dir}/190002

mv ${dcm_dir}/200003 ${dcm_dir}/200002
mv ${dcm_dir}/210003 ${dcm_dir}/210002

mv ${dcm_dir}/220003 ${dcm_dir}/220002

mv ${dcm_dir}/230003 ${dcm_dir}/230002

mv ${dcm_dir}/250003 ${dcm_dir}/250002
mv ${dcm_dir}/260003 ${dcm_dir}/260002

mv ${dcm_dir}/300003 ${dcm_dir}/300002
mv ${dcm_dir}/330003 ${dcm_dir}/330002
mv ${dcm_dir}/340003 ${dcm_dir}/340002
mv ${dcm_dir}/360003 ${dcm_dir}/360002
