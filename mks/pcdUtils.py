import open3d as o3d
import numpy as np


def create_point_cloud(points, colors):
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.colors = o3d.utility.Vector3dVector(colors)
    point_cloud.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    return point_cloud


def save_ply(xyz, rgb, ply_filename):
    rgb *= 255
    formatted_points = []
    for i in range(len(xyz)):
        formatted_points.append(
            "%f %f %f %d %d %d 0\n" % (xyz[i, 0], xyz[i, 1], xyz[i, 2], rgb[i, 0], rgb[i, 1], rgb[i, 2]))

    out_file = open(ply_filename, "w")
    out_file.write('''ply
    format ascii 1.0
    element vertex %d
    property float x
    property float y
    property float z
    property uchar red
    property uchar green
    property uchar blue
    property uchar alpha
    end_header
    %s
    ''' % (len(xyz), "".join(formatted_points)))
    out_file.close()


def pcd_to_mesh(pcd, mesh_filename):
    pcd.estimate_normals()

    # estimate radius for rolling ball
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 1.5 * avg_dist

    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd,
        o3d.utility.DoubleVector([radius, radius * 2]))

    o3d.io.write_triangle_mesh(mesh_filename, mesh)


def icp_registration(source, target, current_transformation=np.identity(4)):
    voxel_radius = [0.16, 0.08, 0.04, 0.02, 0.01]
    max_iter = [50, 30, 14, 8, 2]

    for scale in range(5):
        iter = max_iter[scale]
        radius = voxel_radius[scale]

        source_down = source.voxel_down_sample(radius)
        target_down = target.voxel_down_sample(radius)

        source_down.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))
        target_down.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))

        print("Applying colored point cloud registration")
        result_icp = o3d.pipelines.registration.registration_colored_icp(
            source_down, target_down, radius * 1.5, current_transformation,
            o3d.pipelines.registration.TransformationEstimationForColoredICP(),
            o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
                                                              relative_rmse=1e-6,
                                                              max_iteration=iter))
        current_transformation = result_icp.transformation
        print(current_transformation)

    return current_transformation




def icp_registration_skeleton(skeleton1, skeleton2, current_transformation=np.identity(4)):
    voxel_radius = [0.16, 0.08, 0.04, 0.02, 0.01]
    max_iter = [50, 30, 14, 8, 2]

    source = create_point_cloud(skeleton1, colors=np.zeros_like(skeleton1))
    target = create_point_cloud(skeleton2, colors=np.zeros_like(skeleton2))

    for scale in range(5):
        iter = max_iter[scale]
        radius = voxel_radius[scale]

        source_down = source.voxel_down_sample(radius)
        target_down = target.voxel_down_sample(radius)

        source_down.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))
        target_down.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))

        print("Applying colored point cloud registration")
        result_icp = o3d.pipelines.registration.registration_colored_icp(
            source_down, target_down, radius * 1.5, current_transformation,
            o3d.pipelines.registration.TransformationEstimationForColoredICP(),
            o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
                                                              relative_rmse=1e-6,
                                                              max_iteration=iter))
        current_transformation = result_icp.transformation
        print(current_transformation)

    return current_transformation


def merge_point_cloud(source, target):
    # Extract point coordinates and colors from the transformed source and target point clouds
    source_points = np.asarray(source.points)
    source_colors = np.asarray(source.colors)
    target_points = np.asarray(target.points)
    target_colors = np.asarray(target.colors)

    # Concatenate the point coordinates and colors of the source and target point clouds
    merged_points = np.concatenate((source_points, target_points), axis=0)
    merged_colors = np.concatenate((source_colors, target_colors), axis=0)

    # Create a new Open3D point cloud with the merged points and colors
    merged_cloud = o3d.geometry.PointCloud()
    merged_cloud.points = o3d.utility.Vector3dVector(merged_points)
    merged_cloud.colors = o3d.utility.Vector3dVector(merged_colors)

    o3d.visualization.draw_geometries([merged_cloud])

    return merged_cloud

