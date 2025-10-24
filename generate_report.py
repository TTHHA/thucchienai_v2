from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

# --- Setup ---
# Define corporate colors
TCB_RED = colors.HexColor('#BE1E2D')
TCB_BLUE = colors.HexColor('#00529B')

# ReportLab needs a font that supports Vietnamese characters.
# We will use Times New Roman as requested.
def register_vietnamese_font():
    """Tries to register a Vietnamese font, prioritizing Times New Roman."""
    # Common path for Times New Roman on Windows
    times_path_win = 'C:/Windows/Fonts/times.ttf'
    # Fallback font path
    roboto_path = 'Roboto-Regular.ttf'

    if os.path.exists(times_path_win):
        pdfmetrics.registerFont(TTFont('VietFont', times_path_win))
        print("Successfully registered Times New Roman.")
        return 'VietFont'
    elif os.path.exists(roboto_path):
        pdfmetrics.registerFont(TTFont('VietFont', roboto_path))
        print("Times New Roman not found. Registered Roboto as a fallback.")
        return 'VietFont'
    else:
        print("---")
        print("WARNING: No suitable Vietnamese font found (Times New Roman or Roboto).")
        print("The PDF may not render Vietnamese characters correctly.")
        print("ACTION: Ensure 'times.ttf' is in C:/Windows/Fonts/ or download 'Roboto-Regular.ttf' and place it in this directory.")
        print("---")
        return 'Helvetica' # Default fallback

FONT_NAME = register_vietnamese_font()


# Define Styles
styles = getSampleStyleSheet()

# Modify existing styles, which is the correct approach
styles['Title'].fontName = FONT_NAME
styles['Title'].fontSize = 24
styles['Title'].alignment = TA_CENTER
styles['Title'].spaceAfter = 20

styles['Heading1'].fontName = FONT_NAME
styles['Heading1'].fontSize = 16
styles['Heading1'].spaceAfter = 12
styles['Heading1'].textColor = TCB_RED

styles['Heading2'].fontName = FONT_NAME
styles['Heading2'].fontSize = 14
styles['Heading2'].spaceAfter = 10
styles['Heading2'].textColor = TCB_BLUE

# Use the 'Normal' style for body text
styles['Normal'].fontName = FONT_NAME
styles['Normal'].fontSize = 11
styles['Normal'].alignment = TA_LEFT
styles['Normal'].leading = 14

styles['Bullet'].fontName = FONT_NAME
styles['Bullet'].fontSize = 11
styles['Bullet'].leftIndent = 20
styles['Bullet'].leading = 16

styles['Italic'].fontName = FONT_NAME
styles['Italic'].fontSize = 10
styles['Italic'].textColor = colors.gray
styles['Italic'].leading = 12

# Add a new *custom* style that doesn't conflict with defaults
styles.add(ParagraphStyle(name='SubTitle', fontName=FONT_NAME, fontSize=18, alignment=TA_CENTER, spaceAfter=40))

# Document setup
doc = SimpleDocTemplate("Techcombank_Report_2025.pdf", pagesize=A4,
                        rightMargin=60, leftMargin=60,
                        topMargin=80, bottomMargin=60)
story = []

# --- Header and Footer ---
def header_footer(canvas, doc):
    """Adds a header and footer to each page."""
    canvas.saveState()
    # Header
    header_text = "Báo cáo Hội đồng Quản trị – Techcombank 2025 Insights"
    canvas.setFont(FONT_NAME, 9)
    canvas.setFillColor(colors.gray)
    canvas.drawString(60, A4[1] - 40, header_text)
    canvas.line(60, A4[1] - 50, A4[0] - 60, A4[1] - 50)
    
    # Footer
    footer_text = "Dẫn dắt Tương lai Số - Vững chắc Nền tảng"
    canvas.drawString(60, 40, footer_text)
    canvas.drawRightString(A4[0] - 60, 40, f"Trang {doc.page}")
    canvas.restoreState()

# --- Content Definitions ---

