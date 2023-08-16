import numpy as np
from mks.capture import MultiCapturer
from mks.k4a.kinect_body_tracker import KinectBodyTracker


def start_client_pipeline():
  # step1
  capturer = MultiCapturer()
  devices = capturer.init_cameras(['A', 'B'])

  test_max_frame_count = 10
  i = 0
  while True:
    # step 2.1 get rgb-d
    captures = capturer.capture_frames()
    # skeletons = capturer.frame_to_skeleton(frames)
    ret, image = captures[0].get_color_image()
    if not ret:
      continue
    
    # step 2.2 extract skelecton from rgbd (k4abt); rgbd -> PCD
    skeletons = capturer.get_captures_skeletons(captures)

    # step 2.3 Option1

    # step 2.4 Option1

    # step 2.3 Option 2

    # step 2.4 Option 2 plz see merger_pipeline.py

    # max 10 frames
    i += 1
    if i == test_max_frame_count:
      return



start_client_pipeline()
