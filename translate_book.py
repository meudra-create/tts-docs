from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import copy

doc = Document()

# --- Helper ---
def add(style, text, bold=False, italic=False, align=None, indent=None):
    if style == "Heading 1":
        p = doc.add_heading(text, level=1)
    elif style == "Heading 2":
        p = doc.add_heading(text, level=2)
    else:
        p = doc.add_paragraph(style="Normal")
        run = p.add_run(text)
        if bold: run.bold = True
        if italic: run.italic = True
    if align:
        p.alignment = align
    if indent is not None:
        p.paragraph_format.left_indent = Inches(indent)
    return p

def cite(text):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.4)
    run = p.add_run(text)
    run.italic = True
    return p

def sep():
    add("Normal", "★ ★ ★", align=WD_ALIGN_PARAGRAPH.CENTER)

# ===== FRONT MATTER =====
add("Normal", "Alliance of Sahel States", align=WD_ALIGN_PARAGRAPH.CENTER)
add("Normal", "PEACE,", align=WD_ALIGN_PARAGRAPH.CENTER)
add("Normal", "WE CAN PREVENT IT", align=WD_ALIGN_PARAGRAPH.CENTER)
add("Normal", "Geopolitics of African Resistance", align=WD_ALIGN_PARAGRAPH.CENTER)
add("Normal", "BEN–H2O", align=WD_ALIGN_PARAGRAPH.CENTER)
add("Normal", "— 2026 —", align=WD_ALIGN_PARAGRAPH.CENTER)

# Epigraphs
doc.add_paragraph()
cite('"A people without the knowledge of their past history, origin and culture is like a tree without roots."')
add("Normal", "— Marcus Garvey")
cite('"Freedom is not given, it is taken."')
add("Normal", "— Frantz Fanon, The Wretched of the Earth, 1961")
cite('"We must dare to invent the future."')
add("Normal", "— Thomas Sankara, address to the UN General Assembly, 4 October 1984")
cite('"We prefer poverty in freedom to riches in slavery."')
add("Normal", '— Ahmed Sékou Touré, before de Gaulle, 25 September 1958')
cite('"After more than 60 years of cooperation, the Central African Republic remains the very last among French-speaking countries in the world."')
add("Normal", "— Fridolin Ngoulou, Central African analyst")
cite('"Let us remain vigilant."')
add("Normal", "— General Abdourahamane Tiani, CNSP Niger, 13 November 2025")

# ===== FOREWORD =====
doc.add_paragraph()
add("Normal", "FOREWORD — Method and Analytical Rigour", bold=True)
add("Normal", "This book is the product of rigorous analytical work covering the period 2013–2026. It draws on more than 130 sources from radically different editorial categories: mainstream critical French sources, academic sources, official sources from the governments of the Alliance of Sahel States (AES), Pan-Africanist sources, Central African and Sahelian field sources, and institutional adversarial sources.")
add("Normal", "The method is consistent throughout: to evaluate each source on the basis of its concrete evidence and cross-referencing, without differentiated indulgence based on editorial orientation or geographic origin. African media outlets (Ndjoni Sango, Oubangui Médias, Vox Africa) are held to the same standards as Le Monde or RTL France. What matters is the convergence of evidence and the possibility of independent verification.")
add("Normal", ".")
add("Normal", 'The term "coup" is proscribed. Documented changes of government are designated by the expressions "military transition," "transitional authorities," or "transitional government," consistent with the institutional terminology of the countries concerned.')
cite('"The carrots are cooked for France. Simply look at what is happening everywhere in Africa and observe the discontent that is growing ever louder."')
add("Normal", "— Paul Elvira, Panafrican Média TV, 2 August 2022")

# ===== TABLE OF CONTENTS =====
doc.add_paragraph()
add("Normal", "TABLE OF CONTENTS", bold=True)
toc_entries = [
    "FOREWORD — Method and Analytical Rigour",
    "PROLOGUE — The Villa in Niamey",
    "INTRODUCTION — Why the AES Changes Everything",
    "",
    "PART I — WHAT FRANCE ERASED",
    "  Chapter 1 — Pre-colonial African Empires",
    "  Chapter 2 — Colonial Conquest and Resistance",
    "  Chapter 3 — 1960: Independence Confiscated",
    "",
    "PART II — THE EMPIRE OF LIES",
    "  Chapter 4 — The Camouflaged Colonial Pact",
    "  Chapter 4b — The Pillage Chain: Elf, the Briefcases and the Courts",
    "  Chapter 5 — The Extractive Machine: CFA, Uranium, Gold, Oil",
    "  Chapter 6 — Official Development Aid: A Documented Swindle",
    "  Chapter 7 — Barkhane, or War as After-Sales Service",
    "  Chapter 8 — The Language of Domination",
    "",
    "PART III — WHAT FRANCE ADMITS IN PRIVATE",
    "  Chapter 9 — French Institutional Admissions",
    "  Chapter 10 — The Doctrine of Propaganda: Anne-Sophie Avé's Confession",
    "  Chapter 11 — Alain Juillet and the Diagnosis of Decline",
    "",
    "PART IV — THE THREE CROWNS OF BETRAYAL",
    "  Chapter 12 — ECOWAS as an Instrument",
    "  Chapter 13 — The Comprador Elites",
    "  Chapter 14 — The Multi-Front Information War",
    "",
    "PART V — THE SONS OF LIPTAKO-GOURMA",
    "  Chapter 15 — The Manufacture of Terrorism in the Sahel",
    "  Chapter 16 — Mali: The First Rupture",
    "  Chapter 17 — Burkina Faso: The MPSR and the Traoré Doctrine",
    "  Chapter 18 — Niger: The CNSP and the Final Lock",
    "  Chapter 19 — The Liptako-Gourma Charter: A Founding Act",
    "",
    "PART VI — THE GEOPOLITICS OF RUPTURE",
    "  Chapter 20 — Chad: Mahamat Déby between Two Fires",
    "  Chapter 21 — Algeria: An Ambiguous Mediator",
    "  Chapter 22 — Russia, China, Turkey: Partners or New Masters?",
    "  Chapter 23 — The United States Facing the Recomposition",
    "  Chapter 24 — Mauritania: The Silent Neighbour",
    "",
    "PART VII — THE PROXY WAR",
    "  Chapter 25 — Paris's Ghost Army",
    "  Chapter 25b — Intelligence as a Weapon of War: Spies, PMCs and Secret War in Africa",
    "  Chapter 26 — Sadio Camara: From Architect to Target",
    "  Chapter 27 — The Attacks of 25 April 2026",
    "  Chapter 28 — The AES Response and Total Isolation",
    "",
    "PART VIII — THE AES'S INTERNAL CHALLENGES",
    "  Chapter 29 — The Persistent Jihadist Threat",
    "  Chapter 30 — Intra-Sahelian Fractures",
    "  Chapter 31 — The War Economy and Sanctions",
    "  Chapter 32 — The Democratic Question",
    "",
    "PART IX — THE SOVEREIGN HORIZON",
    "  Chapter 33 — Currency: Breaking the CFA Chain",
    "  Chapter 34 — The Sahelian Federal Army",
    "  Chapter 35 — The Diaspora as a Strategic Force",
    "  Chapter 36 — Sankara Was Right",
    "  Chapter 37 — France-Africa 2.0: The Recomposition of Domination",
    "  Chapter 38 — What the AES Must Achieve to Survive",
    "  Chapter 39 — Senegal Under Faye: Sovereignism through the Ballot Box",
    "",
    "EPILOGUE",
    "  Chapter 40 — Arrogance as Doctrine: Western Contempt for Africa",
    "  Chapter 41 — Anatomy of a Fear: What the West Really Dreads",
]
for entry in toc_entries:
    if entry == "":
        doc.add_paragraph()
    else:
        add("Normal", entry)

sep()

# ===== PROLOGUE =====
add("Normal", "PROLOGUE — The Villa in Niamey", bold=True)
add("Normal", "Five words. A whiteboard. A villa in Niamey.")
add("Normal", "Peace, we can prevent it.")
add("Normal", 'Those who wrote it are not philosophers. They are strategists. Their stated mission: to maintain instability in order to maintain access. To maintain access in order to maintain extraction. The extraction of uranium. Of gold. Of oil. Of rare earths. What the strategists do not say publicly, Jacques Chirac had said plainly: "The essential part of France\'s wealth comes from the exploitation of Africa."')
add("Normal", "One must go back. In 1900, the French Parliament passed the financial autonomy law of the colonies: henceforth, colonised populations would themselves finance the salaries of their occupiers, the police, the roads, the schools built for the colonists. In Algeria in 1909, 90% of the indigenous population paid 70% of direct taxes, while the colonists were largely exempt. To pay the poll tax, one needed CFA francs. To obtain CFA francs, one had to sell one's harvest. Otherwise: prison or forced labour. This is how the CFA franc was born: not as a fair means of exchange, but as an instrument of fiscal extraction. In 1960, at the time of independence, the debts contracted by colonial regimes were transferred to the young states. The Belgian Congo inherited the debts contracted by Belgium in the course of its exploitation. On that day, Congo had 16 university graduates for 14 million inhabitants. Not a single doctor. Not a single engineer. This is not poverty. It is organised pillage followed by an invoice. Legal doctrine calls this an 'odious debt.' Alexandre Sack, 1927: debts contracted to colonise and subjugate a population are not borne by the peoples who were their victims. In 1993, the first Pan-African Conference on Reparations in Abuja stated it clearly: Africa is a creditor, not a debtor.")
add("Normal", "This book begins in that villa in Niamey because that phrase is not a mistake. It is a key. It reveals that peace in the Sahel has always been instrumentalised. Barkhane did not fail. It did what it was there to do: maintain managed disorder. Niger closed the villa. It expelled both the French and American armies in the same year, without a single drop of blood. And the sky did not fall.")
add("Normal", "This book is not a pamphlet. It is not a hagiography. It is an analysis. It draws on adversarial sources — RTL, SWP Berlin, the French parliamentary commission, the UN (United Nations), ACLED — as much as on Pan-Africanist sources. When French institutional sources and African heads of state say the same thing, it becomes a truth that even their adversaries can no longer deny.")
add("Normal", "The peace of cemeteries has been imposed for too long. Just peace remains to be built. Justice cannot be avoided. Dignity cannot. Freedom, never.")

doc.add_paragraph()

# ===== INTRODUCTION =====
add("Normal", "INTRODUCTION — Why the AES Changes Everything", bold=True)
add("Normal", "On 16 September 2023, three African heads of state signed a document in Bamako. None of them had been elected in the classical sense of the term. All three came to power by arms. And all three had just created something that had not existed since independence: a sovereign, armed, explicitly anti-neocolonial bloc at the heart of French-speaking West Africa.")
add("Normal", 'The Western press covered the event with the condescending detachment it reserves for "African instabilities." These same analysts had not seen Brexit coming. They had not seen Trump coming. They had not seen the fall of the Berlin Wall coming. They never see what is coming from below, because they never look below.')
add("Normal", "This book takes the opposite wager. It takes the AES seriously. Not because it is perfect — it is not. Not because its leaders are model democrats — they are not yet. But because it represents something that had not existed since independence: the organised, institutional, militarily credible refusal of French and Western tutelage.")
add("Normal", "To understand what the AES represents, one must understand what it breaks with. And to understand what it breaks with, one must trace back the thread of sixty years of constructed dependency, plundered resources, and leaders installed and overthrown according to the interests of Paris. That is the purpose of this book.")
add("Normal", "The demonstration rests on a simple principle: when the same facts are confirmed by both Pan-Africanist sources and adversarial French, institutional, or academic sources, those facts are no longer theses. They become self-evident. This book is built on these convergences.")
cite('"We cannot allow the history of Africa to be written by those who pillaged it."')
add("Normal", "— General Abdourahamane Tiani, CNSP Niger, August 2023")
sep()