# Page 1: Cover
def build_cover():
    logo_path = "logo.png" # Placeholder for the logo
    try:
        logo = Image(logo_path, width=200, height=100)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 100))
    except:
        story.append(Paragraph("<i>[Không tìm thấy logo.png]</i>", styles['Italic']))
        story.append(Spacer(1, 100))

    story.append(Paragraph("Báo cáo Hội đồng Quản trị – Techcombank 2025 Insights", styles['Title']))
    story.append(Paragraph("Dẫn dắt Tương lai Số - Vững chắc Nền tảng", styles['SubTitle']))
    story.append(Spacer(1, 200))
    story.append(Paragraph("Tháng 10 năm 2025", styles['Normal']))
    story.append(PageBreak())

# Page 3: Foreword
def build_foreword():
    story.append(Paragraph("Trang 3: Thư ngỏ từ Ban Lãnh đạo", styles['Heading1']))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Kính gửi Hội đồng Quản trị,", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Năm 2025 là một năm thể hiện sự vững vàng và năng lực quản trị rủi ro hiệu quả của Techcombank trong bối cảnh thị trường đầy thách thức, qua đó khẳng định vị thế dẫn đầu về niềm tin khách hàng.", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Báo cáo này sẽ tóm tắt những kết quả tài chính chính, phân tích các xu hướng, và đề xuất định hướng chiến lược cho năm 2026, tập trung vào tăng trưởng bền vững, đa dạng hóa nguồn thu và khai thác sâu hơn hệ sinh thái số.", styles['Normal']))
    story.append(PageBreak())

# Page 4: Financial Summary
def build_financial_summary():
    story.append(Paragraph("Trang 4: Tóm tắt Kết quả Tài chính năm 2025", styles['Heading1']))
    story.append(Paragraph("<i>Năm 2025 cho thấy khả năng duy trì nền tảng kinh doanh vững chắc và quản trị rủi ro hiệu quả, dù lợi nhuận chịu áp lực từ bối cảnh kinh tế vĩ mô, thể hiện qua sự sụt giảm nhẹ so với cùng kỳ.</i>", styles['Italic']))
    story.append(Spacer(1, 24))
    
    # Using a table for side-by-side layout
    left_col_text = [
        Paragraph("<b>Các chỉ số chính (Infographic):</b>", styles['Heading2']),
        Spacer(1, 12),
        Paragraph("• Lợi nhuận trước thuế (6T2025): <b>15.135 tỷ VND (-3,2%)</b>", styles['Bullet']),
        Paragraph("• Tổng tài sản: <b>1.037.645 tỷ VND (+6,0%)</b>", styles['Bullet']),
        Paragraph("• Tiền gửi khách hàng: <b>589.078 tỷ VND (+4,3%)</b>", styles['Bullet']),
        Paragraph("• Tỷ lệ CASA: <b>41,1% (Duy trì vị thế dẫn đầu)</b>", styles['Bullet']),
        Paragraph("• Tỷ lệ nợ xấu (NPL): <b>1,32% (Trong tầm kiểm soát)</b>", styles['Bullet'])
    ]
    
    table_data = [[left_col_text, Image('pbt_chart.png', width=250, height=188)]]
    
    table = Table(table_data, colWidths=[250, 260])
    table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    
    story.append(table)
    story.append(PageBreak())

