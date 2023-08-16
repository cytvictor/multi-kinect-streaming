class MKSMerger:

  @staticmethod
  def merge(pcds, trans_mats):
    # below is pseudo-code
    result = pcds[0]
    for i, pcd in enumerate(pcds[1:]):
      result += pcd * trans_mats[i]
    return result
