# core data for the metals
class Metals(object):
    DATA = {
        # SYM: ORD, DENSE, PRICE
        "Au": [79, 19.32, 42000],
        "Al": [13, 2.699, 2.5],
        "Be": [4, 1.848, 7500],
        "Mg": [12, 1.738, 6],
        "Cr": [24, 7.14, 8],
        "Fe": [28, 7.87, 0.1],
        "Pt": [78, 21.45, 35000],
        "Pd": [46, 11.99, 32000],
        "Ni": [28, 8.903, 30],
        "Cu": [29, 8.92, 10],
        "Ir": [77, 22.56, 35000],
        "Ag": [47, 10.4, 750],
        "V": [23, 6.11, 15],
        "Sn": [50, 7.265, 20],
        "Zn": [30, 7.14, 4],
        "Pb": [82, 11.342, 2],
        "Os": [76, 22.59, 30000],
        "Ti": [22, 4.5, 150],
        "W": [74, 19.3, 30],
    }

    SELECTOR = {
        0: ["Au", "Ag", "Cu"],
        1: ["Al", "Ni", "Fe", "Sn", "Zn"],
        2: ["Be", "Pt", "Pd", "Ir", "Os"],
        3: ["Mg", "Cr", "V", "Pb", "Ti", "W"]
    }

class Export(object):
    DPI = 300
    MARGIN = 10

class DE(object):
    """ language class for German """

    METALS = {
        "Au": "Gold",
        "Al": "Aluminium",
        "Be": "Beryllium",
        "Mg": "Magnesium",
        "Cr": "Chrom",
        "Fe": "Eisen",
        "Pt": "Platin",
        "Pd": "Palladium",
        "Ni": "Nickel",
        "Cu": "Kupfer",
        "Ir": "Iridium",
        "Ag": "Silber",
        "V":  "Vanadium",
        "Sn": "Zinn",
        "Zn": "Zink",
        "Pb": "Blei",
        "Os": "Osmium",
        "Ti": "Titan",
        "W": "Wolfram"
    }

    METAL_SELECTION = [
        "die Klassiker",
        "übliche Münzmetalle",
        "wertvolle Metalle",
        "weitere Metalle"
    ]

    METAL_SORTER = {
        "name": "Name",
        "value": "Wert",
        "amount": "Anteil",
        "density": "Dichte"
    }

    MENU_FILE = "Datei"
    MENU_OPEN = "Öffnen ..."
    MENU_SAVE = "Speichern ..."
    MENU_EXIT = "Beenden"

    MENU_TOOLS = "Werkzeuge"
    MENU_ABOUT = "About ..."

    MENU_COIN_DESIGNER = "Münzdesigner"
    MENU_COIN_GENERATOR = "Münzgenerator"
    MENU_METALLURGY = "Legierung schmelzen"

    GENERATE_COINS = "Münzen erzeugen ..."
    GENERATE_SHAPES = "Formen berechnen ..."
    GENERATE_VALUES = "Werte berechnen ..."
    GENERATE_ALLOYS = "Legierungen erzeugen ..."
    ADD_COIN = "Münze hinzufügen ..."

    METAL_GROUPS = "Metalle eingrenzen: "
    METAL_SORT = "Sortierung: "
    MELTING_POT = "Schmelztigel"
    RESULT = "Ergebnis: "
    VOLUME = "Volumen: "
    WEIGHT = "Gewicht: "
    VALUE = "Wert: "
    REMOVE_ALLOY = "Legierung entfernen"

    ACCEPT = "Übernehmen"
    CANCEL = "Abbrechen"
    DELETE = "Entfernen"

    ABOUT_TITLE = "MoneyTool"
    ABOUT_VERSION = "-"
    ABOUT_AUTHOR = "Eric Pöhlsen"

    SELECT_SHAPE = "Form bestimmen"

    SHAPES = {
        "circle": "Kreis",
        "rect": "Rechteck",
        "poly": "Vieleck",
        "generic": "unbestimmt"
    }

    SHAPE_DIMENSIONS = {
        "radius": "Radius",
        "inner_radius": "Innenradius",
        "length": "Länge",
        "width": "Breite",
        "thickness": "Dicke",
        "sides": "Seiten",
        "chamfer": "Fase",
        "corner_radius": "Abrundung"
    }


class EN(DE):
    """ language class for """
    METALS = {
        "Au": "Gold",
        "Al": "Aluminium",
        "Be": "Beryllium",
        "Mg": "Magnesium",
        "Cr": "Chrome",
        "Fe": "Iron",
        "Pt": "Platinum",
        "Pd": "Palladium",
        "Ni": "Nickel",
        "Cu": "Copper",
        "Ir": "Iridium",
        "Ag": "Silver",
        "V":  "Vanadium",
        "Sn": "Tin",
        "Zn": "Zinc",
        "Pb": "Lead",
        "Os": "Osmium",
        "Ti": "Titanium",
        "W": "Tungsten"
    }


"""
Bronze: < 60% Kupfer (ohne Zink)
Messing: Kupferlegierung mit Zink (bis 40%) 

"""