# Page 5: Performance Analysis
def build_performance_analysis():
    story.append(Paragraph("Trang 5: Phân tích Chuyên sâu về Hiệu quả Hoạt động", styles['Heading1']))
    story.append(Paragraph("<i>Việc quản lý rủi ro tín dụng hiệu quả, thể hiện qua chi phí tín dụng giảm, đã giúp bù đắp một phần cho sự sụt giảm của biên lãi ròng (NIM) trong bối cảnh tăng trưởng tín dụng chậm lại.</i>", styles['Italic']))
    story.append(Spacer(1, 12))
    
    # Using a table for a two-column layout
    col1_text = [
        Paragraph("<b>Phân tích Hiệu quả Sinh lời:</b>", styles['Heading2']),
        Paragraph("• NIM (Biên lãi ròng): 3,7%", styles['Bullet']),
        Paragraph("• Chi phí vốn (Cost of Funds): 3,5%", styles['Bullet']),
        Paragraph("• Chi phí tín dụng (Credit Costs): 0.6%", styles['Bullet']),
    ]
    
    col2_text = [
         Paragraph("<b>Phân tích Hiệu quả Quản lý:</b>", styles['Heading2']),
         Paragraph("• ROA (LTM): 2,2%", styles['Bullet']),
         Paragraph("• ROE (LTM): 14,5%", styles['Bullet']),
    ]
    
    data = [[col1_text, col2_text]]
    table = Table(data, colWidths=[250, 250])
    table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(table)
    
    story.append(Spacer(1, 24))
    try:
        story.append(Image('page5.jpg', width=450, height=225))
    except:
        story.append(Paragraph("<i>[Không tìm thấy page5.jpg]</i>", styles['Italic']))
    story.append(PageBreak())

# Page 6: Trends, Risks, Opportunities
def build_trends_analysis():
    story.append(Paragraph("Trang 6: Phân tích Xu hướng, Rủi ro và Cơ hội", styles['Heading1']))
    story.append(Paragraph("<i>Trong bối cảnh kinh tế vĩ mô còn nhiều thách thức, vị thế dẫn đầu về số hóa và dữ liệu mang lại cho Techcombank cơ hội vàng để bứt phá.</i>", styles['Italic']))
    story.append(Spacer(1, 12))
    
    # Table layout for better structure
    trends_text = [
        Paragraph("<b>Xu hướng chính:</b>", styles['Heading2']),
        Paragraph("• Tăng trưởng tín dụng toàn ngành được kỳ vọng ở mức 15%, trong khi TCB ghi nhận 10,6%, phản ánh sự thận trọng và tập trung vào chất lượng.", styles['Bullet']),
    ]
    
    risks_text = [
        Paragraph("<b>Rủi ro cần quản trị:</b>", styles['Heading2']),
        Paragraph("• Áp lực tỷ giá và lãi suất có thể ảnh hưởng đến chi phí vốn.", styles['Bullet']),
        Paragraph("• Cần tiếp tục giám sát chất lượng tài sản, đặc biệt trong lĩnh vực bất động sản.", styles['Bullet']),
    ]
    
    opportunities_text = [
        Paragraph("<b>Cơ hội Vàng:</b>", styles['Heading2']),
        Paragraph("• <b>Chuyển đổi số & Fintech:</b> Tăng trưởng thanh toán số tạo cơ hội lớn để mở rộng dịch vụ ngân hàng số.", styles['Bullet']),
        Paragraph("• <b>Mở rộng Ngân hàng Bán lẻ:</b> Khai thác tiềm năng từ lượng lớn dân số chưa hoặc ít sử dụng dịch vụ ngân hàng.", styles['Bullet']),
        Paragraph("• <b>Dữ liệu lớn & AI:</b> Tận dụng để cá nhân hóa sản phẩm và thúc đẩy thu nhập ngoài lãi.", styles['Bullet']),
    ]
    
    table_data = [[trends_text, risks_text], [opportunities_text, '']]
    table = Table(table_data, colWidths=[250, 250], rowHeights=[100, 100])
    table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('SPAN', (0,1), (1,1)), # Span the opportunities text across two columns
    ]))
    
    story.append(table)
    story.append(PageBreak())

