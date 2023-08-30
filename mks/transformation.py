import numpy as np
from mks.pcdUtils import icp_registration_skeleton


class Transfomation:

  @staticmethod
  def trans_mats_for_skeletons(skeletons):
    trans_mats = []
    for i in range(len(skeletons) - 1):
      trans_mats.append(Transfomation.skeleton_registration(skeletons[i], skeletons[i+1]))
    return trans_mats

  @staticmethod
  def skeleton_icp(skeleton1, skeleton2):
    return icp_registration_skeleton(skeleton1, skeleton2)
    return np.zeros((4, 4))
  
  @staticmethod
  def skeleton_registration(skeleton0, skeleton1):
    skeleton_xyz0 = [list(joint['position']) for joint in skeleton0]
    skeleton_xyz0 = np.asarray(skeleton_xyz0)

    skeleton_xyz1 = [list(joint['position']) for joint in skeleton1]
    skeleton_xyz1 = np.asarray(skeleton_xyz1)

    skeleton_quaternions0 = [list(joint['orientation']) for joint in skeleton0]
    skeleton_quaternions0 = np.asarray(skeleton_quaternions0)

    skeleton_quaternions1 = [list(joint['orientation']) for joint in skeleton1]
    skeleton_quaternions1 = np.asarray(skeleton_quaternions1)

    
    def quaternion_to_matrix(q):
        """
        Convert a quaternion into a rotation matrix.
        q should be in the form [w, x, y, z].
        """
        w, x, y, z = q
        return np.array([
            [1 - 2 * y * y - 2 * z * z, 2 * x * y - 2 * z * w, 2 * x * z + 2 * y * w],
            [2 * x * y + 2 * z * w, 1 - 2 * x * x - 2 * z * z, 2 * y * z - 2 * x * w],
            [2 * x * z - 2 * y * w, 2 * y * z + 2 * x * w, 1 - 2 * x * x - 2 * y * y]
        ])

    rotation0 = quaternion_to_matrix(skeleton_quaternions0[3])
    rotation1 = quaternion_to_matrix(skeleton_quaternions1[3])

    R = rotation1 @ np.linalg.inv(rotation0)

    # set translate to (0,0,0) and set 4th row to 0001
    # print(np.c_[R, [0, 0, 0]])
    R = np.r_[np.c_[R, [0, 0, 0]], [[0, 0, 0, 1]]]
    return R


  @staticmethod
  def pcd_icp(pcd1, pcd2):
    return np.zeros((4, 4))
