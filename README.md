# BIDS TOOLS
* Scripts to organize 9.4T data and videos into BIDS format
* The data from the dicom server is downloaded as a zipped file containing all the data in dcm format
* The data (after unzipping it) is usually organized as follow:

```
DICOM
└── 20221119
    └── Menon^AS-MBN^^^^
        └── 20221119_01.A0002D22
            ├── 170001
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.170001.1.20221119.7BAD6A76.dcm
            ├── 170002
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.170002.1.20221119.FFC1FD2B.dcm
            ├── 180001
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.180001.1.20221119.CEE9FC56.dcm
            ├── 180002
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.180002.1.20221119.672ABE33.dcm
            ├── 190001
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.190001.1.20221119.75D4BDB3.dcm
            ├── 190002
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.190002.1.20221119.60725C8A.dcm
            ├── 200001
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.200001.1.20221119.28625D6F.dcm
            ├── 200002
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.200002.1.20221119.794EF2FF.dcm
            ├── 210001
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.210001.1.20221119.0A900199.dcm
            ├── 210002
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.210002.1.20221119.F4DD181B.dcm
            ├── 220001
            │   └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.220001.1.20221119.34A371B7.dcm
            └── 50001
                └── Menon^AS-MBN^^^^.MR.Menon^AS-MBN.50001.1.20221119.BF04DF23.dcm
```
**The dcm2bids.sh takes the zipped file, animal id, session no, type of fmri data (if any), \noutput dir, and a heuristic file**


```
>>> ./dcm2bids.sh \
-z /Users/aeed/Documents/Work/bids_tools/2.16.756.5.5.200.8323328.47756.1669482679.1142.zip   \
-i 10_389629_F  \
-s s1 \
-t rest \
-d /Users/aeed/Documents/Work/bids_tools \
-f heuristic_9T_rest_awake.py
```

**The heuristic files are tailored towards different projects, but it is easy to modify for a new project**

**The preferred animal id is: EarPunchNo_CageNo_Gender e.g. 10_389629_F. The EarPunch no gets zeropadded to be 3 digits**
**The final subject name will be: sub-010389629F**

### The bids output will look like:
```
sub-010389629F/
└── ses-s1
    ├── anat
    │   ├── sub-00010389629F_ses-s1_run-001_T2w.json
    │   └── sub-00010389629F_ses-s1_run-001_T2w.nii.gz
    ├── fmap
    │   ├── sub-00010389629F_ses-s1_B0MAP.json
    │   └── sub-00010389629F_ses-s1_B0MAP.nii.gz
    ├── func
    │   ├── sub-00010389629F_ses-s1_task-rest_run-001_bold_magnitude_R.json
    │   ├── sub-00010389629F_ses-s1_task-rest_run-001_bold_magnitude_R.nii.gz
    │   ├── sub-00010389629F_ses-s1_task-rest_run-001_bold_magnitude_RV.json
    │   ├── sub-00010389629F_ses-s1_task-rest_run-001_bold_magnitude_RV.nii.gz
    │   ├── sub-00010389629F_ses-s1_task-rest_run-002_bold_magnitude_R.json
    │   ├── sub-00010389629F_ses-s1_task-rest_run-002_bold_magnitude_R.nii.gz
    │   ├── sub-00010389629F_ses-s1_task-rest_run-002_bold_magnitude_RV.json
    │   ├── sub-00010389629F_ses-s1_task-rest_run-002_bold_magnitude_RV.nii.gz
    │   ├── sub-00010389629F_ses-s1_task-rest_run-003_bold_magnitude_R.json
    │   ├── sub-00010389629F_ses-s1_task-rest_run-003_bold_magnitude_R.nii.gz
    │   ├── sub-00010389629F_ses-s1_task-rest_run-003_bold_magnitude_RV.json
    │   └── sub-00010389629F_ses-s1_task-rest_run-003_bold_magnitude_RV.nii.gz
    └── sub-00010389629F_ses-s1_scans.tsv
```
