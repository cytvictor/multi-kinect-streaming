## notes

**performance**

capture=30fps, CPU5%, virt=4.3G, res=600M

+body tracking = 7-8fps, cpu 80%, virt=7.1G, res=630M

## Glossaries

TransMat = transfomation matrix

## Sys Pipeline TODOs

|      | #                                         | On      | Item                                                         | Note         |
| ---- | ----------------------------------------- | ------- | ------------------------------------------------------------ | ------------ |
| ✅    | **Step1**                                 | Capture | launch camera (k4a)                                          |              |
| ✅    | **Step2**                                 | -       | RGB-Ds to (PCDs, TransMats)                                  |              |
| ✅    | &nbsp;&nbsp;&nbsp;&nbsp;2.1               | Capture | get rgb-d (k4a)                                              |              |
| ✅    | &nbsp;&nbsp;&nbsp;&nbsp;2.2               | Capture | extract skelecton from rgbd (k4abt); rgbd -> PCD             | CPU bound    |
|      | &nbsp;&nbsp;&nbsp;&nbsp; _(Option1)_ |         |                                                              |              |
|      | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.3 | Capture | icp(skeleton1, skeleton2) -> TransMat                        |              |
|      | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.4  | Capture | transmit TransMat and PCD to Merger                          | net io bound |
|      | &nbsp;&nbsp;&nbsp;&nbsp; _(Option2)_ |         |                                                              |              |
|      | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.3 | Capture | transmit PCD, skeletons to Merger                            | net io bound |
|      | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.4 | Merger  | icp(skeleton1-6) -> TransMat                                 |              |
| ✅    | **Step3**                                 | Merger  | pcd = merge([PCD1, PCD2, PCD3, PCD4, ...], [TransMat1, TransMat2, TransMat3, ...]) | vis quality  |
| ✅    | **Step4**                                 | Render  | render(pcd)                                                  |              |