# ===== PART I =====
add("Normal", "PART I", bold=True)
add("Heading 1", "WHAT FRANCE ERASED")
add("Normal", "Long memory, African civilisations, colonial conquest")

add("Heading 2", "Chapter 1 — Pre-Colonial African Empires")
add("Normal", 'There is a founding lie in colonial ideology. That lie is called the "civilising mission." It postulates that African peoples had no history, no political organisation, no intellectual production before the arrival of Europeans. This lie is refuted by the facts. It is also functional: without it, colonisation cannot be justified.')
add("Normal", "The Ghana Empire — Wagadou — controlled the trans-Saharan gold and salt trade routes from the 4th to the 11th century. Its sovereigns taxed the caravans crossing their territory — a sophisticated customs system several centuries before the modern European state existed. The Mali Empire, founded by Sundiata Keita after the Battle of Kirina (1235), reached its apogee under Mansa Musa (1312–1337). His pilgrimage to Mecca in 1324 distributed so much gold that the world price of the metal collapsed for twenty years. Europe had not yet emerged from the Black Death. The Songhai Empire incorporated into its trajectory the peoples of present-day Burkina Faso. Sonni Ali Ber, its warrior sovereign, died in 1492 while returning from an expedition against the Mossi — the major ethnic group of present-day Burkina Faso. The historical continuity is there: the peoples fighting together within the AES in 2024–2026 share a history of interactions, conflicts and alliances that precedes the arrival of French colonisation by five centuries.")
add("Normal", "The University of Sankoré in Timbuktu welcomed up to 25,000 students in the 15th century. Oxford did not yet exist in its current form. The texts preserved in Timbuktu — several hundred thousand manuscripts — cover medicine, mathematics, philosophy, and Islamic law. The Charter of Mandé — Kouroukan Fouga, 1222 — is considered one of the earliest declarations of human rights in history: it proclaims the sanctity of human life, equality for all, and the abolition of enslavement through reduction.")
add("Normal", "Herodotus, the father of history in the Western tradition itself, described the Egyptians as 'dark-skinned with curly hair.' Cheikh Anta Diop built on this foundation a convergent demonstration: melanoderm, osteological, linguistic, and mythological data. Africa is the cradle of human civilisation. The erasure of these origins from dominant historiography is not an academic accident. It is functional to domination: one cannot justify 'civilising' a people whom one knows has already been at the summit.")

add("Heading 2", "Chapter 2 — Colonial Conquest and Resistance")
add("Normal", 'The Congress of Berlin (1884–1885) is a surgical operation performed on the African body. Fourteen European powers gathered and drew borders on maps that most of the diplomats had never seen the territories of. André Chassaigne, a French deputy, stated at the National Assembly podium: "They do not look at the communal spaces that exist. They divide families, clans, communities. Which still has consequences to this day."')
add("Normal", "These borders ignored pre-existing ethnic, linguistic and political realities. This cartographic surgery would produce a hundred and fifty years of conflicts that the same powers would present as proof of Africa's incapacity for self-governance. The lie is complete, circular, self-referential. One creates the problem, presents it as proof of the natural inequality of peoples, and imposes oneself as the solution to the problem one has created.")
add("Normal", "Barthélemy Boganda, founder of the Central African Republic, who died in a suspected plane crash in 1959, and Kwame Nkrumah warned against this trap: micro-national, non-viable states, condemned to permanent dependency, individually incapable of carrying weight in an international system built against them. Berlin 1884–1885 had manufactured the condition of impossible sovereignty.")
add("Normal", "But Africa resisted. Samory Touré (c. 1830–1900) founded the Wassoulou Empire and waged a sixteen-year armed resistance against France. He perfected his tactics through successive confrontations, forcing French generals into costly expeditions in men and materiel. Finally captured in 1898 by General Gouraud, he was deported to Gabon where he died. Babemba Traoré, king of Kénédougou, committed suicide in 1898 rather than surrender. Rabah Fadlallah conquered the Bornu Sultanate and resisted French penetration until 1900 — defeated and killed at the Battle of Kousséri. El Hadj Oumar Tall, founder of the Toucouleur theocracy covering Mali, Guinea and Senegal, led 19th-century Islamic resistance to French colonisation before being cornered in a cave in northern Mali in 1864. These names are absent from post-colonial textbooks. They are present in the speeches of Captain Ibrahim Traoré and Assimi Goïta. The connection is doctrinal, not sentimental.")
cite('"Azawad is a political fabrication."')
add("Normal", "— André Bourgeot, CNRS researcher, Sahel specialist")

add("Heading 2", "Chapter 3 — 1960: Independence Confiscated")
add("Normal", "1960 is the year of Africa. Seventeen African countries become independent. In the streets of Bamako, Ouagadougou, Niamey, crowds celebrate. The flags go up. National anthems are sung for the first time. History begins, one believes.")
add("Normal", "But in the offices of Paris, another history is being written. Jacques Foccart, the grey eminence of the Élysée for African affairs, organises the reality of what will follow. The secret cooperation agreements are signed. The CFA franc is maintained. The military bases remain. Elites trained in Paris take power. Independence is formal. Dependency is real. Françafrique is born in the euphoria of independence, invisible, buried in the sub-clauses of treaties that no one will read. The academic biography of Frédéric Turpin (CNRS, 2015) documents the concrete mechanisms of this architecture. Foccart created Safiex in 1944 — an Antilles-African import-export company whose commercial activities deliberately overlap with his political functions alongside de Gaulle. Commerce and intelligence are never separated. De Gaulle formulated the institutional objective in 1966: 'La francophonie will one day take over from colonisation.' The phrase is not a metaphor. It is a programme. Four years later, Pompidou created the ACCT (ancestor of the OIF) to use the 'linguistic cement' to fill the cracks of the Franco-African bloc — while attracting former Belgian colonies: Burundi, Rwanda, Zaire. The Attali report documents the final irony: la Francophonie could reach 770 million speakers by 2060, of whom 85% will be Africans. A 'Francophonie without France' — developing autonomously from the former metropole. The domination tool conceived in 1883 could become the emancipation tool of those it was meant to dominate.")
add("Normal", 'A single country said no. The Guinea of Ahmed Sékou Touré voted no in de Gaulle\'s referendum in 1958, two years before the others. De Gaulle had promised that countries voting no would receive immediate independence but lose all French support. Sékou Touré replied with a phrase that still resonates today:')
cite('"We prefer poverty in freedom to opulence in slavery."')
add("Normal", "— Ahmed Sékou Touré, before de Gaulle, 25 September 1958")
add("Normal", "The French response was immediate and total: French civil servants took or destroyed everything on departure. The archives. The office equipment. The telephones. The hospital medicines. The light bulbs. Everything. The objective was explicit: to punish Guinea and show the other colonies what awaited them. Sixty-five years later, Macron's France applies exactly the same mechanisms to Tiani's Niger: suspension of aid, pressure from financial institutions, military threat via the Economic Community of West African States (ECOWAS). Same doctrine. Same logic. Same conviction that African peoples can be brought back to reality by hunger.")
add("Normal", 'Nathalie Yamb formulates it in simple terms: the independence of the 1960s is not genuine independence. It is "cheap" independence, she writes. Power is transferred to elites trained in Paris, "bleached independentists" who maintain in place the structures of dependency. And the cycle restarts every thirty years. The 1960s produce confiscated independence. The 1990s produce confiscated multipartyism. The 2020s produce sovereignism. If the structures do not change, in thirty years it will all have to start again.')
sep()

# ===== PART II =====
add("Normal", "PART II", bold=True)
add("Heading 1", "THE EMPIRE OF LIES")
add("Normal", "Anatomy of Françafrique: structures, mechanisms, balance sheets")

add("Heading 2", "Chapter 4 — The Camouflaged Colonial Pact")
add("Normal", 'On 26 December 1945, France created the CFA franc. The acronym then stood for "Colonies Françaises d\'Afrique" (French Colonies of Africa). After independence, France discreetly changed the designation: "Communauté Financière Africaine" (African Financial Community) in West Africa, "Coopération Financière en Afrique Centrale" (Financial Cooperation in Central Africa) for the CEMAC zone. The initials remain the same. So does the reality.')
add("Normal", "From 1945 to 1975, 100% of African foreign exchange reserves were deposited at the French Treasury. Since 1975, this rate has been 50%. [Source: Fanny Pigeaud, Mediapart] This mechanism means that African countries in the franc zone finance, with their own reserves, the French budget. Cheikh Anta Diop's metaphor is accurate: it is rent that dares not speak its name. The sequence is not accidental. Tiani names it clearly in his 12 February 2024 speech on RTN: the La Baule speech (1990) imposed multipartyism — result: political fragmentation, more than 200 parties in countries of fewer than 100 million inhabitants. Four years later, 1994: devaluation of the CFA franc. Destruction of 100% of purchasing power overnight. Political fragmentation + economic strangulation: a coordinated sequence, not a coincidence. Jacques Chirac had said it himself — Franklin Nyamsi documented it: 'We must acknowledge that a large part of the money in our pockets comes precisely from the exploitation of Africa over centuries. We must have common sense, the justice to return to Africans what was taken from them.' France knew. It continued.")
add("Normal", "The pyramid of domination described by Dr Yamb Ntimba structures this system into five levels. The military level guarantees the coherence of the whole. The economic level ensures capture. The informational level manufactures consent. The cultural and media level structures imaginaries. The ontological level, the deepest, installs in African minds themselves the conviction of African inferiority.")
cite('"Françafrique cannot die because Françafrique is the very expression of the hideous face of French imperialism. To kill Françafrique is simply to kill France."')
add("Normal", "— Paul Elvira, Panafrican Média TV, 2 August 2022")
add("Normal", "This system has evidence. Evidence from the adversarial camp itself. Jacques Chirac, President of the French Republic, admitted plainly: 'The essential part of France's wealth comes from the exploitation of Africa for centuries.' Nicolas Sarkozy, convicted and wearing an electronic bracelet, testified before Parliament: 'The most brutal, the most savage, the most violent civilisation that exists and has ever existed is European civilisation.' When former French presidents themselves say what Pan-Africanists have been saying for decades, the debate is closed.")

