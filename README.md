# AMB82-mini USB Voice LED Controller

中文專題：以電腦瀏覽器語音辨識控制 AMB82-mini 藍燈與綠燈。

完整原始碼、操作方式、系統架構圖與專題報告請見 [SerialVoiceControl](SerialVoiceControl/README.md)。

## 快速開始

1. 以 Arduino IDE 開啟 [SerialVoiceControl.ino](SerialVoiceControl/SerialVoiceControl.ino)，選擇 `Ameba AMB82-MINI` 與正確 COM 埠後上傳。
2. 關閉 Arduino IDE 的序列監控視窗。
3. 用 Chrome 或 Edge 開啟 [SerialVoiceControl.html](SerialVoiceControl/SerialVoiceControl.html)，連接 AMB82-mini 的 USB COM 埠。
4. 說「左邊開燈」、「右邊開燈」、「左邊 3 次」或「右邊 4 次」。

系統架構圖：[SystemArchitecture.svg](SerialVoiceControl/SystemArchitecture.svg)
