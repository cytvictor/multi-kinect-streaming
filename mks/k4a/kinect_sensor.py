import pykinect_azure as pykinect
import open3d as o3d

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

  def get_capture_pcd(self, capture: pykinect.Capture):
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(capture.get_color_image(), capture.get_depth_image(),
      convert_rgb_to_intensity=False)

    device_calibration_mat = self.device.get_calibration(depth_mode=pykinect.K4A_DEPTH_MODE_NFOV_2X2BINNED,
      color_resolution=pykinect.K4A_COLOR_RESOLUTION_720P).get_matrix(pykinect.K4A_CALIBRATION_TYPE_COLOR)

    intrinsic = o3d.camera.PinholeCameraIntrinsic(
      o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
    intrinsic.set_intrinsics(
        width=1280, height=720, 
        fx=device_calibration_mat[0][0], fy=device_calibration_mat[1][1], 
        cx=device_calibration_mat[0][2], cy=device_calibration_mat[1][2],
    )
    #9%
    point_cloud = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsic,
                                                                      project_valid_depth_only=True)

    point_cloud.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    return point_cloud
