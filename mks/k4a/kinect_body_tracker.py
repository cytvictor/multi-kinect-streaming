import pykinect_azure as pykinect

class KinectBodyTracker:
  def __init__(self) -> None:
    self.body_tracker = pykinect.start_body_tracker()
    pass

  def get_capture_skeleton(self, capture):
    frame = self.body_tracker.update(capture)
    return frame.get_body_skeleton() # TODO: support multiple people
  
