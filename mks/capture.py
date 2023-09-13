from typing import List, Mapping
import pykinect_azure as pykinect
import numpy as np

from mks.k4a.kinect_sensor import KinectSensor, SensorSdk
from mks.utils import logger

# label on the device to SN
CAM_LABEL_SN = {
  'A': '000502714412',
  'B': '000431614412',
  'C': '000966714112',
  'D': '000456614412',
  'E': '000508114412',
  'F': '000437714412',
}


def skeleton_to_array(skeleton: pykinect.k4abt_skeleton_t) -> list:
  if skeleton is None:
    return
  joint: pykinect.k4abt_joint_t = None
  positions = []
  for joint in skeleton.joints:
    positions.append({
      'position': (joint.position.xyz.x, joint.position.xyz.y, joint.position.xyz.z), 
      'orientation': (joint.orientation.wxyz.w, joint.orientation.wxyz.x, joint.orientation.wxyz.y, joint.orientation.wxyz.z), 
      'confidence_level': joint.confidence_level
    })
  return positions


class MultiCapturer:
  def __init__(self) -> None:
    self.devices: List[KinectSensor] = []
    self.label_sequence: List[str] = []

  def init_cameras(self, initialize_label_sequence: List[str]):

    self.label_sequence = initialize_label_sequence
    device_count = SensorSdk.device_get_installed_count()
    logger.info("Found %d Kinect devices", device_count)

    if len(initialize_label_sequence) != device_count:
      logger.error("Installed device count %d does not match the init label sequence count %d", 
                   device_count, len(initialize_label_sequence))
    
    # initialize all devices
    devices_unsorted: Mapping[str, KinectSensor] = {} # SN -> Device
    for idx in range(device_count):
      device = KinectSensor(idx)
      sn = device.get_serialnum()
      devices_unsorted[sn] = device
      logger.info("  Device %d: SN %s", idx, sn)

    # store device sequencially (the first device is the master, other are sequentially synced)
    for label in initialize_label_sequence:
      dev = devices_unsorted.get(CAM_LABEL_SN[label])
      if dev is None:
        logger.error("did not find the camera that has SN %s (label %s), plz check CAM_LABEL_SN", CAM_LABEL_SN[label], label)
      self.devices.append(dev)

    for dev in self.devices:
      dev.start_camera()

    logger.info("  Started: master = %s, slaves = %s", initialize_label_sequence[0], initialize_label_sequence[1:])
    return self.devices


  def capture_frames(self) -> List[pykinect.Capture]: # -> captures
    captures = []
    for dev in self.devices:
      capture = dev.capture()
      # print(capture)
      captures.append(capture)
    
    return captures
  
  def get_captures_skeletons(self, captures) -> List[pykinect.k4abt_skeleton_t]:
    skeletons = []
    for i, cap in enumerate(captures):
      # frame = self.devices[i].body_tracker.update(cap)
      frame = self.devices[i].body_tracker.update(cap)
      skeleton = None
      try:
        skeleton = frame.get_body_skeleton()
      except Exception as e:
        logger.debug("No skeleton for the frame captured on %s!", self.label_sequence[i])
      skeletons.append(skeleton_to_array(skeleton))
    return skeletons # TODO: now get the 0th person skeleton; support multiple people

