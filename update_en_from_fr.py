#!/usr/bin/env python3
"""
Inserts missing content from the French source (LA_PAIX_FR.docx)
into the English translation (PEACE_WE_CAN_PREVENT_IT_EN_4.docx).

Missing sections identified by paragraph-count comparison:
  Ch 14 — Banda Kani paragraph + 'terrorist label' section
  Ch 15 — Bourgeot attribution restored + Itté case + 4 corridor paragraphs
  Ch 19 — AES bank/currency + Tarha Nakal exercises + Force 6 000 men
  Ch 22 — CAR / Touadéra section (3 paras + 2 quotes)
  Ch 24 — Mauritanian stability / Global Slavery Index paragraph
"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from copy import deepcopy
import re

SRC = '/home/user/tts-docs/PEACE_WE_CAN_PREVENT_IT_EN_4.docx'
OUT = '/home/user/tts-docs/PEACE_WE_CAN_PREVENT_IT_EN_5.docx'

doc = Document(SRC)

# ─── XML insertion helper ──────────────────────────────────────────────────────
def insert_para_after(doc, ref_idx, text, bold=False, italic=False):
    """
    Create a new paragraph from `text` and insert it immediately after
    the paragraph at `ref_idx`.  Returns the new paragraph index.
    """
    # Build the new paragraph element
    new_p = OxmlElement('w:p')
    new_pPr = OxmlElement('w:pPr')
    new_pStyle = OxmlElement('w:pStyle')
    new_pStyle.set(qn('w:val'), 'Normal')
    new_pPr.append(new_pStyle)
    new_p.append(new_pPr)

    new_r = OxmlElement('w:r')
    new_rPr = OxmlElement('w:rPr')
    if bold:
        b_el = OxmlElement('w:b'); new_rPr.append(b_el)
        b2_el = OxmlElement('w:bCs'); new_rPr.append(b2_el)
    if italic:
        i_el = OxmlElement('w:i'); new_rPr.append(i_el)
        i2_el = OxmlElement('w:iCs'); new_rPr.append(i2_el)
    # Font
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Garamond')
    rFonts.set(qn('w:hAnsi'), 'Garamond')
    new_rPr.append(rFonts)
    sz = OxmlElement('w:sz');  sz.set(qn('w:val'), '22'); new_rPr.append(sz)
    szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), '22'); new_rPr.append(szCs)

    new_r.append(new_rPr)
    new_t = OxmlElement('w:t')
    new_t.text = text
    new_t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    new_r.append(new_t)
    new_p.append(new_r)

    # Insert after reference paragraph
    ref_el = doc.paragraphs[ref_idx]._element
    ref_el.addnext(new_p)

    # Return new paragraph index (ref_idx + 1 since we inserted after)
    return ref_idx + 1


def replace_para_text(doc, idx, new_text):
    """Replace the text of paragraph at `idx` preserving style."""
    p = doc.paragraphs[idx]
    # Clear runs and re-add
    for run in p.runs:
        run.text = ''
    if p.runs:
        p.runs[0].text = new_text
    else:
        p.add_run(new_text)


def para_text(doc, idx):
    return doc.paragraphs[idx].text.strip()


# ─── Verify anchors before inserting ──────────────────────────────────────────
def check(idx, expected_fragment, label):
    actual = para_text(doc, idx)
    if expected_fragment.lower() not in actual.lower():
        print(f'  ⚠ {label}: expected "{expected_fragment[:60]}" at [{idx}], got "{actual[:60]}"')
        return False
    print(f'  ✓ {label} anchor confirmed at [{idx}]')
    return True


print('── Verifying anchors ──')
check(303, 'Jules Domche', 'Ch14 after-Domche')
check(305, 'dominant narrative', 'Ch14 after-central-mechanism')
check(312, 'Azawad is a political fabrication', 'Ch15 Azawad para')
check(315, 'Abdoulaye Maïga', 'Ch15 Maïga attribution')
check(318, 'cartography reveals', 'Ch15 cartography para')
check(352, 'CNSP Niger', 'Ch19 Tiani attribution')
check(354, 'Assimi Goïta', 'Ch19 Goïta attribution')
check(368, 'honest answer', 'Ch22 nuanced answer')
check(381, 'Bilal Chérif', 'Ch24 Bilal Chérif')
print()


# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 14 — Two missing sections
# ══════════════════════════════════════════════════════════════════════════════
print('── Chapter 14 insertions ──')

# 1. Banda Kani paragraph → insert after EN[303] (Jules Domche attribution)
banda_kani_en = (
    "Banda Kani formulates the place of the Central African Republic (CAR) in pan-Africanist history: "
    "the CAR is 'the first African country to have gone through the full cycle of Françafrique all the way "
    "to its dismantlement' — a laboratory both of the system of domination and of the strategies for "
    "emancipating oneself from it."
)
insert_para_after(doc, 303, banda_kani_en)
print('  ✓ Banda Kani paragraph inserted after EN[303]')
# All subsequent indices shift by +1

# 2. 'Terrorist label' sub-section → insert after EN[306] (now the central-mechanism body)
# Note: after previous insertion, EN[305] → EN[306], EN[305 body] → EN[306]
# Find the central mechanism body paragraph (contains 'dominant narrative presents')
target_idx = None
for i, p in enumerate(doc.paragraphs[302:315], start=302):
    if 'dominant narrative' in p.text.lower():
        target_idx = i
        break

if target_idx:
    print(f'  Central mechanism body now at [{target_idx}]')
    label_en = "The 'terrorist' label: a weapon of narrative warfare"
    insert_para_after(doc, target_idx, label_en, bold=True)
    # Now find the new bold para index
    subhead_idx = target_idx + 1

    saudi_en = (
        "On 5 June 2017, Saudi Arabia, Egypt, the United Arab Emirates (UAE) and Bahrain severed "
        "diplomatic relations with Qatar, accusing it of financing terrorism. France supported the "
        "coalition. Yet the documented reality is unambiguous: Saudi Arabia financed the Group for "
        "the Support of Islam and Muslims (JNIM) and its affiliates throughout the Sahelian crisis, "
        "while Qatar acted as the mediator in Sahel hostage negotiations."
    )
    insert_para_after(doc, subhead_idx, saudi_en)

    lesson_en = (
        "The lesson is mechanical. The 'terrorist' label is not a legal qualification. It is a "
        "narrative instrument. In each new context it designates the actor whose elimination serves "
        "the interests of those who hold the power of labelling. The AES understood this: it expelled "
        "the labellers."
    )
    insert_para_after(doc, subhead_idx + 1, lesson_en)
    print('  ✓ Terrorist-label subhead + 2 paragraphs inserted')
else:
    print('  ⚠ Could not locate central mechanism paragraph — skipping Ch14 label section')


# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 15 — Bourgeot attribution + Itté case + 4 corridor paragraphs
# ══════════════════════════════════════════════════════════════════════════════
print()
print('── Chapter 15 insertions ──')

# Find current index of the Azawad paragraph
azawad_idx = None
for i, p in enumerate(doc.paragraphs[308:330], start=308):
    if 'azawad is a political fabrication' in p.text.lower():
        azawad_idx = i
        break

if azawad_idx:
    print(f'  Azawad para now at [{azawad_idx}]')
    # Prepend Bourgeot attribution to the existing text
    existing = doc.paragraphs[azawad_idx].text.strip()
    bourgeot_prefix = (
        "André Bourgeot, CNRS researcher specialising in the Sahel, is unequivocal: "
    )
    replace_para_text(doc, azawad_idx, bourgeot_prefix + existing)
    print('  ✓ André Bourgeot attribution prepended to Azawad paragraph')

# Find Maïga attribution to insert Sylvain Itté after it
maiga_idx = None
for i, p in enumerate(doc.paragraphs[315:335], start=315):
    if 'abdoulaye maïga' in p.text.lower() and 'azalaï' in p.text.lower():
        maiga_idx = i
        break

if maiga_idx:
    print(f'  Maïga attribution now at [{maiga_idx}]')
    itte_en = (
        "The Sylvain Itté case illustrates the depth of colonial contempt that fuelled the rupture. "
        "Appointed Macron's 'Monsieur Afrique,' Itté declared that the Malian transition government "
        "was 'not legitimate.' This was a former colonial power's representative publicly invalidating "
        "an African government's authority on its own territory — the kind of statement that, in any "
        "other geopolitical context, would constitute a diplomatic incident. In the Sahel, it was "
        "presented as foreign policy analysis."
    )
    insert_para_after(doc, maiga_idx, itte_en)
    print('  ✓ Sylvain Itté paragraph inserted')

# Find the 'cartography reveals' paragraph to insert 4 corridor paragraphs after it
carto_idx = None
for i, p in enumerate(doc.paragraphs[316:340], start=316):
    if 'cartography reveals three structural realities' in p.text.lower():
        carto_idx = i
        break

if carto_idx:
    print(f'  Cartography paragraph now at [{carto_idx}]')

    carto1_en = (
        "The map identifies three operational advantages exploited by armed groups via these routes: "
        "the establishment of connections between northern Mali and Burkina Faso; access to mineral "
        "resources (Niger's uranium, Mali's gold); and the movement of fighters and weapons between "
        "Libya and Mali via the Fezzan."
    )
    insert_para_after(doc, carto_idx, carto1_en)

    carto2_en = (
        "The geographical coincidence between these nomadic routes and the Mauritanian rear base — "
        "where Bilal Chérif, leader of the Liberation Front of Azawad (FLA), has a refuge according "
        "to intelligence sources — reveals a non-random architecture of mobility. It is not chance "
        "that positions jihadist refuges at the crossroads of trans-Saharan trade routes."
    )
    insert_para_after(doc, carto_idx + 1, carto2_en)

    fezzan_en = (
        "The Libyan link completes the cartography. The Fezzan — a vast desert region in southern "
        "Libya — constitutes the principal transit and weapons-storage zone since the collapse of "
        "Gaddafi in 2011. The deliberate destruction of Libyan state capacity by the North Atlantic "
        "Treaty Organization (NATO) intervention created, in the same movement, the conditions for "
        "the permanent militarisation of the Sahelian space."
    )
    insert_para_after(doc, carto_idx + 2, fezzan_en)

    resources_en = (
        "Resource data clarifies the geopolitical stakes. Niger alone holds approximately 5% of the "
        "world's uranium reserves. Mali holds the third-largest gold reserves in West Africa. Terrorist "
        "corridors follow the routes of strategic resources. This is not a documentary coincidence. "
        "It is a structural convergence — and it explains why resolving the security crisis is "
        "inseparable from resolving the question of who controls these resources."
    )
    insert_para_after(doc, carto_idx + 3, resources_en)
    print('  ✓ 4 corridor/cartography paragraphs inserted')
else:
    print('  ⚠ Could not locate cartography paragraph — skipping Ch15 corridor section')


# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 19 — AES bank/currency + Tarha Nakal + Force 6 000
# ══════════════════════════════════════════════════════════════════════════════
print()
print('── Chapter 19 insertions ──')

# Find Tiani summit attribution
tiani_idx = None
for i, p in enumerate(doc.paragraphs[350:380], start=350):
    if 'cnsp niger' in p.text.lower() and 'niamey' in p.text.lower():
        tiani_idx = i
        break

if tiani_idx:
    print(f'  Tiani attribution now at [{tiani_idx}]')

    bank_en = (
        "The summit also decided to establish an AES investment bank and to work towards a common "
        "currency. The economic reintegration of the zone — through infrastructure, currency, and "
        "defence — is the vector of legitimacy that distinguishes the AES from previous African "
        "regional organisations, which stopped at declarations."
    )
    insert_para_after(doc, tiani_idx, bank_en)

    tarha_en = (
        "Tarha Nakal 2 exercises (14 May 2025, Tillia, Niger): joint AES–Chad–Togo operations. "
        "Scenario: attempted border destabilisation by armed groups. Documented result: inter-army "
        "operational coordination at this scale for the first time. The AES is not merely a political "
        "declaration. It is a military apparatus under construction."
    )
    insert_para_after(doc, tiani_idx + 1, tarha_en)
    print('  ✓ AES bank/currency + Tarha Nakal paragraphs inserted')

# Find Goïta attribution and insert Force 6000 after it
goita_idx = None
for i, p in enumerate(doc.paragraphs[358:390], start=358):
    if 'assimi goïta' in p.text.lower() and 'transition' in p.text.lower():
        goita_idx = i
        break

if goita_idx:
    print(f'  Goïta attribution now at [{goita_idx}]')
    force_en = (
        "The AES Unified Force is raised to 6,000 men to cover the Sahelian space. Tiani formulates "
        "the objective: 'This is not a matter of constituting a parade army but a response force for "
        "the hybrid threats striking our populations.' The transition from the political to the "
        "military is the ultimate measure of the AES's credibility — and the ultimate object of "
        "external hostility."
    )
    insert_para_after(doc, goita_idx, force_en)
    print('  ✓ AES Force 6,000 men paragraph inserted')
else:
    print('  ⚠ Could not locate Goïta attribution — skipping Force 6000 insertion')


# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 22 — CAR / Touadéra section
# ══════════════════════════════════════════════════════════════════════════════
print()
print('── Chapter 22 insertions ──')

# Find the 'honest answer' paragraph
honest_idx = None
for i, p in enumerate(doc.paragraphs[368:400], start=368):
    if 'honest answer is nuanced' in p.text.lower():
        honest_idx = i
        break

if honest_idx:
    print(f'  Honest-answer paragraph now at [{honest_idx}]')

    car_en = (
        "The Central African Republic (CAR) prefigures this dilemma. Professor of mathematics "
        "Faustin-Archange Touadéra, democratically elected, requested security assistance from Russia "
        "that Paris had refused to provide. The assistance came. Wagner soldiers arrived. The security "
        "balance sheet is real — armed groups pushed back from major cities. The political balance "
        "sheet is ambiguous — mining contracts ceded, a structural dependency reconfigured but not "
        "eliminated."
    )
    insert_para_after(doc, honest_idx, car_en)

    ngoulou_q_en = (
        '"After more than 60 years of cooperation, the Central African Republic remains always the very '
        'last among the last Francophone countries in everything: education, infrastructure, health, '
        'everything. What are they doing there? What do they bring?"'
    )
    insert_para_after(doc, honest_idx + 1, ngoulou_q_en, italic=True)

    ngoulou_att_en = "— Fridolin Ngoulou, Central African analyst, Oubangui Médias"
    insert_para_after(doc, honest_idx + 2, ngoulou_att_en)

    russia_q_en = (
        '"The presence of the Russian Federation on Central African soil derives from the fact that '
        'the other countries had broken off — or had reduced to nothing — the opportunities for '
        'support to this Central African Republic."'
    )
    insert_para_after(doc, honest_idx + 3, russia_q_en, italic=True)

    baipo_att_en = (
        "— Sylvie Baipo Temon, Minister of Foreign Affairs of the CAR, October 2021"
    )
    insert_para_after(doc, honest_idx + 4, baipo_att_en)
    print('  ✓ CAR/Touadéra section (3 paras + 2 quotes) inserted')
else:
    print('  ⚠ Could not locate honest-answer paragraph — skipping Ch22 CAR section')


# ══════════════════════════════════════════════════════════════════════════════
# CHAPTER 24 — Mauritanian stability / Global Slavery Index
# ══════════════════════════════════════════════════════════════════════════════
print()
print('── Chapter 24 insertion ──')

bilal_idx = None
for i, p in enumerate(doc.paragraphs[385:420], start=385):
    if 'bilal chérif' in p.text.lower() and 'mauritania' in p.text.lower():
        bilal_idx = i
        break

if bilal_idx:
    print(f'  Bilal Chérif paragraph now at [{bilal_idx}]')
    slavery_en = (
        "Mauritanian stability is real. It also masks a reality that the Global Slavery Index 2023 "
        "brings to light: Mauritania has the highest rate of slavery in the world as a proportion of "
        "its population. This internal reality creates a structural social pressure that the Aziz "
        "then Ghazouani regime manages through a latent state of emergency — an authoritarian "
        "equilibrium that external actors, seeking a 'stable' Sahel neighbour, prefer not to examine."
    )
    insert_para_after(doc, bilal_idx, slavery_en)
    print('  ✓ Mauritanian stability/slavery paragraph inserted')
else:
    print('  ⚠ Could not locate Bilal Chérif paragraph — skipping Ch24 insertion')


# ─── Save ─────────────────────────────────────────────────────────────────────
print()
doc.save(OUT)
total_paras = sum(1 for p in doc.paragraphs if p.text.strip())
print(f'✓  Saved → {OUT}')
print(f'   Non-empty paragraphs: {total_paras}')
