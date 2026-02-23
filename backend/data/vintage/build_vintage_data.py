#!/usr/bin/env python3
"""Build the vintage_data.json file."""
import json

data = {
    "metadata": {
        "last_updated": "2026-02-17",
        "sources": [
            "Berry Bros & Rudd",
            "Jeb Dunnuck",
            "Wine Spectator consensus",
            "Manual curation"
        ],
        "year_range": [1970, 2023]
    },
    "regions": {}
}

def tier(score):
    if score >= 90: return "outstanding"
    if score >= 80: return "excellent"
    if score >= 70: return "good"
    if score >= 60: return "average"
    return "poor"

def drinking(year, longevity="medium"):
    age = 2026 - year
    if longevity == "long":
        if age < 5: return "young"
        if age < 15: return "ready"
        if age < 30: return "at_peak"
        if age < 50: return "mature"
        return "past_peak"
    elif longevity == "medium":
        if age < 3: return "young"
        if age < 10: return "ready"
        if age < 20: return "at_peak"
        if age < 35: return "mature"
        return "past_peak"
    else:  # short
        if age < 2: return "young"
        if age < 5: return "ready"
        if age < 10: return "at_peak"
        if age < 20: return "mature"
        return "past_peak"

def v(score_val, desc, notables, year, longevity="medium"):
    return {
        "score": score_val,
        "quality_tier": tier(score_val),
        "description": desc,
        "drinking_window": drinking(year, longevity),
        "notable_wines": notables
    }

