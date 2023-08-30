# Test

- k4abt performance issue
  Runtime(ONNX): CPU, DirectML(Intel ), CUDA(For NVIDIA RTX/GTX/Tesla), TensorRT(Jetson)
  
Quote from MS Docs:

```text
DirectML requires a DirectX 12 capable device. Almost all commercially-available graphics cards released in the last several years support DirectX 12. Examples of compatible hardware include:

AMD GCN 1st Gen (Radeon HD 7000 series) and above
Intel Haswell (4th-gen core) HD Integrated Graphics and above
NVIDIA Kepler (GTX 600 series) and above
Qualcomm Adreno 600 and above
```

- Windows defaults to DirectML (Intel HD Integrated Graphics)
  
- Linux defaults to GPU

## Test metrics

- downsampled to a person: performance (CPU %, GPU%), bandwidth test
    Result: (2 kinects, downsampled to 10%, 20fps, 200Mbps)

- k4abt inference performance test (CPU%, GPU%, FPS)
    on Jetson.

