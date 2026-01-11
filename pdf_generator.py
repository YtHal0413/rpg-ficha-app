from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import mm

from logic import capacidade_inventario, limite_habilidades

def gerar_pdf(dados, destino):
    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        name="Titulo",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    label = ParagraphStyle(
        name="Label",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        spaceAfter=0,
    )

    label2 = ParagraphStyle(
        name="Label",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        spaceAfter=0,
        alignment=TA_CENTER,
    )

    normal = ParagraphStyle(
        name="Normal",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=10,
        spaceAfter=0,
    )

    normal2 = ParagraphStyle(
        name="Normal",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=10,
        spaceAfter=0,
        alignment=TA_CENTER,
    )

    justificado = ParagraphStyle(
        name="Justificado",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=12,
        alignment=TA_JUSTIFY,
        leftIndent=7,
        firstLineIndent=0,
    )

    doc = SimpleDocTemplate(
        destino,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )

    corpo = []

    corpo.append(Paragraph("======================== FICHA DE PERSONAGEM ========================", titulo))

# O nome do condenado e o que carai ele faz da vida
    linha_identificacao = [
        [
            Paragraph("Nome:", label2),
            Paragraph(dados["nome"], normal),
            Paragraph("Arquétipo:", label2),
            Paragraph(dados["arquetipo"], normal),
        ]
    ]

    tabela_id = Table(
        linha_identificacao,
        colWidths=[
            16*mm,
            65*mm,
            24*mm,
            65*mm
        ]
    )

    tabela_id.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (2,0), (-1,-1), 1, colors.black),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (0,0), colors.whitesmoke),
        ('BACKGROUND', (2,0), (2,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (1,0), (1,0), 4),
        ('LEFTPADDING', (3,0), (3,0), 4),
        ('RIGHTPADDING', (1,0), (1,0), 4),
        ('RIGHTPADDING', (3,0), (3,0), 4),
    ]))

    corpo.append(tabela_id)
    corpo.append(Spacer(1,10))

# Os negoço dos atributos dele
    corpo.append(Paragraph("- Atributos", label))
    corpo.append(Spacer(1,10))

    cabecalho_atrib = [
        Paragraph("<b>Força</b>", label2),
        Paragraph("<b>Vigor</b>", label2),
        Paragraph("<b>Agilidade</b>", label2),
        Paragraph("<b>Cognição</b>", label2),
        Paragraph("<b>Expressão</b>", label2),
        Paragraph("<b>Determinação</b>", label2)
    ]
    valores_atrib = [str(dados["atributos"][x]) for x in ["FOR","VIG","AGI","COG","EXP","DET"]]

    tabela_atrib = Table([cabecalho_atrib, valores_atrib],
                         colWidths=[28.35*mm]*6)
    tabela_atrib.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), .5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    corpo.append(tabela_atrib)
    corpo.append(Spacer(1,10))

# A caçamba dos stats tudim
    corpo.append(Paragraph("- Estatísticas", label))
    corpo.append(Spacer(1,10))

    titulos_stats = [
        Paragraph("<b>Saúde</b>", label2),
        "",
        "",
        Paragraph("<b>Disposição</b>", label2),
        "",
        "---",
        Paragraph("<b>Iniciativa</b>", label2),
        "",
        "",
        Paragraph("<b>Presença</b>", label2),
        "",
    ]
    valores_stats = [
        "",
        dados["stats"]["PV"],
        "",
        "",
        dados["stats"]["PD"],
        "---",
        "",
        dados["stats"]["INI"],
        "",
        "",
        dados["stats"]["PRE"]
    ]

    tabela_stats = Table([titulos_stats, valores_stats],
                         colWidths=[15*mm,15*mm,11*mm,15*mm,15*mm,28*mm,15*mm,15*mm,11*mm,15*mm,15*mm,])
    tabela_stats.setStyle(TableStyle([
        ('BOX', (0,0), (1,1), 1, colors.black),
        ('BOX', (3,0), (4,1), 1, colors.black),
        ('BOX', (6,0), (7,1), 1, colors.black),
        ('BOX', (9,0), (10,1), 1, colors.black),
        ('INNERGRID', (0,0), (1,1), .5, colors.black),
        ('INNERGRID', (3,0), (4,1), .5, colors.black),
        ('INNERGRID', (6,0), (7,1), .5, colors.black),
        ('INNERGRID', (9,0), (10,1), .5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('BACKGROUND', (2,0), (2,0), colors.white),
        ('BACKGROUND', (5,0), (5,0), colors.white),
        ('BACKGROUND', (8,0), (8,0), colors.white),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (0,1), (-1,1), 'CENTER'),
        ('SPAN', (0,0), (1,0)),
        ('SPAN', (3,0), (4,0)),
        ('SPAN', (6,0), (7,0)),
        ('SPAN', (9,0), (10,0)),
    ]))
    corpo.append(tabela_stats)
    corpo.append(Spacer(1,15))

