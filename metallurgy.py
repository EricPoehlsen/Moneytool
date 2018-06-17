import tkinter as tk
import tkinter.filedialog as tkfd
from lxml import etree as et
import data
from alloy import Alloy

S = data.DE

class Metallurgy(tk.Frame):
    def __init__(self, screen):

        super().__init__(screen)

        self.widgets = {}

        self.alloy = Alloy()
        self.alloy_value = 0
        self.alloy_density = 0

        self.left_column = tk.Label(self)
        self.build_selector()
        self.left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.smelting_pot = tk.LabelFrame(self, text=S.MELTING_POT)
        self.build_smelting_pot()
        self.smelting_pot.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def build_selector(self):

        self.widgets["metal_filter"] = {}
        selector = tk.LabelFrame(self.left_column, text=S.METAL_GROUPS)
        for i in range(4):
            w = self.widgets["metal_filter"][i] = tk.Checkbutton(selector)
            var = tk.IntVar()
            var.set(1)
            var.trace("w", self.filter)
            w.config(text=S.METAL_SELECTION[i], variable=var)
            w.var = var
            w.pack(anchor=tk.W)
        selector.pack(fill=tk.X, expand=1)

        sorter = tk.LabelFrame(self.left_column, text=S.METAL_SORT)
        criteria = ["name", "value", "amount", "density"]
        for c in criteria:
            button = tk.Button(
                sorter,
                text=S.METAL_SORTER[c],
                command=lambda e=c: self.filter(e)
            )
            button.pack(side=tk.LEFT)
        sorter.pack(fill=tk.X, expand=1)

        label = tk.LabelFrame(self.left_column, text="Name")
        entry = self.widgets["name"] = tk.Entry(label)
        entry.pack(fill=tk.X, expand=1)
        label.pack(fill=tk.X, expand=1)

        label = tk.LabelFrame(self.left_column, text="Beschreibung")
        desc = self.widgets["description"] = tk.Text(label)
        desc.config(width=30, height=10, wrap=tk.WORD)
        desc.pack(fill=tk.X, expand=1)
        label.pack(fill=tk.X, expand=1)

        frame = tk.Frame(self.left_column)
        save = tk.Button(frame, text="save", command=self.xml_save_alloy)
        save.pack(side=tk.LEFT, fill=tk.X, expand=1)
        load = tk.Button(frame, text="load", command=self.xml_load_alloy)
        load.pack(side=tk.LEFT, fill=tk.X, expand=1)
        frame.pack(fill=tk.X, expand=1)

    def build_smelting_pot(self):
        """ build the metallurgy lab frame """

        self.widgets["metal_slider"] = {}
        self.widgets["metal_relative"] = {}
        self.widgets["metal_names"] = {}
        sliders = self.widgets["metal_slider"]
        value = self.widgets["metal_relative"]
        name = self.widgets["metal_names"]

        self.smelting_pot.columnconfigure(1, weight=1)

        for i, m in enumerate(data.Metals.DATA):

            name[m] = tk.Label(self.smelting_pot, text=S.METALS[m], anchor=tk.W)
            name[m].grid(row=i, column=0, sticky=tk.W)
            sliders[m] = tk.Scale(
                self.smelting_pot,
                from_=0,
                to=1,
                showvalue=0,
                resolution = 0.001,
                orient=tk.HORIZONTAL
            )
            sliders[m].bind("<B1-Motion>", lambda e, m=m: self.update_slider(e, m))
            sliders[m].bind("<ButtonRelease-1>", lambda e, m=m: self.force_update(e, m))
            sliders[m].grid(row=i, column=1, sticky=tk.EW)
            text = str(round(self.alloy.alloy[m]*100, 2)) + " %"
            value[m] = tk.Label(self.smelting_pot, text=text, width=7, anchor=tk.E)
            value[m].grid(row=i, column=2)


    def update_slider(self, event, metal):
        old_value = self.alloy.alloy[metal]
        cur_value = self.alloy.alloy[metal] = event.widget.get()
        diff = cur_value - old_value

        active = {k: v for k, v in self.alloy.alloy.items() if k != metal and v > 0}
        total = sum(v for v in active.values())
        for k, v in active.items():
            self.alloy.alloy[k] += -diff * v / total
            self.widgets["metal_slider"][k].set(self.alloy.alloy[k])

            text = str(abs(round(100*self.alloy.alloy[k], 2))) + " %"
            self.widgets["metal_relative"][k].config(text=text)

        text = str(round(100*self.alloy.alloy[metal], 2)) + " %"
        self.widgets["metal_relative"][metal].config(text=text)

        if len(active) == 0:
            self.alloy.alloy[metal] = 1
            self.widgets["metal_slider"][metal].set(1)

        self.smelt()

    def force_update(self, event, metal):
        """ force update after release ... """
        event.widget.set(self.alloy.alloy[metal])
        text = str(round(100*self.alloy.alloy[metal], 2)) + " %"
        self.widgets["metal_relative"][metal].config(text=text)

    def smelt(self):
        """ smelt your metals to create an alloy """

        volume = 0
        price = 0

        # calculate mass percentage
        for name, value in self.alloy.alloy.items():

            # adding to price
            price += value / 1000 * data.Metals.DATA[name][2]
            volume += value / data.Metals.DATA[name][1]

        try:
            density = 1 / volume
            value = price
        except ZeroDivisionError:
            density = 0
            value = 0

        self.alloy_density = density
        self.alloy_value = value

    def filter(self, n=None, e=None, m=None):
        """ filter and sort the metals in the smelting pot """

        # filter based on the selector
        selection = []
        for i in range(4):
            if self.widgets["metal_filter"][i].var.get() == 1:
                selection += data.Metals.SELECTOR[i]

        selection = [x for x in selection]
        metal_data = data.Metals.DATA.items()

        l = [(m, S.METALS[m]) for m in selection]
        l = sorted(l, key=lambda d: d[1])

        if n == "name":
            l = [(m, S.METALS[m]) for m in selection]
            l = sorted(l, key=lambda d: d[1])

        elif n == "density":
            l = [(s, d[1]) for s, d in metal_data if s in selection]
            l = sorted(l, key=lambda d: d[1], reverse=True)

        elif n == "amount":
            l = [(m, self.alloy.alloy[m]) for m in selection]
            l = sorted(l, key=lambda d: d[1], reverse=True)

        elif n == "value":
            l = [(s, d[2]) for s, d in metal_data if s in selection]
            l = sorted(l, key=lambda d: d[1], reverse=True)

        w_abs = self.widgets["metal_slider"]
        w_rel = self.widgets["metal_relative"]
        w_name = self.widgets["metal_names"]

        # remove visibility for all entries
        for w in w_abs.values(): w.grid_forget()
        for w in w_rel.values(): w.grid_forget()
        for w in w_name.values(): w.grid_forget()

        for i, v in enumerate(l):
            w_name[v[0]].grid(row=i, column=0, sticky=tk.W)
            w_abs[v[0]].grid(row=i, column=1)
            w_rel[v[0]].grid(row=i, column=2)

    def xml_load_alloy(self):
        """ loading an alloy from an xml file """

        options = {
            'defaultextension': '.xml',
            'filetypes': [("XML", '.xml')],
            # 'initialdir': './chars',
            # 'initialfile': suggested_filename,
            'parent': self,
            'title': "Save alloy",
        }
        file_name = tkfd.askopenfilename()
        if not file_name: return

        alloy = et.parse(file_name)
        name = alloy.find("name").text
        desc = alloy.find("description").text
        self.widgets["name"].delete("0", tk.END)
        self.widgets["name"].insert("0", name)
        self.widgets["description"].delete("0.0", tk.END)
        self.widgets["description"].insert("0.0", desc)

    def xml_save_alloy(self):
        """ storing the alloy to a xml file """

        options = {
            'defaultextension': '.xml',
            'filetypes': [('XML File', '.xml')],
            'initialdir': './alloys',
            'initialfile': 'alloy.xml',
            'parent': self,
            'title': "Save alloy",
            }
        file_name = tkfd.asksaveasfilename()

        if not file_name: return

        alloy = et.Element("alloy")
        name = self.widgets["name"].get()
        name_tag = et.SubElement(alloy, "name")
        name_tag.text = name
        desc = self.widgets["description"].get("0.0", tk.END)
        desc_tag = et.SubElement(alloy, "description")
        desc_tag.text = desc

        for k, v in self.alloy.alloy.items():
            # only store active elements
            if not v: continue

            et.SubElement(
                alloy,
                "metal",
                attrib={"sym": k, "part": str(round(v, 3))}
            )

        tree = et.ElementTree(alloy)
        tree.write(file_name, xml_declaration=True, pretty_print=True, encoding='UTF-8')