add("Heading 2", "Chapter 4b — The Pillage Chain: Elf, the Briefcases and the Courts")
add("Normal", "The architecture of pillage is best described through its actors.")
add("Normal", 'Loïk Le Floch-Prigent, former CEO of Elf, exposes it himself: he bought African oil at 3–4 dollars a barrel and resold it at 80 dollars. The 76-dollar difference went to "a certain number of people." Those people would finance French electoral campaigns.')
add("Normal", 'Pascal Lissouba, former President of the Republic of Congo (1992–1997), testified for posterity: "We knew nothing of what was happening and we did not even know the quantity of oil leaving our country." A former African head of state, recognised by the UN, states that his country did not know its own oil production. The wells were in the ocean. The vessels were Elf\'s. The figures were given by Elf. And the Congolese authorities "had no means of going to check."')
add("Normal", 'Mamadou Koulibaly, former Finance Minister of Côte d\'Ivoire, describes the same reality from Abidjan: "The tankers come to fill up and then leave, and it is they who tell us, well, we took 10 barrels, 20 barrels, and we account for that in the budget." Two former African finance ministers, two different countries, the same story. Meanwhile, Jean-Bedel Bokassa, the man France had installed and crowned in power in the Central African Republic (CAR), revealed that "since 1966 until today, neither France nor Switzerland has paid a single franc" for the extracted uranium.')
cite('"We are dealing with oil roughly at 3–4 dollars coming out and then we sell it at 80. All that money in between goes to a certain number of people."')
add("Normal", "— Loïk Le Floch-Prigent, former CEO of Elf")
cite('"We knew nothing of what was happening and we did not even know the quantity of oil leaving our country."')
add("Normal", "— Pascal Lissouba, former President of the Republic of Congo, documentary 2001")
add("Normal", "The machine refuels itself. Robert Bourgi, a Franco-Lebanese lawyer and briefcase carrier for the Élysée, testified: he would visit Omar Bongo, Blaise Compaoré, Denis Sassou, Mobutu, with a message from Paris: contribute to the campaign of 'your friend.' 'It never came down below a million dollars.' In 1995: at least 100 million dollars for the Chirac campaign. Laurent Gbagbo, upon his release from the International Criminal Court (ICC), admitted having paid 3 million euros at the request of Chirac and Villepin. Charles Pasqua, former Interior Minister, publicly admitted in Le Parisien that Balladur wanted to 'cut off the socialists' funds' by replacing Le Floch-Prigent at the head of Elf.")
add("Normal", "On 13 April 2026, a French court sentenced the former executives of Lafarge to 6 and 5 years in prison for financing terrorism in Syria. France Inter, on 26 May 2023, revealed that the Castel group is in the sights of the anti-terrorism prosecutor's office for financing armed militias in the CAR. Two French multinationals, two African countries, two judicial proceedings. The financing of African armed groups by French companies is no longer a Pan-Africanist thesis. It is a judicial fact.")
sep()

add("Heading 2", "Chapter 5 — The Extractive Machine: CFA, Uranium, Gold, Oil")
cite('"Currency is the mother of sovereignties. You cannot be sovereign if you do not have your own currency."')
add("Normal", "— Dr Douma Jean-René, Panafrican Média TV, 10 May 2026")
add("Normal", "Arlit, Niger. 1971. Cogema — future Areva, future Orano — establishes its extraction wells. From that date until the 2023 transition, Nigerien uranium is extracted, transported, enriched and sold by French companies. Niger receives the state royalty. France keeps the margin.")
add("Normal", "According to official figures from the French High Committee for Nuclear Transparency: Niger represented 35% of French imports of concentrated uranium in 2020 and 34% in 2021. Without Niger, France loses a decisive share of its energy independence — the very independence of which it boasts when confronting Germany's dependence on Russian gas. This is the absolute paradox: France is 'independent' thanks to a country whose dependence it systematically maintains.")
add("Normal", "The Burkinabè extractive model reproduces the systemic logic documented by Porcher on the Congo. The historic share of the Burkinabè state in revenues from its own gold mines was 10% or less, versus the Western multinationals. The same ratio as the Congo-Brazzaville (Total 60%, ENI 30%, State 10%). This is not a regional coincidence. It is a systemic contractual model imposed continent by continent. It is precisely against this model that Traoré engaged in aggressive renegotiation of mining contracts — threatening nationalisation of recalcitrant companies. Nathalie Yamb explains why France 'screamed, sent terrorists, violated the Vienna Convention' when Niger asked Orano to leave, even as French officials claimed this uranium represented only 20% of their supply. The answer lies in the commercial model: in Niger, Orano bought at discounted prices. In Kazakhstan, Australia, Canada, market price must be paid. The margin disappears.")
add("Normal", "The post-transition data quantifies the rupture. Nyamsi, in December 2025, published Niger's direct revenues since the takeover: uranium managed directly — approximately 300 million dollars. Oil, cash agreement with China — approximately 500 million dollars. Total: nearly 800 million dollars of new annual revenues for the Nigerien state. 'This is unprecedented in the history of a Nigerien state and indeed of any state in French-speaking Africa stemming from French colonialism.' [Franklin Nyamsi, December 2025]")
add("Normal", "In Mali, gold represents more than 70% of exports. In 2023, the transition renegotiated contracts with Barrick Gold: higher royalties, 35% mandatory local content. Canada threatened diplomatic reprisals. Mali held its position. In Congo-Brazzaville: Total captured 60% of oil revenues, ENI 30%, leaving 10% to the country. Thomas Porcher, professor at PSB Paris, documents this figure. Mamadou Koulibaly, former President of the National Assembly of Côte d'Ivoire, confirms the same logic for his country.")
add("Normal", "And André Chassaigne, a French deputy, said it on the floor of the National Assembly: 'Tentacular private firms exploiting today 80% of Africa's gigantic mineral deposits, whose profits are repatriated to tax havens.' A French deputy. In plenary session. In December 2013.")

add("Heading 2", "Chapter 6 — Official Development Aid: A Documented Swindle")
add("Normal", "Official development aid is the most sophisticated instrument of French domination in Africa. Not because it is important — it is relatively modest. But because it is presented as generosity while serving as a lever of political control.")
add("Normal", "Nathalie Yamb describes it clearly: ODA is primarily composed of loans, not grants. Loans conditioned on market opening, on maintaining the CFA franc, on favourable votes in international institutions. Migrant remittances from Africans to their home countries far exceed the amounts of official aid, according to the World Bank's own data. The African diaspora finances its countries more than foreign donors do. In 1960, debts contracted by colonial regimes were transferred to the newly independent states. The Belgian Congo inherited the debts contracted by Belgium in the course of its exploitation. On the day of independence, Congo had 16 university graduates for 14 million inhabitants. Not a single doctor, not a single engineer, not a single agronomist. This is not poverty. It is organised pillage followed by an invoice. Legal doctrine calls this an 'odious debt.' Alexandre Sack, 1927: debts contracted to colonise and subjugate a population are not borne by the peoples who were their victims. In 1993, the first Pan-African Conference on Reparations in Abuja (Nigeria) formulated the Abuja Proclamation: cancellation of colonial debts, financial reparations, restitution of stolen cultural property, increased African representation in international bodies. Thirty years later, European countries are timidly beginning to return objects.")
cite('"Official development aid is a swindle that primarily serves to ease the conscience of donors who know very well the twisted use our heads of state make of this money."')
add("Normal", "— Nathalie Yamb, Afrique Résurrection chronicle, November 2022")
add("Normal", "The CAR illustrates the mechanism in its crudest form. International budgetary aid represents 46 to 69 billion CFA francs depending on the year — or 46% of the Central African national budget. When France suspended its aid in 2021 to force the departure of Wagner, it folded its arms and waited. It said so explicitly: three conditions for resumption. The first: cessation of 'disinformation.' The second: cessation of 'harassment of French companies.' The third: Wagner's departure. At the first condition, France defined 'disinformation' as any information unfavourable to its interests.")
add("Normal", "The Burkinabè response to sanctions was different. On 25 May 2025, Captain Ibrahim Traoré, President of Burkina Faso, handed over to farmers equipment worth 104 billion CFA francs: 1,102 motorised cultivators, 608 tractors, 485 motorised pumps, 935 floating cages, 66,952,895 doses of veterinary medicines. This after the total suspension of French aid in August 2024.")

add("Heading 2", "Chapter 7 — Barkhane, or War as After-Sales Service")
add("Normal", "January 2013: Operation Serval. August 2014: Barkhane. 5 million km². Up to 5,500 men deployed. Approximately 1 billion euros per year — or 1.3 billion CFA francs daily. Cumulative budget 2014–2022: more than 5 billion euros. [French Court of Auditors, 2020] Result: the number of jihadist attacks tripled between 2014 and 2021. [ACLED, 2022] Traoré's formula is surgical: 'Nine years — France did not give a single helicopter to Mali. Today, you see the number of aircraft we have been able to acquire in less than two years from our own resources, at a time when the country is under sanctions and embargo.' The equation speaks for itself.")
add("Normal", "In 2014, the French army had the opportunity to eliminate Iyad Ag Ghali in Gao. François Hollande stopped the operation 'so as not to upset Algeria.' Ag Ghali is today the emir of the JNIM (Jama'at Nusrat al-Islam wal-Muslimin), responsible for the blockade of Bamako in 2025 and the public assassination of Mariam Cissé. The 2014 decision has consequences.")
add("Normal", "The destruction of Libya in 2011 by the NATO intervention led by Sarkozy and Cameron released into the Sahel arsenals of tens of thousands of tonnes of weapons. André Chassaigne documents it in the National Assembly: in 2007, French paratroopers jumped on Birao, in northern CAR. It is in that Muslim north that the Séléka offensive was born five years later. France creates the conditions for chaos, then presents the security bill.")
cite('"France destroyed Libya, dispersed its arsenals throughout the Sahel, and then presented the security bill to African countries in the form of a permanent military presence."')
add("Normal", "— Transitional authorities of Mali, official communiqué, 2022")
add("Normal", "These figures are the verdict. Five billion euros. Nine years. The threat triples. There are two possible explanations. Either the French armies are incompetent, which French propaganda denies. Or the mission was not what we were told. The second hypothesis has evidence.")

add("Heading 2", "Chapter 8 — The Language of Domination")
add("Normal", "All domination needs a lexicon. The lexicon of French domination in Africa is sophisticated: it names things opposite to what they are. This inversion is not a linguistic accident. It is functional: it allows domination to be presented as aid, exploitation as partnership, and resistance as ingratitude.")
cite('"We are reproached for having overthrown an elected president. Nobody has asked us what that elected president did with the sovereignty of our country."')
add("Normal", "— Assimi Goïta, President of the Malian transition, 2022")
add("Normal", "Causal inversion is the central mechanism of propaganda: presenting the Sahelian transitions as products of Russian manipulation, whereas the chronology is the reverse. The first coup (Mali, August 2020) preceded the massive arrival of Wagner. The break with Paris came first. The diversification towards Russia came after. Inverting this sequence is lying. But that is Anne-Sophie Avé's profession.")
sep()

# ===== PART III =====
add("Normal", "PART III", bold=True)
add("Heading 1", "WHAT FRANCE ADMITS IN PRIVATE")
add("Normal", "Institutional admissions, propaganda, diagnosis of decline")

add("Heading 2", "Chapter 9 — French Institutional Admissions")
add("Normal", "There is a paradox in France's African reality: the most damning admissions come from French sources themselves. Not from Pan-Africanist pamphleteers, not from diaspora activists, but from parliamentarians, generals, diplomats, and former presidents. These admissions exist. They were made in official institutions. They have simply never been gathered in a single volume.")
add("Normal", 'The French parliamentary commission on France-Africa relations wrote in black and white: "We need Africa more than Africa needs us." It qualified France\'s African policy as "domination" and recommended a "difficult transition" towards "a phase of cooperation and benevolence." A democratic parliament officially qualifies its own African policy as domination. That word is in the report. Printed. Archived. Accessible.')
add("Normal", "In September 2024, behind closed doors before the National Assembly's defence commission, former Chief of the Defence Staff Thierry Burkhard declared that France has no allied camp in Mali and cannot choose between the JNIM terrorists and Wagner mercenaries — placing them back to back. When a French military chief places the Malian Armed Forces (FAMa) in the same camp as the JNIM, he says something essential about the failure of French policy. And about the French definition of an African 'friend': someone who obeys.")
cite('"We need Africa more than Africa needs us."')
add("Normal", "— French parliamentary commission, report on France-Africa relations")
cite('"This is the 50th French intervention in sub-Saharan Africa since the independence of 50 years ago."')
add("Normal", "— André Chassaigne, GDR/PCF deputy, French National Assembly, debate on Operation Sangaris, December 2013")
cite('"Dictatorships that prefer to defend the interests of tentacular private firms exploiting today 80% of Africa\'s gigantic mineral deposits, whose profits are repatriated to tax havens."')
add("Normal", "— André Chassaigne, ibid.")
add("Normal", 'Chassaigne goes further: he designates the CAR as "an aircraft carrier at the centre of Africa, used in numerous military interventions in the region." He recalls that France supported Bokassa, then Dacko, then Kolingba, then Patassé, then Bozizé — a game of musical chairs orchestrated from Paris. His conclusion: "France bears a historical responsibility in the Central African tragedy. It is therefore not the most qualified to intervene." A French deputy is speaking.')

