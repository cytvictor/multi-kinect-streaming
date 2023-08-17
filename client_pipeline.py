from mks.capture import MultiCapturer
from mks.transformation import Transfomation
from mks.rtc import Rtc
from mks.mq import MQComm
from mks.k4a.kinect_body_tracker import KinectBodyTracker


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
    
    # step 2.2 extract skelecton from rgbd (k4abt); rgbd -> PCD
    skeletons = capturer.get_captures_skeletons(captures)

    # Option 1 step 2.3 
    trans_mats = Transfomation.trans_mats_for_skeletons(skeletons)

    # Option 1 step 2.4 Capture: transmit TransMat and PCD to Merger
    for i, camera_label in enumerate(capturer.label_sequence):
      mq.emit_frame(camera_label, [devices[i].get_capture_pcd(captures[i]), trans_mats[i]])

    # Option 2 step 2.3 Capture: transmit PCD, skeletons to Merger
    for i, camera_label in enumerate(capturer.label_sequence):
      mq.emit_frame(camera_label, [devices[i].get_capture_pcd(captures[i]), skeletons[i]])


    # max 10 frames
    i += 1
    if i == TEST_FRAME_COUNT:
      return



start_client_pipeline()
