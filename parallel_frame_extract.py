import os
import sys
import subprocess
import shutil
import argparse
import pp
from tqdm import tqdm

def extract_each_video(source_dir, target_dir, video_idx):
    source_video_name = os.path.join(source_dir, video_idx + '.webm')
    target_frame_dir = os.path.join(target_dir, video_idx)
    # target_class_dir = os.path.join(target_dir, class_index)
    if not os.path.exists(target_frame_dir):
        os.makedirs(target_frame_dir)


    # source_video_name = os.path.join(source_class_dir, each_video)
    # video_prefix = each_video.split('.')[0]
    # target_video_frames_folder = os.path.join(target_class_dir, video_prefix)
    # if not os.path.exists(target_video_frames_folder):
    #     os.makedirs(target_video_frames_folder)
    target_frames = os.path.join(target_frame_dir, '{}_%06d.jpg'.format(video_idx))

    try:
        # change videos to 30 fps and extract video frames
        subprocess.call('ffmpeg -nostats -loglevel 0 -i %s -r 30 -q:v 1 %s' %
                        (source_video_name, target_frames), shell=True)
        # print('Processed: ' + source_video_name + ' >>>>>>' + target_frame_dir)

        # sanity check video frames
        # video_frames = os.listdir(target_frame_dir)
        # video_frames.sort()
        # if len(video_Frames) == 0:

    except:
        print('Video %s decode failed.' % (source_video_name))
        # continue

def extract_frames(source_dir, target_dir, n_cpus):
    source_videos = os.listdir(source_dir) # 28992.webm
    target_videos_video_names = [name_[:-5] for name_ in source_videos] # 28992
    if not os.path.exists(target_dir): # make target dir
        os.makedirs(target_dir)

    job_server = pp.Server(ncpus=n_cpus)
    print("Starting pp with", job_server.get_ncpus(), "workers")

    jobs = [(video_index, job_server.submit(extract_each_video, (source_dir, target_dir, video_index, ),
                                            (), ("os", "subprocess", "shutil",)))
            for video_index in target_videos_video_names]

    for video_index, job in tqdm(jobs):
        result = job()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Extract frames of Kinetics400 dataset")
    parser.add_argument('--source_dir', type=str, help='the directory of raw videos')
    parser.add_argument('--target_dir', type=str, help='the directory which is used to store the extracted frames')
    parser.add_argument('--n_cpus', type=int, default=64, help='the number of CPUs')
    args = parser.parse_args()

    assert args.source_dir, "You must give the source_dir of raw videos!"
    assert args.target_dir, "You must give the traget_dir for storing the extracted frames!"

    import time
    tic = time.time()
    extract_frames(args.source_dir, args.target_dir, args.n_cpus)
    print(time.time() - tic)
