import pykinect_azure as pykinect
import open3d as o3d
import numpy as np
import cv2


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
    self.vis = o3d.visualization.Visualizer()
    self.vis.create_window()
    self.body_tracker: pykinect.Tracker = None
    self.o3d_started = False
    pass

  def get_serialnum(self):
    return self.device.get_serialnum()
  
  def start_camera(self) -> None:

    # using default device configurations
    device_config = pykinect.default_configuration
    device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
    device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_30
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_2X2BINNED
    
    self.device.start(device_config)
    self.body_tracker = pykinect.start_body_tracker(calibration=self.device.calibration)
    # print(self.device.get_calibration(depth_mode=pykinect.K4A_DEPTH_MODE_NFOV_2X2BINNED,
    #   color_resolution=pykinect.K4A_COLOR_RESOLUTION_720P).get_matrix(pykinect.K4A_CALIBRATION_TYPE_COLOR))
  
  def capture(self) -> pykinect.Capture:
    return self.device.update()

  def get_capture_pcd(self, capture: pykinect.Capture):
    ret, color_image = capture.get_color_image()
    ret_points, points = capture.get_transformed_pointcloud()

    # ret, depth_image = capture.get_depth_image()
    # color_image = o3d.geometry.Image(color_image)
    # depth_image = o3d.geometry.Image(color_image)
    # rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_image, depth_image,
    #   convert_rgb_to_intensity=False)

    # device_calibration_mat = self.device.get_calibration(depth_mode=pykinect.K4A_DEPTH_MODE_NFOV_2X2BINNED,
    #   color_resolution=pykinect.K4A_COLOR_RESOLUTION_720P).get_matrix(pykinect.K4A_CALIBRATION_TYPE_COLOR)

    # intrinsic = o3d.camera.PinholeCameraIntrinsic(
    #   o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
    # intrinsic.set_intrinsics(
    #     width=1280, height=720, 
    #     fx=device_calibration_mat[0][0], fy=device_calibration_mat[1][1], 
    #     cx=device_calibration_mat[0][2], cy=device_calibration_mat[1][2],
    # )
    # #9%
    # point_cloud = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsic,
    #                                                                   project_valid_depth_only=True)

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    colors = cv2.cvtColor(color_image, cv2.COLOR_BGRA2RGB).reshape(-1, 3) / 255
    point_cloud.colors = o3d.utility.Vector3dVector(colors)

    # point_cloud.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

    if not self.o3d_started:
      self.vis.add_geometry(point_cloud)
      self.o3d_started = True
    else:
      self.vis.update_geometry(point_cloud)
    self.vis.poll_events()
    self.vis.update_renderer()
    return [np.asarray(point_cloud.points), np.asarray(point_cloud.colors)]
