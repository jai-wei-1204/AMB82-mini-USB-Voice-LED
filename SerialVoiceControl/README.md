# AMB82-mini USB 語音方向燈

本專案讓使用者在電腦瀏覽器說出中文指令，由瀏覽器辨識語音後，透過 USB 序列埠控制 AMB82-mini 的板載 LED。

## 功能

- 「左邊開燈」：藍燈恆亮。
- 「右邊開燈」：綠燈恆亮。
- 「左邊 3 次」：藍燈閃爍 3 次。
- 「右邊 4 次」：綠燈閃爍 4 次。
- 閃爍次數支援 1–20 次；非控制語句不傳送控制命令。
- 網頁顯示辨識文字、開發板回傳的 LED 狀態與 USB 連線錯誤。

## 檔案說明

- `SerialVoiceControl.ino`：上傳至 AMB82-mini 的 Arduino 韌體。
- `SerialVoiceControl.html`：在電腦端以 Chrome／Edge 開啟的操作介面。
- `SystemArchitecture.svg`：系統架構圖。
- `ProjectReport.md`：專題報告內容。

## 硬體與執行環境

- 板卡：Ameba AMB82-MINI。
- USB 序列埠：COM5（實際埠號依電腦而異）。
- 鮑率：115200。
- 瀏覽器：最新版 Google Chrome 或 Microsoft Edge，需支援 Web Serial 與 Web Speech API。
- 藍燈：`LED_B`（D23），`HIGH` 為亮。
- 綠燈：`LED_G`（D24），`HIGH` 為亮。

## 使用方式

1. 以 Arduino IDE 開啟 `SerialVoiceControl/SerialVoiceControl.ino`。
2. 在「工具」選擇開發板 `Ameba AMB82-MINI`，並選擇 AMB82-mini 的 COM 埠。
3. 按「上傳」燒錄韌體；上傳後請關閉 Arduino IDE 的序列監控視窗，避免占用 COM 埠。
4. 用 Chrome 或 Edge 開啟 `SerialVoiceControl.html`。
5. 按「連接 AMB82-mini」，在跳出的清單選擇 AMB82-mini 的 COM 埠。
6. 按「開始語音辨識」，允許瀏覽器使用麥克風，再說出支援的指令。

## 序列命令

網頁會自動傳送下列命令；也可用序列監控視窗手動測試（115200 baud）：

```text
on-left
on-right
blink-left:3
blink-right:4
status
```

開發板會以 `STATE:left`、`STATE:right`、`STATE:blinking-left:3` 或 `STATE:off` 回傳狀態。若命令不合法，會回傳 `ERROR:invalid command`，並維持 LED 原狀。