# ============================================================
# BORDEAUX RED (1970-2023)
# ============================================================
bordeaux_red_vintages = {}
bx = {
    1970: (88, "Hot dry summer produced powerful tannic wines with deep color and firm structure. A classic vintage that needed decades to soften.", ["Chateau Latour", "Chateau Petrus", "Chateau Palmer"], "long"),
    1971: (82, "Warm vintage with some late-season rain. Elegant and medium-bodied wines, particularly successful on the Right Bank with ripe Merlot.", ["Chateau Petrus", "Chateau Trotanoy", "Chateau Palmer"], "long"),
    1972: (55, "Cold wet growing season with insufficient ripeness. Thin acidic wines lacking fruit and concentration.", ["Chateau Latour", "Chateau Petrus"], "long"),
    1973: (62, "Large crop diluted by September rains. Light pleasant wines for early drinking that lacked staying power.", ["Chateau Petrus", "Chateau Ducru-Beaucaillou"], "long"),
    1974: (58, "Wet autumn ruined a potentially good harvest. Green tannic wines with little charm or fruit.", ["Chateau Latour", "Chateau La Mission Haut-Brion"], "long"),
    1975: (85, "Hot dry summer followed by harvest rains created powerful but austere tannic wines. Right Bank fared best with riper Merlot.", ["Chateau Petrus", "Chateau La Mission Haut-Brion", "Chateau l'Evangelion"], "long"),
    1976: (78, "Exceptionally hot drought-stricken summer produced ripe but sometimes baked wines. Early-maturing with soft tannins.", ["Chateau Ausone", "Chateau Lafite Rothschild", "Chateau Ducru-Beaucaillou"], "long"),
    1977: (52, "Dismal cold wet summer produced underripe angular wines. One of the worst vintages of the decade.", ["Chateau Petrus", "Chateau Latour"], "long"),
    1978: (86, "Late-ripening vintage saved by an Indian summer in October. Elegant wines with fine tannins and good balance.", ["Chateau Margaux", "Chateau La Mission Haut-Brion", "Chateau Pichon Lalande"], "long"),
    1979: (82, "Large crop of even healthy fruit. Correct well-balanced wines that matured gracefully if without exceptional depth.", ["Chateau Margaux", "Chateau Palmer", "Chateau Haut-Brion"], "long"),
    1980: (65, "Cold summer and persistent rain made for a thin difficult vintage. Light wines lacking substance.", ["Chateau Margaux", "Chateau Petrus"], "long"),
    1981: (83, "Warm dry summer though yields were reduced by poor flowering. Elegant structured wines with charm, outshone by 1982.", ["Chateau Margaux", "Chateau Pichon Lalande", "Chateau Certan de May"], "long"),
    1982: (98, "Legendary hot vintage with early harvest. Opulent rich concentrated wines with masses of ripe fruit and sweet tannins. A paradigm-shifting year.", ["Chateau Petrus", "Chateau Lafite Rothschild", "Chateau Mouton Rothschild"], "long"),
    1983: (85, "Hot summer with selective botrytis in Margaux appellation. Rich powerful wines in northern Medoc, more variable on the Right Bank.", ["Chateau Margaux", "Chateau Palmer", "Chateau Pichon Lalande"], "long"),
    1984: (58, "Cold damp growing season failed to ripen Cabernet Sauvignon. Lean green wines, slightly better on the Merlot-dominant Right Bank.", ["Chateau Mouton Rothschild", "Chateau Petrus"], "long"),
    1985: (88, "Warm generous vintage with healthy fruit and smooth tannins. Charming seductive wines with lovely balance, approachable young.", ["Chateau Haut-Brion", "Chateau Margaux", "Chateau Lynch-Bages"], "long"),
    1986: (90, "Classic Cabernet year with a hot dry summer producing powerful structured wines. Left Bank excelled with massive tannic wines built for aging.", ["Chateau Mouton Rothschild", "Chateau Margaux", "Chateau Cos d'Estournel"], "long"),
    1987: (68, "Rain at harvest diluted what could have been a decent crop. Medium-bodied wines for early consumption.", ["Chateau Mouton Rothschild", "Chateau Petrus"], "long"),
    1988: (87, "Classic structured vintage from a dry warm growing season. Firm tannic wines with excellent aging potential, especially in the Medoc.", ["Chateau Mouton Rothschild", "Chateau Haut-Brion", "Chateau Pichon Lalande"], "long"),
    1989: (93, "Scorching hot summer with drought stress produced deeply concentrated hedonistic wines. Early-ripening Merlot excelled on the Right Bank.", ["Chateau Haut-Brion", "Chateau Petrus", "Chateau Clinet"], "long"),
    1990: (96, "Another exceptionally hot year with more balanced conditions than 1989. Generous powerful wines with great depth and fine tannins across all appellations.", ["Chateau Margaux", "Chateau Petrus", "Chateau Le Pin"], "long"),
    1991: (55, "Devastating April frost wiped out much of the crop. Survivors were thin and green from a cool wet summer.", ["Chateau Petrus", "Chateau Latour"], "long"),
    1992: (60, "Persistent rain during harvest rotted much of the crop. Dilute light wines lacking concentration and structure.", ["Chateau Petrus", "Chateau Lafite Rothschild"], "long"),
    1993: (62, "September rains spoiled a promising season. Medium-bodied wines with some charm but lacking depth. Right Bank slightly better.", ["Chateau l'Angelus", "Chateau Troplong Mondot", "Chateau Clinet"], "long"),
    1994: (78, "Hot summer followed by September rain before harvest. Good Cabernet-based wines on well-drained Left Bank soils, more variable elsewhere.", ["Chateau Latour", "Chateau Mouton Rothschild", "Chateau Lafite Rothschild"], "long"),
    1995: (91, "Excellent vintage from hot dry conditions. Powerful structured wines with ripe tannins and great balance. Strong across all appellations.", ["Chateau Margaux", "Chateau Lynch-Bages", "Chateau l'Eglise-Clinet"], "long"),
    1996: (92, "Late-ripening Cabernet benefited from a warm dry October. Firm classical wines with great structure and acidity, superb in the Medoc.", ["Chateau Latour", "Chateau Lafite Rothschild", "Chateau Leoville Las Cases"], "long"),
    1997: (68, "Early harvest from a warm spring and hot August, but September rains diluted the crop. Pleasant easy-drinking wines without concentration.", ["Chateau Petrus", "Chateau Ausone"], "long"),
    1998: (87, "Wet conditions favored the Right Bank where Merlot thrived on clay soils. Outstanding in Pomerol and Saint-Emilion, more mixed in the Medoc.", ["Chateau Petrus", "Chateau Lafleur", "Chateau l'Eglise-Clinet"], "long"),
    1999: (82, "Generous crop of ripe fruit though August rains caused some dilution. Charming medium-bodied wines for mid-term drinking.", ["Chateau Ausone", "Chateau Latour", "Chateau Haut-Brion"], "long"),
    2000: (95, "Millennial vintage with perfect late-season weather. Rich opulent wines with silky tannins and great depth across all appellations.", ["Chateau Margaux", "Chateau Petrus", "Chateau Cheval Blanc"], "long"),
    2001: (88, "Excellent vintage overshadowed by 2000. Cool conditions produced elegant structured wines with fine acidity, especially on the Right Bank.", ["Chateau Ausone", "Chateau Petrus", "Chateau Pichon Lalande"], "long"),
    2002: (78, "Late-season rains disrupted harvest. Best wines come from early-picked Merlot on the Right Bank. Left Bank more inconsistent.", ["Chateau Petrus", "Chateau l'Eglise-Clinet", "Chateau Troplong Mondot"], "long"),
    2003: (84, "Record-breaking heatwave produced atypical powerful wines with high alcohol and low acidity. Some excellent, some overblown and baked.", ["Chateau Ausone", "Chateau Petrus", "Chateau Margaux"], "long"),
    2004: (82, "Classic vintage with good structure and moderate concentration. Cabernet Sauvignon performed well on well-drained Medoc gravel.", ["Chateau Latour", "Chateau Montrose", "Chateau Pontet-Canet"], "long"),
    2005: (97, "Textbook vintage with warm dry conditions throughout. Deeply concentrated balanced wines with ripe firm tannins. Exceptional across the board.", ["Chateau Haut-Brion", "Chateau Margaux", "Chateau Pontet-Canet"], "long"),
    2006: (83, "Warm summer but cooler September. Solid well-structured wines with good fruit but not the opulence of 2005.", ["Chateau Leoville Las Cases", "Chateau l'Eglise-Clinet", "Chateau Pontet-Canet"], "long"),
    2007: (76, "Wet growing season with rain at harvest. Light fruity wines for early drinking. Some decent Right Bank wines from careful producers.", ["Chateau Ausone", "Chateau Petrus", "Chateau Lafleur"], "long"),
    2008: (83, "Cool vintage rescued by a brilliant October. Classical firm wines with bright acidity and moderate weight. Best on the Left Bank.", ["Chateau Cos d'Estournel", "Chateau Leoville Poyferre", "Chateau Pontet-Canet"], "long"),
    2009: (96, "Gloriously warm vintage with ideal conditions throughout. Rich generous wines with velvet tannins and extraordinary depth.", ["Chateau Haut-Brion", "Chateau Latour", "Chateau Pontet-Canet"], "long"),
    2010: (97, "Dry growing season with cool nights preserved acidity in deeply concentrated wines. Powerful structured wines rivaling 2009 but with more classical profile.", ["Chateau Latour", "Chateau Margaux", "Chateau Leoville Las Cases"], "long"),
    2011: (78, "Spring drought followed by wet cool summer. Uneven ripening produced variable wines. Best in Pomerol and Pessac-Leognan.", ["Chateau Haut-Brion", "Chateau l'Eglise-Clinet", "Chateau Lafleur"], "long"),
    2012: (85, "Late-season warmth rescued a challenging start. Ripe Merlot on the Right Bank outperformed the Cabernet-dominant Left Bank.", ["Chateau Petrus", "Chateau Cheval Blanc", "Chateau Lafleur"], "long"),
    2013: (68, "Cold wet summer with September rains. Lean wines with green tannins. Only the most rigorous estates produced acceptable wines.", ["Chateau Margaux", "Chateau Haut-Brion"], "long"),
    2014: (87, "Indian summer in September and October rescued the vintage. Elegant balanced wines, particularly strong in the Medoc and Pessac-Leognan.", ["Chateau Pontet-Canet", "Chateau Montrose", "Chateau Haut-Brion"], "long"),
    2015: (94, "Warm dry vintage with ideal ripening conditions. Generous opulent wines with ripe tannins and great richness across all appellations.", ["Chateau Margaux", "Chateau Haut-Brion", "Chateau Pontet-Canet"], "long"),
    2016: (96, "Dry summer with perfectly timed September rain refreshed the vines. Cabernet Sauvignon excelled, producing powerful structured wines with extraordinary precision.", ["Chateau Latour", "Chateau Lafite Rothschild", "Chateau Leoville Las Cases"], "long"),
    2017: (80, "Devastating April frost reduced crop significantly. Surviving vines produced decent concentrated wines but quantity was dramatically low.", ["Chateau Margaux", "Chateau Cheval Blanc", "Chateau Ausone"], "long"),
    2018: (93, "Hot dry summer with late-season rain providing relief. Rich powerful wines with ripe fruit and polished tannins. Merlot especially successful.", ["Chateau Petrus", "Chateau Haut-Brion", "Chateau Cheval Blanc"], "long"),
    2019: (93, "Warm vintage with drought stress moderated by timely rains. Elegant balanced wines with freshness and finesse, combining power with refinement.", ["Chateau Margaux", "Chateau Mouton Rothschild", "Chateau Ausone"], "long"),
    2020: (95, "Warm early-ripening vintage produced during pandemic lockdowns. Concentrated structured wines with excellent balance and aging potential.", ["Chateau Latour", "Chateau Lafite Rothschild", "Chateau Petrus"], "long"),
    2021: (82, "Cool wet spring with mildew pressure followed by a moderate summer. Classical lighter-styled wines with good acidity but less concentration.", ["Chateau Margaux", "Chateau Haut-Brion", "Chateau Cheval Blanc"], "long"),
    2022: (92, "Extreme drought and heat produced deeply concentrated powerful wines. Careful water management was key. Rich dark wines with firm structure.", ["Chateau Lafite Rothschild", "Chateau Margaux", "Chateau Pontet-Canet"], "long"),
    2023: (88, "Variable conditions with a wet spring followed by a warm dry summer. Balanced wines with good freshness, particularly successful in Pomerol and Saint-Emilion.", ["Chateau Petrus", "Chateau Cheval Blanc", "Chateau Ausone"], "long"),
}
for yr, (sc, desc, notables, lon) in bx.items():
    bordeaux_red_vintages[str(yr)] = v(sc, desc, notables, yr, lon)

