import os
import glob

# define a task list to check if the series descirpiotn has any one of those words
# you consider it as resting state
tasks = ["visual", "whisker"]

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
def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    # anatomical
    t2w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:01d}_T2w')
    # T1_FLASH_3D like the one for synuclein
    t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:01d}_T1w')
    # ==================================================================================================================
    # resting-state
    func_rest_magnitude_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-rest_run-{item:01d}_part-mag_bold')
    func_rest_phase_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-rest_run-{item:01d}_part-phase_bold')

    func_rest_magnitude_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-rest_run-{item:01d}_part-mag_bold')
    func_rest_phase_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-rest_run-{item:01d}_part-phase_bold')

    # single resting-state volume with 20 and 40 averages
    # someitmes, I acquired 20 avg, sometimes 40 avg
    func_rest_40avg_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-rest_run-{item:01d}_bold_40avg')
    func_rest_40avge_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-rest_run-{item:01d}_bold_40avg')

    func_rest_20avg_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-rest_run-{item:01d}_bold_20avg')
    func_rest_20avge_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-rest_run-{item:01d}_bold_20avg')
    # ==================================================================================================================
    # tasks: visual
    func_task_visual_magnitude_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-visual_run-{item:01d}_part-mag_bold')
    func_task_visual_phase_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-visual_run-{item:01d}_part-phase_bold')

    func_task_visual_magnitude_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-visual_run-{item:01d}_part-mag_bold')
    func_task_visual_phase_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-visual_run-{item:01d}_part-phase_bold')
    # ==================================================================================================================
    # tasks: whisker
    func_task_whisker_magnitude_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-whisker_run-{item:01d}_part-mag_bold')
    func_task_whisker_phase_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-whisker_run-{item:01d}_part-phase_bold')

    func_task_whisker_magnitude_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-whisker_run-{item:01d}_part-mag_bold')
    func_task_whisker_phase_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-whisker_run-{item:01d}_part-phase_bold')
    # ==================================================================================================================
    # tasks: visual_whisker
    func_task_visual_whisker_magnitude_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-visual_whisker_run-{item:01d}_part-mag_bold')
    func_task_visual_whisker_phase_R = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-IS_{session}_task-visual_whisker_run-{item:01d}_part-phase_bold')

    func_task_visual_whisker_magnitude_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-visual_whisker_run-{item:01d}_part-mag_bold')
    func_task_visual_whisker_phase_RV = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_dir-SI_{session}_task-visual_whisker_run-{item:01d}_part-phase_bold')
    # =============================================================================================================================
    # the adj B0MAP, that's not part of the standard bids
    fmap = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_b0map')

    info = {t2w: [],
            t1w: [],

            func_rest_magnitude_R: [],
            func_rest_phase_R: [],

            func_rest_magnitude_RV: [],
            func_rest_phase_RV: [],

            func_task_visual_magnitude_R: [],
            func_task_visual_phase_R: [],

            func_task_visual_magnitude_RV: [],
            func_task_visual_phase_RV: [],

            func_task_whisker_magnitude_R: [],
            func_task_whisker_phase_R: [],

            func_task_whisker_magnitude_RV: [],
            func_task_whisker_phase_RV: [],

            func_task_visual_whisker_magnitude_R: [],
            func_task_visual_whisker_magnitude_RV: [],

            func_task_visual_whisker_phase_R: [],
            func_task_visual_whisker_phase_RV: [],


            func_rest_40avg_R: [],
            func_rest_40avge_RV: [],

            func_rest_20avg_R: [],
            func_rest_20avge_RV: [],
            fmap: []}

    # extract the digits of the name to seperate
    # you can even add the videos
    # magnitude data has name: 170001, phase: 170002
    # reverse phase and normal phase
    # we need the json files as well
