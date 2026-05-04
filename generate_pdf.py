#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère le PDF du livre Kémi Séba avec ReportLab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib import colors

OUTPUT = "/home/user/tts-docs/kemi-sebal-livre.pdf"

# ── Couleurs ──────────────────────────────────────────────────────────────────
NOIR    = HexColor("#0a0a0a")
GRIS    = HexColor("#555555")
GRIS_L  = HexColor("#888888")
BEIGE   = HexColor("#f5f2ed")
ROUGE   = HexColor("#8b0000")
BORDURE = HexColor("#cccccc")

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITRE_COUV = S("TitreCouv",
    fontName="Helvetica-Bold", fontSize=38, leading=44,
    alignment=TA_CENTER, textColor=NOIR, spaceAfter=8,
    letterSpacing=3)

SOUS_COUV = S("SousCouv",
    fontName="Helvetica-Oblique", fontSize=16, leading=22,
    alignment=TA_CENTER, textColor=GRIS, spaceAfter=6)

GENRE = S("Genre",
    fontName="Helvetica", fontSize=9, leading=12,
    alignment=TA_CENTER, textColor=GRIS_L, spaceAfter=0,
    letterSpacing=3)

EPIGRAPHE = S("Epigraphe",
    fontName="Helvetica-Oblique", fontSize=10.5, leading=16,
    alignment=TA_LEFT, textColor=HexColor("#333333"),
    leftIndent=30, rightIndent=20, spaceAfter=4)

CITE = S("Cite",
    fontName="Helvetica", fontSize=9, leading=13,
    alignment=TA_LEFT, textColor=GRIS,
    leftIndent=30, rightIndent=20, spaceAfter=20)

AV_TITRE = S("AvTitre",
    fontName="Helvetica-Bold", fontSize=13, leading=17,
    alignment=TA_CENTER, textColor=NOIR, spaceBefore=0, spaceAfter=24,
    letterSpacing=3)

PART_NUM = S("PartNum",
    fontName="Helvetica", fontSize=9, leading=12,
    alignment=TA_CENTER, textColor=GRIS_L, spaceBefore=0, spaceAfter=12,
    letterSpacing=5)

PART_TITLE = S("PartTitle",
    fontName="Helvetica-Bold", fontSize=24, leading=30,
    alignment=TA_CENTER, textColor=NOIR, spaceBefore=0, spaceAfter=0,
    letterSpacing=1)

CHAP = S("Chap",
    fontName="Helvetica-Bold", fontSize=12, leading=16,
    alignment=TA_LEFT, textColor=NOIR, spaceBefore=28, spaceAfter=10,
    letterSpacing=0.5)

BODY = S("Body",
    fontName="Times-Roman", fontSize=11, leading=17.5,
    alignment=TA_JUSTIFY, textColor=NOIR,
    firstLineIndent=18, spaceAfter=8,
    leftIndent=0, rightIndent=0)

BODY_NI = S("BodyNI",  # No indent — 1er § après titre
    fontName="Times-Roman", fontSize=11, leading=17.5,
    alignment=TA_JUSTIFY, textColor=NOIR,
    firstLineIndent=0, spaceAfter=8)

BOLD_LINE = S("BoldLine",
    fontName="Times-Bold", fontSize=11, leading=17.5,
    alignment=TA_LEFT, textColor=NOIR,
    firstLineIndent=0, spaceAfter=6)

QUOTE_TEXT = S("QuoteText",
    fontName="Times-Italic", fontSize=10.5, leading=16,
    alignment=TA_LEFT, textColor=HexColor("#222222"),
    leftIndent=22, rightIndent=15, spaceAfter=4,
    firstLineIndent=0)

QUOTE_CITE = S("QuoteCite",
    fontName="Helvetica", fontSize=9, leading=13,
    alignment=TA_LEFT, textColor=GRIS,
    leftIndent=22, rightIndent=15, spaceAfter=6,
    firstLineIndent=0)

NOTE_TITRE = S("NoteTitre",
    fontName="Helvetica-Bold", fontSize=12, leading=16,
    alignment=TA_LEFT, textColor=NOIR, spaceBefore=0, spaceAfter=16,
    letterSpacing=2)

CHRON_HEAD = S("ChronHead",
    fontName="Helvetica-Bold", fontSize=12, leading=16,
    alignment=TA_LEFT, textColor=NOIR, spaceBefore=20, spaceAfter=16,
    letterSpacing=1)

FOOTER = S("Footer",
    fontName="Helvetica", fontSize=8, leading=10,
    alignment=TA_CENTER, textColor=GRIS_L)

# ── Helpers ───────────────────────────────────────────────────────────────────

def hr(width=12*cm, thickness=0.5, color=BORDURE, spaceB=10, spaceA=10):
    return HRFlowable(width=width, thickness=thickness, color=color,
                      spaceAfter=spaceA, spaceBefore=spaceB)

def p(text, style=BODY):
    return Paragraph(text, style)

def quote(text, source):
    return KeepTogether([
        hr(width=2*cm, thickness=1.5, color=GRIS, spaceB=14, spaceA=0),
        p(text, QUOTE_TEXT),
        p(f"— {source}", QUOTE_CITE),
        Spacer(1, 6),
    ])

def part_page(num_text, title_text):
    """Retourne un bloc 'page de partie' centré verticalement."""
    return [
        PageBreak(),
        Spacer(1, 6*cm),
        p(num_text, PART_NUM),
        hr(width=4*cm, thickness=0.8, color=GRIS_L, spaceB=12, spaceA=12),
        p(title_text, PART_TITLE),
        PageBreak(),
    ]

def chap(text):
    return p(text, CHAP)

# ── Numérotation des pages ─────────────────────────────────────────────────────

def footer_canvas(canvas, doc):
    canvas.saveState()
    if doc.page > 2:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GRIS_L)
        canvas.drawCentredString(A4[0]/2, 1.2*cm, str(doc.page))
        # Titre courant
        canvas.setFont("Helvetica-Oblique", 7)
        canvas.drawString(2.5*cm, 1.2*cm, "KÉMI SÉBA — L'HOMME QUE L'EMPIRE NE POUVAIT PAS ACHETER")
    canvas.restoreState()

# ── Contenu ────────────────────────────────────────────────────────────────────

