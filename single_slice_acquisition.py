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


# TODO: check if StackID exists or not
# TODO: run the script as part of the heuristic
def add_StackID(file_path):
    file_basename = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)

    ds = pydicom.dcmread(file_path)
    seq = ds.PerFrameFunctionalGroupsSequence

    for frame in seq:
        frame.FrameContentSequence[0].StackID = '1'
        frame.FrameContentSequence[0].InStackPositionNumber = 1
        dim_index_value = frame.FrameContentSequence[0].DimensionIndexValues
        frame.FrameContentSequence[0].DimensionIndexValues = [dim_index_value, 1, 1]
    # it will overwrite the original file
    ds.save_as(os.path.join(file_dir, file_basename))
