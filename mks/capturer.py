class MKSCapturer:
  def __init__(self) -> None:
    self.init_cameras()
    pass

  def init_cameras(self):
    pass

  def capture_frames(self): # -> frames
    # frames = sensor.capture()
    # further_process(frames)
    pass

  def frame_to_skeleton(self, frame): # -> skeleton1, skeleton2, skeleton3, ...
    # skeleton = body_tracking.to_skeleton(frame)
    pass

  def send_frames(self, frames, skeletons):
    # 
    pass