add("Heading 2", "Chapter 10 — The Doctrine of Propaganda: Anne-Sophie Avé's Confession")
add("Normal", "Anne-Sophie Avé: former French Ambassador to Mali (2017–2020), then Director for Sub-Saharan Africa at the Quai d'Orsay. She represents the French diplomatic caste at its most sophisticated: no longer the Foccart networks of the 1960s, but the cognitive warfare of the 21st century. Her admission deserves to be quoted in full, slowly, because every word counts.")
cite('"Once you have given this positive narrative, once you make people doubt, you create a cognitive dissonance where people will say: \'I want to believe that France is bad. But what I see is that they built this motorway, that they brought electricity to this hospital. In fact, everything I see concretely is that France loves us and helps us.\'"')
add("Normal", "— Anne-Sophie Avé, former French Ambassador to Mali, Director for Africa at the Quai d'Orsay")
add("Normal", "Let us analyse this text. Avé does not say 'make our achievements known.' She says 'make people doubt.' She does not say 'communicate the truth.' She says 'create cognitive dissonance.' This document proves awareness of manipulation. Avé knows she is manipulating. She is proud of it. One can no longer plead French good faith when the architect of propaganda describes its functioning with satisfaction before an audience.")
add("Normal", "Propaganda does not stop at the major media. It invests community radio stations and local languages. It finances African 'influencers' — Macron admitted it himself in November 2022, in an interview on TV5 Monde: 'There are Africans paid by the Russians.' Implying: there are also some paid by others. In September 2025, a call for tenders was issued to African influencers to destabilise the AES informationally, according to General Tiani himself (speech of 13 November 2025).")
add("Normal", "The Avé doctrine is completed by the cyber school of the 43rd BIMA, which trains 'e-patrollers' specifically targeting Pan-Africanists. On 8 May 2026, Niger suspended ten French media outlets. Mali had already expelled RFI and France 24 in March 2022. Burkina Faso followed in December 2022. This is not censorship. It is the response to a war declared by an ambassador in a public speech.")

add("Heading 2", "Chapter 11 — Alain Juillet and the Diagnosis of Decline")
add("Normal", "Alain Juillet is not a Pan-Africanist. He is the former Director of Intelligence of the DGSE (Direction Générale de la Sécurité Extérieure, 2002–2003), then Senior Adviser for Economic Intelligence to the French Prime Minister. He represents the summit of the French security establishment. His diagnosis is therefore irrefutable in terms of sourcing.")
add("Normal", "Juillet is unsparing: France is losing ground 'everywhere' in French-speaking Africa. The problem 'goes beyond the Sahel.' Even in traditionally allied countries such as Côte d'Ivoire and Senegal, the situation is 'precarious.' Juillet documents the shift of Gabon and Togo towards the British Commonwealth. He notes Russian pressure on Biya's Cameroon. He analyses Guinea: France supported Alpha Condé's third term against the will of the people, which directly produced the coup of Mamadi Doumbouya. France, by seeking to maintain its allies in power against the peoples, accelerated its own exclusion.")
add("Normal", "Juillet's diagnosis joins that of Fridolin Ngoulou from the Central African field: sixty years of cooperation, and the CAR remains the last among French-speaking countries in the world. France has a structural problem in Africa. That problem has a name: it confused Africa with a property, and Africans with subjects.")

# ===== PART IV =====
add("Normal", "PART IV", bold=True)
add("Heading 1", "THE THREE CROWNS OF BETRAYAL")
add("Normal", "ECOWAS, comprador elite, information war")

add("Heading 2", "Chapter 12 — ECOWAS as an Instrument")
add("Normal", "On 30 July 2023, the extraordinary ECOWAS summit in Abuja imposed sanctions on Niger and threatened military intervention. Celebrated as the defence of democracy. Seriously analysed, it is a violation of several international texts and of the ECOWAS texts themselves.")
add("Normal", "Independent African jurists are unequivocal. The African Union (AU) Charter gives ECOWAS no mandate to use force against a member state. The UN Charter (Article 53-1) reserves that mandate solely to the Security Council. The ECOWAS Protocol of 2001 itself, in Article 45, renders the decision procedurally unlawful. To crown the irregularity, Chad — which is not an ECOWAS member — was invited to the Abuja summit. And the Nigerian Senate voted against military intervention, blocking its own president Tinubu.")
cite('"ECOWAS has never sanctioned a state for allowing foreign military bases on its soil. It sanctions those who close them."')
add("Normal", "— General Abdourahamane Tiani, President of the Republic of Niger, 2024")
add("Normal", 'The most damning revelation about ECOWAS comes from General Tiani himself, in his RTN interview of 12 February 2024: "The La Baule speech of 1990 was in reality a balkanisation plan. Macron himself declared that \'Niger belongs to France.\'" ECOWAS is not an African regional organisation. It is an instrument of external governance in disguise.')
sep()

add("Heading 2", "Chapter 13 — The Comprador Elites")
add("Normal", "The word 'comprador' comes from Portuguese: it designates the intermediary merchant who facilitates trade between the coloniser and the population. In post-colonial Africa, the comprador elite is the elite that facilitates the maintenance of dependency. It speaks sovereignty in public. It signs servitude agreements in private. It sends its children to Paris. It places its money in Switzerland.")
add("Normal", 'Mohamed Bazoum perfectly illustrates the profile. Overthrown by the Nigerien CNSP on 26 July 2023, he appealed for help from Washington: "Foreign aid constitutes 40% of the national budget, but it will not be delivered if the coup succeeds." [Washington Post, 6 August 2023] He does not appeal to his own people. He appeals to his external masters. He uses the threat of aid as a tool of political control against his own people. This man represents exactly what the AES defines as the problem.')
cite('"Foreign aid constitutes 40% of the national budget, but it will not be delivered if the coup succeeds."')
add("Normal", "— Mohamed Bazoum, former President of Niger, Washington Post, 6 August 2023")
add("Normal", "Nathalie Yamb, at the grand debate in Niamey, provides a more anthropological image: 'They have the republican minimum at home. If a billionaire comes with millions of dollars to see a French political leader, telling him he needs to stage a coup, arm young men to achieve secession, he will be sent packing. Here, some accept. That is what we call corruption. Corruption implies there is a corruptor and one who is corruptible.' The task of the AES is to build this republican minimum in the Sahel.")
add("Normal", "Tatsinda names the Western media with a formula that enters the corpus: the 'crow sellers' — those who sell misfortune, manufacture fake news and systematically discredit African sovereignty. Banda Kani names the 'revenge of the dunces': the neocolonial elites now qualify as 'incapable' the patriots attempting to rebuild. He also denounces the 'colonised complex': certain Africans validate Western contempt towards their own sovereign electoral processes. The decolonisation of minds begins by refusing to let the adversary be the arbiter of one's legitimacy.")

add("Heading 2", "Chapter 14 — The Multi-Front Information War")
add("Normal", "The war in the Sahel is won or lost first in people's minds. The AES authorities have understood this. So have their adversaries. The information war is multidirectional: it comes from Paris, Moscow, Abu Dhabi, Kyiv, and sometimes from Bamako itself. Identifying the sources and vectors is a prerequisite for any serious analysis.")
add("Normal", "Vector 1: the French media")
add("Normal", "RFI, France 24, TV5 Monde, AFP. Expelled successively from Mali (March 2022), Burkina Faso (December 2022). On 8 May 2026, Niger suspended ten French media outlets: RFI, France 24, AFP, TV5 Monde, TF1 Info, Jeune Afrique, Mediapart, France-AfriqueMÉDIA, LSI Africa. The decision of Niger's High Authority for Communication (HAC, decision no. 2026.0058/P-HAC of 8 May 2026) also banned Al Arabiya at the same date, for broadcasting information 'liable to disturb public order.' Al Arabiya is broadcast from Dubai — confirmation of the UAE (United Arab Emirates) as an actor in the information war against the AES.")
add("Normal", "Vector 2: the digital war")
add("Normal", "The cyber school of the 43rd BIMA trains 'e-patrollers' with a precise objective: to criticise the Russian presence in Africa on social networks and to specifically target Pan-Africanists — with Kemi Séba at the top of the list. [Thomas Dietrich, 2024] Tiani, on 13 November 2025, confirmed the existence of a public call for tenders launched in September 2025 to recruit African influencers tasked with informationally destabilising the AES. 'It is done openly.' Two independent sources — a French investigative journalist and an African head of state — converge on the same mechanism. That is the definition of analytical proof. Dietrich formulates the closing diagnosis in one sentence: 'Françafrique is going to die. But it is still spitting some flames.' The flames are documented. So is the trajectory.")
add("Normal", "Vector 3: manipulation through imagery")
add("Normal", "Ibrahim Moustapha, Al Arabiya correspondent, illegally entered Malian territory and broadcast a report claiming a strategic city was under jihadist control. Mali's Foreign Ministry accused him of 'complicity with terrorist groups.' Jules Domche, from Vox Africa, highlighted a revealing paradox: it was the Western media that first announced the death of General Sadio Camara — even though they have had no correspondents in the Sahel for years. Who transmitted the information to them and in what timeframe?")
cite('"War is not only weapons, images, atrocities. It is also and above all a communications war. Because he who controls information controls strategy."')
add("Normal", "— Jules Domche, Vox Africa, May 2026")
add("Normal", "The central mechanism: causal inversion")
add("Normal", "The dominant narrative presents the Sahelian transitions as products of Russian manipulation. This narrative is refuted by chronology: the first coup (Mali, August 2020) preceded the massive arrival of Wagner. The break with Paris came first. Diversification towards Russia came after. Five years later, RTL France confirmed the proxy war from a French security source, revealing that former French legionnaires are working with the Ukrainian Military Intelligence (GUR) against Mali. Abdoulaye Maïga, labelled a 'conspiracy theorist' in 2021 for saying the same thing, was confirmed in 2026 by an official French source.")
sep()

# ===== PART V =====
add("Normal", "PART V", bold=True)
add("Heading 1", "THE SONS OF LIPTAKO-GOURMA")
add("Normal", "The construction of the AES, state by state")

