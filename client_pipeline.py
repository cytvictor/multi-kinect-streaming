from mks.capture import MultiCapturer

capturer = MultiCapturer()
capturer.init_cameras(['A', 'B'])

def start_client_pipeline():
  frames = capturer.capture_frames()
  # skeletons = capturer.frame_to_skeleton(frames)

start_client_pipeline()