# Page 7: Strategy
def build_strategy():
    story.append(Paragraph("Trang 7: Đề xuất Chiến lược Trọng tâm năm 2026", styles['Heading1']))
    story.append(Paragraph("Ba Trụ cột Chiến lược cho Tăng trưởng Bền vững", styles['SubTitle']))
    
    strategy_data = [
        [Paragraph('1. Tối ưu hóa Hiệu quả & Dẫn dắt bằng Dữ liệu', styles['Heading2']), Paragraph('Ứng dụng AI/ML để tối ưu hóa danh mục cho vay, bán chéo sản phẩm và tự động hóa quy trình.', styles['Normal'])],
        [Paragraph('2. Đa dạng hóa Nguồn thu & Phát triển Ngân hàng Giao dịch', styles['Heading2']), Paragraph('Đẩy mạnh các sản phẩm thẻ, ngoại hối, và dịch vụ quản lý dòng tiền cho doanh nghiệp (Cash Management), và các sản phẩm đầu tư.', styles['Normal'])],
        [Paragraph('3. Đầu tư vào Trải nghiệm Khách hàng & Hệ sinh thái số', styles['Heading2']), Paragraph('Cá nhân hóa hành trình khách hàng trên ứng dụng, mở rộng hợp tác với các đối tác trong hệ sinh thái.', styles['Normal'])]
    ]
    table = Table(strategy_data, colWidths=[180, 280], rowHeights=60)
    table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), FONT_NAME, 11),
        ('TEXTCOLOR', (0,0), (0,-1), TCB_RED),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 1, colors.lightgrey),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(table)
    logo = Image("C:/Users/Tran Thai Hoa/thucchienai/z7150693321576_13d597e2d6652cc836a9f14e97bb1466.jpg" , width=400, height=300)
    logo.hAlign = 'CENTER'
    story.append(logo)
    story.append(PageBreak())
    
# Page 8: Roadmap
def build_roadmap():
    story.append(Paragraph("Trang 8: Kế hoạch hành động & Lộ trình", styles['Heading1']))
    story.append(Spacer(1, 24))
    try:
        story.append(Image('timeline.jpg', width=500, height=250))
    except:
        story.append(Paragraph("<i>[Không tìm thấy timeline.jpg]</i>", styles['Italic']))
    story.append(PageBreak())

# ... And so on for other pages. This is a representative sample.
# For simplicity, we'll combine the rest.

# Page 9: Conclusion
def build_conclusion():
    story.append(Paragraph("Trang 9: Kết luận và Phụ lục", styles['Heading1']))
    story.append(Spacer(1, 24))
    story.append(Paragraph("<b>Kết luận:</b>", styles['Heading2']))
    story.append(Paragraph("2025 là một năm thể hiện năng lực quản trị và sự vững vàng của Techcombank. Dù đối mặt với áp lực thu hẹp biên lãi ròng và tăng trưởng tín dụng chậm hơn so với thị trường chung, ngân hàng vẫn duy trì hiệu quả sinh lời và chất lượng tài sản vượt trội. Nền tảng số hóa và vị thế dẫn đầu về CASA là bệ phóng vững chắc để nắm bắt các cơ hội từ xu hướng thanh toán số và thị trường bán lẻ, qua đó đa dạng hóa nguồn thu trong năm 2026.", styles['Normal']))
    story.append(Spacer(1, 24))
    story.append(Paragraph("<b>Kêu gọi hành động:</b>", styles['Heading2']))
    story.append(Paragraph("Đề nghị HĐQT thông qua 3 định hướng chiến lược và phân bổ nguồn lực cần thiết.", styles['Normal']))
    story.append(PageBreak())
    
# Page 10: Contact
def build_contact():
    story.append(Paragraph("Trang 10: Thông tin liên hệ", styles['Heading1']))
    story.append(Spacer(1, 48))
    story.append(Paragraph("<b>Đơn vị thực hiện:</b> Ban Phân tích Tài chính & Chiến lược", styles['Normal']))
    story.append(Paragraph("<b>Thông tin liên hệ:</b> [Tên người phụ trách], [Email], [Số điện thoại]", styles['Normal']))


# --- Build the PDF ---
print("Building PDF report...")
build_cover()
# Skipping Page 2 (TOC) for simplicity
build_foreword()
build_financial_summary()
build_performance_analysis()
build_trends_analysis()
build_strategy()
build_roadmap()
# Skipping Page 8 (Roadmap)
build_conclusion()
build_contact()

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print("Successfully generated Techcombank_Report_2025.pdf")