def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=3.0*cm, rightMargin=2.8*cm,
        topMargin=2.8*cm, bottomMargin=2.5*cm,
        title="KÉMI SÉBA — L'Homme que l'Empire ne pouvait pas Acheter",
        author="Biographie documentée",
        subject="Panafricanisme, Françafrique, Wagner, Afrique",
    )

    story = []

    # ══════════════════════════════════════════════════════════
    # COUVERTURE
    # ══════════════════════════════════════════════════════════
    story += [
        Spacer(1, 4.5*cm),
        p("BIOGRAPHIE SANS FILTRE", GENRE),
        Spacer(1, 1.2*cm),
        hr(width=5*cm, thickness=2, color=NOIR, spaceB=20, spaceA=20),
        p("KÉMI SÉBA", TITRE_COUV),
        Spacer(1, 0.3*cm),
        p("—", S("Dash", fontName="Helvetica", fontSize=22, alignment=TA_CENTER,
                  textColor=GRIS, spaceAfter=10)),
        p("L'Homme que l'Empire<br/>ne pouvait pas Acheter", SOUS_COUV),
        hr(width=5*cm, thickness=2, color=NOIR, spaceB=20, spaceA=20),
        Spacer(1, 0.5*cm),
        p("TOUTES LES AFFAIRES · SANS FILTRE", GENRE),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # ÉPIGRAPHES
    # ══════════════════════════════════════════════════════════
    story += [
        Spacer(1, 3*cm),
        p("« Votre passeport, ce n'est pas un os que vous nous donnez comme si les Noirs étaient des "
          "chiens. Je suis un homme Noir libre. Je suis un Africain libre. Je suis un Béninois libre. »",
          EPIGRAPHE),
        p("— Kémi Séba, en brûlant son passeport français, 16 mars 2024", CITE),
        Spacer(1, 0.8*cm),
        p("« Les 400 000 dollars dont ils parlent, c'est une insulte pour nous, parce que nous, "
          "il nous en faut beaucoup plus. »", EPIGRAPHE),
        p("— Kémi Séba, sur le financement Wagner, 2023", CITE),
        Spacer(1, 0.8*cm),
        p("« Être panafricaniste maintenant, c'est encenser l'AES. Je ne suis pas à l'aise avec ça. »",
          EPIGRAPHE),
        p("— Kémi Séba, enregistrements audio fuités, mars 2026", CITE),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # AVANT-PROPOS
    # ══════════════════════════════════════════════════════════
    story += [
        Spacer(1, 0.5*cm),
        p("AVANT-PROPOS : UN HOMME ENTRE DEUX FEUX", AV_TITRE),
        hr(spaceB=6, spaceA=20),

        p("Il y a des hommes dont la vie est trop compliquée pour les idoles "
          "et trop significative pour le silence.", BODY_NI),
        p("Kémi Séba est de ceux-là.", BODY),
        p("Dans les rues de Dakar, de Ouagadougou, de Bamako, de Niamey, son nom est prononcé avec "
          "une ferveur qui ressemble à de la religion. Des jeunes hommes qui n'ont jamais lu ses livres "
          "mais ont regardé ses vidéos nuit après nuit, qui récitent ses formules comme des prières — "
          "<i>« L'Afrique libre ou la mort »</i>, <i>« Le franc CFA est un cancer »</i> — et qui "
          "voient en lui l'incarnation d'un refus fondamental : le refus d'être gouverné depuis Paris.", BODY),
        p("Dans les chancelleries occidentales, à la Direction Générale de la Sécurité Intérieure "
          "française, dans les dossiers de la justice sénégalaise et béninoise, son nom apparaît "
          "autrement : comme une menace, un agent d'influence, un instrument de la stratégie russe "
          "en Afrique francophone.", BODY),
        p("La vérité sur Kémi Séba se situe dans l'espace inconfortable entre ces deux "
          "représentations — et c'est exactement dans cet espace que ce livre entend se tenir.", BODY),
        p("Il ne s'agit pas ici de l'absoudre. Ni de le condamner. Il s'agit de raconter — sans "
          "filtre, sans déférence, sans la censure que lui appliquent ses ennemis ni l'hagiographie "
          "que lui offrent ses admirateurs.", BODY),
        p("Un homme est né à Strasbourg sous le nom de Stellio Capo Chichi. Il a combattu, trahi, "
          "été trahi. Il a refusé des choses et en a accepté d'autres. Il a dit des vérités et "
          "proféré des mensonges. Il a été l'ennemi de la France et l'instrument de la Russie. "
          "Il a aimé l'Afrique avec une intensité qui ne peut pas être entièrement feinte — et il "
          "en a profité d'une manière qui ne peut pas être entièrement niée.", BODY),
        p("Voici son histoire. Toute son histoire.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE I
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE I", "Stellio :\nL'Enfant de Strasbourg")

    story += [
        chap("Chapitre 1 — Strasbourg, 2 décembre 1981"),
        p("Il est né <b>Stellio Gilles Robert Capo Chichi</b>.", BODY_NI),
        p("Strasbourg, Alsace, France. Famille d'immigrés béninois. La France des Trente Glorieuses "
          "finissantes, la France qui allait élire Mitterrand quelques mois plus tard, la France qui "
          "avait besoin de bras pour ses usines et accueillait des Africains en leur promettant une "
          "place — une place modeste, bien délimitée, sans ambiguïté sur qui était l'hôte et qui "
          "était l'invité.", BODY),
        p("Peu de choses sont connues publiquement sur son enfance. Kémi Séba a toujours entouré "
          "sa vie familiale d'une opacité soigneusement entretenue. Ce qu'on sait : des parents "
          "béninois, une enfance dans la diaspora africaine de Strasbourg, la double identité de "
          "l'enfant d'immigrés né en France qui n'est jamais tout à fait d'ici ni tout à fait "
          "de là-bas.", BODY),
        p("Cette double appartenance, cette non-appartenance, fonda en lui une question qui ne "
          "s'éteint jamais : <i>Qui suis-je ? D'où est-ce que je viens ? À qui est-ce que "
          "j'appartiens ?</i>", BODY),
        p("Ce sont des questions que tous les enfants d'immigrés africains en France se posent. "
          "Stellio Capo Chichi y apporta une réponse plus radicale que la plupart.", BODY),

        chap("Chapitre 2 — L'Éveil : La Nation of Islam et le Kémitisme"),
        p("Vers l'âge de dix-huit ans, aux alentours de 1999-2000, il rejoint la "
          "<b>Nation of Islam</b> — le mouvement islamique noir américain fondé par Elijah Muhammad, "
          "popularisé par Malcolm X, dirigé au moment où Stellio le découvre par Louis Farrakhan.", BODY_NI),
        p("La Nation of Islam n'est pas l'islam ordinaire. C'est une doctrine syncrétique qui mêle "
          "religion, nationalisme noir et théorie raciale — une vision du monde où l'homme noir est "
          "l'être originel, dépossédé et asservi par une civilisation blanche présentée comme "
          "fondamentalement maléfique. Pour un jeune homme qui cherche une réponse à la "
          "marginalisation qu'il ressent, c'est dévastateur dans son efficacité.", BODY),
        p("En parallèle, il s'inscrit à la <b>Faculté de droit de l'Université Paris X Nanterre</b>, "
          "où il obtient une capacité en droit avec mention — <b>premier de sa promotion parmi "
          "deux cents étudiants</b>. L'intelligence est là, indéniable, et elle sera toujours là — "
          "même quand elle sera mise au service de causes discutables.", BODY),
        p("Puis il voyage en Égypte. Ces voyages sont décisifs. Il découvre le <b>kémitisme</b> — "
          "mouvement afrocentrique qui affirme que les Africains noirs sont les créateurs de la "
          "civilisation égyptienne antique, que toute la pensée occidentale est une décalque "
          "dégénérée d'une sagesse africaine primordiale. Il s'abreuve des thèses de "
          "Cheikh Anta Diop, de Khalid Abdul Muhammad.", BODY),
        p("Il prend le nom de <b>Kémi Séba</b>. <i>Kémi</i> : la terre noire, l'Égypte, en langue "
          "kémite. <i>Séba</i> : l'étoile. Le nom est un programme, une proclamation d'identité, "
          "un refus du nom colonial.", BODY),
        p("Il devient porte-parole du Parti Kémite fondé en 2002. Mais le Parti Kémite est trop "
          "mou pour lui — il accepte les Noirs de toutes confessions, refuse le prosélytisme "
          "agressif. Stellio, devenu Kémi, veut quelque chose de plus radical, de plus total. "
          "Il va le créer.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE II
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE II", "Tribu Ka :\nLa Guerre en France")

    story += [
        chap("Chapitre 3 — La Naissance du Monstre (décembre 2004)"),
        p("En <b>décembre 2004</b>, Kémi Séba fonde <b>Tribu Ka</b> à Paris.", BODY_NI),
        p("L'organisation se présente comme le défenseur du « peuple noir ». Elle affirme que les "
          "populations noires sont à l'origine de la civilisation égyptienne antique. Jusque-là, "
          "rien que d'assez classique dans la tradition afrocentrique.", BODY),
        p("Mais Tribu Ka va beaucoup plus loin.", BODY),
        p("L'organisation prône explicitement la <b>ségrégation raciale</b>. Elle tient des discours "
          "ouvertement <b>antisémites</b>, attribuant aux Juifs — au « sionisme mondial » — un rôle "
          "central dans l'oppression des peuples noirs. Elle se structure comme un groupe "
          "paramilitaire : membres en uniformes sombres, hiérarchie stricte, discipline de corps.", BODY),
        p("C'est une chose étrange et révélatrice : un homme qui combat le racisme dont il a été "
          "victime en tant qu'Africain en France, et qui y répond par un racisme d'une autre couleur. "
          "L'antisémitisme de Tribu Ka n'est pas une conséquence accidentelle de son idéologie — "
          "il en est une composante centrale.", BODY),

        chap("Chapitre 4 — La Rue des Rosiers (mai 2006)"),
        p("En <b>mai 2006</b>, l'affaire qui va tout faire basculer.", BODY_NI),
        p("Des membres de Tribu Ka — plus d'une vingtaine — défilent dans la <b>rue des Rosiers</b>, "
          "dans le quartier du Marais à Paris. La rue des Rosiers est le cœur de la communauté juive "
          "parisienne. Des boutiques, des restaurants, des synagogues. Des familles qui font leurs "
          "courses, des enfants qui rentrent de l'école.", BODY),
        p("Les membres de Tribu Ka y scandent des slogans antisémites. Ils menacent les piétons et "
          "les commerçants. C'est une démonstration de force délibérément choisie pour son caractère "
          "provocateur et humiliant.", BODY),
        p("L'indignation est immédiate et nationale. Le ministre de l'Intérieur <b>Nicolas Sarkozy</b> "
          "saisit le garde des Sceaux <b>Pascal Clément</b>. Les associations antiracistes portent "
          "plainte. Les politiques de gauche comme de droite se relaient pour condamner.", BODY),
        p("Le <b>26 juillet 2006</b>, le Conseil des ministres prononce la <b>dissolution de "
          "Tribu Ka</b> pour incitation à la haine raciale et antisémitisme.", BODY),

        chap("Chapitre 5 — Les Condamnations"),
        p("La machine judiciaire s'emballe.", BODY_NI),
        p("<b>Septembre 2006 :</b> Arrêté pour des posts antisémites sur son site internet.", BODY),
        p("<b>Février 2007 :</b> Nouvelle arrestation pour avoir qualifié un officiel de "
          "« déchet sioniste ».", BODY),
        p("<b>2008 :</b> Condamné à <b>6 mois de prison dont 2 fermes</b> pour reconstitution de "
          "ligue dissoute — le groupe s'est reconstitué sous le nom de « Génération Kémi Séba » "
          "à Sarcelles. En appel, la peine passe à <b>1 an avec sursis</b>.", BODY),
        p("<b>Avril 2009 :</b> Condamné à <b>8 mois avec sursis</b> pour provocation à la haine "
          "raciale.", BODY),
        p("<b>2011 :</b> Condamné à <b>2 mois avec sursis</b> et mise à l'épreuve pour violences "
          "en réunion.", BODY),
        p("<b>2014 :</b> Les sursis sont révoqués. Il purge une peine de prison — plusieurs semaines "
          "d'incarcération effective.", BODY),
        p("Un palmarès judiciaire lourd. Des condamnations prononcées par des juges indépendants, "
          "sur la base de faits établis. Ce n'est pas une persécution — c'est le résultat de "
          "choix délibérés.", BODY),

        chap("Chapitre 6 — Les Fréquentations Troubles : Dieudonné et Soral"),
        p("Après la dissolution de Tribu Ka, Kémi Séba traverse une période de transition "
          "idéologique. Il se rapproche du comédien controversé <b>Dieudonné M'bala M'bala</b> et "
          "de l'idéologue d'extrême droite <b>Alain Soral</b>, fondateur d'Égalité &amp; "
          "Réconciliation. Il fréquente le Théâtre de la Main-d'Or.", BODY_NI),
        p("Ce rapprochement est révélateur. Soral est un nationaliste d'extrême droite dont "
          "l'antisémitisme est une ligne directrice. Cette période de la vie de Kémi Séba est celle "
          "qu'il élude le plus soigneusement dans ses interviews africaines. L'histoire avec Soral "
          "et Dieudonné rappelle que les lignes idéologiques ne sont pas si simples.", BODY),
        p("En <b>avril 2010</b>, il est nommé représentant en France du <b>New Black Panther Party</b> "
          "américain — organisation considérée par le FBI comme un groupe haineux. Il quitte cette "
          "responsabilité en juillet 2010. Le pivot vers l'Afrique est en cours.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE III
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE III", "Le Tournant Africain")

    story += [
        chap("Chapitre 7 — Dakar, 2011 : Tout Recommencer"),
        p("En <b>2011</b>, Kémi Séba quitte définitivement la France pour s'installer à "
          "<b>Dakar, Sénégal</b>.", BODY_NI),
        p("Ce n'est pas un exil — pas encore. C'est un choix stratégique. Le terrain de la diaspora "
          "africaine en France est trop étroit, trop surveillé, trop encombré de condamnations "
          "judiciaires. L'Afrique est un continent entier. Une jeunesse de plusieurs centaines de "
          "millions de personnes, de plus en plus connectée, de plus en plus en colère, cherchant "
          "des mots pour nommer ce qu'elle ressent.", BODY),
        p("Kémi Séba a les mots.", BODY),
        p("À partir de <b>2013</b>, il multiplie les interventions sur les télévisions "
          "ouest-africaines comme <b>analyste géopolitique</b>. Il parle du franc CFA, de la "
          "Françafrique, des bases militaires françaises, de la dette odieuse. Il dit des choses "
          "que des professeurs d'université ont soigneusement documentées pendant des décennies — "
          "mais il les dit autrement, avec la flamme de la conviction et la clarté de la simplicité. "
          "Sa popularité monte. Rapidement.", BODY),

        chap("Chapitre 8 — Le Franc CFA : L'Arme Symbolique"),
        p("La grande cause de Kémi Séba en Afrique, c'est le <b>franc CFA</b>.", BODY_NI),
        p("Sa position est radicale et simple : le franc CFA est un instrument de domination "
          "néocoloniale. Créé en 1945, il lie les économies de quatorze pays africains à la France, "
          "qui garde une influence sur leur politique monétaire. Le taux de change est fixe, ce qui "
          "empêche ces pays d'ajuster leur monnaie à leurs besoins économiques. Pour lui, c'est "
          "une évidence : une monnaie qu'on ne contrôle pas entièrement est une chaîne.", BODY),
        p("En <b>janvier 2017</b>, il crée le <b>Front Anti-CFA</b>, qui organise des manifestations "
          "simultanées dans plusieurs capitales africaines — Cotonou, Bamako, Ouagadougou, "
          "Niamey, Yaoundé. Et puis vient le geste.", BODY),

        chap("Chapitre 9 — Le Billet Brûlé (Dakar, 19 août 2017)"),
        p("<b>19 août 2017, Dakar.</b>", BODY_NI),
        p("Lors d'une manifestation contre la Françafrique, devant des caméras soigneusement "
          "positionnées, Kémi Séba sort un billet de <b>5 000 francs CFA</b> et y met le feu.", BODY),
        p("Le geste dure quelques secondes. La flamme est petite. La portée est immense. L'image "
          "fait le tour du monde en quelques heures. Des jeunes Africains la regardent en boucle. "
          "C'est le geste le plus simple et le plus fort qui pouvait être fait : détruire la "
          "monnaie coloniale. Littéralement la brûler.", BODY),
        p("Le <b>25 août 2017</b>, il est arrêté à Dakar pour destruction de monnaie ayant cours "
          "légal. Le <b>29 août 2017</b>, le tribunal correctionnel de Dakar l'<b>acquitte</b>, "
          "après deux heures de délibérations.", BODY),
        p("Kémi Séba sort du tribunal en triomphateur. Mais le Sénégal ne l'entend pas ainsi.", BODY),
        p("<b>6 septembre 2017 :</b> Les autorités sénégalaises prononcent son <b>expulsion pour "
          "« menace grave pour l'ordre public »</b>. Malgré l'acquittement judiciaire, le pouvoir "
          "exécutif choisit de se débarrasser de l'homme. Ce paradoxe — acquitté par la justice, "
          "expulsé par l'État — révèle quelque chose d'important sur la nature de son combat et "
          "sur la nature de ceux qui le combattent.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE IV
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE IV", "L'Empire Russe")

    story += [
        chap("Chapitre 10 — Le Projet Kémi (2018-2019) : 440 000 Dollars de Moscou"),
        p("C'est l'affaire la plus dérangeante de toute la biographie de Kémi Séba. Celle qui "
          "dérange ses admirateurs. Celle qu'il ne peut pas nier totalement.", BODY_NI),
        p("<b>Mars-avril 2023.</b> Une enquête publiée par <i>Jeune Afrique</i> en collaboration "
          "avec Arte/CAPA, <i>Die Welt</i>, les organisations All Eyes On Wagner et le Dossier "
          "Center révèle l'existence du <b>« Projet Kémi »</b>.", BODY),
        p("Entre <b>mai 2018 et juillet 2019</b>, Evgueni Prigojine et les réseaux Wagner ont "
          "financé les activités de Kémi Séba en Afrique à hauteur de <b>440 000 dollars</b> — "
          "environ 400 000 euros.", BODY),
        p("Ce n'est pas une subvention philanthropique. C'est de l'argent avec un objectif : "
          "utiliser Kémi Séba comme <b>vecteur de l'influence russe</b>. Affaiblir l'influence "
          "de Paris. Préparer le terrain à l'implantation de Wagner.", BODY),
    ]
    story.append(quote(
        "« Les 400 000 dollars dont ils parlent, c'est une insulte pour nous, parce que nous, "
        "il nous en faut beaucoup plus. »",
        "Kémi Séba, répondant aux révélations du Projet Kémi, 2023"
    ))
    story += [
        p("Il assume. Il parle de <b>« partenariats géopolitiques temporaires »</b>. Il reconnaît "
          "avoir été invité par Prigojine en Russie, au Soudan et en Libye. Il dit l'avoir fait "
          "en toute conscience.", BODY),
        p("C'est à la fois honnête et troublant. Honnête parce qu'il ne ment pas, ne se défausse "
          "pas. Troublant parce que Wagner, à la même période, assassine des civils au Mali, torture "
          "au Soudan, finance des guerres en Libye. Prendre leur argent en sachant qui ils sont, "
          "c'est faire un choix.", BODY),

        chap("Chapitre 11 — Alexandre Douguine et l'Eurasisme"),
        p("Au-delà de Prigojine, il y a <b>Alexandre Douguine</b> — philosophe de l'empire russe "
          "réinventé, théoricien du « monde multipolaire », idéologue du « Grand Continent "
          "eurasiatique » contre l'hégémonie américaine, proche de Poutine.", BODY_NI),
        p("Douguine décrit publiquement Kémi Séba comme <i>« l'espoir africain d'un monde "
          "multipolaire »</i> et <i>« un éminent combattant contre le colonialisme »</i>. "
          "Kémi Séba partage et relaie largement la pensée eurasiste de Douguine.", BODY),
        p("Dans les interventions de Kémi Séba à partir de 2018, on retrouve de plus en plus "
          "la terminologie douguinienne : multipolarité, résistance à l'unipolarisme, civilisations "
          "contre globalisation. Le discours panafricaniste est réenchâssé dans une architecture "
          "idéologique <i>made in Russia</i>.", BODY),

        chap("Chapitre 12 — Afrique Média TV : La Machine de Propagande"),
        p("Kémi Séba est un invité régulier de <b>Afrique Média TV</b>, la chaîne de télévision "
          "camerounaise dirigée par Justin B. Tagouh. Ce qui n'est pas dit en antenne : la chaîne "
          "est identifiée par plusieurs équipes de chercheurs et journalistes d'investigation comme "
          "un <b>relais structuré de la propagande pro-Wagner</b> en Afrique francophone. "
          "L'AFRIC — Association for Free Research and International Cooperation — qui lui est "
          "liée, est elle-même connectée aux réseaux de Prigojine.", BODY_NI),
        p("Le système est élaboré : des voix africaines crédibles et populaires portent un discours "
          "anti-français et pro-russe sur des chaînes qui semblent africaines, vers un public "
          "africain. L'architecture de l'influence est invisible depuis l'intérieur. On voit un "
          "militant panafricaniste. On ne voit pas le financeur.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE V
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE V", "Les Juntes et la Gloire")

    story += [
        chap("Chapitre 13 — Les Coups d'État au Sahel : De Soutien à Conseiller"),
        p("À partir de <b>2020</b>, le Sahel s'enflamme de coups d'État militaires. "
          "Kémi Séba soutient chacun d'eux.", BODY_NI),
        p("<b>Mali, août 2020 :</b> Le colonel Assimi Goïta renverse Ibrahim Boubacar Keïta.", BODY),
        p("<b>Mali, mai 2021 :</b> Second coup d'État de Goïta, qui s'autoproclame président "
          "de transition.", BODY),
        p("<b>Guinée, septembre 2021 :</b> Le colonel Mamadi Doumbouya renverse Alpha Condé.", BODY),
        p("<b>Burkina Faso, janvier 2022 :</b> Sandaogo Damiba renverse Roch Kaboré.", BODY),
        p("<b>Burkina Faso, septembre 2022 :</b> Le capitaine Ibrahim Traoré renverse Damiba.", BODY),
        p("<b>Niger, juillet 2023 :</b> Le général Tchiani renverse Mohamed Bazoum.", BODY),
        p("Dans tous ces cas, le schéma est identique : le coup d'État est présenté comme une "
          "rupture avec la Françafrique, une reconquête de la souveraineté. Kémi Séba est là pour "
          "mettre les mots, pour légitimer symboliquement, pour amplifier le message auprès de "
          "la jeunesse connectée.", BODY),
        p("<b>Août 2024 :</b> Le général Tchiani le nomme <b>conseiller spécial du Niger</b> et "
          "lui octroie un <b>passeport diplomatique nigérien</b>. C'est la consécration — et aussi "
          "une nouvelle dépendance. Il n'est plus seulement un militant libre. Il est maintenant "
          "un fonctionnaire de facto d'une junte militaire.", BODY),

        chap("Chapitre 14 — La Deuxième Expulsion du Sénégal (Février 2020)"),
        p("Un procès en appel est programmé à Dakar pour l'affaire du billet brûlé. Kémi Séba "
          "tente d'y revenir en <b>février 2020</b> pour comparaître. Il est intercepté à "
          "l'aéroport de Dakar. <b>30 heures de rétention administrative.</b> Puis expulsion "
          "vers la Belgique. Il ne comparaîtra jamais à ce procès d'appel.", BODY_NI),
        p("La procédure est kafkaïenne dans sa logique : un homme expulsé ne peut pas répondre "
          "à une convocation dans le pays qui l'a expulsé. Il reste en dehors, ni condamné ni "
          "totalement libre.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE VI
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE VI", "La Guerre avec la France")

    story += [
        chap("Chapitre 15 — La Déchéance de Nationalité (2024)"),
        p("<b>29 février 2024.</b> Les autorités françaises initient une procédure de déchéance "
          "de nationalité contre Stellio Gilles Robert Capo Chichi.", BODY_NI),
        p("Les motifs retenus : messages hostiles à la France lors de conférences publiques, "
          "appels à la rébellion contre des autorités locales proches de Paris, liens établis "
          "avec la milice russe Wagner, activités d'influence au profit d'une puissance étrangère.", BODY),
        p("La procédure est rarissime. La France a très peu déchu des citoyens de leur nationalité "
          "depuis la Seconde Guerre mondiale. Le recours à cet instrument extrême dit quelque "
          "chose de la gravité avec laquelle l'État français perçoit le cas Kémi Séba.", BODY),
        p("Lui y répond avec son sens du geste.", BODY),
        p("<b>16 mars 2024.</b> Conférence de presse à Fleury-Mérogis, en Île-de-France — que "
          "la préfecture avait tenté d'interdire, mais que le tribunal administratif a autorisée. "
          "Devant les caméras, il sort son <b>passeport français</b> et y met le feu.", BODY),
    ]
    story.append(quote(
        "« Votre passeport, ce n'est pas un os que vous nous donnez comme si les Noirs étaient "
        "des chiens. Je suis un homme Noir libre. Je suis un Africain libre. Je suis un "
        "Béninois libre. »",
        "Kémi Séba, Fleury-Mérogis, 16 mars 2024"
    ))
    story += [
        p("<b>8 juillet 2024.</b> Un décret paru au <b>Journal officiel de la République "
          "française</b> officialise la déchéance de nationalité de Stellio Gilles Robert Capo "
          "Chichi. C'est l'une des premières applications de cette mesure pour des activités "
          "d'influence au profit de la Russie.", BODY),

        chap("Chapitre 16 — La DGSI (Octobre 2024)"),
        p("<b>14 octobre 2024.</b> Paris, 15e arrondissement. Un restaurant. Des agents de la "
          "<b>Direction Générale de la Sécurité Intérieure</b> interpellent Kémi Séba et son "
          "collaborateur <b>Cyrille Kamden</b>. Il voyage avec son passeport diplomatique nigérien. "
          "Il est à Paris pour rendre visite à son père, hospitalisé.", BODY_NI),
        p("La charge retenue est lourde : <b>intelligences avec une puissance étrangère en vue "
          "de susciter des hostilités ou des actes d'agression contre la France</b> — infraction "
          "criminelle passible de <b>trente ans d'emprisonnement</b>.", BODY),
        p("<b>16 octobre 2024.</b> Il est relâché sans poursuites immédiates. L'enquête "
          "préliminaire se poursuit. Il parle de « réaction néocoloniale ».", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE VII
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE VII", "La Chute et l'Exil")

    story += [
        chap("Chapitre 17 — Le Bénin Trahit Son Fils (Décembre 2025)"),
        p("<b>7 décembre 2025.</b> Une tentative de coup d'État au Bénin.", BODY_NI),
        p("Des soldats commandés par le <b>lieutenant-colonel Pascal Tigri</b> annoncent à la "
          "télévision nationale le renversement du président <b>Patrice Talon</b>. La tentative "
          "échoue. Des forces d'Afrique de l'Ouest interviennent pour stabiliser la situation.", BODY),
        p("Kémi Séba publie immédiatement une vidéo dans laquelle il se félicite du prétendu "
          "renversement, déclarant que <b>« le jour de la libération »</b> est venu.", BODY),
        p("Le coup d'État échoue dans les heures qui suivent. La vidéo reste. Il ne peut pas "
          "la nier.", BODY),
        p("Le <b>Bénin</b> — le pays de la famille de ses parents — émet un <b>mandat d'arrêt "
          "international</b> pour <b>« apologie de crimes contre la sûreté de l'État et incitation "
          "à la rébellion »</b>. Un premier mandat d'arrêt béninois avait déjà été lancé en "
          "<b>juin 2025</b> pour des faits de <b>blanchiment de capitaux</b>.", BODY),

        chap("Chapitre 18 — Natou Pedro Sakombi : L'Amour comme Otage"),
        p("<b>22 décembre 2025.</b> Au Bénin, les autorités arrêtent "
          "<b>Natou Pedro Sakombi</b>.", BODY_NI),
        p("Historienne et artiste-écrivaine de nationalité belge, Natou a été la compagne de "
          "Kémi Séba pendant sept ans. Ils ont eu plusieurs enfants ensemble — Imhotep, Vérona, "
          "Anupé. Elle a partagé sa vie, son combat, ses exils.", BODY),
        p("Elle est accusée de <b>blanchiment de capitaux, fraude fiscale et contrebande</b>. "
          "La défense parle d'une arrestation utilisée comme <b>moyen de pression</b> sur "
          "Kémi Séba.", BODY),
        p("Depuis l'étranger, Kémi Séba publie une déclaration dans laquelle il affirme que "
          "Natou est désormais son « ex-épouse » et qu'elle n'est pas liée à ses activités. "
          "Un geste ambigu — protection de la femme qu'il a aimée, ou distanciation pour "
          "préserver ses propres intérêts ?", BODY),
        p("<b>26 décembre 2025.</b> Natou Pedro Sakombi est libérée et placée sous convocation.", BODY),

        chap("Chapitre 19 — Les Enregistrements : La Vérité qui Fuit (Mars 2026)"),
        p("Juste avant son arrestation en Afrique du Sud, quelque chose d'extraordinaire se "
          "produit.", BODY_NI),
        p("Des <b>enregistrements audio</b> attribués à Kémi Séba circulent massivement sur les "
          "réseaux sociaux. La société <b>Whispeak</b>, spécialisée en biométrie vocale, authentifie "
          "que les fichiers n'ont pas été modifiés et ne sont pas générés par intelligence "
          "artificielle.", BODY),
        p("Dans ces conversations privées, Kémi Séba dit ce qu'il ne dit jamais en public.", BODY),
    ]
    story.append(quote(
        "« Être panafricaniste maintenant, c'est encenser l'AES. "
        "Je ne suis pas à l'aise avec ça. »",
        "Kémi Séba, enregistrements audio fuités, mars 2026"
    ))
    story += [
        p("Il reproche aux militaires sahéliens d'avoir instrumentalisé le mouvement "
          "panafricaniste pour <i>« sécuriser leurs positions présidentielles »</i>. C'est un "
          "séisme dans les milieux panafricanistes pro-AES. <b>Nathalie Yamb</b> — l'une des "
          "figures les plus proches de lui — garde un silence assourdissant.", BODY),
        p("Les enregistrements révèlent un homme plus complexe que l'image publique — un homme "
          "capable de doute, de lucidité sur ses propres contradictions. Ils révèlent aussi qu'il "
          "a dit en privé ce qu'il ne pouvait pas dire en public, ce qui soulève la question "
          "fondamentale : jusqu'à quel point la dissidence qu'il incarne est-elle sincère, et "
          "jusqu'à quel point est-elle une posture ?", BODY),

        chap("Chapitre 20 — La Rivière Limpopo (Avril 2026)"),
        p("<b>13 avril 2026. Pretoria, Afrique du Sud.</b>", BODY_NI),
        p("Kémi Séba est arrêté lors d'une <b>opération de surveillance policière</b> "
          "sud-africaine. Il se trouve avec son fils <b>Khonsou Seba Capo Chichi</b>, "
          "dix-huit ans.", BODY),
        p("Les circonstances sont saisissantes : il tentait de <b>franchir illégalement la "
          "rivière Limpopo</b> — la frontière naturelle entre l'Afrique du Sud et le Zimbabwe — "
          "pour rejoindre l'Europe via une route clandestine, en payant des passeurs. L'homme "
          "qui avait brûlé son passeport français comme acte de libération, qui avait obtenu "
          "un passeport diplomatique africain comme reconnaissance de sa stature, fuyait "
          "désormais à travers un fleuve africain.", BODY),
        p("Parmi les personnes arrêtées dans la même opération : <b>François Van der Merwe</b>, "
          "dirigeant du groupe afrikaner identitaire <b>Bittereinders</b>, lié à la Russie. "
          "Les deux hommes affirment ne pas se connaître.", BODY),
        p("<b>318 000 rands sont saisis</b> — environ 16 000 euros, dont la majorité était "
          "destinée à payer les passeurs.", BODY),
        p("Il comparaît le <b>20 avril 2026</b> devant le tribunal de première instance de "
          "Pretoria. Il demande l'<b>asile politique en Afrique du Sud</b>. Le Niger lui a "
          "retiré son passeport diplomatique. Le Bénin a déposé une demande formelle "
          "d'extradition via la CRIET. La procureure s'oppose à sa libération sous caution. "
          "L'audience est renvoyée au 11 mai 2026.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE VIII
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE VIII", "L'Homme et ses Contradictions")

    story += [
        chap("Chapitre 21 — Les Femmes"),
        p("Kémi Séba vit selon un modèle familial polygame.", BODY_NI),
        p("<b>Première épouse — Etuma :</b> Sa première compagne, avec qui il a au moins deux "
          "enfants — Satherou et Khonsou, ce dernier né vers 2008, dix-huit ans au moment de "
          "l'arrestation en Afrique du Sud.", BODY),
        p("<b>Deuxième compagne — Natou Pedro Sakombi :</b> Historienne et artiste-écrivaine de "
          "nationalité belge, elle partage sa vie pendant sept ans. Ensemble ils ont plusieurs "
          "enfants : Imhotep, Vérona, Anupé.", BODY),
        p("La vie familiale est rendue complexe par les exils successifs, les expulsions, les "
          "arrestations. Des enfants qui grandissent sans père présent. Quand Natou est arrêtée "
          "au Bénin en décembre 2025, Kémi Séba la désigne comme son « ex-épouse ». La mécanique "
          "de la désaffiliation est rapide. La femme qu'il a présentée pendant des années comme "
          "sa compagne devient une étrangère quand sa proximité devient dangereuse.", BODY),
        p("C'est peut-être la chose la moins glorieuse de toute cette histoire.", BODY),

        chap("Chapitre 22 — Les Livres"),
        p("Car il faut le dire : Kémi Séba pense. Il a publié des livres qui ne sont pas que "
          "du verbe creux.", BODY_NI),
        p("<b>Supra-Négritude</b> (2013) — Premier essai philosophique majeur, proposant des "
          "outils intellectuels pour la libération des peuples noirs.", BODY),
        p("<b>Black Nihilism</b> (2014) — Une philosophie nihiliste noire comme réponse à "
          "l'oppression systémique.", BODY),
        p("<b>Obscure Époque</b> (2016) — Analyse de la période contemporaine.", BODY),
        p("<b>L'Afrique libre ou la mort</b> (2018) — L'œuvre la plus accessible et la plus "
          "diffusée, en plusieurs tomes.", BODY),
        p("<b>Philosophie de la panafricanité fondamentale</b> — Synthèse de sa pensée.", BODY),
        p("<b>Ma'at Ikh-s Philosophie</b> — Retour aux fondements kémites.", BODY),
        p("Ces livres méritent une lecture critique sérieuse — pas le rejet automatique des uns, "
          "ni l'adhésion aveugle des autres. Il y a de la pensée là-dedans, des intuitions vraies "
          "sur la décolonisation économique et culturelle, et aussi des angles morts, des "
          "simplifications, des obsessions qui limitent ce qu'ils auraient pu être.", BODY),

        chap("Chapitre 23 — Ce Qui Est Vrai et Ce Qui Ne L'Est Pas"),
        p("<b>Ce qui est vrai dans le discours de Kémi Séba :</b>", BOLD_LINE),
        p("Le franc CFA a des défauts structurels réels que des économistes sérieux documentent "
          "depuis des décennies. La Françafrique — le système de relations opaques entre Paris "
          "et les élites africaines — est un fait historique établi. Les bases militaires "
          "françaises en Afrique sont des instruments de politique étrangère. La jeunesse "
          "africaine mérite des dirigeants qui ne gouvernent pas sous tutelle.", BODY),
        p("<b>Ce qui est faux ou problématique :</b>", BOLD_LINE),
        p("L'antisémitisme de la période Tribu Ka était réel, documenté, condamnable. Pas "
          "une caricature, pas une interprétation : des marches rue des Rosiers, des textes "
          "précis, des condamnations de justice.", BODY),
        p("Le financement Wagner n'était pas un « partenariat géopolitique neutre ». Prendre "
          "l'argent de Prigojine, c'est accepter d'être un instrument — même si on pense "
          "négocier de égal à égal.", BODY),
        p("Le soutien systématique aux putschistes sahéliens ne s'est pas traduit par davantage "
          "de démocratie, de liberté ou de prospérité. Les juntes ont utilisé l'anti-impérialisme "
          "comme discours de légitimation du pouvoir personnel.", BODY),
        p("Les enregistrements de 2026 montrent qu'il le sait.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # ÉPILOGUE
    # ══════════════════════════════════════════════════════════
    story += [
        Spacer(1, 1*cm),
        hr(width=4*cm, thickness=1, color=GRIS, spaceB=20, spaceA=20),
        p("ÉPILOGUE — LA RIVIÈRE", AV_TITRE),
        hr(spaceB=6, spaceA=20),

        p("<b>Avril 2026. La rivière Limpopo.</b>", BODY_NI),
        p("Il y a une image que l'histoire retiendra, quelle que soit l'issue de la procédure "
          "sud-africaine : un homme qui a brûlé son passeport français comme geste de libération, "
          "qui a obtenu un passeport diplomatique africain comme reconnaissance de sa stature, "
          "se retrouve à essayer de traverser un fleuve en payant des passeurs.", BODY),
        p("Cette image n'invalide pas tout ce qu'il a dit. Elle ne valide pas non plus tout ce "
          "qu'on lui reproche. Elle est simplement vraie, dans toute sa complexité tragique.", BODY),
        p("L'Empire — la France, le système Françafrique — n'a pas pu l'acheter. C'est vrai. "
          "Il a refusé les offres d'intégration, les postes confortables, la reconversion en "
          "consultant respectable. Cette résistance est réelle.", BODY),
        p("Mais une autre puissance — Moscou, Prigojine, le système Wagner — a réussi à trouver "
          "sa prise. Pas nécessairement en l'achetant — peut-être en jouant sur les mêmes cordes "
          "que son propre discours jouait sur celles de la jeunesse africaine : la haine de "
          "l'impérialisme occidental, le désir d'un monde différent, l'urgence de l'action.", BODY),
        p("Kémi Séba n'a peut-être pas été acheté par l'Empire français. Mais il a peut-être "
          "été utilisé par l'Empire russe.", BODY),
        p("La différence entre les deux est réelle, et elle compte moralement. Elle ne change "
          "pas entièrement les effets.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # CHRONOLOGIE
    # ══════════════════════════════════════════════════════════
    story += [
        p("CHRONOLOGIE DES AFFAIRES", CHRON_HEAD),
        hr(thickness=1.5, color=NOIR, spaceB=0, spaceA=16),
    ]

    chron_data = [
        ["Année", "Événement"],
        ["1981", "Naissance à Strasbourg — Stellio Gilles Robert Capo Chichi"],
        ["1999", "Adhésion à la Nation of Islam"],
        ["2000", "Capacité en droit, Paris X Nanterre — 1er de promo sur 200 étudiants"],
        ["2002", "Prise du nom Kémi Séba, porte-parole du Parti Kémite"],
        ["Déc. 2004", "Fondation de Tribu Ka à Paris"],
        ["Mai 2006", "Marche antisémite rue des Rosiers à Paris"],
        ["Juil. 2006", "Dissolution de Tribu Ka par décret du Conseil des ministres"],
        ["2006–2014", "Multiples condamnations judiciaires — incarcération en 2014"],
        ["2008–2010", "Période Dieudonné / Soral / New Black Panther Party"],
        ["2011", "Départ définitif pour Dakar"],
        ["2015", "Fondation d'Urgences Panafricanistes"],
        ["Jan. 2017", "Création du Front Anti-CFA"],
        ["Août 2017", "Arrestation puis acquittement à Dakar après brûlage du billet CFA"],
        ["Sept. 2017", "1ère expulsion du Sénégal malgré l'acquittement"],
        ["2018–2019", "Financement de 440 000 $ par les réseaux Wagner / Prigojine"],
        ["Fév. 2020", "2ème expulsion du Sénégal — 30h de rétention administrative"],
        ["2020–2023", "Soutien public à tous les coups d'État au Sahel"],
        ["2023", "Révélations du « Projet Kémi » dans Jeune Afrique / Arte / Die Welt"],
        ["Mars 2024", "Brûlage du passeport français à Fleury-Mérogis"],
        ["Juil. 2024", "Déchéance de nationalité française publiée au Journal officiel"],
        ["Août 2024", "Conseiller spécial du Niger + passeport diplomatique nigérien"],
        ["Oct. 2024", "Garde à vue à la DGSI Paris — risque 30 ans d'emprisonnement"],
        ["Juin 2025", "1er mandat d'arrêt béninois (blanchiment de capitaux)"],
        ["Déc. 2025", "Soutien au coup d'État raté au Bénin → mandat d'arrêt international"],
        ["Déc. 2025", "Arrestation de Natou Pedro Sakombi au Bénin"],
        ["Mars 2026", "Enregistrements audio fuités — critique privée des juntes AES"],
        ["Avr. 2026", "Arrestation en tentant de traverser la rivière Limpopo, Afrique du Sud"],
        ["Avr. 2026", "Retrait du passeport diplomatique nigérien"],
        ["Mai 2026", "En détention provisoire à Pretoria — procédure d'extradition béninoise"],
    ]

    col_w = [2.8*cm, 13.4*cm]
    tbl = Table(chron_data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NOIR),
        ("TEXTCOLOR",  (0, 0), (-1, 0), white),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, 0), 8),
        ("FONTNAME",   (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",   (0, 1), (-1, -1), 8.5),
        ("LEADING",    (0, 1), (-1, -1), 12),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f7f5f0")]),
        ("GRID",       (0, 0), (-1, -1), 0.3, HexColor("#dddddd")),
        ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(tbl)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════
    # NOTE FINALE
    # ══════════════════════════════════════════════════════════
    story += [
        Spacer(1, 1*cm),
        p("NOTE FINALE", AV_TITRE),
        hr(spaceB=6, spaceA=20),

        p("Kémi Séba n'est pas un saint. Il n'est pas non plus uniquement ce que la DGSI, "
          "la justice sénégalaise ou le gouvernement béninois disent de lui.", BODY_NI),
        p("Il est le produit d'une époque — d'une époque où des millions de jeunes Africains "
          "cherchent une voix pour leur colère légitime, et où des puissances mondiales rivales "
          "utilisent cette colère comme matière première géopolitique.", BODY),
        p("Il a été cette voix. Il a été cet instrument. Les deux peuvent être vrais en même "
          "temps.", BODY),
        p("Ce qui est certain, c'est que son histoire n'est pas terminée. Et quelle que soit la "
          "suite, la question qu'il a posée à l'Afrique reste entière :", BODY),
        p("<i>À qui appartiennent les ressources africaines ? Qui décide des monnaies africaines ? "
          "Qui choisit les dirigeants africains ?</i>", BODY),
        p("Ces questions méritent des réponses honnêtes — pas les réponses simples de l'empire "
          "français, pas non plus les réponses simples de l'empire russe.", BODY),
        Spacer(1, 2*cm),
        hr(width=4*cm, thickness=1.5, color=NOIR, spaceB=20, spaceA=20),
        p("KÉMI SÉBA — L'HOMME QUE L'EMPIRE NE POUVAIT PAS ACHETER", GENRE),
        Spacer(1, 0.3*cm),
        p("Biographie basée sur des faits documentés et des sources journalistiques vérifiées.", GENRE),
        Spacer(1, 0.2*cm),
        p("Sources : Jeune Afrique · France 24 · Arte/CAPA · Die Welt · Wikipédia FR/EN · "
          "VOA Afrique · Le JDD · Senenews · The Conversation", GENRE),
    ]

    # ── Build ──────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=footer_canvas, onLaterPages=footer_canvas)
    print(f"PDF généré : {OUTPUT}")

if __name__ == "__main__":
    build()
