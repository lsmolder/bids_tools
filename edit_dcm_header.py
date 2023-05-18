# Single slice acquisitions creates a problem with heudiconv:
# AttributeError: 'Dataset' object has no attribute 'StackID'
# the problem is because there are two attributes missing from the dcm header
# StackID and InStackPositionNumber
# moreover, dimension index values are a int, and it should be a list

# you need also to change DimensionIndexSequence to be 3d instead of 1d
# so, you have to create a two empty datasets and append them to the original one
import pydicom
from pydicom.dataset import Dataset
import os
import sys
import glob
from datetime import datetime


# you can use the script from the bash or as a python function
def help_message():
    print("""Input argument missing \n
    >>> python edit_dcm_header.py dcm_file.dcm \n
    """)


if len(sys.argv) < 2:
    help_message()
    exit(0)

# TODO: check if StackID exists or not => DONE
# TODO: run the script as part of the heuristic => DONE

dcm_path = sys.argv[1]


def add_StackID_file(dcm_path):
    print(f"+++++++++++++++Stacking the file: {dcm_path}+++++++++++++++")
    file_basename = os.path.basename(dcm_path)
    file_dir = os.path.dirname(dcm_path)

    ds = pydicom.dcmread(dcm_path)
    seq = ds.PerFrameFunctionalGroupsSequence

    # check if the file has StackID or not
    # this equivalent to the first frame
    if not hasattr(ds.PerFrameFunctionalGroupsSequence[0].FrameContentSequence[0], 'StackID'):
        for frame in seq:
            frame.FrameContentSequence[0].StackID = '1'
            frame.FrameContentSequence[0].InStackPositionNumber = 1
            dim_index_value = frame.FrameContentSequence[0].DimensionIndexValues
            frame.FrameContentSequence[0].DimensionIndexValues = [dim_index_value, 1, 1]
        # it will overwrite the original file
        ds.save_as(os.path.join(file_dir, file_basename))


def add_StackID_folder(dcm_folder):
    for root, _, files in os.walk(dcm_folder):
        for file in files:
            if file.lower().endswith('.dcm'):
                dcm_path = os.path.join(root, file)
                add_StackID_file(dcm_path)


def find_file(target_file):
    """"the example_dcm_file and dcm_dir_name cannot be joined to give you the abs path
     as dcm_dir_name will give you the top parent dir, so you need to search for teh abs path for your dcms
     so, you would take the s.example_dcm_file and search for it in the current dir and its subdir
     """
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if file == target_file:
                return os.path.join(root, file)
    return None


def add_acquisition_date(dcm_path):
    """the AcquisitionDate is missing from the dcm header, so we need to add it
    All we have is AcquisitionDateTime, however, there is SeriesDate and StudyDate.
    We need to set an additional field inside the dicom header, so heudiconv can extract it"""
    print(f"+++++++++++++++Adding AcquisitionDate: {dcm_path}+++++++++++++++")
    file_basename = os.path.basename(dcm_path)
    file_dir = os.path.dirname(dcm_path)

    ds = pydicom.dcmread(dcm_path)
    ds.AcquisitionDate = ds.SeriesDate
    ds.AcquisitionTime = ds.SeriesTime
    # it will overwrite the original file
    ds.save_as(os.path.join(file_dir, file_basename))



def get_subj_age(scan_date, birth_date):
    """get the age of the subject at the time of the scan"""
    # dates look like this: 20190101
    scan_date = datetime.strptime(scan_date, '%Y%m%d')
    birth_date = datetime.strptime(birth_date, '%Y%m%d')
    age = (scan_date - birth_date).days
    return age



def modify_dcm_header(dcm_path):
    """add some of the missing fields in the same function, so you don't import the same file multiple times"""
    print(f"+++++++++++++++modifying dcm header: {dcm_path}+++++++++++++++")
    file_basename = os.path.basename(dcm_path)
    file_dir = os.path.dirname(dcm_path)

    ds = pydicom.dcmread(dcm_path)
    # these fiedls already exist, you don't need them
    ds.AcquisitionDate = ds.SeriesDate
    ds.AcquisitionTime = ds.SeriesTime
    ds.RepetitionTime = float(ds.SharedFunctionalGroupsSequence[0].MRTimingAndRelatedParametersSequence[0].RepetitionTime)
    ds.EchoTime = float(ds.SharedFunctionalGroupsSequence[0].MREchoSequence[0].EffectiveEchoTime)
    ds.SliceThickness = float(ds.SharedFunctionalGroupsSequence[0].PixelMeasuresSequence[0].SliceThickness)

    ds.PatientAge = str(get_subj_age(ds.SeriesDate, ds.PatientBirthDate))
    # it will overwrite the original file
    ds.save_as(os.path.join(file_dir, file_basename))
