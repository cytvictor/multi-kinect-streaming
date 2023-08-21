from mks.capture import MultiCapturer
from mks.transformation import Transfomation
from mks.mq import MQComm
from mks.k4a.kinect_body_tracker import KinectBodyTracker
from mks.utils import save_sample_frame
from mks.k4a.kinect_sensor import KinectSensor
import numpy as np
from scipy.spatial import procrustes 

DEVICE_SEQUENCE = ['A', 'B']


def start_client_pipeline():
  # step1
  capturer = MultiCapturer()
  mq = MQComm()
  devices = capturer.init_cameras(DEVICE_SEQUENCE)

  TEST_FRAME_COUNT = 10
  i = 0
  while True:
    # step 2.1 get rgb-d
    captures = capturer.capture_frames()
    ret, image = captures[0].get_color_image()
    if not ret:
      continue

  pcd0 = devices[0].get_capture_pcd(captures[0])
  pcd1 = devices[1].get_capture_pcd(captures[1])

  print(np.asarray(pcd0))
  print(np.asarray(pcd1))


start_client_pipeline()