# Feng-Yuan Kuo

**English** | [繁體中文](README.zh-TW.md)

I'm Feng-Yuan Kuo, a developer based in Taiwan. I work on 3D vision and reconstruction, with a focus on Gaussian Splatting and training models directly on mobile devices.

- **On-device 3DGS:** Swift and Metal training on iPhone, with live previews and model editing.
- **Capture and reconstruction:** ARKit/LiDAR capture, camera-pose refinement, depth fusion and COLMAP dataset preparation.
- **3D viewers:** Web-based splat viewers and geospatial 3D data with CesiumJS and 3D Tiles.

**[Try the iPhone app](https://testflight.apple.com/join/hKhVdTUR)** · [Watch the demo](#iphone-demo) · [Browse projects](#projects)

## Projects

| Project | What it does |
| --- | --- |
| [Splatify-Anything](https://github.com/KuoFengYuan/splatify-anything) | iPhone scanning, on-device 3DGS training and COLMAP dataset export. |
| [prior-pose-refine](https://github.com/KuoFengYuan/prior-pose-refine) | Refine prior camera poses, focal length and lens distortion with COLMAP, then export a 3DGS training dataset. |
| [align-capture](https://github.com/KuoFengYuan/align-capture) | Extract frames from a drone's RTSP stream with matching MAVLink GPS data for COLMAP. |
| [Recon Studio](https://github.com/KuoFengYuan/reconstudio) | Process video frames, run COLMAP and train 3DGS from a local web interface. |
| [3D Tiles Splat Viewer](https://github.com/KuoFengYuan/cesium-gaussian-splat-viewer) | Convert PLY models to 3D Tiles and view them on a CesiumJS globe. |
| [RAGGlass](https://github.com/KuoFengYuan/RAGGlass) | Inspect document retrieval, source passages and answers side by side. |

## AnyReplica

Scan a space with an iPhone and train a 3D Gaussian Splatting model on the phone. Walk through the result, edit it, or export a model or COLMAP dataset.

[Splatify-Anything on GitHub](https://github.com/KuoFengYuan/splatify-anything).

### iPhone demo

Scanning, training, walking through the model and editing. Recorded on iPhone, sped up to 30 seconds.

https://github.com/user-attachments/assets/3f8944d1-145c-4fc3-96c1-3cb5fdb734bf

<sub>Demo footage: [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/).</sub>

## prior-pose-refine

Start from approximate camera poses and a point cloud, refine the poses, focal length and lens distortion with COLMAP, and export undistorted images for 3DGS training. The output stays aligned to the input's metric coordinate frame.

It works with ARKit/LiDAR exports from Splatify-Anything and other sources that provide a compatible prior model.

[Code and usage](https://github.com/KuoFengYuan/prior-pose-refine) · [Method](https://github.com/KuoFengYuan/prior-pose-refine/blob/main/docs/method.md) · [Benchmarks](https://github.com/KuoFengYuan/prior-pose-refine/blob/main/docs/benchmark.md)

## Tools I use

Swift, Metal, ARKit, COLMAP, Gaussian Splatting, Python, TypeScript and CesiumJS.
