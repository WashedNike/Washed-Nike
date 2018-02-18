from pathlib import Path
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import csv

from gui.product import Product

class ProductMan:
    def __init__(self, tree):
        self.tree = tree
        self.PROMPT_DELETE = True

    def addProductToTree(self, cardID, site, keywords, category, size, colorKeywords, popup=None):
        '''
        Private method for adding products to the tree
        keywords and colorKeywords are comma-separated strings
        shoptype, size are "determined" strings (not very flexible)
        '''
        # add to the tree, and close the popup
        self.tree.insert("", "end", values=(cardID, site, keywords, category, size, colorKeywords))
        if popup:
            popup.destroy()


    def add_product(self):
        '''
        Public method that handles the UI for adding a product (via popup/Toplevel)
        '''
        # create pop up for entering details
        # wip: background color?
        popup = Toplevel()
        popup.title("Add a Product")

        #################################
        ####### Card Number
        Label(popup, text="Card ID:").grid(row=6, column=1, sticky=W)
        cardBox = Combobox(popup,
                           width=12,
                           name="combobox_cardID",
                           state="readonly",
                           values=self._get_list_card_nums())
        cardBox.grid(row=6, column=2, columnspan=2, sticky=W)

        Label(popup, text='Site').grid(row=7, column=1, sticky=W)
        siteBox = Combobox(popup,
                           width=12,
                           name="combobox_site",
                           state="readonly",
                           values=[("Supreme")]
                           )
        siteBox.grid(row=7, column=2, sticky=W)

        #################################
        # wip: specify case-sensitive?
        ####### Keyword Entry
        Label(popup, text="Keywords (comma-separated):").grid(row=1, column=1, sticky=W)
        keywordEntry = Entry(popup, name="entry_keywords", width=30)
        keywordEntry.grid(row=1, column=2, columnspan=2, sticky=W)

        #################################
        ####### size dropdown
        Label(popup, text="Size:").grid(row=3, column=1, sticky=W)
        sizeBox = Combobox(popup,
                           width=12,
                           state="readonly",
                           name="combobox_size")
        sizeBox.grid(row=3, column=2, columnspan=2, sticky=W)
        sizeBox.bind("<<ComboboxSelected>>", lambda x: self._manual_size_entry(popup, sizeBox))

        #################################
        ####### Shop type dropdown
        Label(popup, text="Category:").grid(row=2, column=1, sticky=W)
        typeBox = Combobox(popup,
                           width=12,
                           state="readonly",
                           name="combobox_type",
                           values=["jackets", "tops-sweaters", "sweatshirts", "t-shirts", "accessories", "shoes", "hats", "bags", "skate"])
        typeBox.grid(row=2, column=2, columnspan=2, sticky=W)

        # intialize the type box to jackets, and set sizing options accordingly
        typeBox.set("jackets")
        self._update_size_dropdown_values(popup, sizeBox, typeBox.get())

        # bind an action that forces size selection if type is changed
        typeBox.bind("<<ComboboxSelected>>", lambda x: self._update_size_dropdown_values(popup, sizeBox, typeBox.get()))

        #################################
        ####### color keywords
        Label(popup, text="Color(s) (comma-separated):").grid(row=4, column=1, sticky=W)
        colorEntry = Entry(popup, name="entry_colors", width=30)
        colorEntry.grid(row=4, column=2, columnspan=2, sticky=W)


        # Submit / add product to the tree via private method
        Button(popup,
               text="Add Product",
               name="button_confirm",
               command=lambda: self.addProductToTree(
                                                      cardBox.get(),
                                                      siteBox.get(),
                                                      keywordEntry.get(),
                                                      typeBox.get(),
                                                      self._get_size(popup),
                                                      colorEntry.get(),
                                                      popup
                                                      )
               ).grid(row=5, column=1)

        # or cancel the new product
        Button(popup, text="Cancel", command=popup.destroy).grid(row=5, column=2)
        return popup

    def edit_product(self):
        itemToEdit = self.tree.focus()
        if itemToEdit != "":
            item = self.tree.item(itemToEdit)
            product = Product(tkTreeValueList=item["values"])

            # re-use the popup created by add_product()
            popup = self.add_product()

            # rename the popup
            popup.title("Edit Product")

            # populate the popup widgets with existing data
            cardBox = popup.children["combobox_cardID"]
            cardBox.set(product.cardID)

            keywordEntry = popup.children["entry_keywords"]
            keywordEntry.delete(0, END)
            keywordEntry.insert(0, product.get_comma_str_keywords(product.keywordList))

            typeBox = popup.children["combobox_type"]
            typeBox.set(product.type)

            sizeBox = popup.children["combobox_size"]
            sizeBox.set(product.size)

            colorEntry = popup.children["entry_colors"]
            colorEntry.delete(0, END)
            colorEntry.insert(0, product.get_comma_str_keywords(product.colorList))

            # modify the add button to perform edit
            button = popup.children["button_confirm"]
            button.configure(text="Edit Product")
            button.configure(command=lambda: self._edit_product(
                                                                itemToEdit,
                                                                cardBox.get(),
                                                                keywordEntry.get(),
                                                                typeBox.get(),
                                                                self._get_size(popup),
                                                                colorEntry.get(),
                                                                popup
                                                                ))



    def _confirm_delete(self, itemID):
        '''
        Private method for initializing a popup to confirm deletion
        '''
        # init popup
        popup = Toplevel()
        popup.title("Confirm Delete")

        # contents of popup: show the card detail being deleted
        Label(popup, text="Are you sure you want to delete:\n").grid(row=1, column=1, columnspan=2)
        values = self.tree.item(itemID)["values"]
        dataStr = ""
        for value in values:
            dataStr += str(value)+"\n"
        Label(popup, text=dataStr).grid(row=2, column=1, columnspan=2, sticky=W)


        # confirm deletion (call private method) or cancel
        Button(popup, text="Delete", command=lambda: self._delete_product(itemID, popup)).grid(row=3, column=1)
        Button(popup, text="Cancel", command=popup.destroy).grid(row=3, column=2)

    def delete_product(self):
        '''
        Public method for handling deletion of a selected product
        '''
        # determine which item was selected
        itemToDelete = self.tree.focus()

        # ensure a selected item actually exists
        if itemToDelete != "":
            if self.PROMPT_DELETE: # if true, create popup to confirm delete
                self._confirm_delete(itemToDelete)
            else: # possibly useful for future unit tests
                self.tree.delete(itemToDelete)

    def save_products(self):
        '''
        Public method for handling saving the products to csv
        '''
        # wip file extension
        filepath = filedialog.asksaveasfilename()

        # when filepath is empty, the filedialog was cancelled...do nothing by returning
        if filepath == "":
            return

        with open(filepath, "w") as f:
            fields = ["cardID", "keywords", "category", "size", "colors"]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            # write each product as a row in csv
            for itemID in self.tree.get_children():
                item = self.tree.item(itemID)

                # handle the tree values via an object
                product = Product(tkTreeValueList=item["values"])
                writer.writerow({
                                "cardID": product.cardID,
                                "keywords": product.keywordTildas,
                                "category": product.type,
                                "size": product.size,
                                "colors": product.colorTildas
                })

    def load_products(self):
        '''
        Public method for handling loading products saved in a csv
        '''
        filepath = filedialog.askopenfilename()

        # if the filedialog was cancelled, just return
        if filepath == "":
            return
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            # for each row in the csv, add them to the tree
            for row in reader:
                self.tree.insert('', 'end',
                    values=Product(dictrow=row).to_tree_tuple()
                )

    def _edit_product(self, itemID, cardID, keywordCommaStr, category, size, colorCommaStr, popup=None):
        '''
        Private method for handling editing a product.
        Recreate an "add-product" popup and populate the values
        with the selected item (via itemID)
        '''
        self.tree.set(itemID, column="cardID", value=cardID)
        self.tree.set(itemID, column="keywords", value=keywordCommaStr)
        self.tree.set(itemID, column="type", value=category)
        self.tree.set(itemID, column="size", value=size)
        self.tree.set(itemID, column="color", value=colorCommaStr)
        if popup:
            popup.destroy()




    def _delete_product(self, itemID, popup=None):
        '''
        Private method for specifically deleting an item from the tree
        closes the popup when done
        '''
        self.tree.delete(itemID)
        if popup:
            popup.destroy()

    def _get_size(self, popup):
        '''
        Private method for determining the size (either from dropdown or manual entry)
        '''
        if "entry_manual_size" in popup.children.keys():
            return popup.children["entry_manual_size"].get()
        # wip: check for other, OR THROW ERROR
        elif popup.children["combobox_size"].get() == "SELECT":
            return "FIX THIS"
        else:
            return popup.children["combobox_size"].get()


    def _update_size_dropdown_values(self, popup, sizeBox, category):
        '''
        Private method for populating the dropdown options for the sizing
        options for sizing is dependent on the category!
        '''
        sizeBox.set("SELECT")
        self._manual_size_entry(popup, sizeBox)

        #["jackets", "tops-sweaters", "sweatshirts", "t-shirts", "accessories", "shoes", "hats", "bags", "skate"]
        values = ["Manually Enter", "Any Size", "Small", "Medium", "Large", "Xlarge"]
        if category == "accessories" or category == "bags" or category == "hats":
            values.append("S/M")
            values.append("X/XL")
        if category == "skate" or category == "shoes":
            values.append("--COMING SOON--")
        sizeBox.configure(values=values)

    def _manual_size_entry(self, popup, sizeBox):
        '''
        Private method for enabling/disabling manual size entry
        '''
        if sizeBox.get() == "Manually Enter":
            sizeBox.grid(row=3, column=2, columnspan=1, sticky=W)
            Entry(popup, width=10, name="entry_manual_size").grid(row=3, column=3, sticky=W)
        else:
            if "entry_manual_size" in popup.children.keys():
                popup.children["entry_manual_size"].destroy()
            sizeBox.grid(row=3, column=2, columnspan=2, sticky=W)

    def _get_list_card_nums(self):
        # traverse up the hierarchy to product frame and then the notebook
        productFrame = self.tree.nametowidget(self.tree.winfo_parent())
        notebook = productFrame.nametowidget(productFrame.winfo_parent())

        # traverse down the hierarchy to card frame and then the tree
        cardTree = notebook.children["cards"].children["tree_cards"]

        # iterate the cards, and retrieve their text (tied to id)
        returnList = []
        for cardItem in cardTree.get_children():
            returnList.append(cardTree.item(cardItem)["text"])

        return returnList
