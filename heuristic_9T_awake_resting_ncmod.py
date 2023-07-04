import os
import glob
from edit_dcm_header import add_StackID_folder, add_StackID_file, find_file, add_acquisition_date, modify_dcm_header
import pydicom

# give the DICOM directory and it will navigate to where the files are
# use --files flag with the folder you get from unzipping
# do not use -d flag
try:
    # keep going down the tree as long as you are facing dirs
    while os.path.isdir(os.getcwd()):
        curr_dir = glob.glob("*")
        os.chdir(curr_dir[-1])

    # once you face dicoms, go up one level (that's where all data is)
except NotADirectoryError:
    os.chdir(os.path.dirname(os.getcwd()))


# ======================================================================================================================
def create_key(template, outtype='nii.gz', annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')

    return template, outtype, annotation_classes


# ======================================================================================================================
def filter_files(fl):
    if fl.endswith(".dcm"):
        # better to add the SatckId and the rest of info separately, otherwise it messes up the header
        add_StackID_file(fl)
        # fields already exist, but you add them for the dcminfo.tsv file
        modify_dcm_header(fl)
    return fl


# ======================================================================================================================
def infotodict(seqinfo):
    """
    From the documentation (https://heudiconv.readthedocs.io/en/latest/heuristics.html):

    item: an index of seqinfo (e.g., 1),
    subject: a subject label (e.g., qa)
    seqitem: sequence item, index with a sequence/protocol name (e.g., 3-anat-scout_ses-{date})
    subindex: an index within the seqinfo (e.g., 1),
    session: empty (no session) or a session entity (along with ses-, e.g., ses-20191216),
    bids_subject_session_prefix: shortcut for BIDS file name prefix combining subject and optional session (e.g., sub-qa_ses-20191216),
    bids_subject_session_dir: shortcut for BIDS file path combining subject and optional session (e.g., sub-qa/ses-20191216).
    """
    # anatomical
    t2w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:01d}_T2w')
    # T1_FLASH_3D like the one for synuclein
    t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:01d}_T1w')
    # ==================================================================================================================
    # resting-state
    func_rest_magnitude_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-PA_{session}_task-rest_run-{item:01d}_part-mag_bold')
    func_rest_phase_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-PA_{session}_task-rest_run-{item:01d}_part-phase_bold')

    func_rest_magnitude_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-AP_{session}_task-rest_run-{item:01d}_part-mag_bold')
    func_rest_phase_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-AP_{session}_task-rest_run-{item:01d}_part-phase_bold')
   # =============================================================================================================================
    # the adj B0MAP, that's not part of the standard bids
    fmap = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_b0map')

    info = {t2w: [],
            t1w: [],

            func_rest_magnitude_R: [],
            func_rest_phase_R: [],

            func_rest_magnitude_RV: [],
            func_rest_phase_RV: [],

            fmap: []}
    
    # Define how we will distinguish between the files:
    for idx, s in enumerate(seqinfo):
        if ('T2_' in s.protocol_name):
            info[t2w].append(s.series_id)

        if 'T1_FLASH_3D' in s.protocol_name:
            info[t1w].append(s.series_id)
        
        # ==================================================rest========================================================
        
        # Save booleans to human-readable variables:
        is_magnitude = int(s.dcm_dir_name[-1]) == 1
        is_t2star_func = ('epi' in s.protocol_name.lower() or 't2star' in s.protocol_name.lower())
        is_phase_encode_PA = s.image_orientation == (1, 0, 0, 0, 1, 0)
        is_phase_encode_AP = s.image_orientation == (1, 0, 0, 0, -1, 0)

        # T2* acquisitions acquired PA (normal) phase - magnitude images
        if is_t2star_func and is_magnitude and is_phase_encode_PA:
            info[func_rest_magnitude_R].append(s.series_id)
        # T2* acquisitions acquired PA (normal) phase - not magnitude images
        if is_t2star_func and not is_magnitude and is_phase_encode_PA:
            info[func_rest_phase_R].append(s.series_id)
        
        # T2* acquisitions acquired AP (reverse) phase - magnitude images
        if is_t2star_func and is_magnitude and is_phase_encode_AP:
            info[func_rest_magnitude_RV].append(s.series_id)
        # T2* acquisitions acquired AP (reverse) phase - not magnitude images
        if is_t2star_func and not is_magnitude and is_phase_encode_AP:
            info[func_rest_phase_RV].append(s.series_id)
        
        # =========================================================B0map================================================

        if 'B0MAP' in s.protocol_name:
            info[fmap].append(s.series_id)

    return info

