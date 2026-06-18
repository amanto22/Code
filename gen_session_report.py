# -*- coding: utf-8 -*-
"""Genera un PDF di report di questa sessione locale di Claude Code."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ACCENT = HexColor(0x6C4CF1)   # viola "Claude/AI"
DARK   = HexColor(0x1F2430)
GRAY   = HexColor(0x5A6472)
LIGHT  = HexColor(0xF4F5F7)
LINE   = HexColor(0xE3E6EA)
GREEN  = HexColor(0x1E8E55)
WHITE  = colors.white

OUT = "Report_Sessione_Claude_Code.pdf"
PW, PH = A4
ss = getSampleStyleSheet()

def S(name, **kw):
    base = kw.pop("parent", ss["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

st_body  = S("body", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=DARK)
st_small = S("small", fontName="Helvetica", fontSize=8, leading=11, textColor=GRAY)
st_h1    = S("h1", fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=DARK, spaceAfter=2)
st_h2    = S("h2", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=ACCENT, spaceBefore=8, spaceAfter=4)
st_cell  = S("cell", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK)
st_cellb = S("cellb", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK)
st_li    = S("li", parent=st_body, leading=13)
st_mono  = S("mono", fontName="Courier", fontSize=8.5, leading=12, textColor=DARK)

def header(c, doc):
    c.saveState()
    c.setFillColor(WHITE); c.rect(0, PH-20*mm, PW, 20*mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 12); c.setFillColor(DARK)
    c.drawString(18*mm, PH-13*mm, "Claude Code")
    w = c.stringWidth("Claude Code", "Helvetica-Bold", 12)
    c.setFillColor(ACCENT); c.circle(18*mm + w + 3, PH-13*mm + 1.2, 1.9, fill=1, stroke=0)
    c.setFont("Helvetica", 7.5); c.setFillColor(GRAY)
    c.drawRightString(PW-18*mm, PH-13*mm, "Report di sessione")
    c.setStrokeColor(LINE); c.setLineWidth(0.8)
    c.line(18*mm, PH-20*mm, PW-18*mm, PH-20*mm)
    c.line(18*mm, 14*mm, PW-18*mm, 14*mm)
    c.setFont("Helvetica", 7.5); c.setFillColor(GRAY)
    c.drawString(18*mm, 9.5*mm, "Sessione · Famiglia Cotarella / Italiaonline")
    c.drawRightString(PW-18*mm, 9.5*mm, "Pag. %d" % doc.page)
    c.restoreState()

def bullets(items, color=DARK):
    lis = [ListItem(Paragraph(x, st_li), leftIndent=8) for x in items]
    return ListFlowable(lis, bulletType="bullet", start="•", bulletColor=color,
                        bulletFontSize=9, leftIndent=10, spaceBefore=1, spaceAfter=1)

def kv_table(rows, cw=(40*mm, 125*mm)):
    data = [[Paragraph(k, st_cellb), Paragraph(v, st_cell)] for k, v in rows]
    t = Table(data, colWidths=cw)
    style = [("VALIGN",(0,0),(-1,-1),"TOP"),
             ("LINEBELOW",(0,0),(-1,-2),0.5,LINE),
             ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
             ("LEFTPADDING",(0,0),(0,-1),0)]
    for i in range(len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND",(0,i),(-1,i),LIGHT))
    t.setStyle(TableStyle(style))
    return t

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                      topMargin=24*mm, bottomMargin=18*mm,
                      title="Report di sessione — Claude Code", author="Claude Code")
frame = Frame(18*mm, 16*mm, PW-36*mm, PH-40*mm, id="c")
doc.addPageTemplates([PageTemplate(id="C", frames=[frame], onPage=header)])

story = []
story += [Paragraph("Report di sessione", st_h1)]
story += [Paragraph("Riepilogo delle attività svolte da Claude Code in questa sessione di lavoro.", st_small), Spacer(1, 6)]

story += [kv_table([
    ("Data", "18 giugno 2026"),
    ("Ambiente", "Claude Code on the web — container remoto effimero"),
    ("Repository", "amanto22/Code"),
    ("Branch", "claude/famiglia-cotarella-qualification-dvmk19"),
    ("Working dir", "/home/user/Code"),
    ("Oggetto", "Qualificazione prospect e audit digitale — Famiglia Cotarella"),
])]

story += [Spacer(1, 6), Paragraph("Richiesta dell'utente", st_h2)]
story += [bullets([
    "Analisi e prospect qualification del sito famigliacotarella.it, con SEO audit.",
    "Preparazione di un PDF brand Italiaonline a uso dell'agente per la call col cliente.",
    "Generazione di un PDF di report di questa sessione locale.",
])]

story += [Paragraph("Attività svolte", st_h2)]
story += [bullets([
    "<b>Ricerca prospect:</b> dati camerali (fatturato ~€12,16 mln 2024, −11% YoY; 20–49 dipendenti), "
    "storia e governance (rebranding 2017, le tre eredi Cotarella), portfolio brand.",
    "<b>Audit digitale/SEO:</b> condotto su segnali osservabili — sito che risponde 403 ai crawler automatici, "
    "doppia versione EN (/en/ e /gb/), assenza di e-commerce DTC e di booking enoturismo digitalizzato.",
    "<b>Tentativo dati Semrush:</b> non disponibili — account corporate sub-account privo di unità API. "
    "Segnalato come limite da risolvere per l'audit quantitativo.",
    "<b>Produzione deliverable:</b> generato il PDF di briefing brand Italiaonline (6 pagine) via reportlab.",
    "<b>Versionamento:</b> commit e push sul branch dedicato e apertura PR draft #1.",
])]

story += [Paragraph("Risultati chiave", st_h2)]
story += [bullets([
    "<b>Verdetto:</b> prospect caldo (classe A) — brand premium, decisori orientati al design, "
    "gap monetizzabile (e-commerce diretto + booking enoturismo), motivazione dal calo di fatturato.",
    "<b>Issue SEO #1:</b> doppia versione inglese → rischio contenuti duplicati / hreflang errati.",
    "<b>Gap di business #1:</b> nessun canale di vendita e dato cliente diretti (solo marketplace terzi).",
], color=GREEN)]

story += [Paragraph("Deliverable prodotti", st_h2)]
files = Table([
    [Paragraph("File / artefatto", st_cellb), Paragraph("Descrizione", st_cellb)],
    [Paragraph("Briefing_Famiglia_Cotarella_Italiaonline.pdf", st_mono),
     Paragraph("Briefing pre-call brand Italiaonline (6 pagine), uso interno rete vendita.", st_cell)],
    [Paragraph("gen_briefing.py", st_mono),
     Paragraph("Script reportlab generatore del briefing.", st_cell)],
    [Paragraph("Report_Sessione_Claude_Code.pdf", st_mono),
     Paragraph("Questo documento di report di sessione.", st_cell)],
    [Paragraph("gen_session_report.py", st_mono),
     Paragraph("Script reportlab generatore di questo report.", st_cell)],
    [Paragraph("PR #1 (draft)", st_mono),
     Paragraph("github.com/amanto22/Code/pull/1 — branch della qualificazione.", st_cell)],
], colWidths=[72*mm, 93*mm])
files.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),LIGHT),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LINEBELOW",(0,0),(-1,-1),0.5,LINE),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
]))
story += [files]

story += [Paragraph("Note tecniche e limiti", st_h2)]
story += [bullets([
    "Sito non accessibile ai fetch automatici (HTTP 403): audit basato su fonti pubbliche e segnali indiretti.",
    "Dati SEO quantitativi (traffico, keyword, backlink) non estratti: account Semrush privo di unità API.",
    "Container effimero: tutti gli artefatti sono stati committati e pushati per non andare persi.",
])]

story += [Spacer(1, 8), HRFlowable(width="100%", color=LINE, thickness=0.8), Spacer(1, 4)]
story += [Paragraph(
    "<b>Fonti principali.</b> Sito ufficiale famigliacotarella.it; dati camerali ufficiocamerale.it e "
    "fatturatoitalia.it; stampa di settore (FIRSTonline, DoctorWine, Italy's Finest Wines); marketplace "
    "(Callmewine). Documento generato automaticamente da Claude Code il 18/06/2026.", st_small)]

doc.build(story)
print("OK ->", OUT)
