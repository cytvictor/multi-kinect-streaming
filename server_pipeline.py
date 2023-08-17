from mks.transformation import Transfomation
from mks.rtc import Rtc
from mks.mq import MQComm
from mks.render import Renderer

CAMERA_LABELS = ['A', 'B']

def start_client_pipeline():

  TEST_FRAME_COUNT = 10
  i = 0

  mq = MQComm()
  render = Renderer()

  while True:
    # Option 1 step 2.4 Capture: transmit TransMat and PCD to Merger
    trans_mats = []
    pcds = []
    # receive TransMats, PCDs in a specified order
    for label in CAMERA_LABELS:
      dat = mq.recv_frame(label)
      trans_mats.append(dat[1])
      pcds.append(dat[0])

    # Option 2 step 2.3
    # receives PCD, skeletons
    skeletons = []
    for label in CAMERA_LABELS:
      dat = mq.recv_frame(label)
      skeletons.append(dat[1])
      pcds.append(dat[0])

    # Option 2 step 2.4: icp(skeleton1-6) -> TransMat
    trans_mats = Transfomation.trans_mats_for_skeletons(skeletons)

    # Step 3 Merger: pcd = merge([PCD1, PCD2, PCD3, PCD4, ...], [TransMat1, TransMat2, TransMat3, ...])
    # Step 4 Render: render(pcd)
    render.update(pcds, trans_mats)

    # max 10 frames
    i += 1
    if i == TEST_FRAME_COUNT:
      return



start_client_pipeline()