# TODO: no of volumes
    for idx, s in enumerate(seqinfo):
        if 'T2_TurboRARE' in s.protocol_name:
            info[t2w].append(s.series_id)

        if 'T1_FLASH_3D' in s.protocol_name:
            info[t1w].append(s.series_id)
        # ==================================================rest========================================================
        # if the name does not contain "_RV_" then it is a normal phase
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" not in s.series_description) and (
                s.dim4 > 1) and all(task.lower() not in s.series_description.lower() for task in tasks):
            info[func_rest_magnitude_R].append(s.series_id)
        #
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" not in s.series_description) and (
                s.dim4 > 1) and all(task.lower() not in s.series_description.lower() for task in tasks):
            info[func_rest_phase_R].append(s.series_id)
        #
        # # if the name contains "_RV_" then it is a reveresed phase
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" in s.series_description) and (
                s.dim4 > 1) and all(task.lower() not in s.series_description.lower() for task in tasks):
            info[func_rest_magnitude_RV].append(s.series_id)

        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" in s.series_description) and (
                s.dim4 > 1) and all(task.lower() not in s.series_description.lower() for task in tasks):
            info[func_rest_phase_RV].append(s.series_id)
        # ========================================================40avg=================================================
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" not in s.series_description) and (
                "40avg" in s.series_description) and (
                s.dim4 == 1) and all(task.lower() not in s.series_description.lower() for task in tasks):
            info[func_rest_40avg_R].append(s.series_id)

        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" in s.series_description) and (
                "40avg" in s.series_description) and (
                s.dim4 == 1) and all(task.lower() not in s.series_description.lower() for task in tasks):
            info[func_rest_40avge_RV].append(s.series_id)

        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" not in s.series_description) and (
                "20avg" in s.series_description) and (
                s.dim4 == 1) and all(task.lower() not in s.series_description.lower() for task in tasks):
            info[func_rest_20avg_R].append(s.series_id)

        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" in s.series_description) and (
                "20avg" in s.series_description) and (
                s.dim4 == 1) and all(task.lower() not in s.series_description.lower() for task in tasks):
            info[func_rest_20avge_RV].append(s.series_id)
        # ===============================================visual=========================================================
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" not in s.series_description) and (
                "visual" in s.series_description) and (
                "whisker" not in s.series_description) and (
                s.dim4 > 1):
            info[func_task_visual_magnitude_R].append(s.series_id)
        #
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" not in s.series_description) and (
                "visual" in s.series_description) and (
                "whisker" not in s.series_description) and (
                s.dim4 > 1):
            info[func_task_visual_phase_R].append(s.series_id)
        #
        # # if the name contains "_RV_" then it is a reveresed phase
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" in s.series_description) and (
                "visual" in s.series_description) and (
                "whisker" not in s.series_description) and (
                s.dim4 > 1):
            info[func_task_visual_magnitude_RV].append(s.series_id)

        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" in s.series_description) and (
                "visual" in s.series_description) and (
                "whisker" not in s.series_description) and (
                s.dim4 > 1):
            info[func_task_visual_phase_RV].append(s.series_id)
        # =================================================whisker======================================================
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" not in s.series_description) and (
                "whisker" in s.series_description) and (
                "visual" not in s.series_description) and (
                s.dim4 > 1):
            info[func_task_whisker_magnitude_R].append(s.series_id)
        #
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" not in s.series_description) and (
                "whisker" in s.series_description) and (
                "visual" not in s.series_description) and (
                s.dim4 > 1):
            info[func_task_whisker_phase_R].append(s.series_id)
        #
        # # if the name contains "_RV_" then it is a reveresed phase
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" in s.series_description) and (
                "whisker" in s.series_description) and (
                "visual" not in s.series_description) and (
                s.dim4 > 1):
            info[func_task_whisker_magnitude_RV].append(s.series_id)

        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" in s.series_description) and (
                "whisker" in s.series_description) and (
                "visual" not in s.series_description) and (
                s.dim4 > 1):
            info[func_task_whisker_phase_RV].append(s.series_id)
        # ==================================================visual and whisker==========================================
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" not in s.series_description) and (
                "whisker" in s.series_description) and (
                "visual" in s.series_description) and (
                s.dim4 > 1):
            info[func_task_visual_whisker_magnitude_R].append(s.series_id)
        #
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" not in s.series_description) and (
                "whisker" in s.series_description) and (
                "visual" in s.series_description) and (
                s.dim4 > 1):
            info[func_task_visual_whisker_phase_R].append(s.series_id)
        #
        # # if the name contains "_RV_" then it is a reveresed phase
        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 1) and (
                "_RV_" in s.series_description) and (
                "whisker" in s.series_description) and (
                "visual" in s.series_description) and (
                s.dim4 > 1):
            info[func_task_visual_whisker_magnitude_RV].append(s.series_id)

        if ('EPI' in s.protocol_name) and (int(s.dcm_dir_name[-1]) == 2) and (
                "_RV_" in s.series_description) and (
                "whisker" in s.series_description) and (
                "visual" in s.series_description) and (
                s.dim4 > 1):
            info[func_task_visual_whisker_phase_RV].append(s.series_id)
        # =========================================================B0map================================================

        if 'B0MAP' in s.protocol_name:
            info[fmap].append(s.series_id)

    return info