add("Heading 2", "Chapter 15 — The Manufacture of Terrorism in the Sahel")
add("Normal", "Understanding Sahelian terrorism requires going back to the destruction of Libya. In 2011, the NATO intervention led by Sarkozy and Cameron pulverised the Libyan state. Gaddafi's arsenals — tens of thousands of tonnes of weapons: missiles, rocket launchers, automatic weapons, armoured vehicles — scattered throughout the Sahelo-Saharan belt. Armed Tuareg groups from northern Mali, some of whom had served in the Libyan army, returned home armed. The National Movement for the Liberation of Azawad (MNLA) was formed. In May 2012, it allied with Ansar al-Din to proclaim an independent Azawad. Timbuktu, Gao, Kidal fell.")
add("Normal", "'Azawad is a political fabrication.' Not a historical reality. A constructed and instrumentalised entity. The Tuareg exist. Azawad as the MNLA defines it is a political operation with external backers.")
add("Normal", "What Barkhane never did: allow the FAMa to occupy the north of Mali. Abdoulaye Maïga, Prime Minister of Mali, stated at the UN General Assembly in September 2021: 'Abandoned in mid-flight. France prohibited the FAMa from occupying the north. Takuba is an instrument of partition. Deliberate sanctuarisation of terrorists.' Five years later, RTL France confirmed the proxy war from a French security source. The conspiracy theorist of 2021 is the prophetic analyst of 2026.")
cite('"As long as terrorism is not cut off from its sponsors and supporters, then crushed, it will not come to the table. Any negotiation is defeatism."')
add("Normal", "— Abdoulaye Maïga, Prime Minister of Mali, Azalaï Hotel Bamako, 19 October 2024")
add("Normal", "The Sahelian corridors: the invisible infrastructure of war")
add("Normal", "The manufacture of terrorism is not merely ideological or financial. It is geographical. A cartography produced by the Telegram channel @RYBAR_AFRICA documents in May 2026 the trans-Saharan nomadic trails as routes used by armed groups in Mali. These visual data corroborate ACLED field analyses and the testimonies of Malian transitional authorities on the cross-border logistics of jihadist groups.")
add("Normal", "The cartography reveals three structural realities. First reality: the zones under anti-government control — northern and central Mali, the Mali-Niger corridor, Burkinabè fringes — correspond exactly to the zones that Barkhane had sanctuarised for ten years. Visual confirmation of Choguel Kokalla Maïga's 2021 UN diagnosis: France prohibited the FAMa from advancing. Second reality: the trans-Saharan nomadic trails traverse Algeria and Mauritania almost entirely, connecting the Malian jihadist control zones to Mediterranean rear bases. Third reality: these corridors predate colonisation. Berlin 1884–1885 drew borders. The desert routes, however, have never changed.")
sep()

add("Heading 2", "Chapter 16 — Mali: The First Rupture")
add("Normal", "18 August 2020. 4 a.m. Shots ring out at the Kati military base, 15 km from Bamako. Within hours, President Ibrahim Boubacar Keïta is arrested at his residence. Colonel Assimi Goïta takes command of the National Committee for the Salvation of the People. IBK announces his resignation on national television during the night.")
add("Normal", "In the streets of Bamako, crowds dance. This gap between the unanimous international condemnation — European Union, ECOWAS, France, United Nations — and the spontaneous popular celebration is the most significant political fact of 2020 in Africa. It will never be properly analysed by the mainstream media, which prefer to condemn the soldiers rather than question what IBK represented for those crowds.")
add("Normal", "The first transition did not stop in August 2020. On 24 May 2021, Goïta struck again. He overthrew transitional president Bah N'Daw and his Prime Minister Moctar Ouane, accused of wanting to marginalise the military in the new government. Goïta was sworn in as president of the transition. Choguel Kokalla Maïga, a figure of the M5-RFP movement that had driven popular protest against IBK, became Prime Minister. This is not an accident: the military transition draws on the civil legitimacy of the M5-RFP. The junction between popular protest and military rupture is institutionalised.")
add("Normal", "What Goïta represents goes beyond his person. He embodies the rupture of an African military generation trained on the front against terrorism, which watched its men die while French generals prohibited the FAMa from advancing northward. This generation has a simple reading of the situation: those supposed to help do not want the problem to be solved.")
add("Normal", "10 July 2022: 49 Ivorian special forces were captured at Bamako airport. They were disguised as students and electrical technicians. No mission orders. The MINUSMA confirmed that no rotation was planned. An intercepted conversation between President Ouattara and Boubou Cissé (17 February 2022): 'Within 2 weeks they will fall.' Sadio Camara identified as a priority target.")
add("Normal", "14 November 2023: fall of Kidal. The symbolic city, the MNLA stronghold since 2012, fell in less than 24 hours to the FAMa. What Barkhane had failed to achieve in ten years, the FAMa accomplished sixteen months after the expulsion of the French. The demonstration is complete.")
cite('"Mali is and will remain One and Indivisible."')
add("Normal", "— Assimi Goïta, following the fall of Kidal, 14 November 2023")

add("Heading 2", "Chapter 17 — Burkina Faso: The MPSR and the Traoré Doctrine")
add("Normal", "Two coups in eight months. January 2022: Lieutenant-Colonel Paul-Henri Sandaogo Damiba overthrew Roch Marc Christian Kaboré. September 2022: Captain Ibrahim Traoré overthrew Damiba. Each coup corrects and radicalises the preceding one. Damiba hesitates over the break with Paris. Traoré does not.")
add("Normal", "Captain Ibrahim Traoré, President of the Burkina Faso transition (MPSR), is the most radical embodiment of the Sahelian project. 35 years old at the time of taking power. Armoured corps officer, cited several times for bravery at the front against armed groups. His doctrine can be summarised in one phrase he pronounced in 2023: 'The imperialists decided that we must die. We decided to live. That is the entire debate.'")
add("Normal", "Traoré names the mechanism of internal weakening with a precision that goes beyond merely denouncing the foreign military presence: French military advisers are 'more dangerous than the bases.' Their mission was not to strengthen the Burkinabè Armed Forces (FAB). It was to dictate inappropriate training policies to keep the Burkinabè army in structural dependency. The military base is visible. The adviser is invisible. And it is the invisible who commands. Burkina Faso engaged the nationalisation of Total on its territory. It became the leading tomato producer in West Africa. Pan-Africanist works were translated into Mooré and distributed in villages to directly raise the political consciousness of rural populations. This is not propaganda. It is sovereignist popular education. Traoré refused 200 mosques financed by Saudi Arabia: 'Give us schools, hospitals and jobs.' He expelled the French forces. He launched general mobilisation, establishing civic national service for defence.")
cite('"The imperialists decided that we must die. We decided to live. That is the entire debate."')
add("Normal", "— Captain Ibrahim Traoré, President of Burkina Faso, 2023")
cite('"If he is not an atheist, every time he wakes up and prays, he should also pray for Africans, because it is thanks to our ancestors that France exists today."')
add("Normal", "— Captain Ibrahim Traoré, response to Macron, 14 January 2025")
add("Normal", "On 8 November 2024, the Burkinabè security forces (FDS) thwarted an attempted corruption of a documented unprecedented scale: an intermediary proposed to elements of the security forces that they participate in overthrowing the government in exchange for 5 billion CFA francs. Acting on orders from their superiors, the soldiers feigned compliance. At the moment of handing over the suitcases, the individual was arrested in flagrante delicto. The funds were seized and deposited with the Public Treasury pending the conclusions of the investigation into the identity of the sponsors. Five billion CFA francs for a coup. The figure simultaneously documents two realities: the determination of sponsors to destabilise the transition, and the internal resistance of the FDS to corruption. The battle for the AES is also fought inside the barracks.")

add("Heading 2", "Chapter 18 — Niger: The CNSP and the Final Lock")
add("Normal", "On 26 July 2023, the Nigerien presidential guard placed President Mohamed Bazoum under house arrest. General Abdourahamane Tiani, head of the Presidential Guard, took command of the National Council for the Safeguard of the Homeland (CNSP). The international reaction was immediate and hysterical. For a simple reason: Niger is the last lock.")
add("Normal", "3 August 2023: a Boeing C-17A Globemaster took off from Ramstein heading for Niamey. It turned back over Algeria — the CNSP refused it landing rights. The sovereignty of Niger's airspace was asserted in practice even before the defence agreements were officially denounced.")
add("Normal", "December 2023: departure of French soldiers. Spring 2024: closure of US Base 201. Nathalie Yamb, at the grand debate in Niamey, formulated the achievement in its historical dimension: 'No country in the world, except Vietnam, has managed to get both the French and American armies to leave simultaneously, one after the other, without shedding a single drop of blood. This is extraordinary. History will remember it for centuries and centuries.'")
cite('"No country in the world, except Vietnam, has managed to get both the French and American armies to leave simultaneously, one after the other, without shedding a single drop of blood."')
add("Normal", "— Nathalie Yamb, grand debate, Nigerien television, Niamey, post-July 2023")
add("Normal", "Nigerien oil revenues post-transition: +218% between 2020 (64.1 bn CFA francs) and 2024 (204 bn CFA francs). Domestic needs coverage: from 20% to 60%. [Minister Sahabi Oumarou, 24 February 2025] March 2025: withdrawal from the OIF (Organisation internationale de la Francophonie) during Francophonie Week — a non-accidental timing. Sequence of ruptures: ECOWAS (January 2024), OIF (March 2025), suspension of French media in Niger (May 2026). Each step is irreversible.")
add("Normal", "On 12 February 2024, Tiani delivered a ninety-minute speech on RTN (Radio-Télévision Nigérienne) that structures the intellectual architecture of the rupture. He formulated what had never been said at this level of official responsibility: 'It is no longer a matter of our states serving as France's cash cow. France has pillaged us for 107 years. France must pay cash for the debts of 65 years of systematic pillaging of resources.'")

add("Heading 2", "Chapter 19 — The Liptako-Gourma Charter: A Founding Act")
add("Normal", "16 September 2023. Bamako. Three men signed a document. Assimi Goïta for Mali. Captain Ibrahim Traoré for Burkina Faso (MPSR). Abdourahamane Tiani for Niger (CNSP). The Liptako-Gourma Charter created the Alliance of Sahel States.")
add("Normal", "The name is deliberate: Liptako-Gourma is the tri-national border zone between the three countries, the ancestral territory of the Fulani, Tuareg, Songhai, and Mossi peoples. The AES anchors its rupture in a historical continuity that transcends colonisation. Before Berlin 1884, this territory existed. After Paris 2023, it is being rebuilt.")
add("Normal", "28 January 2024: simultaneous withdrawal from ECOWAS. 6 July 2024: proclamation of the Confederation of Sahel States, at the Niamey summit. 21 December 2025: Goïta installed the Unified AES Force. Each step renders the preceding one irreversible. This is not improvisation. It is construction.")
add("Normal", "The summit of 6 July 2024 at the Mahatma Gandhi International Conference Centre in Niamey produced four documents binding the three states: a treaty establishing the AES Confederation; internal rules for the heads of state college; a 25-point final communiqué; and the Niamey Declaration. This is not a statement of intent. It is a legal corpus. On ECOWAS, Tiani was unambiguous.")
cite('"This popular momentum constitutes the best guarantee of building a confederation of peoples and not a bureaucratic edifice. Our peoples have irrevocably turned their backs on ECOWAS."')
add("Normal", "— General Abdourahamane Tiani, CNSP Niger, address at the Niamey summit, 6 July 2024")
cite('"The new threats are steered by state sponsors. The AES is an irreversible reality."')
add("Normal", "— Assimi Goïta, President of the Malian transition, 21 December 2025")
sep()

# ===== PART VI =====
add("Normal", "PART VI", bold=True)
add("Heading 1", "THE GEOPOLITICS OF RUPTURE")
add("Normal", "The AES in its regional and global environment")

add("Heading 2", "Chapter 20 — Chad: Mahamat Déby between Two Fires")
add("Normal", "Chad is the blind spot of Sahelian analysis. The country shares borders with Niger, Sudan, Libya, Cameroon, the CAR, and Nigeria. It is the geographic pivot of the African continent. According to the SWP report of May 2026, Mahamat Déby's Chad is also a logistical hub in the Emirati network supplying the Sudanese RSF (Rapid Support Forces): President Déby has at least temporarily authorised the UAE to use Chadian territory as a hub.")
add("Normal", "Idriss Déby died on 20 April 2021, officially at the front during combat against the FACT (Front for Change and Concord in Chad) rebellion in the north of the country — the day after his re-election. The coincidence of timing has been noted by several analysts. The dynastic succession is an absolute constitutional anomaly. Mahamat Déby took power the day after his father's death. Macron attended the funeral and publicly endorsed the succession. The same Macron who vehemently condemned the transitions in Mali and Burkina Faso in the name of constitutional order. This difference in treatment is analytically revealing: it is not democracy that matters to Paris, it is obedience.")
add("Normal", "In 2024, Chad entered into negotiations on the revision of Franco-Chadian defence agreements. Paris negotiated with a gentleness never applied to Bamako or Niamey. The reason is simple: the N'Djamena base remains France's last major military installation in sub-Saharan Africa.")

