**notes**

capture=30fps, CPU5%, virt=4.3G, res=600M

+body tracking = 7-8fps, cpu 80%, virt=7.1G, res=630M

Glossaries:
TransMat: transfomation matrix

**Step1**: Capture: launch camera (k4a)

**Step2**: RGB-Ds to (PCDs, TransMats)

2.1 Capture: get rgb-d (k4a)

2.2 Capture: extract skelecton from rgbd (k4abt); rgbd -> PCD

*(Option 1)*

2.3 Capture: icp(skeleton1, skeleton2) -> TransMat

2.4 Capture: transmit TransMat and PCD to Merger

*(Option 2)*

2.3 Capture: transmit PCD, skeletons to Merger

2.4 Merger: icp(skeleton1, skeleton2) -> TransMat


**Step 3**: Merger: pcd = merge([PCD1, PCD2, PCD3, PCD4, ...], [TransMat1, TransMat2, TransMat3, ...])

**Step 4**: Render: render(pcd)
