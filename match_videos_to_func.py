# rename the videos to match the functional runs names
# there is a delay between the acquisition time of the runs in the json files and the recording time of the videos names
# the average difference is around 4min:54sec (294sec)
# there is 3min:10sec between the console operating system and the raspberry pi linux
# the rest is probably the time consumed by the scanner doing adjustments
# the acquisition time of the scanner is always earlier
import json
import re
import glob


def get_acq_time_json(json_file):
    """get acquisition time from json file"""
    with open(json_file, 'r') as f:
        data = json.load(f)
        acq_time = data['AcquisitionTime']
        # the acq date is in this format '19:57:3.660000'
        # I want to be '19:57:3:660000' to match the videos time stamp
        json_time = datetime.strptime(acq_time, '%H:%M:%S.%f')
        acq_time = json_time.strftime('%H:%M:%S:%f')
        return acq_time


def get_acq_time_video(video_file):
    """get acquisition time from video file"""
    # get the video file name
    video_name = os.path.basename(video_file)
    pattern = r"(\d{4}_\w+_\d{1,2})__(\d{2}_\d{2}_\d{2}_\d{6})"
    match = re.search(pattern, video_name)
    date = match.group(1).replace('_', ' ')
    video_time = match.group(2).replace('_', ':')
    return video_time


def get_acq_time_diff(video_file, json_file):
    """get the difference between the acquisition time of the video and the json file"""
    time_format = "%H:%M:%S:%f"
    # get the acquisition time of the video
    video_time = get_acq_time_video(video_file)
    # get the acquisition time of the json file
    json_time = get_acq_time_json(json_file)
    # Convert the strings to datetime objects
    video_time = datetime.strptime(video_time, time_format)
    json_time = datetime.strptime(json_time, time_format)
    # get the difference between the two
    time_diff = (video_time - json_time).total_seconds()

    return time_diff


# we have to check each video against all the json files
def rename_video(video_file, json_file):
    """rename the videos to match the functional runs names"""
    video_ext = os.path.splitext(video_file)[1]

    json_name = os.path.splitext(json_file)[0]
    json_name = os.path.basename(json_name)
    # get the difference between the two
    time_diff = get_acq_time_diff(video_file, json_file)
    # rename the video file
    if 4 * 60 <= time_diff <= 6 * 60:
        # the video was recorded after the functional run
        # add the time difference to the video time
        new_video_name = f"{json_name}{video_ext}"
        new_video_name = os.path.join(os.path.dirname(video_file), new_video_name)
        os.rename(video_file, new_video_name)


def match_videos_func_ses(session_dir):
    func_runs = glob.glob(os.path.join(session_dir, 'func', '*bold.json'))
    videos = glob.glob(os.path.join(session_dir, 'video', '*'))
    for video in videos:
        for func_run in func_runs:
            rename_video(video, func_run)