add("Heading 2", "Chapter 21 — Algeria: An Ambiguous Mediator")
add("Normal", "Algeria maintains a complex relationship with the AES. It facilitated the Algiers Accords (2015) that supposedly disarmed Malian Tuareg groups. It plays a role of discreet mediator between certain armed groups and the transitional authorities. On 3 August 2023, the American C-17 turned back over Algerian airspace — a de facto diplomatic shield. The most analytically solid reading of the Algiers Accords in the corpus does not come from a Pan-Africanist militant. It comes from inside the UN system itself. Albert Anatole Ayissi formulated this judgement: 'The Algiers Accords consisted of balkanising the country. It was a matter of the European Union, led by France and supported by the UN, getting the legitimate authorities of Bamako and the leaders of terrorist groups to sit at the same table to make bad arrangements to the detriment of Mali's interests.'")
add("Normal", "But on 22 March 2026, at the Arab League meeting, Mali recognised Moroccan sovereignty over Western Sahara. Algiers was furious. Mali had just chosen Rabat over Algiers on the most sensitive question of Maghrebi geopolitics. A few days later: the attacks of 25 April 2026. The analytical tension remains open: did the attacks occur by coincidence or by causality? Iyad Ag Ghali, the JNIM leader, has historically had ties to Algerian intelligence services.")

add("Heading 2", "Chapter 22 — Russia, China, Turkey: Partners or New Masters?")
add("Normal", "The question must be asked. The AES replaced French partners with Russian, Chinese, and Turkish partners. African sovereignty requires verifying whether these new partnerships reproduce the logics of domination they were supposed to replace.")
add("Normal", "The honest answer is nuanced. Captain Ibrahim Traoré refused 200 Saudi-financed mosques. Tiani expelled Chinese executives for wage discrimination against African workers. These facts show that AES sovereignty is also exercised against non-Western partners. This is not a pro-Russian position. It is a pro-African stance that chooses its partners without submitting to them.")
add("Normal", "In June 2024, Medvedev spoke before UNESCO and named the CFA franc 'monetary neocolonialism.' He cited Sankara. He quantified African extraction at 62,000 billion dollars between 1960 and 2018. The analysis is not wrong because it comes from Moscow. It is a calculated geopolitical positioning. What matters analytically: it is the first time that a senior official of a Security Council power has used this framework in an international session. The Pan-Africanist narrative enters great-power diplomacy.")
add("Normal", "The UAE: an actor of African destabilisation (SWP, May 2026)")
add("Normal", "SWP Comment No. 19, May 2026 — The Destabilising Role of the United Arab Emirates in African Conflicts. Authors: Dr Gerrit Kurtz, Dr Wolfram Lacher, Dr Stephan Roll, Africa and Middle East Division, SWP (German Institute for International and Security Affairs). Independent institutional academic source, peer-reviewed.")
add("Normal", "The facts established by the report: the UAE are the most important military, logistical and financial supporters of the RSF (Rapid Support Forces/Hemeti) in Sudan. October 2025: the RSF captured El-Fasher, committing massacres qualified as having 'hallmarks of genocide' by a UN inquiry mission. In autumn 2025, the UAE established an RSF training camp in Benishangul-Gumuz, western Ethiopia. The Emirati security company Global Security Services Group recruited and transported several hundred Colombian mercenaries — some training children to fight. US sanctions were imposed in 2025 against the actors involved, with the exception of the Emirati firm itself.")
cite('"The United Arab Emirates have become one of the most aggressive external actors in African conflicts. Its role impedes conflict resolution efforts and worsens humanitarian crises and regional instability."')
add("Normal", "— Kurtz, Lacher, Roll, SWP Comment No. 19, May 2026")

add("Heading 2", "Chapter 23 — The United States Facing the Recomposition")
add("Normal", "Washington is not Paris. The United States defends interests, not a symbolic system. Their relationship with the AES is pragmatic. The withdrawal from Base 201 in spring 2024 was negotiated, not imposed. The Americans left without slamming doors, leaving open the possibility of other forms of security cooperation.")
add("Normal", "Nathalie Yamb, at the Niamey debate, analysed Trump's election as a 'window of opportunity': the AES's classic adversaries no longer present a united front. Europe is destabilised. If the AES acts quickly to consolidate its economic and institutional assets, it can benefit from this moment. But she warned: if this window is not exploited, Europeans will rearm and 'go looking for money elsewhere, and that elsewhere is among us.'")
add("Normal", "On 23 April 2026: the EU Council finalised 90 billion euros for Ukraine, of which 60 billion for defence with 'targeted exemptions.' Two days later: the attacks of 25 April. The chronological coincidence between the European financial release and the coordinated attacks in Mali is noted by several analysts. It does not constitute proof. It constitutes a question.")

add("Heading 2", "Chapter 24 — Mauritania: The Silent Neighbour")
add("Normal", "Mauritania is the forgotten player in Sahelian analysis. Border with Mali over 2,200 km. Border with Senegal, Algeria, Morocco. A country 70% desert. Population: 4.7 million. And yet: outside the AES, maintaining correct relations with France, hosting on its territory rear bases of groups that Bamako considers hostile.")
add("Normal", "Bilal Chérif, leader of the Liberation Front of Azawad (FLA), has his rear base in Mauritania according to field sources. In May 2025, he travelled to France with a Schengen visa even though his movement maintains relations with the JNIM. He reportedly received in Paris according to Africa Intelligence. Ghazouani was re-elected in 2024 in an election without genuine alternation. His stability rests on a fragile balance: good relations with Paris, pragmatic foreign policy, silence on documented internal human rights violations. President Ghazouani was received by Macron on a state visit shortly before the attacks of 25 April 2026. Mali was at the heart of the discussions.")
sep()

# ===== PART VII =====
add("Normal", "PART VII", bold=True)
add("Heading 1", "THE PROXY WAR")
add("Normal", "From the ghost army to the attacks of 25 April 2026")

add("Heading 2", "Chapter 25 — Paris's Ghost Army")
add("Normal", "After the official expulsions, France did not leave the Sahel. It reconstituted itself. Discreetly. Clandestinely.")
add("Normal", "The pyramid of domination described by Dr Yamb Ntimba structures this system into five levels. The military level is the most visible.")
add("Normal", "Two cases document the ghost army from African field sources. Rémy Juan Quignolot: former French non-commissioned officer, head of security at the French embassy in Bamako, responsible for networks of informants, arrested by Malian authorities. Yan Vesiller: DGSE agent arrested in Bamako, accused of preparing a coup d'état. Still detained in Mali at the time of writing.")

add("Heading 2", "Chapter 26 — Sadio Camara: From Architect to Target")
add("Normal", "February 2022: the intercepted conversation between Ivorian President Ouattara and Boubou Cissé identified Sadio Camara as a priority target.")
add("Normal", "November 2022: Camara travelled to Ouagadougou to formalise Mali-Burkina cooperation. May 2023: architect of the operation to retake Kidal. 14 November 2023: Kidal falls in less than 24 hours. A man who achieved what ten years of Barkhane could not.")
add("Normal", "25 April 2026. Car bomb attack in Kati, targeting his personal residence. The neighbouring mosque was hit. Several victims. Camara was absent.")
add("Normal", "Sadio Camara is not Lumumba. He is not Sankara. He does not govern a country. He is the chief of staff of a transition army in a country under sanctions. And yet someone decided to kill him with a suicide bomber.")
cite('"We are in the cold reality of the field. Former French Legionnaires are working with the Ukrainian GUR. The lock on the Sahel has changed hands."')
add("Normal", "— George Malbruno, RTL France, from a French security source, 9 May 2026")

add("Heading 2", "Chapter 27 — The Attacks of 25 April 2026")
add("Normal", "The night of 28 to 29 January 2026, Niamey's Diori Hamani International Airport and Air Base 101 were attacked. This unprecedented attack on Niger's sovereignty set the tone for what was to follow.")
add("Normal", "25 April 2026 is the date that separates a before and an after. On that day, the most significant attacks since the transitions were recorded simultaneously in Mali and Burkina Faso. The coordination is documented. The scale is unprecedented.")
add("Normal", "The proof of FLA-JNIM coordination is public. The FLA spokesperson declared: 'We have good contacts with the JNIM. We coordinate.' This public statement constitutes direct evidence of a joint operation between two groups officially designated as terrorist organisations by the Malian state.")
add("Normal", "On 9 May 2026, RTL France published revelations from George Malbruno from a French security source: former French Legionnaires are working with the Ukrainian GUR (Military Intelligence) against Mali. Abdoulaye Maïga, labelled a conspiracy theorist in 2021 for saying this, was confirmed in 2026 by an official French source. The chronology closes on itself.")

add("Heading 2", "Chapter 28 — The AES Response and Total Isolation")
add("Normal", "The AES response to the 25 April 2026 attacks is documented at three levels. Militarily: 15,000 men mobilised. The Unified AES Force, installed on 21 December 2025, demonstrates its operational capacity six months after its establishment.")
add("Normal", "Diplomatically: suspension of ten French media outlets by Niger on 8 May. Banning of Al Arabiya (Dubai). The Malian government's response was to restructure the command: General Assimi Goïta personally assumed the Defence portfolio.")
cite('"By personally taking command of this sovereign ministry, General Assimi Goïta reinforces his control over the security apparatus and sends a clear message: the transition is in command."')
add("Normal", "— ORTM, Malian national television, 10 May 2026")
add("Normal", "The pressure continued on all fronts simultaneously. Military (proxy attacks). Informational (suspended media). Economic (sanctions maintained). Diplomatic (AES internationally isolated). The siege was total. And yet the AES held.")
add("Normal", "Proof through direct quotation. Djerba, 19 November 2022. Macron: 'La Francophonie is the language of pan-Africanism.' [Emmanuel Macron, OIF summit, Djerba, November 2022] La Francophonie, designed in 1883 to perpetuate colonial domination, was being redefined by the man who embodies it as the language of pan-Africanism. The tool of domination becoming the vocabulary of emancipation — whether Macron intended it or not.")
sep()

# ===== PART VIII =====
add("Normal", "PART VIII", bold=True)
add("Heading 1", "THE AES'S INTERNAL CHALLENGES")
add("Normal", "What the sovereign project must overcome")

add("Heading 2", "Chapter 29 — The Persistent Jihadist Threat")
add("Normal", "The AES has not made jihadism disappear. It has changed the rules of the game: it refuses the French military presence that allegedly contained it, while affirming that that very presence was in fact producing it. The bet is existential.")
add("Normal", "Since September 2025, the JNIM has been imposing a methodical blockade of fuel supply chains in Mali. Targeted axes: Bamako-Mopti-Gao, Bamako-Ségou-San-Mopti. First consequence: a significant fuel shortage at Bamako's Modibo Keïta International Airport.")
add("Normal", "Mariam Cissé: TikTok blogger, originally from Tonka (Timbuktu region), a figure of popular civilian resistance. Assassinated publicly and filmed by JNIM in May 2025. Her death produced the opposite of what the JNIM intended: it made her a martyr figure of the Sahelian resistance.")
cite('"Asymmetric terrorism targeting civilians is strategic cowardice that itself rests on the instrumentalisation of religious extremism to serve geopolitical and economic ends."')
add("Normal", "— Dr Yves Ekoué Amaïzo, Afrocentricity Think Tank, 29 November 2025")

