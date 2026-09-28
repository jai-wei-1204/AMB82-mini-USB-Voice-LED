# AMB82-mini USB 語音方向燈

此版本不使用 Wi-Fi。電腦以 USB 連接 AMB82-mini，Chrome／Edge 網頁透過 Web Serial 將語音控制指令傳至 COM 埠。

1. 上傳 `SerialSmokeTest.ino` 到 AMB82-mini。
2. 關閉 Arduino IDE 的 Serial Monitor，否則瀏覽器無法使用 COM5。
3. 在電腦版 Chrome 或 Edge 開啟 `SerialVoiceControl.html`。
4. 按「連接 AMB82-mini」，在選擇器選取 COM5。
5. 按「開始語音辨識」，允許麥克風後說「左邊開燈」或「右邊開燈」讓對應 LED 恆亮；說「左邊 3 次」或「右邊 4 次」則閃爍指定次數。左邊控制藍燈，右邊控制綠燈。

板子以 `STATE:left` 或 `STATE:right` 回報狀態，介面只依這個板端回報更新 LED 顯示。非控制語音不會送出控制命令；板子收到未知指令也不會改變 LED。
