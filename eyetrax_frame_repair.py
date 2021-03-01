import os
import argparse
import cv2 as cv
from tqdm import tqdm
from pathlib import Path

def readFrames(directory, file_name):
    cap = cv.VideoCapture(str(directory / file_name))
    print("reading frames from", file_name)
    frames = []
    success = True
    while success:
        success, frame = cap.read()
        frames.append(frame)
    
    print("total frames readed:", len(frames))
    cap.release()
    
    return frames

def writeFrames(directory, file_name, frames, frame_rate):
    height, width = frames[0].shape[:2]
    size = (width, height)
    out = cv.VideoWriter(str(directory / file_name), cv.VideoWriter_fourcc(*'mp4v'), frame_rate, size)
    
    for i in tqdm(range(len(frames)), desc = "writing video"):
        out.write(frames[i])
    out.release()

def restoreFrames(directory, file_name, frame_rate):
    # read frames
    frames = readFrames(directory, file_name)
    # rename src
    name, extension = os.path.splitext(file_name)
    name += "_back"
    name += extension
    os.rename(directory / file_name, directory / name)
    print("renaming", file_name, "to", name)
    # write frames 
    writeFrames(directory, file_name, frames, frame_rate)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
    help="input directory, containing eye0.mp4 and eye1.mp4")
ap.add_argument("-f", "--frame_rate", required=True,
    help="video frame rate")
args = vars(ap.parse_args())

directory = Path("C:/Temp/EyeTrax_Problem_1_23_5_src/bfa75fd7-7ed8-4922-a74c-fd0e3be1ffd3/000")
directory = Path(args["input"])
file_names = ["eye0.mp4", "eye1.mp4"]
frame_rate = int(args["frame_rate"])

for file_name in file_names:
    restoreFrames(directory, file_name, frame_rate)