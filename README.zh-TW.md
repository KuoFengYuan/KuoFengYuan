# Feng-Yuan Kuo

[English](README.md) | **繁體中文**

我做 3D 掃描與重建工具，從 iPhone 拍攝、Gaussian Splatting 訓練，到網頁上的模型檢視。

**[試用 iPhone App](https://testflight.apple.com/join/hKhVdTUR)** · [看實錄](#iphone-實錄) · [找專案](#專案)

## 專案

| 專案 | 用途 |
| --- | --- |
| [Splatify-Anything](https://github.com/KuoFengYuan/splatify-anything) | iPhone 掃描、手機端 3DGS 訓練與 COLMAP 資料集匯出。 |
| [align-capture](https://github.com/KuoFengYuan/align-capture) | 從無人機 RTSP 影像擷取照片，寫入對應的 MAVLink GPS 資料，供 COLMAP 使用。 |
| [Recon Studio](https://github.com/KuoFengYuan/reconstudio) | 在本機網頁介面處理影片影格、執行 COLMAP 與訓練 3DGS。 |
| [3D Tiles Splat Viewer](https://github.com/KuoFengYuan/cesium-gaussian-splat-viewer) | 將 PLY 模型轉為 3D Tiles，放到 CesiumJS 地球上檢視。 |
| [RAGGlass](https://github.com/KuoFengYuan/RAGGlass) | 對照文件檢索結果、來源段落與回答。 |

## SplatCapture Studio

用 iPhone 掃描空間，直接在手機上訓練 3D Gaussian Splatting 模型。完成後可以走進模型、編輯，或匯出模型與 COLMAP 資料集。

[GitHub 專案：Splatify-Anything](https://github.com/KuoFengYuan/splatify-anything)。

### iPhone 實錄

掃描、訓練、模型走訪與編輯。iPhone 螢幕錄影，加速至 30 秒。

https://github.com/user-attachments/assets/3f8944d1-145c-4fc3-96c1-3cb5fdb734bf

<sub>示範影片採 [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/)，限非商用。</sub>

## 使用的工具

Swift、Metal、ARKit、COLMAP、Gaussian Splatting、Python、TypeScript 與 CesiumJS。
