# BIDS TOOLS
* scripts to organize 9.4T data and videos into BIDS format
* the data from the dicom server is downloaded as a zipped file containing all the data in dcm format
* the data (after unzipping it) is usually organized as follow:

```
DICOM
    └── 20221126
        └── 15Ear_390792^^^^
            └── 20221126_01.FD20847F
                ├── 100001
                │   └── 15Ear_390792^^^^.MR.Menon^NcMod-fmri.100001.1.20221126.C8152BD7.dcm
                ├── 110001
                │   └── 15Ear_390792^^^^.MR.Menon^NcMod-fmri.110001.1.20221126.E8E820AD.dcm
                ├── 120001
                │   └── 15Ear_390792^^^^.MR.Menon^NcMod-fmri.120001.1.20221126.1FC860A9.dcm
                ├── 130001
                │   └── 15Ear_390792^^^^.MR.Menon^NcMod-fmri.130001.1.20221126.BCFF7F90.dcm
                ├── 160001
                │   └── 15Ear_390792^^^^.MR.Menon^NcMod-fmri.160001.1.20221126.55DC8001.dcm
                ├── 20001
                │   └── 15Ear_390792^^^^.MR.Menon^NcMod-fmri.20001.1.20221126.B83A3D8D.dcm
                ├── 30001
                │   └── 15Ear_390792^^^^.MR.Menon^NcMod-fmri.30001.1.20221126.B8729B91.dcm
                └── 50001
                    └── 15Ear_390792^^^^.MR.Menon^NcMod-fmri.50001.1.20221126.A29E276C.dcm
```
