from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def gerar_pdf(dados, destino):
    c = canvas.Canvas(destino, pagesize=A4)
    w, h = A4
    y = h - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "FICHA DE PERSONAGEM")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "Nome: " + dados["nome"])
    y -= 20
    c.drawString(50, y, "Arquétipo: " + dados["arquetipo"])
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Atributos")
    y -= 20
    c.setFont("Helvetica", 12)
    for k in ["FOR","VIG","AGI","COG","EXP","DET"]:
        c.drawString(60, y, k + ": " + str(dados["atributos"][k]))
        y -= 15
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Estatisticas")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(60, y, "Saúde: " + str(dados["stats"]["Saúde"]))
    y -= 15
    c.drawString(60, y, "Disposição: " + str(dados["stats"]["Disposição"]))
    y -= 15
    c.drawString(60, y, "Iniciativa: " + str(dados["stats"]["Iniciativa"]))
    y -= 15
    c.drawString(60, y, "Presença: " + str(dados["stats"]["Presença"]))
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Habilidades")
    y -= 20
    c.setFont("Helvetica", 12)
    if dados["habilidades"]:
        for h in dados["habilidades"]:
            if y < 80:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = h - 40
            c.drawString(60, y, h["nome"] + " (Custo: " + str(h["custo"]) + ")")
            y -= 15
            txt = h["descricao"]
            linha = ""
            for palavra in txt.split():
                if len(linha + palavra) < 60:
                    linha += palavra + " "
                else:
                    c.drawString(80, y, linha)
                    y -= 15
                    linha = palavra + " "
            if linha:
                c.drawString(80, y, linha)
                y -= 20
    else:
        c.drawString(60, y, "Nenhuma")
        y -= 20
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Inventário")
    y -= 20
    c.setFont("Helvetica", 12)
    if dados["inventario"]:
        for i in dados["inventario"]:
            if y < 80:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = h - 40
            c.drawString(60, y, i["nome"] + " (Carga: " + str(i["carga"]) + ")")
            y -= 15
            txt = i["descricao"]
            linha = ""
            for palavra in txt.split():
                if len(linha + palavra) < 60:
                    linha += palavra + " "
                else:
                    c.drawString(80, y, linha)
                    y -= 15
                    linha = palavra + " "
            if linha:
                c.drawString(80, y, linha)
                y -= 20
    else:
        c.drawString(60, y, "Nenhum item")
    c.save()
