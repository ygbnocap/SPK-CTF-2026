#!/usr/bin/env python3
"""SPK-Steg-06: generate a fictitious contract with searchable invisible text."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = Path(__file__).resolve().parent / 'contract.pdf'
FLAG = 'SPKctf{invisible_pdf_text}'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu', FONT))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', FONT_BOLD))

c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
c.setTitle('Договор об участии в учебном мероприятии')
c.setAuthor('SPK.ctf — учебный документ')
W, H = A4
navy=(0.10,0.17,0.30)
blue=(0.13,0.34,0.70)
muted=(0.40,0.45,0.52)

def txt(x,y,s,size=10,bold=False,color=navy):
    c.setFillColorRGB(*color)
    c.setFont('DejaVu-Bold' if bold else 'DejaVu',size)
    c.drawString(x,y,s)

c.setFillColorRGB(*blue)
c.rect(0,H-14,W,14,stroke=0,fill=1)
txt(52,H-72,'SPK.ctf / 2026',13,True,blue)
txt(52,H-110,'ДОГОВОР № 06',20,True)
txt(52,H-140,'об участии в учебном мероприятии',12)
c.setStrokeColorRGB(.78,.82,.87)
c.line(52,H-158,W-52,H-158)
txt(52,H-190,'г. Омск',10)
txt(W-180,H-190,'20 октября 2026 г.',10)

sections=[
('1. Предмет соглашения',[
'Настоящий документ регулирует участие в учебном мероприятии SPK.ctf.',
'Организатор предоставляет участникам набор практических заданий.',
'Все материалы предназначены исключительно для образовательных целей.']),
('2. Порядок участия',[
'Участник решает задания в пределах специально выделенной среды.',
'Полученные ответы отправляются через интерфейс соревнования.',
'Результаты учитываются согласно правилам мероприятия.']),
('3. Обязанности участников',[
'Не допускаются действия за пределами учебной инфраструктуры.',
'Запрещены перегрузка сервисов и вмешательство в чужие учётные записи.',
'Участник самостоятельно обеспечивает сохранность своих материалов.']),
('4. Заключительные положения',[
'Документ вступает в силу в момент начала мероприятия.',
'Изменения доводятся до сведения участников организатором.',
'Стороны подтверждают ознакомление с правилами SPK.ctf.']),
]
y=H-235
for heading,lines in sections:
    txt(52,y,heading,11,True,blue)
    y-=25
    for line in lines:
        txt(52,y,line,8.8)
        y-=20
    y-=15
c.setStrokeColorRGB(.65,.7,.76)
c.line(52,120,245,120)
c.line(340,120,W-52,120)
txt(52,103,'Организатор',9,color=muted)
txt(340,103,'Участник',9,color=muted)
txt(52,58,'SPK.ctf • Учебный образец. Не является юридическим договором.',8,color=muted)
# Invisible *searchable* text: white, size 1pt, positioned inside the page.
# It remains part of the PDF text layer and is recoverable by pdftotext / select all.
c.setFillColorRGB(1,1,1)
c.setFont('DejaVu',1)
c.drawString(54,76,FLAG)
c.showPage()
c.save()
print('Created:', OUT)