class MetallurgyWindow(tk.Toplevel):
    def __init__(self, master, number):
        """ This creates a toplevel metallurgy window

        Args:
            number (int): number of the entry in CoinGenerator
        """

        super().__init__(master)
        self.number = number

        self.main_frame = Metallurgy(self)
        self.load_alloy()
        self.main_frame.pack(side=tk.TOP)
        remove_button = tk.Button(
            self,
            text=S.REMOVE_ALLOY,
            command=lambda:self.destroy(mode="remove")
        )
        remove_button.pack(side=tk.TOP, fill=tk.X)

    def load_alloy(self):
        """ loading the current alloy into the editor """

        # get the widgets
        sliders = self.main_frame.widgets["metal_slider"]
        value = self.main_frame.widgets["metal_relative"]

        # get the alloy
        alloy = self.master.coins[self.number].get("alloy", None)

        # ... go ...
        if alloy:
            self.main_frame.alloy = {metal: 0 for metal in data.Metals.DATA}
            for metal, percentage in alloy.items():
                self.main_frame.alloy[metal] = percentage
                sliders[metal].set(percentage)
                text = str(abs(round(100 * alloy[metal], 2))) + " %"
                value[metal].config(text=text)

    def destroy(self, mode="save"):
        """ destroy the toplevel window and write the alloy back to the app """

        alloy = self.main_frame.alloy
        if mode == "remove": alloy = None

        # writing app coin data ...
        coins = self.master.coins
        coins[self.number]["alloy"] = alloy

        # updating the button ...
        text = ""
        if alloy:
            short_alloy = [(v, k) for k, v in alloy.alloy.items() if v]
            short_alloy = sorted(short_alloy, reverse=True)

            for entry in short_alloy:
                v, k = entry
                text += k + ": " + str(round(v * 100, 2)) + "% - "
            text = text[:-3]
        else: text="Legierung"
        button = coins[self.number]["widgets"][2]
        button.config(text=text)

        # done ...
        super().destroy()