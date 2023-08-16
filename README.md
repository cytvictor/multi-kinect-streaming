**notes**

capture=30fps, CPU5%, virt=4.3G, res=600M
+body tracking = 7-8fps, cpu 80%, virt=7.1G, res=630M


1. Client: launch camera
2. thread1: get rgb-d -> rgbd to skelecton

Option1: 
3. on Client: def icp(skeleton) -> transformation matrix
4. transmit transformation matrix and PCD to merging server

Option2:
3. transmit PCD to merging server
4. on Merging Server: icp(PCD1, PCD2) -> transformation maxtrix

5. render(PCD1, PCD2, transformation matrix)
