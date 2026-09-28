from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "output" / "pdf" / "AMB82_mini_語音方向燈專題報告.pdf"
FONT_PATH = r"C:\Windows\Fonts\msjh.ttc"
FONT = "MSJH"
ACCENT = colors.HexColor("#1F4E79")
PALE = colors.HexColor("#D9EAF7")
SCREEN_CONNECTED = Path(r"C:\Users\iwin4\AppData\Local\Temp\codex-clipboard-0f0fbfe9-319d-45c5-9fe3-b9db2e4f33c1.png")
SCREEN_DISCONNECTED = Path(r"C:\Users\iwin4\AppData\Local\Temp\codex-clipboard-5b93f526-8375-44fd-b61e-188fcbea951c.png")

pdfmetrics.registerFont(TTFont(FONT, FONT_PATH, subfontIndex=0))
addMapping(FONT, 0, 0, FONT)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CJKTitle", parent=styles["Title"], fontName=FONT, fontSize=22, leading=30, alignment=TA_CENTER, textColor=colors.black, spaceAfter=12))
styles.add(ParagraphStyle(name="CJKH1", parent=styles["Heading1"], fontName=FONT, fontSize=15, leading=22, textColor=colors.black, spaceBefore=12, spaceAfter=7))
styles.add(ParagraphStyle(name="CJKH2", parent=styles["Heading2"], fontName=FONT, fontSize=12, leading=18, textColor=colors.black, spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name="CJKBody", parent=styles["BodyText"], fontName=FONT, fontSize=10, leading=16, spaceAfter=7))
styles.add(ParagraphStyle(name="CJKSmall", parent=styles["BodyText"], fontName=FONT, fontSize=8, leading=11, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="CJKCenter", parent=styles["BodyText"], fontName=FONT, fontSize=10, leading=15, alignment=TA_CENTER))

def P(text, style="CJKBody"):
    return Paragraph(text.replace("\n", "<br/>"), styles[style])

def table(rows, widths=None, small=False):
    formatted = []
    for r, row in enumerate(rows):
        formatted.append([P(str(v), "CJKSmall" if small else "CJKBody") for v in row])
    t = Table(formatted, colWidths=widths, repeatRows=1, hAlign="CENTER")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), FONT),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D9D9D9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for r in range(1, len(rows)):
        if r % 2 == 0:
            commands.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#F7FAFC")))
    t.setStyle(TableStyle(commands))
    return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(A4[0] / 2, 1.0 * cm, f"AMB82-mini USB 語音方向燈專題報告  |  第 {doc.page} 頁")
    canvas.restoreState()