# A disgraça das Habilidades que ele tem
    titulo_hab = Paragraph(
        f"<b>Habilidades</b>", normal
    )
    limite_hab = Paragraph(
        f"{len(dados['habilidades'])} / {limite_habilidades(dados['atributos']['COG'])}", normal2
    )

    lista_hab = []
    if dados["habilidades"]:
        for hab in dados["habilidades"]:
            if hab['custo'] != 0:
                titulo_h = f"<b>• {hab['nome']} [{hab['custo']} PD]</b>"
            else:
                titulo_h = f"<b>• {hab['nome']}</b>"
            lista_hab.append(Paragraph(titulo_h, normal))
            lista_hab.append(Paragraph(hab["descricao"].replace("\n","<br/>"), justificado))
            lista_hab.append(Spacer(1,4))
    else:
        lista_hab.append(Paragraph("Nenhuma habilidade cadastrada.", normal))

# E o que djabo ele ta levando nos bolso
    titulo_inv = Paragraph(
        f"<b>Inventário</b>", normal
    )
    lim_inv = Paragraph(
        f"{sum(x['carga'] for x in dados['inventario'])} / {capacidade_inventario(dados['atributos']['FOR'])}", normal2
    )

    lista_inv = []
    if dados["inventario"]:
        for inv in dados["inventario"]:
            titulo_i = f"<b>• {inv['nome']} [{inv['carga']}]</b>"
            lista_inv.append(Paragraph(titulo_i, normal))
            lista_inv.append(Paragraph(inv["descricao"].replace("\n","<br/>"), justificado))
            lista_inv.append(Spacer(1,4))
    else:
        lista_inv.append(Paragraph("Nenhum item cadastrado.", normal))

    tabela_listas = Table(
        [
            [titulo_hab, limite_hab, "", titulo_inv, lim_inv],
            [lista_hab, "", "", lista_inv, ""]
        ],
        colWidths=[68*mm,15*mm, 4*mm, 68*mm,15*mm,]
    )

    tabela_listas.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (1,1), 1, colors.black),
        ('BOX', (3,0), (4,1), 1, colors.black),
        ('INNERGRID', (0,0), (1,1), .5, colors.black),
        ('INNERGRID', (3,0), (4,1), .5, colors.black),
        ('BACKGROUND', (0,0), (1,0), colors.whitesmoke),
        ('BACKGROUND', (3,0), (4,0), colors.whitesmoke),
        ('LINEBEFORE', (1,0), (1,-1), .5, colors.black),
        ('LINEABOVE', (0,1), (1,1), .5, colors.black),
        ('LINEBEFORE', (4,0), (1,-1), .5, colors.black),
        ('LINEABOVE', (3,1), (4,1), .5, colors.black),
        ('SPAN', (0,1), (1,1)),
        ('SPAN', (3,1), (4,1)),
    ]))
    corpo.append(tabela_listas)

# Cria logo essa porra de pdf hom
    doc.build(corpo)
