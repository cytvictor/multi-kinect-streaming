import open3d as o3d
from typing import List

class Renderer:

  def __init__(self) -> None:
    self.point_clouds: List[o3d.geometry.PointCloud] = []
    self.vis = o3d.visualization.VisualizerWithKeyCallback()
    self.vis.create_window()
  
  def update(self, pcds, trans_mats):
    while len(self.point_clouds) < len(pcds):
      pc = o3d.geometry.PointCloud()
      self.point_clouds.append(pc)
      self.vis.add_geometry(pc)
    
    for idx, pcd in enumerate(pcds):
      self.point_clouds[idx].points = o3d.utility.Vector3dVector(pcd.points)
      self.point_clouds[idx].colors = o3d.utility.Vector3dVector(pcd.colors)

      if idx > 0:
        self.point_clouds[idx].transform(trans_mats[idx - 1])
      
      self.vis.update_geometry(self.point_clouds[idx])


    # self.vis.update(geometr)
    coordinate_widget = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.6, origin=[0, 0, 0])
    self.vis.update_geometry(coordinate_widget)

    self.vis.poll_events()
    self.vis.update_renderer()
