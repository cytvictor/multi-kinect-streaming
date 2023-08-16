import pykinect_azure as pykinect

pykinect.initialize_libraries(track_body=True)


class SensorSdk:
  def __init__(self) -> None:
    pass

  @staticmethod
  def device_get_installed_count():
    return pykinect.Device.device_get_installed_count()

class KinectSensor:
  def __init__(self, device_index=0) -> None:
    self.device = pykinect.Device(device_index)
    self.body_tracker: pykinect.Tracker = None
    pass

  def get_serialnum(self):
    return self.device.get_serialnum()
  
  def start_camera(self) -> None:

    # using default device configurations
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
    device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_30
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
    
    self.device.start(device_config)
    self.body_tracker = pykinect.start_body_tracker(calibration=self.device.calibration)
  
  def capture(self) -> pykinect.Capture:
    return self.device.update()
