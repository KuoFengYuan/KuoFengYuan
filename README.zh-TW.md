# Feng-Yuan Kuo

[English](README.md) | **繁體中文**

我是 Feng-Yuan Kuo，在台灣做 3D 視覺與重建開發，主要方向是 Gaussian Splatting 和行動裝置上的模型訓練。

- **手機端 3DGS**：用 Swift 和 Metal 在 iPhone 上訓練，提供即時預覽與模型編輯。
- **拍攝與重建**：ARKit／LiDAR 拍攝、相機姿態優化、深度融合與 COLMAP 資料集整理。
- **3D 檢視工具**：網頁上的 Splat 模型檢視，以及 CesiumJS、3D Tiles 地理空間資料展示。

**[試用 iPhone App](https://testflight.apple.com/join/hKhVdTUR)** · [看實錄](#iphone-實錄) · [找專案](#專案)

## 專案

| 專案 | 用途 |
| --- | --- |
| [Splatify-Anything](https://github.com/KuoFengYuan/splatify-anything) | iPhone 掃描、手機端 3DGS 訓練與 COLMAP 資料集匯出。 |
| [prior-pose-refine](https://github.com/KuoFengYuan/prior-pose-refine) | 用 COLMAP 修正先驗相機姿態、焦距與鏡頭畸變，輸出 3DGS 訓練資料集。 |
| [align-capture](https://github.com/KuoFengYuan/align-capture) | 從無人機 RTSP 影像擷取照片，寫入對應的 MAVLink GPS 資料，供 COLMAP 使用。 |
| [Recon Studio](https://github.com/KuoFengYuan/reconstudio) | 在本機網頁介面處理影片影格、執行 COLMAP 與訓練 3DGS。 |
| [3D Tiles Splat Viewer](https://github.com/KuoFengYuan/cesium-gaussian-splat-viewer) | 將 PLY 模型轉為 3D Tiles，放到 CesiumJS 地球上檢視。 |
| [RAGGlass](https://github.com/KuoFengYuan/RAGGlass) | 對照文件檢索結果、來源段落與回答。 |

## AnyReplica

用 iPhone 掃描空間，直接在手機上訓練 3D Gaussian Splatting 模型。完成後可以走進模型、編輯，或匯出模型與 COLMAP 資料集。

[GitHub 專案：Splatify-Anything](https://github.com/KuoFengYuan/splatify-anything)。

### iPhone 實錄

掃描、訓練、模型走訪與編輯。iPhone 螢幕錄影，加速至 30 秒。

https://github.com/user-attachments/assets/3f8944d1-145c-4fc3-96c1-3cb5fdb734bf

<sub>示範影片採 [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/)，限非商用。</sub>

## prior-pose-refine

從近似的相機姿態與點雲出發，用 COLMAP 修正姿態、焦距與鏡頭畸變，輸出去畸變影像供 3DGS 訓練。輸出會維持與輸入的公尺座標系對齊。

可搭配 Splatify-Anything 匯出的 ARKit／LiDAR 資料，也能使用其他來源提供的相容先驗模型。

[程式與用法](https://github.com/KuoFengYuan/prior-pose-refine) · [運作方式](https://github.com/KuoFengYuan/prior-pose-refine/blob/main/docs/method.zh-TW.md) · [實驗數據](https://github.com/KuoFengYuan/prior-pose-refine/blob/main/docs/benchmark.zh-TW.md)

## 使用的工具

Swift、Metal、ARKit、COLMAP、Gaussian Splatting、Python、TypeScript 與 CesiumJS。