add("Heading 2", "Chapter 30 — Intra-Sahelian Fractures")
add("Normal", "The AES sovereign project cannot be evaluated solely in terms of its external adversaries. It must also be assessed in relation to the internal fractures it must surmount if it is to be durable.")
add("Normal", "Human Rights Watch and Amnesty International document extrajudicial executions by security forces and militias, arbitrary detentions, and enforced disappearances in the three AES countries. These facts are documented. The analyst who ignores them produces incomplete analysis.")
cite('"We cannot fight injustice coming from outside by practising injustice inside."')
add("Normal", "— Thomas Sankara, 1984")
add("Normal", "Nathalie Yamb places this tension in a broader analytical framework: the notion of 'protection of minorities' is instrumentalised by Western powers as a lever of destabilisation — a concept of sovereignty deployed against sovereignty. Identifying this manipulation does not exempt the AES from the obligation to actually protect its minorities. The distinction between the two arguments matters.")

add("Heading 2", "Chapter 31 — The War Economy and Sanctions")
add("Normal", "Sanctions are an instrument of economic warfare. They obey a logic that history constantly validates: they hurt the populations more than they hurt the leaders. The IMF and World Bank know this. They apply them anyway.")
add("Normal", "On 7 August 2023, Burkina Faso denounced its tax treaty with France. On 8 November 2023, the effect took force on the Côte d'Ivoire side. A tax treaty is a legal instrument of economic integration. Its denunciation is a step towards monetary and fiscal sovereignty.")
add("Normal", "Lafarge: former executives convicted on 13 April 2026 (6 and 5 years in prison) for financing terrorism in Syria. The French state's judicial arm condemning a French company for financing terrorism in a foreign conflict is a founding juridical fact. The same mechanism — financing armed groups to control resources — is documented in Africa. The precedent matters.")
add("Normal", "The precedent of Muammar Gaddafi: in 2010–2011, he was preparing an African Monetary Fund (Yaoundé), an African Central Bank (Sirte), and an African Investment Bank (Tripoli). These three institutions would have competed directly with the CFA franc, the IMF (International Monetary Fund), and the World Bank. He was eliminated in March 2011. The three institutions died with him. Causal coincidence or consequence? The question is legitimate.")

add("Heading 2", "Chapter 32 — The Democratic Question")
add("Normal", "The democratic question is the most difficult for an honest AES analyst. The AES governments came to power through military transitions. They are not democratically elected. This fact cannot be concealed behind analytical elegance.")
add("Normal", "But the overthrown regimes were formal electoral democracies. IBK was elected. Kaboré was elected. Bazoum was elected. And the populations celebrated their fall. This gap between electoral legitimacy and popular legitimacy is the central political fact of the Sahelian transitions.")
add("Normal", "Nathalie Yamb formulates the criterion: what separates a good leader from a bad one is not their mode of access to power. It is what they do with that power. Do they serve sovereignty or servitude? This is a criterion. It is not sufficient. But it is necessary.")
add("Normal", "The real democratic question for the AES is this: do the transitions produce institutions or personalised rule? Are there mechanisms for holding leaders accountable? Is there room for dissent? Are there civilian structures capable of succeeding the military? These questions remain open. The fact that they are asked is itself a sign of intellectual honesty.")
sep()

# ===== PART IX =====
add("Normal", "PART IX", bold=True)
add("Heading 1", "THE SOVEREIGN HORIZON")
add("Normal", "What the AES must build to endure")

add("Heading 2", "Chapter 33 — Currency: Breaking the CFA Chain")
cite('"Currency is the mother of sovereignties. You cannot be sovereign if you do not have your own currency."')
add("Normal", "— Dr Douma Jean-René, Panafrican Média TV, 10 May 2026")
add("Normal", "The CFA franc is not an African currency. It is a French currency deployed in Africa. Its real management is in Paris. The Banque de France validates the monetary policy of fourteen African states. This is not cooperation. It is suzerainty.")
add("Normal", "Bloomberg and Citigroup recommended in May 2026 a devaluation of the CFA franc in the CEMAC zone — analysed by Jonathan Batenguène as yet another French economic attack against Central Africa. The devaluation of 1994 destroyed 100% of purchasing power overnight. A new devaluation in 2026 would produce the same effect.")
add("Normal", "The sequence of sovereignty is not optional. It is ordered. Yves Ekoué Amaïzo, an economist specialising in monetary strategies, details it: military sovereignty first — guaranteeing territorial integrity. Then customs sovereignty — controlling borders and trade flows. Then fiscal sovereignty — collecting taxes on its own territory. Then economic sovereignty — controlling the investment cycle. Then monetary sovereignty — issuing and managing one's own currency. You cannot do the last without the first four.")
cite('"There is no sovereignty without military sovereignty, then territorial, then customs, fiscal, economic, monetary sovereignty in that order — failing which you are destroying yourself."')
add("Normal", "— Yves Ekoué Amaïzo, economist, Afrocentricity Think Tank, Africa Connect, 18 January 2024")

add("Heading 2", "Chapter 34 — The Sahelian Federal Army")
add("Normal", "The Unified AES Force was established on 21 December 2025. Operations Yokoo 1 and 2 cited by Goïta. Tarha nakal 2 exercises (14 May 2025, Tillia, Niger): joint AES-Chad-Togo manoeuvres. Scenario: an attempted secession supported by rebel groups with external backing. The exercise scenario corresponded exactly to the attacks of 25 April 2026. Eleven months before, the AES armies were training against the exact scenario that would unfold.")
add("Normal", "The VDP — Volontaires pour la Défense de la Patrie (Volunteers for the Defence of the Homeland) — represent an innovation in Burkina Faso: a civilian militia integrated into the national defence chain. This model integrates territorial knowledge, social embeddedness, and operational flexibility that a conventional army cannot replicate.")

add("Heading 2", "Chapter 35 — The Diaspora as a Strategic Force")
add("Normal", "African migrant remittances to their home countries far exceed the amounts of official aid, according to World Bank data. The African diaspora is the primary financial actor of African development — not the donors, not the international financial institutions.")
add("Normal", "But the diaspora can also be a vector of destabilisation. It can be influenced, divided, instrumentalised. The AES must build a relationship with its diaspora based on trust, not on unilateral appeals. The diaspora must be a strategic asset, not a passive source of foreign exchange.")

add("Heading 2", "Chapter 36 — Sankara Was Right")
add("Normal", "Thomas Sankara was President of Burkina Faso from 1983 to 1987. Four years. Assassinated on 15 October 1987, along with twelve of his companions, by a coup orchestrated by Blaise Compaoré with documented external support.")
add("Normal", "In four years: 2.5 million children vaccinated against measles, meningitis and yellow fever. 10 million trees planted. Abolition of the bride price. Prohibition of female genital mutilation. 54,000 km of rural roads. Land reform benefiting farmers. A country feeding itself. All of this in four years. Without oil. Without foreign loans.")
cite('"Debt is a cleverly managed reconquest. We have been pauperised; we have been put in conditions such that we are forced to borrow... from those who enslaved us."')
add("Normal", "— Thomas Sankara, address to the UN General Assembly, 4 October 1984")
add("Normal", "Thirty-nine years later, Captain Ibrahim Traoré, President of the Burkina Faso transition (MPSR), governs from the same palace. He cites Sankara systematically. He has adopted the same doctrinal logic: sovereignty first, partnership from a position of strength second. He is 37 years old. The continuity is not accidental.")

add("Heading 2", "Chapter 37 — France-Africa 2.0: The Recomposition of Domination")
add("Normal", "France is not disappearing. It is recomposing. Less military, more economic and technological. The 'Africa for the Future' summit organised by Macron in Paris attempts to reinvent the relationship — while maintaining the essentials of the architecture of extraction.")
cite('"France today is a label. It no longer belongs to itself. Imperialism, for its survival, is prepared to make concessions on the label while maintaining the substance."')
add("Normal", "— Jonathan Batenguène, Panafrican Média TV, 10 May 2026")
add("Normal", "Banda Kani appeals to CEMAC and directly to Paul Biya for the sub-region to invest alongside the Central African people. He documents the structural contradiction: France gives the illusion of having departed while controlling the monetary and economic levers.")
cite('"France gives the illusion of having left while controlling the monetary and economic levers."')
add("Normal", "— Charly Kengne, L'intermédiation de la servitude, 17 March 2026")
add("Normal", "Nathalie Yamb warns of this evolution: the Europeans are rearming, they need resources for this rearmament, and those resources are in Africa. The rearmament of Europe is not only a military project. It is an extractive project. Its beneficiaries will not be African populations.")

add("Heading 2", "Chapter 38 — What the AES Must Achieve to Survive")
add("Normal", "Nathalie Yamb formulates the challenge with historical precision: the 1960s produced confiscated independence. The 1990s produced confiscated multipartyism. The 2020s are producing sovereignism. If the structures do not change in depth — monetary, economic, security — in thirty years it will all have to start again.")
add("Normal", "The status quo had a record. HDI 184th, 185th, 189th out of 191. Less than 20% access to electricity in the richest country in uranium. A 46% dependency rate on foreign aid in the CAR. Barkhane's attacks multiplied by three in nine years. This was not a stable equilibrium. It was a managed crisis. The AES seeks a different equilibrium. Its success is not guaranteed. Its failure is not inevitable.")

add("Heading 2", "Chapter 39 — Senegal Under Faye: Sovereignism through the Ballot Box")
add("Normal", "On 24 March 2024, Bassirou Diomaye Faye was elected President of Senegal with 54% of the vote in the first round. He came out of prison ten days before the election. His running mate Ousmane Sonko had spent the entire campaign period under judicial detention.")
sep()
add("Normal", "The trajectory that led to this election is one of a repression that rebounded. In 2023, riots killed several dozen people following the conviction of Sonko. Macron openly supported the incumbent president Macky Sall. The repression did not prevent the election. It accelerated it.")
add("Normal", "Faye and Sonko subscribe to an explicit sovereignist and pan-Africanist rhetoric: revision of petroleum and gas contracts, renegotiation of defence agreements, exit from the CFA franc. Language identical to that of the AES transitions — with one fundamental difference: Faye was elected. He has electoral legitimacy.")
add("Normal", "The regional shockwave is real. A sovereignist president in Senegal modifies the geopolitical equation of West Africa as a whole. Senegal is not marginal: it is the historic seat of French West Africa (AOF), home to the ECOWAS headquarters in Abuja via its symbolic weight, and has a diaspora among the most active on the continent. If sovereignism penetrates Dakar, it can no longer be presented as an exclusively military-junta project.")
add("Normal", "The three-phase doctrine finds here an unexpected validation. Phase 2 — the transitional alliance with states in rupture — gains a democratic actor. The geopolitical landscape of the Sahel is changing, not only through the barrel of a gun.")
sep()

# ===== EPILOGUE =====
add("Normal", "EPILOGUE", bold=True)
add("Normal", "Justice cannot be avoided")

add("Normal", "Chapter 40 — Arrogance as Doctrine: Western Contempt for Africa", bold=True)
add("Normal", "Contempt is not an incidental misstep in the relationship between France and Africa. It is a doctrine. It is structurally necessary. A power that extracts cannot simultaneously acknowledge the humanity of those from whom it extracts. The cognitive dissonance would be unbearable. So it institutionalises the contempt.")
add("Normal", "January 2025. Macron denounces 'African ingratitude' before French ambassadors. [Emmanuel Macron, January 2025, conference of ambassadors] The term is not a slip. It reveals the mental framework: France has done good, Africa is ungrateful. This inversion of creditor and debtor is the very foundation of Françafrique.")
add("Normal", "Institutional contempt also takes the form of condescension disguised as respect. Macron in Nairobi, May 2026: 'If you fail, we will have nothing.' [Emmanuel Macron, Nairobi, 11 May 2026] The head of the French state, on African soil, addresses African leaders as potential failures — with France as the ultimate safety net. The paternalism is structural.")
add("Normal", "Arrogance also structures the diplomatic gaze of local relays. Hassoumi Massaoudou qualified on LCI the demonstrators celebrating the departure of the French army from Niger as 'manipulated idiots.' A Nigerien diplomat, on French television, insults his own people to please his French hosts. This is the comprador elite in its purest form.")
add("Normal", "The ultimate paradox is formulated by the French institutions themselves. The French parliamentary commission: 'We need Africa more than Africa needs us.' And yet the same institutions finance the media, the influence networks, the proxy militias to prevent Africa from acting accordingly. The explicit recognition of Africa's indispensability — and the simultaneous refusal to accept its consequences — is the perfect definition of a system that knows it is unjust and perpetuates itself by force.")

