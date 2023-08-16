**notes**

capture=30fps, CPU5%, virt=4.3G, res=600M

+body tracking = 7-8fps, cpu 80%, virt=7.1G, res=630M

  
**Step1**: Capture: launch camera (k4a)

**Step2 (Option 1)**:

2.1 Capture: get rgb-d (k4a) -> rgbd to skelecton (k4abt)

2.2 Capture: def icp(skeleton1, skeleton2) -> transformation matrix

2.3 Capture: transmit transformation matrix and PCD to Merger

**Step2 (Option 2)**:

2.1 Capture: get rgb-d (k4a)

2.2 Capture: transmit PCD to Merger

2.3 Merger: rgb-d to skeleton (k4abt)

2.3 Merger: icp(skeleton1, skeleton2) -> transformation matrix


**Step 3**: render(PCD1, PCD2, transformation matrix)
