from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
w, h=A4
c = canvas.Canvas("figuras.pdf", pagesize=A4)
c.drawImage("Linux.png", 20, h-50,width=50, height=50)
c.showPage()
c.save()
