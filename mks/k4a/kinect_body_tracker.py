import pykinect_azure as pykinect

from typing import List


class KinectBodyTracker:
  def __init__(self, device: pykinect.Device) -> None:
    self.device = device
    self.body_tracker = pykinect.start_body_tracker(device.calibration)
    pass

  def get_capture_skeleton(self, captures) -> List[pykinect.k4abt_skeleton_t]:
    skeletons = []
    for cap in captures:
      frame = self.body_tracker.update(cap)
      skeletons.append(frame.get_body_skeleton())
    return skeletons # TODO: support multiple people
  
