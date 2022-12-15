import os
import glob

# give the DICOM directory and it will navigate to where the files are
# use --files flag with the folder you get from unzipping
# do not use -d flag
try:
    # keep going down the tree as long as you are facing dirs
    while (os.path.isdir(os.getcwd())):
         curr_dir = glob.glob("*")
         os.chdir(curr_dir[-1])

    # once you face dicoms, go up one level (that's where all data is)
except NotADirectoryError:
    os.chdir(os.path.dirname(os.getcwd()))

# =============================================================================================================================
def create_key(template, outtype=('nii.gz'), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# =============================================================================================================================
def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    t2w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-00{item:01d}_T2w')
    func_rest_magnitude_R = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-00{item:01d}_bold_magnitude_R')
    func_rest_phase_R = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-00{item:01d}_bold_phase_R')

    func_rest_magnitude_RV = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-00{item:01d}_bold_magnitude_RV')
    func_rest_phase_RV = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-00{item:01d}_bold_phase_RV')

    info = {t2w: [], func_rest_magnitude_R: [], func_rest_phase_R: [], func_rest_magnitude_RV: [], func_rest_phase_RV: []}


    # extract the digits of the name to seperate
    # you can even add the videos
    # magnitude data has name: 170001, phase: 170002
    # reverse phase and normal phase
    # we need the json files as well

    for idx, s in enumerate(seqinfo):
        if ('T2_TurboRARE' in s.protocol_name):
            info[t2w].append(s.series_id)
        # if the name does not contain "_RV_" then it is a normal phase
        if ('T2star_FID_EPI_sat' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1):
            info[func_rest_magnitude_R].append(s.series_id)

        if ('T2star_FID_EPI_sat' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2):
            info[func_rest_phase_R].append(s.series_id)

        # if the name contains "_RV_" then it is a reveresed phase
        if ('T2star_FID_EPI_sat' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and ("_RV_" in s.series_description):
            info[func_rest_magnitude_RV].append(s.series_id)

        if ('T2star_FID_EPI_sat' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and ("_RV_" in s.series_description):
            info[func_rest_phase_RV].append(s.series_id)
    return info
