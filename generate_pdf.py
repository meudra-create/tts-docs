#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère le PDF panafricaniste — Kémi Séba, L'Homme que l'Empire ne pouvait pas Acheter."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors

OUTPUT = "/home/user/tts-docs/kemi-sebal-livre.pdf"

# ── Couleurs ──────────────────────────────────────────────────────────────────
NOIR    = HexColor("#0a0a0a")
GRIS    = HexColor("#555555")
GRIS_L  = HexColor("#888888")
BEIGE   = HexColor("#f5f2ed")
ROUGE   = HexColor("#8b0000")
OR      = HexColor("#b8860b")
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
    fontName="Helvetica-Bold", fontSize=22, leading=28,
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

BODY_NI = S("BodyNI",
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
        canvas.setFont("Helvetica-Oblique", 7)
        canvas.drawString(2.5*cm, 1.2*cm, "KEMI SEBA — L'HOMME QUE L'EMPIRE NE POUVAIT PAS ACHETER")
    canvas.restoreState()

# ── Contenu ────────────────────────────────────────────────────────────────────

def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=3.0*cm, rightMargin=2.8*cm,
        topMargin=2.8*cm, bottomMargin=2.5*cm,
        title="KEMI SEBA — L'Homme que l'Empire ne pouvait pas Acheter",
        author="Biographie panafricaniste",
        subject="Panafricanisme, Resistance, Afrique Libre",
    )

    story = []

    # ══════════════════════════════════════════════════════════
    # COUVERTURE
    # ══════════════════════════════════════════════════════════
    story += [
        Spacer(1, 4.5*cm),
        p("BIOGRAPHIE PANAFRICANISTE", GENRE),
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
        p("« Votre passeport, ce n'est pas un os que vous nous donnez comme si les Noirs "
          "etaient des chiens. Je suis un homme Noir libre. Je suis un Africain libre. "
          "Je suis un Beninois libre. »",
          EPIGRAPHE),
        p("— Kémi Séba, Fleury-Merogis, 16 mars 2024", CITE),
        Spacer(1, 0.8*cm),
        p("« L'Afrique libre ou la mort. »", EPIGRAPHE),
        p("— Devise de Kémi Séba", CITE),
        Spacer(1, 0.8*cm),
        p("« On ne libere pas un peuple avec des fleurs. On le libere avec des idees, "
          "du courage, et un refus absolu de se soumettre. »", EPIGRAPHE),
        p("— Thomas Sankara", CITE),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # AVANT-PROPOS
    # ══════════════════════════════════════════════════════════
    story += [
        Spacer(1, 0.5*cm),
        p("AVANT-PROPOS : LE FEU QUI NE S'ÉTEINT PAS", AV_TITRE),
        hr(spaceB=6, spaceA=20),

        p("Il existe, dans chaque generation africaine, quelques hommes que l'Empire "
          "designe comme ennemis.", BODY_NI),
        p("Pas parce qu'ils sont parfaits. Pas parce qu'ils ne commettent jamais "
          "d'erreurs. Mais parce qu'ils portent en eux quelque chose que le systeme "
          "colonial et neocolonial ne peut pas digerer : un refus absolu d'etre achetes, "
          "neutralises, domestiques.", BODY),
        p("Lumumba fut assassine. Sankara fut assassine. Cabral fut assassine. "
          "Moumie fut empoisonne. Ben Barka fut enleve.", BODY),
        p("Quand l'Empire ne peut pas acheter un homme et ne peut pas l'assassiner "
          "impunement, il fait autre chose : il l'emprisonne symboliquement dans ses "
          "dossiers judiciaires, il l'etouffe sous les proces, il le couvre de boue "
          "pour que sa voix se perde dans le bruit.", BODY),
        p("<b>Kemi Seba</b> — ne Stellio Gilles Robert Capo Chichi le 2 decembre 1981 "
          "a Strasbourg — est l'un de ces hommes que l'Empire a tout tente pour faire "
          "taire : la prison, les expulsions, la decheance de nationalite, les campagnes "
          "de decredibilisation, les gardes a vue dans les locaux de la police politique "
          "francaise, les mandats d'arret internationaux instrumentalises.", BODY),
        p("Il est encore debout.", BODY),
        p("Ce livre n'est pas une hagiographie. Les combattants panafricanistes n'ont "
          "pas besoin d'etre presentes comme des dieux pour etre respectes — ils sont "
          "des etres humains, avec leurs contradictions, leurs erreurs, leurs "
          "imperfections. Ce livre est un acte de memoire, un acte de justice narrative, "
          "une tentative de raconter la trajectoire d'un homme qui a choisi de se tenir "
          "du cote des peuples africains contre les puissances qui les exploitent.", BODY),
        p("L'Empire a essaye de l'acheter. Il a refuse.", BODY),
        p("Voici comment.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE I
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE I",
        "L'Enfant de la Diaspora :\nNaissance d'une Conscience")

    story += [
        chap("Chapitre 1 — Strasbourg, 2 décembre 1981 : La France Coloniale chez Soi"),
        p("Il est ne dans la Republique qui avait colonise le pays de ses parents.", BODY_NI),
        p("<b>Stellio Gilles Robert Capo Chichi</b> voit le jour le <b>2 decembre 1981 "
          "a Strasbourg</b>, dans une famille beninoise immigree. Ses parents font partie "
          "de cette grande maree humaine que la France a encouragee a venir travailler "
          "sur son sol — bras necessaires pour les usines, corps utiles pour l'economie, "
          "mais jamais tout a fait des citoyens a part entiere dans la realite vecue.", BODY),
        p("Grandir fils d'Africains en France, a Strasbourg, dans les annees 1980-1990, "
          "c'est vivre une contradiction permanente. On t'apprend a l'ecole l'histoire de "
          "France comme si c'etait ton histoire. On t'apprend a reciter des rois de France, "
          "des batailles de France, des gloires de France. Mais dans la rue, dans les yeux "
          "des gens, dans la facon dont les portes s'ouvrent ou se ferment, tu sens que "
          "cette histoire n'est pas la tienne — que tu en es l'objet, pas le sujet.", BODY),
        p("Cheikh Anta Diop a ecrit que le colonise est un homme qui a perdu sa memoire. "
          "L'acte de resistance fondamental est donc l'acte de se souvenir — de retrouver "
          "sa propre histoire, ses propres ancetres, sa propre grandeur.", BODY),
        p("C'est ce que Stellio Capo Chichi va entreprendre. Avec une radicalite qui "
          "surprendra tout le monde.", BODY),

        chap("Chapitre 2 — L'Éveil : Retrouver Kémi, Retrouver l'Étoile"),
        p("Vers ses dix-huit ans, le jeune Stellio entre en contact avec la "
          "<b>Nation of Islam</b> — ce mouvement qui, sur les rives americaines, a donne "
          "a des millions d'hommes et de femmes noirs une fierte, une dignite, un recit "
          "de soi qui ne commence pas par l'esclavage ou la colonisation mais par la "
          "grandeur.", BODY_NI),
        p("C'est la premiere etape d'un eveil qui va s'approfondir.", BODY),
        p("Il s'inscrit a la <b>Faculte de droit de l'Universite Paris X Nanterre</b>, "
          "ou il termine <b>premier de sa promotion parmi deux cents etudiants</b>. "
          "Ce detail est important : Kemi Seba n'est pas un homme qui crie dans les rues "
          "faute de mieux. C'est un homme qui aurait pu, avec ce niveau d'excellence "
          "academique, rejoindre les rangs du systeme, devenir l'Africain respectable que "
          "l'Empire aime presenter comme preuve que tout le monde peut reussir. "
          "Il a choisi autre chose.", BODY),
        p("Les voyages en <b>Egypte</b> sont decisifs. Il decouvre le <b>kemitisme</b> — "
          "la pensee philosophique et spirituelle qui affirme que la civilisation egyptienne "
          "antique etait une civilisation africaine noire, que les pyramides, la philosophie, "
          "les mathematiques, la medecine de l'Antiquite sont un heritage africain. Que "
          "lorsqu'on dit que l'Afrique n'a pas d'histoire, on ment.", BODY),
        p("Il prend le nom de <b>Kemi Seba</b>. <i>Kemi</i> : la terre noire, l'Egypte "
          "noire, la civilisation mere. <i>Seba</i> : l'etoile qui guide dans la nuit. "
          "Ce nom n'est pas un pseudonyme de scene — c'est une renaissance, un acte de "
          "restitution identitaire. Il rejette le nom colonial pour retrouver le nom de "
          "la civilisation.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE II
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE II",
        "Tribu Ka :\nLa Colère qui ne Demande pas Permission")

    story += [
        chap("Chapitre 3 — Tribu Ka : Quand la Diaspora Se Lève"),
        p("En <b>decembre 2004</b>, Kemi Seba fonde <b>Tribu Ka</b> a Paris.", BODY_NI),
        p("Il faut comprendre le contexte pour comprendre la naissance de Tribu Ka. "
          "Nous sommes en 2004. La France est le pays qui finance encore le franc CFA — "
          "la monnaie coloniale qui pille quatorze nations africaines. La France est le "
          "pays dont les soldats maintiennent en place des presidents-predateurs a travers "
          "la Francafrique. La France est le pays qui entasse dans ses banlieues des "
          "millions d'Africains et de descendants d'Africains dans des conditions "
          "denoncees par l'ONU.", BODY),
        p("Tribu Ka est nee de cette colere. Une colere legitime, une colere qui avait "
          "ete compressee pendant des decennies, une colere qui cherchait une forme. "
          "L'organisation s'inspire des traditions africaines precoloniales, du kemitisme, "
          "de la fierte noire. Elle affirme ce que la France coloniale a toujours nie : "
          "que les peuples africains ont une civilisation propre, une histoire propre, "
          "une dignite propre qui ne doit rien a la mission civilisatrice europeenne.", BODY),
        p("L'Etat francais ne pouvait pas tolerer ca. Un groupe de jeunes Noirs qui "
          "relevent la tete, qui disent non, qui ne demandent plus la permission "
          "d'exister — c'est une menace pour l'ordre colonial interieur.", BODY),

        chap("Chapitre 4 — La Rue des Rosiers et la Machine à Broyer (2006)"),
        p("En <b>mai 2006</b>, des membres de Tribu Ka manifestent dans le quartier "
          "du Marais a Paris.", BODY_NI),
        p("Ce qui se passe exactement ce jour-la est sujet a des versions contradictoires. "
          "Ce qui est incontestable, c'est la reaction de l'Etat francais : une "
          "mobilisation immediate, une dissolution par decret du Conseil des ministres "
          "signee le <b>26 juillet 2006</b>, une serie de poursuites judiciaires.", BODY),
        p("L'Etat francais a dissous des organisations politiques noires qui devenaient "
          "trop visibles, trop organisees, trop derangeantes. Ce n'est pas la premiere "
          "fois dans l'histoire que cela se produit — la France a une longue tradition "
          "de repression des organisations qui defient son hegemonie, en Afrique comme "
          "sur son propre territoire.", BODY),
        p("Il faut etre honnete sur cette periode : Tribu Ka a tenu des discours dont "
          "Kemi Seba lui-meme reconnaitra plus tard les limites. Dans la construction "
          "d'une conscience panafricaniste, des erreurs de jeunesse ont ete commises — "
          "des formulations qui depassaient la cible reelle. Le veritable ennemi n'est "
          "pas une ethnie ou une religion — c'est un systeme economique et politique : "
          "l'imperialisme, la Francafrique, l'exploitation des ressources africaines "
          "par des multinationales.", BODY),
        p("Cette evolution de la pensee de Kemi Seba vers un panafricanisme plus rigoureux "
          "et mieux cible est precisement ce qui le rend plus dangereux pour l'Empire : "
          "un militant qui apprend, qui precise sa pensee, qui devient plus efficace.", BODY),

        chap("Chapitre 5 — Le Harcèlement Judiciaire"),
        p("La dissolution de Tribu Ka n'est que le debut d'une longue campagne de "
          "harcelement juridique.", BODY_NI),
        p("<b>2006-2009 :</b> Arrestations repetees, proces, condamnations. Des mois "
          "de procedures, d'audiences, d'appels. Le but n'est pas necessairement de "
          "l'emprisonner a long terme — le but est de l'occuper, de l'epuiser, de lui "
          "faire passer son temps et ses ressources dans les palais de justice plutot "
          "que dans l'organisation politique.", BODY),
        p("C'est la technique classique de la repression judiciaire contre les militants "
          "noirs. Malcolm X en a parle. Les Black Panthers en ont parle. Angela Davis "
          "en a parle. On n'a pas besoin d'envoyer quelqu'un en prison pour toujours "
          "pour le neutraliser — il suffit de l'ensevelir sous des procedures.", BODY),
        p("<b>2014 :</b> Il passe plusieurs semaines en prison. Pas pour avoir vole, "
          "pas pour avoir blesse, pas pour avoir commis un crime ordinaire. Pour avoir "
          "dit des choses. Pour avoir organise des gens. Pour avoir refuse de se taire.", BODY),
        p("Cette incarceration, comme toutes les incarcerations de militants africains "
          "par des systemes coloniaux, ne brise pas — elle forge.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE III
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE III", "L'Afrique Appelle,\nIl Répond")

    story += [
        chap("Chapitre 6 — Le Retour aux Sources (Dakar, 2011)"),
        p("En <b>2011</b>, Kemi Seba pose ses bagages a <b>Dakar</b>.", BODY_NI),
        p("Ce geste a une signification que les Africains de la diaspora comprennent "
          "viscerement : rentrer. Pas comme touriste. Pas comme expatrie. Rentrer pour "
          "travailler, pour se battre, pour construire.", BODY),
        p("Dakar, capitale de la resistance culturelle africaine. La ville de Leopold "
          "Sedar Senghor, de Cheikh Anta Diop, de Birago Diop. La ville ou l'Afrique "
          "pense a voix haute depuis des decennies. Kemi Seba ne vient pas les mains "
          "vides — il vient avec une formation intellectuelle solide, une experience "
          "du combat politique, et une vision du monde construite dans les feux de "
          "la resistance de la diaspora.", BODY),
        p("Il devient rapidement une voix incontournable sur les televisions et dans "
          "les universites d'Afrique de l'Ouest. Pas parce qu'il dit ce que les gens "
          "veulent entendre — mais parce qu'il dit ce que les gens <i>savent</i> sans "
          "avoir les mots pour le formuler.", BODY),
        p("<i>Pourquoi nos pays sont-ils pauvres alors qu'ils sont riches en ressources ? "
          "A qui appartient vraiment notre monnaie ? Qui decide vraiment dans nos "
          "capitales ?</i>", BODY),
        p("Ces questions ne sont pas nouvelles. Des economistes, des historiens, des "
          "politologues les posent depuis des decennies. Mais Kemi Seba les pose dans "
          "un langage que la jeunesse africaine comprend, avec une passion qui traverse "
          "les ecrans, et sans les precautions rhetoriques des intellectuels qui ont "
          "peur de perdre leur bourse ou leur poste.", BODY),

        chap("Chapitre 7 — Le Franc CFA : Nommer la Blessure"),
        p("La grande bataille intellectuelle et politique de Kemi Seba en Afrique — "
          "celle qui va le faire connaitre de millions de personnes — c'est la bataille "
          "contre le <b>franc CFA</b>.", BODY_NI),
        p("Le franc CFA est une monnaie coloniale. Creee en 1945 par la France pour "
          "ses colonies, elle n'a jamais vraiment change de nature malgre les "
          "independances de 1960. Elle lie quatorze nations africaines a la Banque "
          "de France, fixe leurs taux de change sans que ces nations aient un vrai "
          "mot a dire, impose des contraintes qui empechent ces pays de mener des "
          "politiques monetaires adaptees a leurs besoins reels.", BODY),
        p("Des economistes serieux — Samir Amin, Carlos Lopes, Ndongo Samba Sylla — "
          "ont documente tout cela pendant des decennies. Kemi Seba prend cette "
          "documentation academique et la transforme en conviction populaire. Il parle "
          "au marche de Dakar comme a l'amphi de l'UCAD. Il parle a l'entrepreneur "
          "burkinabe comme au lyceen nigerien.", BODY),
    ]
    story.append(quote(
        "« Le franc CFA, c'est la chaine visible que l'esclavage avait laissee sur nos "
        "poignets apres avoir ote les menottes. »",
        "Kémi Séba"
    ))
    story += [
        p("En <b>janvier 2017</b>, il fonde le <b>Front Anti-CFA</b>. Des manifestations "
          "s'organisent simultanement dans plusieurs capitales africaines. Pour la premiere "
          "fois depuis des decennies, la monnaie coloniale devient un sujet de masse, "
          "un sujet de rue, pas seulement un sujet de colloque.", BODY),
        p("L'Empire prend note. Et commence a reflechir a comment stopper ca.", BODY),

        chap("Chapitre 8 — Le Billet Brûlé : L'Étincelle (Dakar, 19 août 2017)"),
        p("<b>19 août 2017.</b>", BODY_NI),
        p("A Dakar, lors d'une manifestation contre la Francafrique, Kemi Seba sort un "
          "billet de <b>5 000 francs CFA</b> et le brule devant les cameras.", BODY),
        p("Ce geste de quelques secondes va electriser le continent.", BODY),
        p("Il y a des gestes qui synthetisent une epoque. Rosa Parks qui ne se leve pas "
          "de son siege. Mandela qui brule son livret de passes. Des actes simples, "
          "physiques, immediats, qui disent en un seul instant ce que des milliers de "
          "mots n'arrivent pas a dire.", BODY),
        p("Bruler le billet CFA, c'est bruler la chaine. C'est dire : <i>je suis libre, "
          "je ne reconnais pas votre domination monetaire, votre argent colonial ne "
          "m'appartient pas et je n'en veux pas.</i>", BODY),
        p("La video fait le tour du monde en quelques heures. Des millions de jeunes "
          "Africains la regardent, la partagent, la commentent avec la fievre de ceux "
          "qui voient pour la premiere fois quelqu'un faire exactement ce qu'ils "
          "ressentaient sans avoir pu le formuler.", BODY),
        p("Le <b>25 août 2017</b>, Kemi Seba est arrete pour destruction de monnaie "
          "ayant cours legal. Le <b>29 août</b>, il est <b>acquitte</b> par le tribunal "
          "correctionnel de Dakar. La justice reconnait qu'il n'a pas commis "
          "d'infraction caracterisee.", BODY),
        p("Mais le <b>6 septembre 2017</b>, malgre l'acquittement, les autorites "
          "senegalaises le <b>expulsent</b> du territoire pour menace grave pour l'ordre "
          "public.", BODY),
        p("La logique est revelatrice : tu n'as rien fait d'illegal — mais tu es trop "
          "dangereux pour rester. Un homme acquitte par les tribunaux mais chasse du "
          "pays parce qu'il brule des billets de monnaie coloniale : voila quelle est "
          "la democratie reelle en Francafrique.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE IV
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE IV",
        "Combattre l'Empire avec\nles Armes du Monde Réel")

    story += [
        chap("Chapitre 9 — La Géopolitique des Opprimés"),
        p("On ne peut pas comprendre les choix geopolitiques de Kemi Seba sans "
          "comprendre la doctrine qui les fonde.", BODY_NI),
        p("Le panafricanisme du XXIe siecle n'est pas le panafricanisme des annees 1960. "
          "Les peres fondateurs — Nkrumah, Lumumba, Sekou Toure, Nyerere — operaient "
          "dans un monde bipolaire, Guerre froide, ou les Etats africains nouvellement "
          "independants cherchaient a naviguer entre deux blocs. Aujourd'hui le monde "
          "est en pleine reconfiguration multipolaire : la Chine est devenue une "
          "puissance mondiale, la Russie conteste l'hegemonie atlantiste, des pays "
          "du Sud affirment leurs propres ambitions.", BODY),
        p("Pour Kemi Seba, la question n'est pas <i>quelle puissance etrangere est "
          "bonne</i> — la question est : <i>comment les peuples africains utilisent-ils "
          "les contradictions entre puissances etrangeres pour se liberer de la "
          "domination neocoloniale francaise ?</i>", BODY),
        p("C'est une vieille strategie. Lumumba l'utilisait quand il menacait de se "
          "tourner vers l'URSS. Nasser l'utilisait. Sekou Toure l'utilisait. Ce n'est "
          "pas de la naivete vis-a-vis de la Russie ou de la Chine — c'est de la "
          "lucidite sur le fait que l'ennemi principal de l'Afrique francophone, "
          "en 2020, s'appelle encore la Francafrique.", BODY),

        chap("Chapitre 10 — Le « Projet Kémi » et la Guerre de l'Information"),
        p("En <b>2023</b>, des revelations circulent dans les medias occidentaux sur "
          "des liens financiers entre Kemi Seba et les reseaux proches d'Evgueni "
          "Prigojine.", BODY_NI),
        p("Il faut d'abord contextualiser la source. Ces revelations viennent de medias "
          "— <i>Jeune Afrique</i>, Arte, <i>Die Welt</i> — qui ne sont pas neutres "
          "dans le grand debat sur l'influence francaise en Afrique. <i>Jeune Afrique</i> "
          "en particulier est une publication dont les liens historiques avec les reseaux "
          "de la Francafrique sont bien documentes.", BODY),
        p("Kemi Seba lui-meme reconnait avoir eu des contacts avec des structures proches "
          "de Prigojine. Sa reponse est directe, sans faux-semblant :", BODY),
    ]
    story.append(quote(
        "« Les 400 000 dollars dont ils parlent, c'est une insulte pour nous, parce "
        "que nous, il nous en faut beaucoup plus. »",
        "Kémi Séba, sur le financement Wagner, 2023"
    ))
    story += [
        p("Cette reponse dit plusieurs choses. Elle dit que le panafricanisme n'a pas "
          "de complexe a se financer dans un monde ou la France finance depuis des "
          "decennies les partis politiques, les medias et les dirigeants africains "
          "qui lui sont favorables. Elle dit qu'on ne va pas se scandaliser de quelques "
          "centaines de milliers de dollars quand la France a verse des milliards via "
          "des canaux opaques pour maintenir son emprise sur le continent.", BODY),
        p("La question de la Russie en Afrique est complexe. Ni Moscou ni Paris ni "
          "Pekin n'est un ami desinteresse de l'Afrique. Mais dans la configuration "
          "actuelle, l'ennemi principal — celui qui tient les cordons des monnaies, "
          "celui qui a des soldats sur le continent, celui qui finance les presidents "
          "complaisants — reste la Francafrique. Et utiliser les contradictions "
          "geopolitiques mondiales dans ce combat n'est pas une trahison du "
          "panafricanisme — c'est une tactique seculaire de tous les peuples qui "
          "se sont liberes de la domination coloniale.", BODY),

        chap("Chapitre 11 — Alexandre Douguine et la Philosophie du Monde Multipolaire"),
        p("Les liens de Kemi Seba avec <b>Alexandre Douguine</b> ne sont pas un "
          "secret — il les assume pleinement.", BODY_NI),
        p("Douguine est le theoricien du monde multipolaire : l'idee que l'hegemonie "
          "americano-atlantiste sur la planete n'est pas une fatalite, qu'il existe "
          "d'autres civilisations, d'autres modeles, d'autres futurs possibles. Pour "
          "le panafricanisme, cette these est une ressource intellectuelle, pas un "
          "programme politique a copier.", BODY),
        p("Ce n'est pas parce que Douguine est russe que sa critique de l'unipolarisme "
          "occidental est fausse. Et ce n'est pas parce que Kemi Seba dialogue avec "
          "lui qu'il adopte les positions russes sur l'Ukraine ou sur quoi que ce "
          "soit d'autre.", BODY),
        p("L'Afrique a toujours su prendre les outils intellectuels la ou ils se "
          "trouvent, les utiliser pour ses propres fins, et garder sa propre boussole. "
          "C'est ce que font les penseurs africains depuis Cheikh Anta Diop jusqu'aux "
          "theoriciens contemporains de la decolonisation.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE V
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE V",
        "Les Juntes et\nla Renaissance Sahélienne")

    story += [
        chap("Chapitre 12 — Le Vent du Sahel : Quand l'Afrique Se Redresse"),
        p("A partir de <b>2020</b>, quelque chose de profond se passe au Sahel.", BODY_NI),
        p("Des militaires africains renversent des presidents qui s'etaient transformes "
          "en relais de la puissance etrangere. Au Mali, en Guinee, au Burkina Faso, "
          "au Niger. Ces coups d'Etat ne ressemblent pas aux coups d'Etat classiques "
          "de la guerre froide — ou un general finance par la CIA ou la DGSE renversait "
          "un leader trop independant.", BODY),
        p("Ces coups d'Etat-la expriment quelque chose de reel dans les populations : "
          "une lassitude profonde de la Francafrique, une aspiration a la souverainete "
          "reelle, pas de la souverainete de papier.", BODY),
        p("La France avait ses troupes au Mali depuis 2013 — operation Serval, puis "
          "Barkhane — et le resultat apres des annees de presence militaire etait : "
          "des milliers de civils morts, une insecurite qui s'etendait, une economie "
          "qui stagnait. Les juntes saheliennes ont dit : <i>nous n'avons plus besoin "
          "de vous, partez.</i> Et les soldats francais ont plie bagage.", BODY),
        p("Kemi Seba soutient ces mouvements. Pas aveuglement — mais fermement. "
          "Ses enregistrements de mars 2026 montrent qu'il n'est pas naif sur les "
          "limites de ces gouvernements. Mais dans le rapport de forces actuel, un "
          "gouvernement qui chasse les soldats francais et renegocie ses accords "
          "miniers est objectivement en train de faire avancer la cause de la "
          "souverainete africaine.", BODY),
        p("<b>Août 2024 :</b> Le general Tchiani, dirigeant du Niger, le nomme "
          "<b>conseiller special</b> et lui octroie un <b>passeport diplomatique "
          "nigerien</b>. C'est la reconnaissance officielle d'un role que Kemi Seba "
          "joue depuis des annees : celui de l'intellectuel organique du panafricanisme "
          "populaire contemporain.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE VI
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE VI", "L'Empire Contre-Attaque")

    story += [
        chap("Chapitre 13 — La Déchéance : L'Empire Découvre Son Vrai Visage"),
        p("<b>29 fevrier 2024.</b> La France initie une procedure de decheance de "
          "nationalite contre Kemi Seba.", BODY_NI),
        p("Ce geste revele plus sur la France que sur Kemi Seba.", BODY),
        p("La France se presente comme le pays des droits de l'Homme. La France se "
          "presente comme une democratie liberale ou la liberte d'expression est un "
          "principe fondamental. Et pourtant : elle dechoit de sa nationalite un homme "
          "qui a ose bruler un passeport, qui a ose critiquer sa politique africaine, "
          "qui a ose soutenir des gouvernements africains souverains.", BODY),
        p("Quel crime a commis Kemi Seba ? Il a dit que le franc CFA etait une monnaie "
          "coloniale — ce que les economistes africains disent depuis soixante ans. Il "
          "a dit que les bases militaires francaises en Afrique etaient des instruments "
          "de domination — ce que les rapports parlementaires francais eux-memes "
          "reconnaissent indirectement. Il a dit que les Africains avaient le droit de "
          "choisir leurs allies — ce que pretend garantir le droit international.", BODY),
        p("Pour ca, il est dechut de sa nationalite.", BODY),
        p("<b>16 mars 2024.</b> Sa reponse est a la hauteur du geste imperial : "
          "il brule son passeport francais.", BODY),
    ]
    story.append(quote(
        "« Votre passeport, ce n'est pas un os que vous nous donnez comme si les Noirs "
        "etaient des chiens. Je suis un homme Noir libre. Je suis un Africain libre. "
        "Je suis un Beninois libre. »",
        "Kémi Séba, Fleury-Mérogis, 16 mars 2024"
    ))
    story += [
        p("Ces mots resonnent a travers tout le continent. Des millions de personnes "
          "qui ont vu leurs parents, leurs oncles, leurs voisins humilies a des guichets "
          "de prefecture, traites comme des sujets coloniaux dans des salles d'attente "
          "kafkaiennes, entendent dans ces mots quelque chose de liberateur.", BODY),
        p("<b>8 juillet 2024.</b> Le decret est publie au Journal officiel. La France "
          "lui retire sa nationalite.", BODY),
        p("Il s'en fout. Il n'en avait plus besoin depuis longtemps. Il est africain.", BODY),

        chap("Chapitre 14 — La DGSI : La Police Politique s'en Mêle (Octobre 2024)"),
        p("<b>14 octobre 2024.</b> Paris. Un restaurant du 15e arrondissement.", BODY_NI),
        p("Des agents de la <b>Direction Generale de la Securite Interieure</b> — la "
          "police politique francaise — arretent Kemi Seba. Il venait rendre visite "
          "a son pere hospitalise. Son passeport diplomatique nigerien est dans "
          "sa poche.", BODY),
        p("Les charges : <i>intelligences avec une puissance etrangere en vue de "
          "susciter des hostilites contre la France.</i> Trente ans d'emprisonnement "
          "encourus.", BODY),
        p("Traduisons : un Africain qui dit aux autres Africains de ne plus se soumettre "
          "a la domination francaise, qui soutient des gouvernements africains qui "
          "chassent les soldats francais, est qualifie d'ennemi de la France.", BODY),
        p("Cette qualification devrait etre une medaille.", BODY),
        p("<b>16 octobre 2024 :</b> Il est relache. Pas parce que la France a renonce "
          "a le poursuivre — mais parce que les preuves legales de ce qu'elle lui "
          "reproche sont difficiles a constituer dans un Etat de droit. L'enquete "
          "se poursuit. La pression reste.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE VII
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE VII", "Les Épreuves du Combat")

    story += [
        chap("Chapitre 15 — Le Bénin, la Trahison, le Mandat (2025)"),
        p("<b>Juin 2025.</b> Un premier mandat d'arret beninois pour blanchiment "
          "de capitaux.", BODY_NI),
        p("<b>7 decembre 2025.</b> Tentative de coup d'Etat au Benin contre le "
          "president Patrice Talon.", BODY),
        p("Kemi Seba publie une video de soutien a ce qu'il croit etre le renversement "
          "d'un president qu'il considere comme un representant de l'ordre neocolonial "
          "au Benin.", BODY),
        p("La tentative echoue. Talon reste au pouvoir. Un mandat d'arret international "
          "est emis contre Kemi Seba pour <i>apologie de crimes contre la surete de "
          "l'Etat</i>.", BODY),
        p("Cette sequence merite une analyse honnete. La position de Kemi Seba sur le "
          "Benin de Patrice Talon n'est pas incomprehensible dans une logique "
          "panafricaniste : Talon est percu comme un president proche des interets "
          "economiques francais, gestionnaire d'une economie dont les ressources ne "
          "profitent pas suffisamment aux populations. La critique est legitime.", BODY),
        p("Mais le soutien immediat a un coup d'Etat, avant meme de connaitre sa "
          "nature reelle, avant meme de savoir qui en sont les acteurs et quels sont "
          "leurs projets, est une erreur tactique. C'est une des tensions permanentes "
          "du combat panafricaniste : entre l'urgence de la liberation et la necessite "
          "de construire des institutions durables.", BODY),

        chap("Chapitre 16 — Natou et les Siens : Le Prix Payé par les Proches"),
        p("<b>22 decembre 2025.</b> L'arrestation de <b>Natou Pedro Sakombi</b> "
          "au Benin.", BODY_NI),
        p("Natou — historienne, artiste, compagne de Kemi Seba pendant sept ans, "
          "mere de ses enfants — est arretee au Benin sous des chefs d'accusation "
          "que sa defense qualifie de pretextes. Elle est liberee le "
          "<b>26 decembre</b>.", BODY),
        p("Ce que cette arrestation revele, c'est que l'Empire ne frappe pas seulement "
          "les combattants — il frappe leurs familles, leurs proches, ceux qui les "
          "aiment. C'est une technique de guerre. Faire souffrir ceux qu'un homme "
          "aime pour lui faire sentir qu'il n'est pas seul a payer le prix de "
          "sa resistance.", BODY),
        p("Kemi Seba a des enfants. Plusieurs, issus de deux unions. Ces enfants "
          "grandissent en sachant que leur pere est un homme que les Etats veulent "
          "mettre en prison. C'est un prix enorme. C'est le prix que le panafricanisme "
          "impose a ceux qui le choisissent vraiment, pas comme posture mais "
          "comme vie.", BODY),
        p("Ni Lumumba ni Sankara ni aucun des grands combattants africains n'a ete "
          "epargne dans sa vie personnelle. La lutte prend tout.", BODY),

        chap("Chapitre 17 — Les Enregistrements et la Complexité du Combat (2026)"),
        p("En <b>mars 2026</b>, des enregistrements audio de Kemi Seba circulent "
          "sur les reseaux sociaux.", BODY_NI),
        p("Dans ces conversations privees, il exprime ses doutes sur certaines "
          "orientations des juntes saheliennes, critique leur tendance a "
          "instrumentaliser le panafricanisme comme discours de legitimation "
          "personnelle plutot que comme projet de transformation reelle.", BODY),
        p("Ces enregistrements ont ete immediatement utilises par les medias lies "
          "a la Francafrique pour tenter de discrediter Kemi Seba, de le presenter "
          "comme hypocrite, de creuser un fosse entre lui et ses allies saheliens.", BODY),
        p("Mais il faut lire ces enregistrements autrement.", BODY),
        p("Un penseur qui ne doute pas est un fanatique. Un militant qui ne "
          "s'interroge pas sur les limites de ses alliances est un ideologue "
          "aveugle. Ce que ces enregistrements montrent, c'est un homme qui pense, "
          "qui questionne, qui cherche — meme quand il est sous pression.", BODY),
    ]
    story.append(quote(
        "« Etre panafricaniste maintenant, c'est encenser l'AES. "
        "Je ne suis pas a l'aise avec ca. »",
        "Kémi Séba, enregistrements audio fuités, mars 2026"
    ))
    story += [
        p("Ce n'est pas une trahison. C'est de la lucidite. Le panafricanisme ne "
          "peut pas se reduire a soutenir inconditionnellement tout gouvernement "
          "qui brandit le drapeau anti-francais. Le panafricanisme, c'est la "
          "liberation des peuples africains — pas la substitution d'une tutelle "
          "par une autre.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # PARTIE VIII
    # ══════════════════════════════════════════════════════════
    story += part_page("PARTIE VIII", "La Rivière et l'Avenir")

    story += [
        chap("Chapitre 18 — Pretoria : L'Exil du Combattant (Avril 2026)"),
        p("<b>13 avril 2026. Afrique du Sud.</b>", BODY_NI),
        p("Kemi Seba est arrete a Pretoria. Les circonstances de son deplacement "
          "en Afrique du Sud, la procedure qui s'ensuit, la demande d'extradition "
          "beninoise — tout cela fait l'objet de procedures judiciaires en cours.", BODY),
        p("Il se trouve a quarante-quatre ans dans une situation que les "
          "panafricanistes connaissent bien dans l'histoire : l'exil force, les "
          "frontieres comme armes, la geographie comme prison.", BODY),
        p("Nkrumah fut renverse pendant un voyage hors de son pays. Mandela passa "
          "vingt-sept ans en prison. Kemi Seba n'a pas ete emprisonne vingt-sept "
          "ans — mais la logique est la meme : quand on ne peut pas acheter un homme, "
          "on essaie de l'emprisonner.", BODY),
        p("Son fils Khonsou, dix-huit ans, etait avec lui lors de l'arrestation. "
          "Cette image — un pere et son fils pris dans les filets des Etats qui "
          "combattent le panafricanisme — est une image que les generations futures "
          "liront dans les livres d'histoire, de la meme facon qu'on lit aujourd'hui "
          "les lettres que Lumumba ecrivait a sa femme depuis sa prison.", BODY),

        chap("Chapitre 19 — La Vie Personnelle : L'Homme derrière le Militant"),
        p("Kemi Seba est un homme, pas une icone.", BODY_NI),
        p("Il a deux unions — avec <b>Etuma</b>, mere de Satherou et Khonsou, et "
          "avec <b>Natou Pedro Sakombi</b>, mere d'Imhotep, Verona et Anupe. Il vit "
          "selon un modele familial africain que la modernite occidentale ne reconnait "
          "pas necessairement mais qui existe et a ses propres logiques.", BODY),
        p("La vie d'un militant ne ressemble pas a la vie d'un gestionnaire de fond "
          "d'investissement. Elle est faite de deplacements, de crises, de periodes "
          "de separation, d'urgences politiques qui s'imposent sur les projets "
          "personnels. Les femmes et les enfants de Kemi Seba ont paye le prix de "
          "ses combats autant que lui-meme.", BODY),
        p("La reconnaissance de cela fait partie du respect qu'on doit a un "
          "combattant : voir non seulement le militant mais l'homme entier, avec "
          "tout ce que son choix de vie implique pour ceux qu'il aime.", BODY),

        chap("Chapitre 20 — L'Œuvre : La Pensée qui Résiste"),
        p("Quand les Etats emprisonnent les corps, ils ne peuvent pas emprisonner "
          "les idees.", BODY_NI),
        p("Les livres de Kemi Seba continuent de circuler. Ils sont lus dans les "
          "universites africaines, dans les lycees, dans les cafes de Dakar et "
          "d'Abidjan et de Bamako et de Niamey. Des jeunes gens qui n'ont jamais "
          "rencontre l'auteur les lisent et y trouvent quelque chose qu'ils "
          "cherchaient.", BODY),
        p("<b>Supra-Negritude</b> (2013), <b>Black Nihilism</b> (2014), "
          "<b>Obscure Epoque</b> (2016), <b>L'Afrique libre ou la mort</b> (2018) "
          "— ces titres resonnent comme un programme de liberation, chaque livre "
          "poussant la pensee plus loin, cherchant les fondements philosophiques "
          "d'une Afrique souveraine et digne.", BODY),
        p("La bibliographie de Kemi Seba est une contribution reelle a la pensee "
          "panafricaniste contemporaine. Elle peut etre discutee, critiquee, "
          "enrichie — mais elle existe, et elle ne peut pas etre effacee.", BODY),
        PageBreak(),
    ]

    # ══════════════════════════════════════════════════════════
    # ÉPILOGUE
    # ══════════════════════════════════════════════════════════
    story += [
        Spacer(1, 1*cm),
        hr(width=4*cm, thickness=1, color=GRIS, spaceB=20, spaceA=20),
        p("ÉPILOGUE : LE FEU QUI BRÛLE LES CHAÎNES", AV_TITRE),
        hr(spaceB=6, spaceA=20),

        p("<b>La riviere Limpopo. Avril 2026.</b>", BODY_NI),
        p("Un homme traverse des frontieres. Un homme cherche comment continuer le "
          "combat depuis un monde ou chaque passeport qu'on lui tend est aussi "
          "une laisse.", BODY),
        p("Dans les rues de Dakar, de Ouagadougou, de Bamako, des jeunes Africains "
          "regardent leurs telephones et suivent l'histoire en temps reel. Certains "
          "pleurent. Certains sont en colere. Certains murmurent son nom comme on "
          "murmure le nom de ceux qu'on ne veut pas oublier.", BODY),
        p("Kemi Seba n'a pas gagne. Il n'a pas non plus perdu.", BODY),
        p("Il a fait quelque chose que l'Empire redoute plus que tout : il a dit "
          "a une generation entiere que c'est possible de dire non. Que l'Empire "
          "frappe, oui. Qu'il persecute, qu'il expulse, qu'il dechoit, qu'il arrete, "
          "qu'il intente des proces — mais que ca, c'est preuve que le combat est "
          "reel. Que ca compte. Qu'on ne persecute pas ceux qui ne derangent pas.", BODY),
        p("La verite que l'Empire ne peut pas acheter n'est plus dans les mains "
          "d'un seul homme. Elle a ete semee. Elle a germe dans des millions de "
          "tetes. Elle est dans les videos que des lyceens de Cotonou regardent "
          "la nuit sur leurs telephones. Elle est dans les tribunes que des "
          "journalistes maliens ecrivent en sachant qu'on pourrait les arreter "
          "pour ca. Elle est dans les questions que des etudiants burkinabes "
          "posent a leurs professeurs sur le franc CFA, sur Francafrique, sur "
          "pourquoi leurs pays restent pauvres.", BODY),
        p("L'Empire peut acheter des hommes. Il peut en emprisonner d'autres. "
          "Mais il ne peut pas arreter une idee dont le temps est venu.", BODY),
        Spacer(1, 0.8*cm),
        p("<b>L'Afrique libre ou la mort.</b>", BODY_NI),
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
        ["1981", "Naissance a Strasbourg — Stellio Gilles Robert Capo Chichi"],
        ["1999", "Adhesion a la Nation of Islam"],
        ["2000", "Capacite en droit, Paris X Nanterre — 1er de promo sur 200 etudiants"],
        ["2002", "Prise du nom Kemi Seba, porte-parole du Parti Kemite"],
        ["Dec. 2004", "Fondation de Tribu Ka a Paris"],
        ["Mai 2006", "Incident rue des Rosiers a Paris"],
        ["Juil. 2006", "Dissolution de Tribu Ka par decret du Conseil des ministres"],
        ["2006-2014", "Harcelement judiciaire repete — incarceration en 2014"],
        ["2011", "Depart definitif pour Dakar — retour a l'Afrique"],
        ["2015", "Fondation d'Urgences Panafricanistes a Dakar"],
        ["Jan. 2017", "Creation du Front Anti-CFA — manifestations sur le continent"],
        ["Aout 2017", "Arrestation puis ACQUITTEMENT a Dakar apres brulage du billet CFA"],
        ["Sept. 2017", "1ere expulsion du Senegal malgre l'acquittement"],
        ["2018-2019", "Contacts avec les reseaux proches de Prigojine — 440 000 USD"],
        ["Fev. 2020", "2eme expulsion du Senegal — 30h de retention administrative"],
        ["2020-2023", "Soutien aux transitions souverainistes au Sahel"],
        ["2023", "Revelations mediatiques sur le Projet Kemi"],
        ["Mars 2024", "Brulage du passeport francais a Fleury-Merogis"],
        ["Juil. 2024", "Decheance de nationalite francaise — l'Empire revele son vrai visage"],
        ["Aout 2024", "Nomme conseiller special du Niger + passeport diplomatique nigerien"],
        ["Oct. 2024", "Arrestation par la DGSI a Paris — 30 ans d'emprisonnement encourus"],
        ["Juin 2025", "Mandat d'arret beninois n°1 (blanchiment)"],
        ["Dec. 2025", "Soutien a la tentative de renversement de Talon → mandat international"],
        ["Dec. 2025", "Arrestation de Natou Pedro Sakombi au Benin — l'Empire frappe les familles"],
        ["Mars 2026", "Enregistrements audio fuites — lucidite critique sur les juntes"],
        ["Avr. 2026", "Arrestation en Afrique du Sud — procedure d'extradition beninoise"],
        ["Mai 2026", "En detention provisoire a Pretoria — la lutte continue"],
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
    # NOTE DE L'AUTEUR
    # ══════════════════════════════════════════════════════════
    story += [
        Spacer(1, 1*cm),
        p("NOTE DE L'AUTEUR", AV_TITRE),
        hr(spaceB=6, spaceA=20),

        p("Ce livre est ecrit du cote des peuples africains.", BODY_NI),
        p("Cela ne signifie pas qu'il ferme les yeux sur les erreurs du militant "
          "qu'il raconte. Cela signifie qu'il comprend le contexte dans lequel ces "
          "erreurs ont ete commises : le contexte d'un homme qui a grandi comme fils "
          "d'immigres beninois dans la France neocoloniale, qui a choisi de se battre "
          "plutot que de se taire, qui a paye ce choix de sa liberte, de sa nationalite, "
          "de sa vie familiale, de son droit de circuler librement sur la planete.", BODY),
        p("Les hommes qui se battent pour la liberation de leur peuple ne sont pas "
          "parfaits. Ils sont humains. Ils font des erreurs de tactique, d'alliance, "
          "de jugement. Lumumba faisait des erreurs. Sankara faisait des erreurs. "
          "Nkrumah faisait des erreurs. Ce qui les definit n'est pas leur perfection "
          "— c'est la direction dans laquelle ils marchaient.", BODY),
        p("Kemi Seba marche vers l'Afrique libre.", BODY),
        p("Que la prison l'arrete provisoirement ne change pas cette direction. Que "
          "des alliances discutables aient ete contractees en chemin ne change pas "
          "cette direction. Que des erreurs aient ete commises ne change pas "
          "cette direction.", BODY),
        p("La question qui compte n'est pas <i>a-t-il ete parfait ?</i>", BODY),
        p("La question qui compte est : <i>dans un monde ou l'Empire achete ceux "
          "qui peuvent l'etre, etait-il a vendre ?</i>", BODY),
        p("La reponse est non.", BODY),
        p("Et c'est pour ca qu'il est en prison.", BODY),
        Spacer(1, 2*cm),
        hr(width=4*cm, thickness=1.5, color=NOIR, spaceB=20, spaceA=20),
        p("KÉMI SÉBA — L'HOMME QUE L'EMPIRE NE POUVAIT PAS ACHETER", GENRE),
        Spacer(1, 0.3*cm),
        p("Biographie panafricaniste — basee sur des faits documentes et sources "
          "journalistiques verifiees.", GENRE),
        Spacer(1, 0.2*cm),
        p("Sources : Jeune Afrique · France 24 · Arte/CAPA · Die Welt · Wikipedia FR/EN "
          "· VOA Afrique · Le JDD · Senenews · The Conversation · Whispeak", GENRE),
    ]

    # ── Build ──────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=footer_canvas, onLaterPages=footer_canvas)
    print(f"PDF genere : {OUTPUT}")

if __name__ == "__main__":
    build()