data["regions"]["bordeaux_red"] = {
    "display_name": "Bordeaux (Red)",
    "country": "France",
    "primary_grapes": ["Cabernet Sauvignon", "Merlot", "Cabernet Franc"],
    "wine_style": "red",
    "vintages": bordeaux_red_vintages
}

# ============================================================
# BURGUNDY RED (1970-2023)
# ============================================================
br = {
    1970: (72, "Abundant crop diluted by rain. Light fruity wines without great depth or aging potential.", ["Domaine de la Romanee-Conti", "Domaine Leroy"], "medium"),
    1971: (87, "Small crop of concentrated wines from a hot dry summer. Rich Pinot Noir with good structure and depth.", ["Domaine de la Romanee-Conti", "Domaine Dujac", "Domaine Rousseau"], "medium"),
    1972: (62, "Cold wet growing season produced thin acidic wines. Poor ripeness made for a difficult vintage.", ["Domaine de la Romanee-Conti", "Domaine Leroy"], "medium"),
    1973: (68, "Generous yields from a warm vintage. Pleasant fruity wines that lacked concentration and aged quickly.", ["Domaine de la Romanee-Conti", "Domaine Henri Jayer"], "medium"),
    1974: (58, "Rain at harvest damaged the crop. Lean dilute wines with little character.", ["Domaine de la Romanee-Conti"], "medium"),
    1975: (55, "Rot from persistent rain devastated the harvest. Thin weedy wines that were largely unsuccessful.", ["Domaine de la Romanee-Conti", "Domaine Leroy"], "medium"),
    1976: (82, "Scorching summer and drought produced ripe concentrated wines, though some lacked acidity and dried out quickly.", ["Domaine de la Romanee-Conti", "Domaine Rousseau", "Domaine Ponsot"], "medium"),
    1977: (50, "Terrible cold wet vintage with no ripeness. Undrinkable thin wines from most producers.", ["Domaine de la Romanee-Conti"], "medium"),
    1978: (92, "Exceptional late-ripening vintage saved by a warm September and October. Beautifully balanced wines with depth and elegance.", ["Domaine de la Romanee-Conti", "Domaine Dujac", "Domaine Rousseau"], "medium"),
    1979: (80, "Good vintage with a large healthy crop. Attractive fruity wines with moderate concentration and good balance.", ["Domaine de la Romanee-Conti", "Domaine Henri Jayer", "Domaine Ponsot"], "medium"),
    1980: (70, "Cool vintage producing light but pleasant wines with decent acidity. Better than the difficult 1970s vintages.", ["Domaine de la Romanee-Conti", "Domaine Dujac"], "medium"),
    1981: (72, "Modest vintage of correct wines without excitement. Medium-bodied with moderate fruit and structure.", ["Domaine de la Romanee-Conti", "Domaine Rousseau"], "medium"),
    1982: (75, "Large crop from a hot summer. Ripe wines with soft tannins that matured quickly. Overproduction diluted many wines.", ["Domaine Henri Jayer", "Domaine Leroy", "Domaine de la Romanee-Conti"], "medium"),
    1983: (78, "Hail damage in some communes but warm conditions ripened the surviving fruit. Rich sometimes rustic wines, variable quality.", ["Domaine de la Romanee-Conti", "Domaine Roumier", "Domaine Ponsot"], "medium"),
    1984: (55, "Cold summer and fall rains produced thin underripe wines. One of the weakest vintages of the 1980s.", ["Domaine de la Romanee-Conti"], "medium"),
    1985: (93, "Perfect growing conditions with warm dry weather throughout. Silky elegant wines with beautiful fruit purity and fine tannins.", ["Domaine de la Romanee-Conti", "Domaine Henri Jayer", "Domaine Dujac"], "medium"),
    1986: (75, "Cool damp vintage producing lean structured wines. Decent acidity but lacking flesh and generosity.", ["Domaine de la Romanee-Conti", "Domaine Leroy"], "medium"),
    1987: (78, "Good vintage overshadowed by 1985 and 1988. Charming medium-weight wines with pleasant fruit and moderate structure.", ["Domaine Dujac", "Domaine Roumier", "Domaine Rousseau"], "medium"),
    1988: (89, "Classic vintage with excellent structure and acidity from a long cool growing season. Firm wines that aged beautifully.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
    1989: (85, "Warm generous vintage with early harvest. Ripe open wines with soft tannins and forward fruit.", ["Domaine de la Romanee-Conti", "Domaine Henri Jayer", "Domaine Dujac"], "medium"),
    1990: (95, "Outstanding vintage combining richness with structure. Deep concentrated wines with superb balance from an ideal growing season.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Henri Jayer"], "medium"),
    1991: (78, "Frost reduced the crop but surviving grapes ripened well in a warm autumn. Small lots of concentrated wine from top growers.", ["Domaine de la Romanee-Conti", "Domaine Dujac", "Domaine Roumier"], "medium"),
    1992: (65, "September rains diluted the harvest. Light watery wines from most producers, though a few made decent short-term wines.", ["Domaine de la Romanee-Conti", "Domaine Leroy"], "medium"),
    1993: (90, "Excellent vintage with superb color and concentration. Warm September after a cool start yielded rich structured wines with great aging potential.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
    1994: (68, "Harvest rains spoiled a promising vintage. Dilute wines with some rot-affected batches. Careful selection was essential.", ["Domaine de la Romanee-Conti", "Domaine Leroy"], "medium"),
    1995: (87, "Warm summer with timely rains. Rich round wines with sweet fruit and polished tannins. Very consistent vintage.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Dujac"], "medium"),
    1996: (92, "Brilliant vintage with extraordinary acidity and structure from cool nights. Precise mineral wines with stunning purity and longevity.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    1997: (76, "Early-ripening warm vintage. Pleasant forward wines with soft fruit but less structure and depth than 1996.", ["Domaine de la Romanee-Conti", "Domaine Dujac"], "medium"),
    1998: (78, "Uneven vintage with variable quality depending on harvest timing. Some attractive wines with good fruit but many diluted by rain.", ["Domaine de la Romanee-Conti", "Domaine Roumier", "Domaine Leroy"], "medium"),
    1999: (91, "Generous yields of ripe healthy fruit from a warm vintage. Seductive voluptuous wines with great depth and silky tannins.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
    2000: (82, "Warm vintage with some rain at harvest. Attractive forward wines for medium-term aging. Mildew pressure required vigilant viticulture.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    2001: (83, "Cool classic vintage producing elegant restrained wines with bright acidity. Not flashy but refined and age-worthy.", ["Domaine de la Romanee-Conti", "Domaine Roumier", "Domaine Dujac"], "medium"),
    2002: (90, "Late-season warmth concentrated the fruit after a difficult start. Powerful structured wines with great density and impressive aging potential.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    2003: (78, "Extreme heatwave produced atypical rich heavy wines. High alcohol and low acidity made for unusual Burgundy that divided opinion.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    2004: (76, "Large crop of pleasant fruity wines from a cool summer. Charming if lightweight, best consumed in the medium term.", ["Domaine de la Romanee-Conti", "Domaine Dujac"], "medium"),
    2005: (94, "Exceptional vintage with perfect ripeness and concentration. Rich powerful wines with great structure and intensity yet retaining Burgundian elegance.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    2006: (82, "Warm August after a mixed summer. Attractive wines with good fruit and moderate weight, if without the depth of 2005.", ["Domaine de la Romanee-Conti", "Domaine Roumier", "Domaine Dujac"], "medium"),
    2007: (80, "Variable vintage with rain at harvest. Lighter-styled fruity wines that matured quickly. Best from top domaines with strict selection.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
    2008: (83, "Cool vintage with good acidity producing classic lean wines with red fruit character. Improved considerably with bottle age.", ["Domaine de la Romanee-Conti", "Domaine Rousseau", "Domaine Dujac"], "medium"),
    2009: (91, "Warm generous vintage producing rich ripe wines with great depth and plush tannins. Forward and appealing from the start.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
    2010: (93, "Cool growing season with late harvest yielded intensely concentrated wines with vibrant acidity and remarkable precision. Age-worthy and complex.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    2011: (80, "Variable year with hail damage in some villages. Lighter elegant wines with good fruit where unaffected by storms.", ["Domaine de la Romanee-Conti", "Domaine Roumier", "Domaine Dujac"], "medium"),
    2012: (86, "Small crop from hail and poor flowering but concentrated healthy fruit. Rich focused wines with good structure from reduced yields.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    2013: (78, "Difficult vintage with late harvest and rain. Lighter wines with high acidity. Best showed charm and purity despite the challenges.", ["Domaine de la Romanee-Conti", "Domaine Dujac"], "medium"),
    2014: (85, "Warm dry September rescued a cool wet summer. Elegant bright wines with red fruit purity and fine tannins.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
    2015: (93, "Warm dry vintage with perfectly ripe fruit. Rich generous wines with beautiful depth and approachable tannins. Superb across the Cote d'Or.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    2016: (88, "Frost damage reduced crops dramatically but survivors produced concentrated elegant wines with fine acidity and mineral character.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
    2017: (85, "Early harvest from a warm growing season. Ripe charming wines with good fruit and moderate structure, approachable young.", ["Domaine de la Romanee-Conti", "Domaine Dujac", "Domaine Rousseau"], "medium"),
    2018: (88, "Hot dry summer produced rich concentrated wines with dark fruit character. Power balanced by good acidity in the best examples.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
    2019: (94, "Outstanding vintage with perfect balance of richness and freshness. Precise elegant wines with extraordinary purity and depth.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    2020: (93, "Warm early vintage producing deeply colored concentrated wines with remarkable energy and fine-grained tannins. Small crop but high quality.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
    2021: (87, "Cool classic vintage after spring frosts reduced crop. Elegant perfumed wines with bright acidity and finesse, recalling old-school Burgundy.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Dujac"], "medium"),
    2022: (89, "Drought year with early harvest. Concentrated wines with firm tannins and dark fruit, though some lacked the classic Burgundian delicacy.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Rousseau"], "medium"),
    2023: (86, "Moderate vintage with a warm dry summer after a damp spring. Balanced wines with good freshness and attractive red fruit.", ["Domaine de la Romanee-Conti", "Domaine Leroy", "Domaine Roumier"], "medium"),
}
burgundy_red_vintages = {}
for yr, (sc, desc, notables, lon) in br.items():
    burgundy_red_vintages[str(yr)] = v(sc, desc, notables, yr, lon)

data["regions"]["burgundy_red"] = {
    "display_name": "Burgundy (Red)",
    "country": "France",
    "primary_grapes": ["Pinot Noir"],
    "wine_style": "red",
    "vintages": burgundy_red_vintages
}

# ============================================================
# BURGUNDY WHITE (1970-2023)
# ============================================================
bw = {
    1970: (72, "Average vintage with decent acidity but lacking richness. Simple wines for early consumption.", ["Domaine Leflaive", "Domaine Ramonet"], "short"),
    1971: (78, "Warm vintage producing rich white Burgundy with good weight and moderate acidity.", ["Domaine Leflaive", "Domaine Coche-Dury"], "short"),
    1972: (65, "Cool year with high acidity and lean character. Thin wines without much fruit expression.", ["Domaine Leflaive"], "short"),
    1973: (72, "Large crop of pleasant everyday wines. Agreeable but lacking concentration.", ["Domaine Ramonet", "Domaine Leflaive"], "short"),
    1974: (60, "Difficult year with rain at harvest. Dilute wines with little interest.", ["Domaine Leflaive"], "short"),
    1975: (68, "Modest wines with decent structure but limited fruit richness.", ["Domaine Leflaive", "Domaine Ramonet"], "short"),
    1976: (76, "Hot drought year with rich heavy wines. Many lacked the acidity for long aging.", ["Domaine Leflaive", "Domaine Ramonet"], "short"),
    1977: (55, "Very weak vintage of thin underripe wines. Almost entirely forgettable.", ["Domaine Leflaive"], "short"),
    1978: (86, "Excellent vintage with ripe fruit balanced by firm acidity. Rich complex wines that aged gracefully.", ["Domaine Leflaive", "Domaine Ramonet", "Domaine Coche-Dury"], "short"),
    1979: (80, "Good crop of clean fresh wines with attractive fruit and moderate depth.", ["Domaine Leflaive", "Domaine Ramonet"], "short"),
    1980: (65, "Cool lean vintage producing simple wines with high acidity and little flesh.", ["Domaine Leflaive"], "short"),
    1981: (74, "Decent vintage with balanced wines showing moderate richness and clean flavors.", ["Domaine Leflaive", "Domaine Ramonet"], "short"),
    1982: (78, "Warm large crop of ripe generous whites. Pleasant and forward but many lacked staying power.", ["Domaine Leflaive", "Domaine Coche-Dury"], "short"),
    1983: (82, "Rich powerful wines from a warm vintage. Some of the best had excellent concentration and balance.", ["Domaine Ramonet", "Domaine Leflaive", "Domaine Coche-Dury"], "short"),
    1984: (68, "Cool vintage of lean crisp wines. Decent acidity but not much generosity.", ["Domaine Leflaive"], "short"),
    1985: (85, "Warm vintage with excellent ripe fruit and good structure. Generous complex wines from top sites.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    1986: (88, "Classic vintage with outstanding acidity and minerality. Steely structured wines that developed beautifully with age.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    1987: (72, "Modest vintage of pleasant light wines. Charming but without depth or complexity.", ["Domaine Leflaive", "Domaine Coche-Dury"], "short"),
    1988: (84, "Firm structured wines with excellent acidity and moderate richness. Classical age-worthy white Burgundy.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    1989: (88, "Opulent rich vintage from a hot summer. Generous wines with tropical fruit and creamy texture.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    1990: (87, "Another warm year producing rich wines. Slightly less acidity than 1989 but great depth and concentration.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    1991: (72, "Frost-affected vintage with reduced yields. Simple wines without great distinction.", ["Domaine Coche-Dury", "Domaine Leflaive"], "short"),
    1992: (86, "Excellent vintage with ripe healthy fruit and great balance. Rich wines with good acidity that proved very age-worthy.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    1993: (76, "Cool wet vintage producing lean wines with decent acidity. Better than the reds this year.", ["Domaine Leflaive", "Domaine Coche-Dury"], "short"),
    1994: (78, "Rain at harvest but careful sorting produced decent wines. Rich but sometimes lacking precision.", ["Domaine Coche-Dury", "Domaine Leflaive"], "short"),
    1995: (85, "Warm vintage producing rich opulent wines with good depth. Ripe fruit balanced by firm acidity.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    1996: (90, "Outstanding vintage with brilliant acidity and mineral intensity. Precise focused wines with exceptional aging potential.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    1997: (76, "Forward early-maturing wines from a warm season. Pleasant but premature oxidation affected many bottles.", ["Domaine Leflaive", "Domaine Coche-Dury"], "short"),
    1998: (75, "Mixed vintage with some pleasant wines though many showed early signs of oxidation. Inconsistent quality.", ["Domaine Coche-Dury", "Domaine Leflaive"], "short"),
    1999: (82, "Generous warm vintage producing ripe plush wines. Good concentration though many suffered premature oxidation later.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    2000: (82, "Rich warm year producing forward generous wines with moderate acidity. Premature oxidation issues affected some bottles.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    2001: (80, "Classical vintage with bright acidity and mineral character. Restrained elegant wines, though oxidation problems persisted.", ["Domaine Coche-Dury", "Domaine Leflaive"], "short"),
    2002: (88, "Superb vintage with rich fruit and great acidity. Powerful concentrated wines from ideal harvest conditions.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    2003: (72, "Extreme heat produced heavy wines with low acidity. Atypical white Burgundy that aged poorly in most cases.", ["Domaine Coche-Dury", "Domaine Leflaive"], "short"),
    2004: (82, "Good vintage with clean fruit and decent acidity. Attractive balanced wines for medium-term consumption.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    2005: (86, "Rich concentrated vintage from a warm dry year. Powerful wines that needed time to show their complexity.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    2006: (82, "Good vintage with attractive fruit and moderate weight. Clean well-made wines for medium-term drinking.", ["Domaine Coche-Dury", "Domaine Leflaive"], "short"),
    2007: (84, "Ripe generous wines from an early harvest. Good richness and approachable young, though some lacked acidity.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Ramonet"], "short"),
    2008: (85, "Classical cool-climate vintage with racy acidity and mineral drive. Lean but precise wines that improved with age.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2009: (84, "Warm vintage producing generous ripe wines. Forward and appealing with good fruit but moderate aging potential.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2010: (91, "Exceptional vintage with brilliant acidity and concentration. Intense mineral wines with outstanding structure and longevity.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2011: (80, "Warm early vintage with decent fruit. Pleasant wines that matured relatively quickly.", ["Domaine Leflaive", "Domaine Roulot", "Domaine Coche-Dury"], "short"),
    2012: (84, "Small crop of concentrated wines after poor flowering. Good richness and depth from naturally low yields.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2013: (85, "Cool vintage with excellent acidity and purity. Lean precise wines with great mineral character and aging potential.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2014: (90, "Outstanding vintage with ripe fruit and razor-sharp acidity. Generous complex wines with remarkable precision and depth.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2015: (84, "Warm vintage with ripe generous fruit. Rich wines that sometimes lacked the acidity of the best vintages.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2016: (87, "Frost-affected vintage with tiny yields but exceptional concentration. Intense mineral wines from a cool growing season.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2017: (88, "Excellent vintage with ripe fruit and great balance. Rich generous wines with good acidity and depth.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2018: (85, "Hot dry summer produced rich powerful wines. Best examples retained freshness through careful harvest timing.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2019: (88, "Warm vintage with balancing acidity. Generous wines with depth and minerality from well-managed vineyards.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2020: (89, "Early harvest of concentrated fruit with excellent natural acidity. Precise intense wines with great aging potential.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2021: (86, "Cool classic vintage with high acidity and lean profile. Mineral-driven wines recalling the great 2014s.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2022: (87, "Drought conditions concentrated the fruit. Rich wines with surprisingly good acidity from early-morning coolness.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
    2023: (85, "Balanced vintage with good fruit and fresh acidity. Attractive wines showing classic Burgundian minerality.", ["Domaine Coche-Dury", "Domaine Leflaive", "Domaine Roulot"], "short"),
}
burgundy_white_vintages = {}
for yr, (sc, desc, notables, lon) in bw.items():
    burgundy_white_vintages[str(yr)] = v(sc, desc, notables, yr, lon)

data["regions"]["burgundy_white"] = {
    "display_name": "Burgundy (White)",
    "country": "France",
    "primary_grapes": ["Chardonnay"],
    "wine_style": "white",
    "vintages": burgundy_white_vintages
}

with open("/Users/michaelpyon/VintageMap/backend/data/vintage/vintage_data.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Written {len(data['regions'])} regions so far")
for r in data["regions"]:
    print(f"  {r}: {len(data['regions'][r]['vintages'])} vintages")