add("Normal", "Chapter 41 — Anatomy of a Fear: What the West Really Dreads", bold=True)
add("Normal", "The arrogance documented in the preceding chapter has a reverse side. Behind the discourse of power, there is fear. Not the stated fear of 'instability' or 'terrorism.' The deeper fear: that Africa will succeed.")
add("Normal", "The demographic data frame the issue. In 2025, the United States and Europe together represent no more than 9% of the world's population. Africa alone represents 18% — and will represent 26% in 2050. This demographic shift is irreversible. The political consequences are not yet fully visible. But they are being prepared. In the Sahel. In Dakar. In Bangui. In Bamako.")
add("Normal", "The fear specific to Africa is formulated precisely. The West does not fear that the AES will fail. It fears that the AES will succeed. It fears that a continent-wide model will emerge: military sovereignty recovered, resources renegotiated, currencies de-Frenchified, institutions decolonised. A successful AES would constitute a demonstration of possibility for the entire global south. That is what they fear. Not chaos. Precedent.")
add("Normal", "The synthesis is formulated by Macron himself, unwittingly, in Nairobi on 11 May 2026: 'If you fail, we will have nothing.' [Emmanuel Macron, Nairobi, 11 May 2026] He did not say: 'if you fail, Africans will suffer.' He said: 'we will have nothing.' The subject is France. Africa's success or failure is measured by its consequences for France. This is the colonial gaze in its purest form. And it was delivered on African soil, to African leaders, in 2026.")
add("Normal", "We have come back to the starting point. The villa in Niamey. The whiteboard. The five words.")
add("Normal", "Peace, we can prevent it.")
add("Normal", "This phrase was a strategy. It was also a monumental miscalculation. Its authors underestimated three things.")
add("Normal", "They underestimated memory. Sahelian peoples remember Samory Touré, who resisted for sixteen years. They remember El Hadj Oumar Tall. They remember Sankara. They remember Boganda. The long memory is not nostalgia. It is a doctrine of resistance.")
add("Normal", "They underestimated youth. The Sahelian population has a median age below 18 years. These young people grew up knowing that they are living on some of the most mineral-rich soil in the world, while their countries remain among the least developed. This knowledge produces not resignation, but rage. Organised rage.")
add("Normal", "They underestimated doctrine. The AES is not an emotional reaction. It is a constructed project. It has an institutional framework, a charter, a confederation, a unified force. It has intellectuals — Yamb, Amaïzo, Nyamsi, Maïga — who articulate it theoretically. It has leaders — Goïta, Traoré, Tiani — who implement it politically. The five words of the whiteboard met an organised response.")
sep()
add("Normal", "This book did not promise you that the AES would succeed. No one can promise that. History is open. The obstacles are real. The internal fractures exist. The threats are lethal.")
add("Normal", "This book promised to analyse it seriously. Without condescendence. Without the presumption that Africans in uniform cannot construct anything viable. Without the bad faith that consists in applying one standard to transitions and another to electoral façades maintained by coercion.")
add("Normal", "It promised to cite its sources. To signal its uncertainties. Convergences rather than prophecies.")
doc.add_paragraph()
add("Normal", "The peace of cemeteries has been imposed for too long.")
add("Normal", "Just peace remains to be built.")
doc.add_paragraph()
add("Normal", "Justice cannot be avoided.")
add("Normal", "Dignity, no.")
add("Normal", "Freedom, never.")
add("Normal", "The Sahel has chosen. Now, the rest of Africa is watching.")

# ===== METHODOLOGICAL NOTES =====
doc.add_paragraph()
add("Normal", "METHODOLOGICAL NOTES & CORPUS", bold=True)
add("Normal", "Analytical corpus: 130+ sources.")
doc.add_paragraph()
add("Normal", "PRIMARY OFFICIAL AES SOURCES", bold=True)
add("Normal", "Dr Anatole Ayissi, UNOCA (Chief of Cabinet of the UN Special Representative for Central Africa, Libreville) — For You Media Africa. General Abdourahamane Tiani — RTN speech 12/02/2024; interview Télé Sahel; address of 13/11/2025. Assimi Goïta — address 21/12/2025; statement on Kidal 14/11/2023. Captain Ibrahim Traoré — public addresses 2023–2026. Ali Mahaman Lamine Zeine, Prime Minister of Niger — economic press releases. Abdoulaye Maïga, Prime Minister of Mali — UN General Assembly 09/2021; Azalaï Hotel Bamako 19/10/2024. Sahabi Oumarou, Nigerien Minister — 24/02/2025.")
doc.add_paragraph()
add("Normal", "FRENCH ADVERSARIAL SOURCES", bold=True)
add("Normal", "RTL France, George Malbruno (09/05/2026 — former Legionnaires + GUR). Thomas Dietrich: Bénin (13/07/2024) + L'armée fantôme de Paris. Anne-Sophie Avé, former Ambassador of France to Mali — public speech on propaganda. General Thierry Burkhard — National Assembly defence commission, behind closed doors, 09/2024. André Chassaigne, GDR/PCF deputy — National Assembly, December 2013. French parliamentary commission on France-Africa relations — official report. Loïk Le Floch-Prigent, Robert Bourgi, Pascal Lissouba — documented testimonies. Alain Juillet, former DGSE Director. French Court of Auditors (Barkhane 2020).")
doc.add_paragraph()
add("Normal", "PAN-AFRICANIST AND AFRICAN SOURCES", bold=True)
add("Normal", "Dr Yamb Ntimba — pyramid of domination. Nathalie Yamb — development aid chronicle (Nov. 2022) + grand debate Niamey [Two Scoops]. Franklin Nyamsi — Elf/Chirac + Niger revenues December 2025. Banda Kani — CAR, information war, Togo. Bertrand Tatsinda — CAR, FACA. Jules Domche — Vox Africa, information war. Jonathan Batenguène — CFA franc, CEMAC. Yves Ekoué Amaïzo — monetary sovereignty. Mariam Tamousang — CADTM, Afrohpique. Siké Doumbé — For You Media, Sahel resources. Paul Elvira — Panafrican Média TV. Fridolin Ngoulou — Oubangui Médias. Mamadou Koulibaly — Côte d'Ivoire. Thomas Porcher — Congo-Brazzaville. Charly Kengne — L'intermédiation de la servitude. Dr Douma Jean-René.")
doc.add_paragraph()
add("Normal", "INSTITUTIONAL AND ACADEMIC SOURCES", bold=True)
add("Normal", "French Court of Auditors (Barkhane 2020). UNCTAD. UNDP (HDI). World Bank. ACLED (2015–2022). French Nuclear High Committee (uranium). SWP Comment No. 19, May 2026 — Kurtz, Lacher, Roll. Frédéric Turpin, Jacques Foccart, dans l'ombre du pouvoir, CNRS Éditions, 2015. André Bourgeot, CNRS. Cheikh Anta Diop. Éric Toussaint, CADTM. Medvedev/UNESCO 16/06/2024. Africa Intelligence. Bloomberg/Citigroup, May 2026. Al Arabiya ban — HAC Niger decision no. 2026.0058/P-HAC.")
doc.add_paragraph()
add("Normal", "Rigour is not the preserve of those who dominate. It is the weapon of those who resist.", italic=True)
sep()
cite('"Let us remain vigilant." — General Tiani, 13 November 2025')
add("Normal", "BEN-H2O — 130+ sources — 2026", align=WD_ALIGN_PARAGRAPH.CENTER)

# ===== SEGMENT GLOSSARIES =====
doc.add_paragraph()
add("Normal", "TRANSLATION GLOSSARY", bold=True)
add("Normal", "The following acronyms and key terms have been systematically converted throughout this translation:")

glossary = [
    ("AES — Alliance des États du Sahel", "AES — Alliance of Sahel States (also used as AES throughout)"),
    ("CEDEAO — Communauté Économique des États de l'Afrique de l'Ouest", "ECOWAS — Economic Community of West African States"),
    ("ONU — Organisation des Nations Unies", "UN — United Nations"),
    ("OTAN — Organisation du Traité de l'Atlantique Nord", "NATO — North Atlantic Treaty Organization"),
    ("RCA — République Centrafricaine", "CAR — Central African Republic"),
    ("EAU — Émirats Arabes Unis", "UAE — United Arab Emirates"),
    ("UA — Union Africaine", "AU — African Union"),
    ("UE — Union Européenne", "EU — European Union"),
    ("FMI — Fonds Monétaire International", "IMF — International Monetary Fund"),
    ("ONG — Organisation Non Gouvernementale", "NGO — Non-Governmental Organisation"),
    ("CPI — Cour Pénale Internationale", "ICC — International Criminal Court"),
    ("CIJ — Cour Internationale de Justice", "ICJ — International Court of Justice"),
    ("OIF — Organisation Internationale de la Francophonie", "OIF — Organisation internationale de la Francophonie (retained)"),
    ("DGSE — Direction Générale de la Sécurité Extérieure", "DGSE — General Directorate for External Security (France's foreign intelligence service)"),
    ("FAMa — Forces Armées Maliennes", "FAMa — Malian Armed Forces"),
    ("FAB — Forces Armées du Burkina", "FAB — Burkinabè Armed Forces"),
    ("FACA — Forces Armées Centrafricaines", "FACA — Central African Armed Forces"),
    ("GUR — Holovne Upravlinnia Rozvidky", "GUR — Ukrainian Military Intelligence"),
    ("JNIM — Jama'at Nusrat al-Islam wal-Muslimin", "JNIM — Group for the Support of Islam and Muslims"),
    ("MNLA — Mouvement National de Libération de l'Azawad", "MNLA — National Movement for the Liberation of Azawad"),
    ("FLA — Front de Libération de l'Azawad", "FLA — Liberation Front of Azawad"),
    ("FSR — Forces de Soutien Rapide", "RSF — Rapid Support Forces (Sudan)"),
    ("VDP — Volontaires pour la Défense de la Patrie", "VDP — Volunteers for the Defence of the Homeland"),
    ("MPSR — Mouvement Patriotique pour la Sauvegarde et la Restauration", "MPSR — Patriotic Movement for Safeguard and Restoration (Burkina Faso)"),
    ("CNSP — Conseil National pour la Sauvegarde de la Patrie", "CNSP — National Council for the Safeguard of the Homeland (Niger)"),
    ("APD — Aide Publique au Développement", "ODA — Official Development Aid"),
    ("SWP — Stiftung Wissenschaft und Politik", "SWP — German Institute for International and Security Affairs"),
    ("PNUD — Programme des Nations Unies pour le Développement", "UNDP — United Nations Development Programme"),
    ("CNUCED — Conférence des Nations Unies sur le Commerce et le Développement", "UNCTAD — UN Conference on Trade and Development"),
]
for fr, en in glossary:
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.3)
    run_fr = p.add_run(fr)
    run_fr.bold = True
    p.add_run(f" → {en}")

# Save
out_path = "/home/user/tts-docs/PEACE_WE_CAN_PREVENT_IT_EN.docx"
doc.save(out_path)
print("Done →", out_path)