def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    portrait_frame = Frame(1.8*cm, 1.6*cm, A4[0]-3.6*cm, A4[1]-3.0*cm, id="portrait")
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=1.8*cm, rightMargin=1.8*cm, topMargin=1.7*cm, bottomMargin=1.6*cm)
    doc.addPageTemplates([PageTemplate(id="portrait", frames=[portrait_frame], onPage=footer)])
    story = []
    story += [P("AMB82-mini USB 語音方向燈專題報告", "CJKTitle"),
              P("繳交者：＿＿＿＿＿＿　　日期：＿＿＿＿＿＿", "CJKCenter"),
              P("YouTube 示範影片：https://＿＿＿＿＿＿", "CJKCenter"),
              P("GitHub 專案：https://＿＿＿＿＿＿", "CJKCenter"), Spacer(1, 12)]
    story += [P("一、系統架構", "CJKH1"),
              P("本系統不使用 Wi-Fi。使用者在電腦版 Chrome 或 Edge 的自訂網頁介面說出語音，瀏覽器進行中文語音辨識，將辨識出的方向與次數轉為 USB 序列埠命令，傳送至 AMB82-mini。開發板執行 LED 控制後，會將實際執行狀態回傳至網頁，介面再更新顯示。")]
    story += [table([
        ["電腦端", "傳輸", "AMB82-mini"],
        ["麥克風 → Web Speech 語音辨識 → 指令解析 → Web Serial", "USB / COM5 / 115200 baud", "序列埠接收 → 指令驗證 → LED 控制 → STATE 狀態回傳"],
    ], [7.0*cm, 3.3*cm, 7.0*cm]), Spacer(1, 8)]
    story += [P("LED 腳位與控制邏輯", "CJKH2"), table([
        ["功能", "AMB82-mini 腳位", "控制邏輯"],
        ["藍燈", "LED_B / D23", "HIGH 點亮，LOW 熄滅"],
        ["綠燈", "LED_G / D24", "HIGH 點亮，LOW 熄滅"],
    ], [3*cm, 5*cm, 8*cm])]
    story += [P("二、功能說明", "CJKH1"), table([
        ["使用者語音", "網頁轉換命令", "開發板動作"],
        ["左邊開燈", "on-left", "藍燈恆亮，綠燈熄滅"],
        ["右邊開燈", "on-right", "綠燈恆亮，藍燈熄滅"],
        ["左邊 3、左邊三次", "blink-left:3", "藍燈閃爍 3 次，結束後熄滅"],
        ["右邊 4、右邊四下", "blink-right:4", "綠燈閃爍 4 次，結束後熄滅"],
        ["非控制語句", "不傳送", "LED 維持原狀"],
    ], [4.5*cm, 4.0*cm, 7.5*cm])]
    story += [P("系統支援 1 到 20 次閃爍。「次」或「下」可省略，例如「左邊三」也可控制藍燈閃爍 3 次。")]
    story += [P("三、操作說明", "CJKH1")]
    steps = [
        "將 AMB82-mini 以 USB 線連接電腦。",
        "在 Arduino IDE 開啟 SerialSmokeTest.ino，選擇 Ameba AMB82-MINI 與 COM5，完成上傳。",
        "關閉 Arduino IDE 的 Serial Monitor，避免 COM5 被占用。",
        "使用電腦版 Chrome 或 Edge 開啟 SerialVoiceControl.html。",
        "按下「連接 AMB82-mini」，在瀏覽器選擇器中選取 COM5。",
        "按「開始語音辨識」，允許瀏覽器使用麥克風。",
        "說出控制語音，例如「左邊開燈」、「右邊開燈」、「左邊三」或「右邊四次」。",
        "確認網頁顯示的辨識文字與開發板回傳的 LED 狀態一致。",
    ]
    for n, item in enumerate(steps, 1):
        story.append(P(f"{n}. {item}"))
    story += [P("異常處理", "CJKH2"), table([
        ["情況", "系統處理方式"],
        ["語音非控制指令", "網頁顯示提示，不傳送序列埠命令，LED 不改變"],
        ["次數不在 1–20", "網頁拒絕傳送並提示合法範圍"],
        ["開發板收到未知指令", "回傳 ERROR:invalid command，LED 不改變"],
        ["USB 傳送失敗或拔除板子", "網頁顯示 USB 通訊失敗或連線中斷"],
        ["COM 埠被占用", "網頁提示關閉 Serial Monitor 或其他序列工具"],
    ], [5.0*cm, 11.0*cm])]
    story += [P("四、現場測試紀錄", "CJKH1"), P("請在示範前完成下表，並將影片連結填入本報告首頁。")]
    story += [table([
        ["測試項目", "第 1 次", "第 2 次", "第 3 次", "第 4 次", "第 5 次", "LED 實際反應與結論"],
        ["左邊開燈", "＿＿", "＿＿", "＿＿", "＿＿", "＿＿", "＿＿"],
        ["右邊開燈", "＿＿", "＿＿", "＿＿", "＿＿", "＿＿", "＿＿"],
    ], [2.7*cm, 1.25*cm, 1.25*cm, 1.25*cm, 1.25*cm, 1.25*cm, 4.0*cm], small=True)]
    story += [Spacer(1, 8), table([
        ["額外測試", "辨識結果或系統顯示", "LED 實際反應", "結論"],
        ["非控制語句，例如前面五次", "＿＿", "＿＿", "＿＿"],
        ["USB 通訊中斷", "＿＿", "＿＿", "＿＿"],
        ["左邊三次 加分", "＿＿", "＿＿", "＿＿"],
    ], [4.2*cm, 5.2*cm, 3.8*cm, 2.8*cm], small=True)]
    story += [P("五、AI 協作紀錄", "CJKH1")]
    ai_items = [
        "需求拆解：將語音控制 LED 分為語音辨識、指令解析、USB 傳輸、LED 控制與狀態回傳。",
        "硬體確認：確認 LED_B 對應 D23、LED_G 對應 D24，兩者皆以 HIGH 點亮。",
        "韌體設計：建立支援恆亮、指定次數閃爍、狀態查詢與未知命令拒絕的序列埠協定。",
        "介面設計：建立使用 Web Speech 與 Web Serial 的中文語音控制介面。",
        "除錯協助：分析麥克風權限、COM 埠被占用、中文數字「兩」解析與韌體版本不一致等問題。",
        "文件整理：協助建立系統架構、操作說明、測試表格與專題心得。",
    ]
    for item in ai_items:
        story.append(P("• " + item))
    story += [P("AI 提供程式建議與文件協作；板卡接線、程式上傳、現場測試與結果確認仍由專題製作者執行與驗證。")]
    story += [P("六、學習心得", "CJKH1"),
              P("本專題讓我了解語音控制系統不只有「辨識語音」一個步驟，而是需要將辨識結果安全且正確地傳送至硬體，再由硬體回報實際狀態。使用瀏覽器語音辨識可以降低 AMB82-mini 的運算負擔，但也要處理瀏覽器麥克風權限與不同瀏覽器的相容性問題。"),
              P("在硬體控制方面，我學到不能只根據網頁送出的命令更新畫面。介面應等待 AMB82-mini 回傳 STATE 訊息後才顯示 LED 狀態，才能反映真正的執行結果。針對非控制語句與不合法次數，系統採取「不傳送或不執行」的方式，可避免誤動作。"),
              P("本次加分功能實作了「方向加次數」的動態控制，而不是固定幾句指令。例如使用者說「左邊三」或「右邊四次」，系統會解析方向與次數，再讓對應 LED 閃爍指定次數。未來可繼續加入中英文語音、語音回覆、更多 LED 模式，或改用離線語音模型以降低對瀏覽器服務的依賴。")]
    story += [P("七、原始碼與執行環境", "CJKH1"),
              P("完整原始碼預計上傳至 GitHub，專案至少應包含 SerialSmokeTest.ino、SerialVoiceControl.html 與 README.md。"),
              table([
                  ["項目", "設定"],
                  ["開發板", "AMB82-mini"],
                  ["Arduino IDE 板卡", "Ameba AMB82-MINI"],
                  ["電腦連線", "USB 序列埠 COM5，115200 baud"],
                  ["瀏覽器", "電腦版 Google Chrome 或 Microsoft Edge"],
                  ["網頁 API", "Web Speech API、Web Serial API"],
              ], [5.0*cm, 11.0*cm])]
    story += [P("八、介面與異常處理截圖", "CJKH1"),
              P("下列截圖為電腦端自訂控制介面的實作證據。左圖顯示 AMB82-mini 已連接及語音、手動閃爍控制介面；右圖顯示 USB 連線中斷時的明確提示。")]
    if SCREEN_CONNECTED.exists() and SCREEN_DISCONNECTED.exists():
        img1 = Image(str(SCREEN_CONNECTED), width=7.7*cm, height=6.53*cm)
        img2 = Image(str(SCREEN_DISCONNECTED), width=7.7*cm, height=6.53*cm)
        screenshot_table = Table([[img1, img2], [P("圖 1 正常連線與自訂控制介面", "CJKSmall"), P("圖 2 USB 連線中斷提示", "CJKSmall")]], colWidths=[8.0*cm, 8.0*cm])
        screenshot_table.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("ALIGN", (0,0), (-1,-1), "CENTER"), ("BOTTOMPADDING", (0,0), (-1,-1), 6)]))
        story.append(screenshot_table)
    else:
        story.append(P("截圖檔案未找到，請重新插入正常連線與通訊中斷畫面。"))
    doc.build(story)
    print(OUT)

if __name__ == "__main__":
    build()
