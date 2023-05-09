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


# you can use the script from the bash or as a python function
def help_message():
    print("""Input argument missing \n
    >>> python single_slice_acquisition.py dcm_file.dcm \n
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
