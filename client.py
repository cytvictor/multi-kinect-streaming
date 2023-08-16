from mks.capturer import MKSCapturer

capturer = MKSCapturer()
def client_pipeline():
  frames = capturer.capture_frames()
  # skeletons = capturer.frame_to_skeleton(frames)
