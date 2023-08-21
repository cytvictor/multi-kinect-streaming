import numpy as np
from mks.pcdUtils import icp_registration_skeleton


class Transfomation:

  @staticmethod
  def trans_mats_for_skeletons(skeletons):
    trans_mats = []
    for i in range(len(skeletons) - 1):
      trans_mats.append(Transfomation.skeleton_icp(skeletons[i], skeletons[i+1]))
    return trans_mats

  @staticmethod
  def skeleton_icp(skeleton1, skeleton2):
    return icp_registration_skeleton(skeleton1, skeleton2)
    return np.zeros((4, 4))

  @staticmethod
  def pcd_icp(pcd1, pcd2):
    return np.zeros((4, 4))
