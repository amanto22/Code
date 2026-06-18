# -*- coding: utf-8 -*-
"""Genera il PDF di briefing pre-call (brand Italiaonline) per Famiglia Cotarella."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    FrameBreak, NextPageTemplate, PageBreak, ListFlowable, ListItem, HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ---- Brand palette Italiaonline -------------------------------------------
IOL_RED   = HexColor(0xE2001A)   # rosso brand Italiaonline
IOL_DARK  = HexColor(0x1F2430)   # antracite
IOL_GRAY  = HexColor(0x5A6472)
IOL_LIGHT = HexColor(0xF4F5F7)
IOL_LINE  = HexColor(0xE3E6EA)
GREEN     = HexColor(0x1E8E55)
AMBER     = HexColor(0xB7791F)
WHITE     = colors.white

OUT = "Briefing_Famiglia_Cotarella_Italiaonline.pdf"
PW, PH = A4

# ---- Styles ----------------------------------------------------------------
ss = getSampleStyleSheet()
def S(name, **kw):
    base = kw.pop("parent", ss["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

st_body   = S("body", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=IOL_DARK)
st_small  = S("small", fontName="Helvetica", fontSize=8, leading=11, textColor=IOL_GRAY)
st_h1     = S("h1", fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=IOL_DARK, spaceAfter=2)
st_h2     = S("h2", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=IOL_RED, spaceBefore=8, spaceAfter=4)
st_kicker = S("kicker", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=IOL_RED, spaceAfter=2)
st_cell   = S("cell", fontName="Helvetica", fontSize=9, leading=12, textColor=IOL_DARK)
st_cellb  = S("cellb", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=IOL_DARK)
st_cellw  = S("cellw", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=WHITE)
st_li     = S("li", parent=st_body, leading=13)
st_cover_t= S("covt", fontName="Helvetica-Bold", fontSize=30, leading=34, textColor=WHITE)
st_cover_s= S("covs", fontName="Helvetica", fontSize=13, leading=18, textColor=WHITE)
st_cover_k= S("covk", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=WHITE)
st_wordmark = S("wm", fontName="Helvetica-Bold", fontSize=20, leading=22, textColor=WHITE)

# ---- Page furniture --------------------------------------------------------
def wordmark_text(c, x, y, size=13, color=IOL_DARK, dot=IOL_RED):
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(color)
    c.drawString(x, y, "Italiaonline")
    # accent dot
    w = c.stringWidth("Italiaonline", "Helvetica-Bold", size)
    c.setFillColor(dot)
    c.circle(x + w + size*0.28, y + size*0.10, size*0.16, fill=1, stroke=0)

def cover_bg(c, doc):
    c.saveState()
    c.setFillColor(IOL_DARK)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    # red band
    c.setFillColor(IOL_RED)
    c.rect(0, PH*0.62, PW, 6, fill=1, stroke=0)
    # decorative corner block
    c.setFillColor(IOL_RED)
    c.rect(PW-70*mm, PH-8*mm, 70*mm, 8*mm, fill=1, stroke=0)
    c.restoreState()

def content_bg(c, doc):
    c.saveState()
    # header
    c.setFillColor(WHITE)
    c.rect(0, PH-20*mm, PW, 20*mm, fill=1, stroke=0)
    wordmark_text(c, 18*mm, PH-13*mm, size=12, color=IOL_DARK, dot=IOL_RED)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(IOL_GRAY)
    c.drawRightString(PW-18*mm, PH-13*mm, "Scheda Pre-Call · Uso interno riservato")
    c.setStrokeColor(IOL_LINE); c.setLineWidth(0.8)
    c.line(18*mm, PH-20*mm, PW-18*mm, PH-20*mm)
    # footer
    c.setStrokeColor(IOL_LINE); c.setLineWidth(0.8)
    c.line(18*mm, 14*mm, PW-18*mm, 14*mm)
    c.setFont("Helvetica", 7.5); c.setFillColor(IOL_GRAY)
    c.drawString(18*mm, 9.5*mm, "Italiaonline · Prospect: Famiglia Cotarella S.r.l.")
    c.drawRightString(PW-18*mm, 9.5*mm, "Pag. %d" % doc.page)
    c.setFont("Helvetica-Oblique", 7); c.setFillColor(IOL_GRAY)
    c.drawCentredString(PW/2, 6*mm, "Documento riservato a uso interno della rete vendita — non distribuire al cliente")
    c.restoreState()

# ---- Helpers ---------------------------------------------------------------
def chip(text, fill, tc=WHITE):
    t = Table([[Paragraph(text, S("c", fontName="Helvetica-Bold", fontSize=8, textColor=tc, alignment=TA_CENTER))]],
              colWidths=[60*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),fill),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("ROUNDEDCORNERS",[4,4,4,4]),
    ]))
    return t

def kv_table(rows, cw=(46*mm, 119*mm)):
    data = [[Paragraph(k, st_cellb), Paragraph(v, st_cell)] for k, v in rows]
    t = Table(data, colWidths=cw)
    style = [
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LINEBELOW",(0,0),(-1,-2),0.5,IOL_LINE),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(0,-1),0),
    ]
    for i in range(len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND",(0,i),(-1,i),IOL_LIGHT))
    t.setStyle(TableStyle(style))
    return t

def bullets(items, color=IOL_DARK, bullet="•"):
    lis = [ListItem(Paragraph(x, st_li), leftIndent=8, value=None) for x in items]
    return ListFlowable(lis, bulletType="bullet", start=bullet, bulletColor=color,
                        bulletFontSize=9, leftIndent=10, spaceBefore=1, spaceAfter=1)

def section_title(t):
    return Paragraph(t, st_h2)

# ---- Document --------------------------------------------------------------
doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=18*mm, rightMargin=18*mm,
                      topMargin=24*mm, bottomMargin=18*mm, title="Briefing Pre-Call — Famiglia Cotarella",
                      author="Italiaonline")

cover_frame = Frame(0, 0, PW, PH, leftPadding=22*mm, rightPadding=22*mm,
                    topPadding=24*mm, bottomPadding=24*mm, id="cover")
content_frame = Frame(18*mm, 16*mm, PW-36*mm, PH-38*mm, id="content")

doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_bg),
    PageTemplate(id="Content", frames=[content_frame], onPage=content_bg),
])

story = []

# ===== COVER =====
story += [Spacer(1, 8*mm)]
story += [Paragraph("Italiaonline", st_wordmark)]
story += [Spacer(1, 60*mm)]
story += [Paragraph("SCHEDA PRE-CALL · SALES BRIEFING", st_cover_k)]
story += [Spacer(1, 3*mm)]
story += [Paragraph("Famiglia Cotarella", st_cover_t)]
story += [Spacer(1, 2*mm)]
story += [Paragraph("Qualificazione prospect &amp; audit digitale per la call commerciale", st_cover_s)]
story += [Spacer(1, 14*mm)]
cover_meta = Table([
    [Paragraph("CLIENTE", st_cover_k), Paragraph("Famiglia Cotarella S.r.l. — Montecchio (TR)", st_cover_s)],
    [Paragraph("CALL", st_cover_k), Paragraph("Venerdì 19 giugno 2026 — mattina", st_cover_s)],
    [Paragraph("SETTORE", st_cover_k), Paragraph("Vitivinicolo premium / wine &amp; hospitality", st_cover_s)],
    [Paragraph("PRIORITÀ", st_cover_k), Paragraph("Prospect caldo (A) — alto potenziale", st_cover_s)],
], colWidths=[28*mm, 120*mm])
cover_meta.setStyle(TableStyle([
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ("LEFTPADDING",(0,0),(-1,-1),0),
]))
story += [cover_meta]
story += [NextPageTemplate("Content"), PageBreak()]

# ===== P1: SNAPSHOT + VERDETTO =====
story += [Paragraph("1 · Snapshot azienda", st_h1)]
story += [Paragraph("Chi hai davanti e perché vale la chiamata.", st_small), Spacer(1, 4)]
story += [kv_table([
    ("Ragione sociale", "Famiglia Cotarella S.r.l. (già Az. Vinicola Falesco / Liaison) — P.IVA 00472180553"),
    ("Sede", "Loc. San Pietro · Montecchio (TR), Umbria"),
    ("Attività", "Produzione vino premium · enoturismo · ospitalità"),
    ("Fondazione", "1979 (come Falesco). Rebranding in “Famiglia Cotarella” nel 2017"),
    ("Fatturato", "~ € 12,16 mln (2024), in calo da ~ € 13,74 mln (2023) — circa −11% YoY"),
    ("Dipendenti", "20–49 (costo del personale ~ € 1,81 mln)"),
    ("Governance", "2ª generazione: Dominga, Marta ed Enrica Cotarella (subentro 2017)"),
    ("Figura-chiave", "Riccardo Cotarella — enologo di fama mondiale, Presidente Assoenologi"),
    ("Brand di punta", "Montiano (Merlot icona), Ferentano (Roscetto), linea Falesco, Cotarella, Liaison"),
])]
story += [Spacer(1, 8)]
story += [section_title("Verdetto di qualificazione")]
verdict = Table([[
    Paragraph("PROSPECT CALDO — Classe A", S("vt", fontName="Helvetica-Bold", fontSize=12, textColor=WHITE)),
    Paragraph("Azienda strutturata e brand premium · decision-maker accessibili e orientati al design · "
              "gap monetizzabile evidente (e-commerce diretto + booking enoturismo) · "
              "calo di fatturato = motivazione concreta a investire sui canali a margine. "
              "<b>Approccio consigliato: vendita a valore, non a prezzo.</b>",
              S("vb", fontName="Helvetica", fontSize=9, leading=12.5, textColor=WHITE)),
]], colWidths=[42*mm, 123*mm])
verdict.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,0),IOL_RED),
    ("BACKGROUND",(1,1),(1,1),IOL_DARK),
    ("BACKGROUND",(1,0),(1,0),IOL_DARK),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
    ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
]))
story += [verdict]
story += [PageBreak()]

# ===== P2: FIT / PERCHE COMPRA =====
story += [Paragraph("2 · Perché è un buon prospect", st_h1)]
story += [Paragraph("Leve da usare in apertura e segnali a cui prestare attenzione.", st_small), Spacer(1, 4)]

story += [section_title("Segnali a favore (leve di vendita)")]
story += [bullets([
    "<b>Gap e-commerce proprietario:</b> i vini si comprano solo tramite terzi (Callmewine, Tannico, Vinissimus…). "
    "L'azienda regala margine e dati cliente agli intermediari → opportunità DTC enorme.",
    "<b>Management femminile di 2ª generazione</b> (Dominga, Marta, Enrica): profilo aperto a brand, design e digitale.",
    "<b>Fatturato in flessione (~−11%):</b> spinta a presidiare canali diretti, più redditizi, e a internazionalizzare.",
    "<b>Enoturismo già attivo</b> (visite e degustazioni in IT/EN/PT) ma <b>senza booking &amp; pagamento online</b> → upsell immediato.",
    "<b>Vocazione internazionale</b> (versioni IT/EN/GB del sito, export forte) → terreno per SEO e advertising internazionale.",
    "<b>Brand premium con storytelling forte</b> e capacità di spesa: azienda strutturata, non micro-cantina.",
], color=GREEN)]

story += [Spacer(1, 4), section_title("Punti di attenzione")]
story += [bullets([
    "<b>Budget marketing possibilmente sotto pressione</b> per il calo di fatturato — usalo come leva, non come freno.",
    "<b>Probabili fornitori già attivi</b> (brand curato): entra con un angolo differenziante — DTC + enoturismo, non il semplice “rifacimento sito”.",
    "<b>Sensibilità estetica alta:</b> qualunque proposta deve essere all'altezza del posizionamento luxury del brand.",
], color=AMBER)]
story += [PageBreak()]

# ===== P3: AUDIT =====
story += [Paragraph("3 · Audit digitale &amp; SEO", st_h1)]
story += [Paragraph("Basato su segnali tecnici osservabili e fonti pubbliche. I dati quantitativi Semrush "
                    "(traffico, keyword, backlink) non sono ancora disponibili sull'account.", st_small), Spacer(1, 4)]

audit_rows = [
    ["Area", "Rilevazione", "Stato"],
    ["E-commerce DTC", "Nessuno shop ufficiale: vendita solo tramite marketplace terzi.", "CRITICO"],
    ["Booking enoturismo", "Prenotazione esperienze “su richiesta”, non digitalizzata né con pagamento online.", "CRITICO"],
    ["Internazionalizzazione", "Doppia versione inglese (/en/ e /gb/): rischio contenuti duplicati e hreflang errati.", "DA RISOLVERE"],
    ["Accesso crawler", "Sito risponde 403 a richieste automatiche (WAF aggressivo): verificare in GSC che non blocchi bot legittimi.", "DA VERIFICARE"],
    ["Struttura URL", "URL puliti e parlanti, gerarchia chiara dei prodotti.", "BUONO"],
    ["Dati strutturati", "Da verificare Schema.org (Product, Winery/LocalBusiness, Event per le degustazioni).", "DA VERIFICARE"],
    ["First-party data / CRM", "Senza shop e booking diretti, raccolta dati e remarketing fortemente limitati.", "OPPORTUNITÀ"],
]
status_color = {"CRITICO": IOL_RED, "DA RISOLVERE": AMBER, "DA VERIFICARE": IOL_GRAY,
                "BUONO": GREEN, "OPPORTUNITÀ": IOL_DARK}
data = [[Paragraph(audit_rows[0][0], st_cellw), Paragraph(audit_rows[0][1], st_cellw), Paragraph(audit_rows[0][2], st_cellw)]]
for r in audit_rows[1:]:
    data.append([Paragraph(r[0], st_cellb), Paragraph(r[1], st_cell),
                 Paragraph("<b>%s</b>" % r[2], S("stt", fontName="Helvetica-Bold", fontSize=8,
                           textColor=status_color[r[2]], alignment=TA_CENTER))])
audit = Table(data, colWidths=[33*mm, 100*mm, 32*mm])
astyle = [
    ("BACKGROUND",(0,0),(-1,0),IOL_DARK),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ("LINEBELOW",(0,0),(-1,-1),0.5,IOL_LINE),
    ("ALIGN",(2,0),(2,-1),"CENTER"),
]
for i in range(1, len(data)):
    if i % 2 == 0:
        astyle.append(("BACKGROUND",(0,i),(-1,i),IOL_LIGHT))
audit.setStyle(TableStyle(astyle))
story += [audit]
story += [Spacer(1, 6)]
story += [section_title("Da estrarre prima/durante la trattativa (con Semrush + GSC)")]
story += [bullets([
    "Authority Score e profilo backlink vs competitor (Antinori, Frescobaldi, Lungarotti, Caprai).",
    "Keyword organiche e traffico stimato: mercato IT vs export.",
    "Core Web Vitals e performance mobile (PageSpeed).",
], color=IOL_RED)]
story += [PageBreak()]

# ===== P4: SOLUZIONI ITALIAONLINE + PITCH =====
story += [Paragraph("4 · Soluzioni Italiaonline da proporre", st_h1)]
story += [Paragraph("Mappa “bisogno del cliente → prodotto Italiaonline”. Parti dal valore di business, non dalla tecnologia.", st_small), Spacer(1, 4)]

sol = [
    ["Bisogno rilevato", "Soluzione Italiaonline", "Priorità"],
    ["Vendere in diretta, recuperare margine e dati", "E-commerce / Sito transazionale + gestione catalogo", "ALTA"],
    ["Digitalizzare visite e degustazioni", "Sito + booking esperienze, landing dedicate, pagamenti online", "ALTA"],
    ["Presidio export e ricerca organica", "SEO (incl. internazionale/hreflang) + SEM / Google Ads", "ALTA"],
    ["Visibilità locale enoturismo", "Local marketing / Google Business Profile (heritage PagineGialle)", "MEDIA"],
    ["Fidelizzazione &amp; riacquisto", "Email marketing / DEM + CRM", "MEDIA"],
    ["Awareness brand premium", "Display/Adv su network premium Libero·Virgilio + social advertising", "MEDIA"],
]
sd = [[Paragraph(sol[0][0], st_cellw), Paragraph(sol[0][1], st_cellw), Paragraph(sol[0][2], st_cellw)]]
pri_color = {"ALTA": IOL_RED, "MEDIA": AMBER}
for r in sol[1:]:
    sd.append([Paragraph(r[0], st_cellb), Paragraph(r[1], st_cell),
               Paragraph("<b>%s</b>" % r[2], S("pr", fontName="Helvetica-Bold", fontSize=8,
                         textColor=pri_color[r[2]], alignment=TA_CENTER))])
soltab = Table(sd, colWidths=[55*mm, 78*mm, 32*mm])
sstyle = [
    ("BACKGROUND",(0,0),(-1,0),IOL_RED),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ("LINEBELOW",(0,0),(-1,-1),0.5,IOL_LINE),
    ("ALIGN",(2,0),(2,-1),"CENTER"),
]
for i in range(1, len(sd)):
    if i % 2 == 0:
        sstyle.append(("BACKGROUND",(0,i),(-1,i),IOL_LIGHT))
soltab.setStyle(TableStyle(sstyle))
story += [soltab]

story += [Spacer(1, 8), section_title("Angolo di apertura consigliato")]
story += [Paragraph(
    "“Oggi i vostri vini si comprano quasi solo su negozi terzi: state lasciando margine e i dati dei vostri clienti "
    "a chi vende per voi. Vi mostro come trasformare il vostro brand — già fortissimo — in un canale di vendita e di "
    "relazione diretto, partendo da e-commerce ed esperienze in cantina.”", st_body)]
story += [PageBreak()]

# ===== P5: DOMANDE + CHECKLIST =====
story += [Paragraph("5 · Domande da fare in call", st_h1)]
story += [Paragraph("Per qualificare budget, decisori e tempi (BANT) senza sembrare invadente.", st_small), Spacer(1, 4)]
story += [section_title("Discovery")]
story += [bullets([
    "Oggi quanto pesa la vendita diretta rispetto ai canali terzi e all'horeca? Avete mai valutato un e-commerce vostro?",
    "Le esperienze in cantina quanto incidono? Come gestite oggi prenotazioni e pagamenti?",
    "Quali mercati esteri sono prioritari per la crescita nei prossimi 12–24 mesi?",
    "Chi segue oggi il digitale (interno o agenzia)? Cosa funziona e cosa vi manca?",
    "Su quali obiettivi vi misurate quest'anno: vendite dirette, awareness, export, enoturismo?",
], color=IOL_DARK)]
story += [section_title("Qualificazione (BANT)")]
story += [bullets([
    "<b>Budget:</b> è già allocato un budget per digitale/e-commerce nel 2026?",
    "<b>Authority:</b> chi decide? (le tre titolari? un direttore commerciale/marketing?)",
    "<b>Need:</b> la priorità è vendita diretta, export o enoturismo?",
    "<b>Timing:</b> ci sono scadenze — nuova annata, fiere, campagna di Natale?",
], color=IOL_RED)]

story += [Spacer(1, 6), section_title("Checklist pre-call (5 minuti prima)")]
story += [bullets([
    "Apri il sito famigliacotarella.it e nota a colpo d'occhio l'assenza del carrello.",
    "Tieni pronti 2 competitor che vendono già online in DTC (es. Antinori, Frescobaldi).",
    "Ricorda i nomi: Dominga, Marta, Enrica Cotarella — e Riccardo Cotarella (enologo, Presidente Assoenologi).",
    "Obiettivo della call: fissare un secondo incontro con audit Semrush completo alla mano.",
], color=IOL_DARK)]

story += [Spacer(1, 8), HRFlowable(width="100%", color=IOL_LINE, thickness=0.8), Spacer(1, 4)]
story += [Paragraph(
    "<b>Note &amp; fonti.</b> Dati economici da fonti camerali pubbliche (ufficiocamerale.it, fatturatoitalia.it). "
    "Profilo azienda da sito ufficiale e stampa di settore. Dati SEO quantitativi non inclusi: account Semrush "
    "privo di unità API al momento della redazione — richiedere allocazione all'owner per l'audit completo. "
    "Documento generato il 18/06/2026 a uso interno della rete vendita Italiaonline.", st_small)]

doc.build(story)
print("OK ->", OUT)
