from typing import List, Mapping
import pykinect_azure as pykinect

from mks.utils import logger

# label on the device to SN
CAM_LABEL_SN = {
  'A': '000502714412',
  'B': '000431614412',
  'C': 'SNXXXX3',
  'D': 'SNXXXX4',
}

class MultiCapturer:
  def __init__(self) -> None:
    self.devices: List[pykinect.Device] = []
    self.device_body_trakcers: List[pykinect.Tracker] = []

  def init_cameras(self, initialize_label_sequence: List[str]):
    pykinect.initialize_libraries(track_body=True)

    # using default device configurations
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
    device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_30
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED

    device_count = pykinect.Device.device_get_installed_count()

    logger.info("Found %d Kinect devices", device_count)
    if len(initialize_label_sequence) != device_count:
      logger.error("Installed device count %d does not match the init label sequence count %d", 
                   device_count, len(initialize_label_sequence))
    
    # initialize all devices
    devices_unsorted: Mapping[str, pykinect.Device] = {} # SN -> Device
    for idx in range(device_count):
      device = pykinect.Device(idx)
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
      dev.start(device_config)

      tracker = pykinect.start_body_tracker(calibration=dev.calibration)
      self.device_body_trakcers.append(tracker)
    
    logger.info("  Started: master = %s, slaves = %s", initialize_label_sequence[0], initialize_label_sequence[1:])
    return self.devices


  def capture_frames(self) -> List[pykinect.Capture]: # -> captures
    # frames = sensor.capture()
    # further_process(frames)
    captures = []
    for dev in self.devices:
      capture = dev.update()
      captures.append(capture)
    
    return captures
  
  def get_captures_skeletons(self, captures):
    skeletons = []
    for i, cap in enumerate(captures):
      frame = self.device_body_trakcers[i].update(cap)
      skeleton = None
      try:
        skeleton = frame.get_body_skeleton()
      except Exception as e:
        logger.debug("No skeleton for this frame!")
      skeletons.append(skeleton)
    return skeletons # TODO: support multiple people

