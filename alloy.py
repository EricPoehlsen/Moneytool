import random
from lxml import etree as et

from data import Metals


class Alloy(object):
    """ This class handles alloys ... """

    def __init__(self):
        self.alloy = {k: 0 for k in Metals.DATA}
        self.selector = []
        self.name = ""
        self.description = ""

    def selector_add(self, group):
        """ add a selector group to the selector """

        for metal in Metals.SELECTOR.get(group):
            if metal not in self.selector: self.selector.append(metal)

    def selector_del(self, group):
        """ delete a group from the selector """

        remove = Metals.SELECTOR.get(group)
        self.selector = [m for m in self.selector if m not in remove]

    def random_generation(self):
        # this will be the resulting alloy dict
        alloy = {}

        # selection lists for common metals, roughly sorted into three value groups
        high = ["Au", "Au", "Au", "Au", "Au", "Pt", "Pt", "Pd"]
        medium =["Ag", "Ag", "Ag", "Ag", "Ti"]
        low = ["Cu", "Cu", "Cu", "Fe", "Fe", "Al", "Sn", "Zn"]

        # creating the percentages for (up to three) metals in the alloy
        primary = min(random.randint(50, 105), 100)
        secondary = min(random.randint(0, 40), 100-primary)
        tertiary = max(0, 100-primary-secondary)
        parts = [primary, secondary, tertiary]
        parts = sorted([x for x in parts], reverse=True)

        # selecting three metal groups to smelt the alloy
        variants = [
            (high, high, high),
            (high, high, medium),
            (high, medium, medium),
            (medium, medium, high),
            (medium, medium, low),
            (medium, low, low),
            (low, low, medium),
            (low, low, low),
            (medium, low, low),
            (low, low, medium),
            (low, low, low)
        ]
        variant = random.choice(variants)

        # creating the alloy ...
        for amount, metals in zip(parts, variant):
            metal = random.choice(metals)
            amount = round(amount / 100, 2)
            if not amount: continue
            if alloy.get(metal): alloy[metal] += amount
            else: alloy[metal] = amount

        self.alloy = alloy

    def generate_from_value_cm3(self, value, elements=2):
        """ generate an alloy with a specific volumetric value
        Args:
            value (float): monetary value per cm³
            elements (int): number of elements in the alloy
        """

        higher = []
        lower = []
        prices = {}
        for metal, data in Metals.DATA.items():
            price = data[1] * data[2] / 1000
            prices[metal] = price
            if price > value:
                higher.append((metal, price))
            else:
                lower.append((metal, price))

        # we need elements with higher and lower values to get the desired alloy
        if not lower or not higher:
            raise ValueError("Target value outside range of available element values")

        # and we need enough elements for our alloy
        if len(lower) + len(higher) < elements:
            raise ValueError("not enough elements available for desired alloy")

        # select the elements to use ...
        while len(lower) + len(higher) > elements:
            if len(lower) > len(higher):
                lower.pop(random.randint(0,len(lower)-1))
            else:
                higher.pop(random.randint(0,len(higher)-1))

        def partial_alloy(elements):
            result = []
            percent = 100
            total_prices = 0
            for i, element in enumerate(elements):
                element = element[0]
                rest = len(elements) - i
                percentage = random.randint(1, percent - rest)
                if i == len(elements) - 1: percentage = percent
                percent -= percentage
                result.append([element, percentage])
                total_prices += percentage * Metals.DATA[element][1] * Metals.DATA[element][2] / 1000
            return (total_prices / 100, result)

        low_price, low_alloy = partial_alloy(lower)
        high_price, high_alloy = partial_alloy(higher)

        low_percent = (value - high_price) / (low_price - high_price)
        high_percent = 1 - low_percent

        alloy = {}
        for element in low_alloy:
            alloy[element[0]] = element[1] * low_percent / 100
        for element in high_alloy:
            alloy[element[0]] = element[1] * high_percent / 100

        # transforming volumetric alloy to mass based alloy:
        total_mass = 0
        transformed_alloy = {}
        for element, percentage in alloy.items():
            mass = percentage * Metals.DATA[element][1]
            transformed_alloy[element] = mass
            total_mass += mass
        for element in alloy:
            transformed_alloy[element] = transformed_alloy[element] / total_mass

        self.alloy = transformed_alloy

    def generate_from_density(self, density, elements=2):
        """ generate an alloy with a target density
        Args:
            density (float): target density g/cm³
            elements (int): number of elements in the alloy
        """

        # sort elements into groups with higher and lower density than the target
        lower = []
        higher = []
        for metal, data in Metals.DATA.items():
            if metal not in self.selector: continue
            if data[1] > density: higher.append((metal, data[1]))
            else: lower.append((metal, data[1]))

        # we need elements with higher and lower densities to get the desired alloy
        if not lower or not higher:
            raise ValueError("Target density outside range of available element densities")

        # and we need enough elements for our alloy
        if len(lower) + len(higher) < elements:
            raise ValueError("not enough elements available for desired alloy")

        # select the elements to use ...
        while len(lower) + len(higher) > elements:
            if len(lower) > len(higher):
                lower.pop(random.randint(0,len(lower)-1))
            else:
                higher.pop(random.randint(0,len(higher)-1))

        # create pseudo-random partial alloys
        def partial_alloy(elements):
            result = []
            percent = 100
            total_mass = 0
            for i, element in enumerate(elements):
                element = element[0]
                rest = len(elements) - i
                percentage = random.randint(1, percent - rest)
                if i == len(elements) - 1: percentage = percent
                percent -= percentage
                result.append([element, percentage])
                total_mass += percentage * Metals.DATA[element][1]
            return (total_mass / 100, result)

        low = partial_alloy(lower)
        high = partial_alloy(higher)
        low_density, low_alloy = low
        high_density, high_alloy = high

        # combine into one alloy
        low_percent = (density - high_density) / (low_density - high_density)
        high_percent = 1 - low_percent

        alloy = {}
        for element in low_alloy:
            alloy[element[0]] = element[1] * low_percent / 100
        for element in high_alloy:
            alloy[element[0]] = element[1] * high_percent / 100

        self.alloy = alloy

    def load_from_xml(self, filename):
        xml = et.parse(filename)
        name = xml.find("name").text
        desc = xml.find("description").text

    def save_to_xml(self, filename):
        """ write the current alloy as xml file
        Args:
            filename (str): the intended output filename

        Returns:
            bool: True if successfully written ...
        """

        if not filename: return False

        alloy_tag = et.Element("alloy")
        name_tag = et.SubElement(alloy_tag, "name")
        name_tag.text = self.name
        desc_tag = et.SubElement(alloy_tag, "description")
        desc_tag.text = self.description

        for k, v in self.alloy.items():
            # only store active elements
            if not v: continue

            et.SubElement(
                alloy_tag,
                "metal",
                attrib={"sym": k, "part": str(v)}
            )

        tree = et.ElementTree(alloy_tag)
        try:
            tree.write(filename, xml_declaration=True, pretty_print=True, encoding='UTF-8')
        except:
            return False

        return True

    def __str__(self):
        return str(self.alloy)

