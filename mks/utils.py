import logging
import numpy as np
import json



class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     datefmt='%Y-%m-%d:%H:%M:%S',
#     level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

def save_sample_frame(devices, captures, skeletons, i = 0):

  # ret, image0 = captures[0].get_color_image()
  # ret, image1 = captures[1].get_color_image()
  # np.save(f'frame-{i}-colors_0', np.asarray(image0))
  # np.save(f'frame-{i}-colors_1', np.asarray(image1))
  # ret, depth0 = captures[0].get_depth_image()
  # ret, depth1 = captures[1].get_depth_image()
  # np.save(f'frame-{i}-depth_0', np.asarray(depth0))
  # np.save(f'frame-{i}-depth_1', np.asarray(depth1))
  pcd0 = devices[0].get_capture_pcd(captures[0])
  pcd1 = devices[0].get_capture_pcd(captures[1])
  np.save(f'frame-{i}-point_cloud_0-points', np.asarray(pcd0[0]))
  np.save(f'frame-{i}-point_cloud_0-colors', np.asarray(pcd0[1]))
  np.save(f'frame-{i}-point_cloud_1-points', np.asarray(pcd1[0]))
  np.save(f'frame-{i}-point_cloud_1-colors', np.asarray(pcd1[1]))
  with open(f'frame-{i}-skeleton_0', 'w+') as fp:
    json.dump(skeletons, fp)

  # print(np.asarray(skeletons[0].joints))
  print()
  # print(np.asarray(skeletons[1].joints))
  # joints = []
  # for i, joint in enumerate(skeletons[0].joints):
  #   print(joint)
  #   joints.append(joint)
  # # np.save('joints_0', np.asarray(joints))
  # joints = []
  # print()
  # for i, joint in enumerate(skeletons[1].joints):
  #   print(joint)
  #   joints.append(joint)
  # np.save('joints_1', np.asarray(joints))
  # print(np.asarray(skeletons[0]))
  # print(np.asarray(skeletons[1]))
  # np.save('skeleton_1', np.asarray(skeletons[1]))
#   exit(0)
