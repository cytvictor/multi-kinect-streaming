class MKSClient:
  def __init__(self) -> None:
    pass

  def start_pipeline(self):
    if self.cameras is None:
      self.init_cameras()
    
    while True:
      frames = self.capture_frames()
      skeletons = self.frame_to_skeleton(frames)
      self.send_frames(frames, skeletons)

  def init_cameras(self):
    pass

  def capture_frames(self):
    # frames = sensor.capture()
    # further_process(frames)
    pass

  def frame_to_skeleton(self, frame):
    # skeleton = body_tracking.to_skeleton(frame)
    pass

  def send_frames(self, frames, skeletons):
    # 
    pass

