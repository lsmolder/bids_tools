import os
import glob


# Heudiconv cannot extract correct information from the dcm, it switches dim4 and dim3
# that's why you have to put dim3 > 30, which is reasonable for functional data (we can go even to 40, just to be sure)
# the 30 here is the number of slices => does not work
# I found out for 4D images, the image_type has to be ('ORIGINAL', 'PRIMARY', 'NON_PARALLEL', 'NONE')
# and the 3d volumes => ('ORIGINAL', 'PRIMARY', 'VOLUME', 'NONE')


# give the DICOM directory and it will navigate to where the files are
# use --files flag with the folder you get from unzipping
# do not use -d flag
# try:
#     # keep going down the tree as long as you are facing dirs
#     while os.path.isdir(os.getcwd()):
#         curr_dir = glob.glob("*")
#         os.chdir(curr_dir[-1])
#
#     # once you face dicoms, go up one level (that's where all data is)
# except NotADirectoryError:
#     os.chdir(os.path.dirname(os.getcwd()))


# ======================================================================================================================
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')

    return template, outtype, annotation_classes
# ======================================================================================================================
def filter_files(fl):
    if fl.endswith(".dcm"):
        # better to add the SatckId and the rest of info separately, otherwise it messes up the header
        pass
    return fl

# ======================================================================================================================
def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    # anatomical
    t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:01d}_T1w')

    t2w_rare = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-rare_run-{item:01d}_T2w')
    
    t2w_tse = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-tse_run-{item:01d}_T2w')

    tof = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-3dtof_run-{item:01d}_angio')
    # ==================================================================================================================
    # resting-state
        
    fMRI = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:01d}_bold')

    fMRI_RPE = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:01d}_bold')

    #  ==================================================================================================================

    info = {t1w: [],
            t2w_tse: [],
            t2w_rare: [],
            tof: [],

            fMRI: [],
            fMRI_RPE: [],


            }

    # extract the digits of the name to separate
    # you can even add the videos
    # magnitude data has name: 170001, phase: 170002
    # reverse phase and normal phase
    # we need the json files as well
    # TODO: no of volumes
    # trying to get the denopised version which is usually x0002
    for idx, s in enumerate(seqinfo):
        if s.series_description == 'Gre3Dinvivo_3Echo_ISO100_1A':
            info[t1w].append(s.series_id)  
            
        if s.series_description == 'T2_RAREvfl_ISO100_1A':
            info[t2w_rare].append(s.series_id) 
            
        if s.series_description == 'T2_85x85x500_tse2d_4A':
            info[t2w_tse].append(s.series_id) 

        if s.series_description == 'TOF3D_FLASH_flc_ISO40':
            info[tof].append(s.series_id)
        # ==================================================rest========================================================
        # if the name does not contain "_RV_" then it is a normal phase
            
        if  s.series_description == 'T2Star_rsfMRI_170x170x500_01':
            info[fMRI].append(s.series_id)
         #RPE is reverse phase encoding   
        if  s.series_description == 'T2Star_rsfMRI_170x170x500_RPE_02':
            info[fMRI_RPE].append(s.series_id)

        # 











    return info
