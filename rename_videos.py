import sys
import os
from match_videos_to_func import match_videos_func_ses

def help_message():
    print("""Input argument missing \n
    >>> python rename_videos.py ses_dir \n
    Examples :
    >>> python rename_videos.py /Users/aeed/Documents/Work/BIDS/Menon^AS-MBN/sub-04393073M/ses-02
    """)


if len(sys.argv) < 2:
    help_message()
    exit(0)

ses_dir = sys.argv[1]
match_videos_func_ses(ses_dir)

