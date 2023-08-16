from mks.transformation import Transfomation
from mks.rtc import Rtc


def start_client_pipeline():

  TEST_FRAME_COUNT = 10
  i = 0

  while True:
    # Option 1 step 2.4 Capture: transmit TransMat and PCD to Merger
    # receive TransMats, PCDs in a specified order
    # trans_mats, pcds = recv()

    # Option 2 step 2.3
    # receives PCD, skeletons
    # pcds, skeletons = recv()

    # Option 2 step 2.4: icp(skeleton1-6) -> TransMat
    trans_mats = Transfomation.trans_mats_for_skeletons(skeletons)

    # Step 3 Merger: pcd = merge([PCD1, PCD2, PCD3, PCD4, ...], [TransMat1, TransMat2, TransMat3, ...])
    
    # Step 4 Render: render(pcd)

    # max 10 frames
    i += 1
    if i == TEST_FRAME_COUNT:
      return



start_client_pipeline()
