from pathlib import Path
from tkinter import ttk
from tkinter import *


class ProfileMan:
    MINYEAR = 2018
    MAXYEAR = 2026

    def __init__(self, tree, cardTree):
        self.tree = tree
        self.cardTree = cardTree
        self.PROMPTDELETE = True

    def addCardToList(self, name, email, phone, address1, addressApt, address2, 
                      zipcode, city, state, country, cardnum, cardmonth, cardyear, cvv, popup=None):

        cardID = self.getNextCardNum()
        self.tree.insert("", "end", text=cardID, values=(name, email, phone, address1, addressApt, 
                                                         address2, zipcode, city, state, country))
        self.cardTree.insert("", "end", text=cardID, values=(cardnum, cardmonth, cardyear, cvv))

        if popup:
            popup.destroy()

    def addProfile(self):
        popup = Toplevel()
        popup.title("Create Profile")

        inputframe = Frame(popup)
        inputframe.grid(row=1, column=1, columnspan=2)

        Label(inputframe, text="Name: ").grid(row=1, column=1, sticky=W)
        nameEntry = Entry(inputframe, name="Name", width=10)
        nameEntry.grid(row=1, column=2, sticky=W)

        Label(inputframe, text="Email: ").grid(row=2, column=1, sticky=W)
        emailEntry = Entry(inputframe, name="Email", width=10)
        emailEntry.grid(row=2, column=2, sticky=W)

        Label(inputframe, text="Phone: ").grid(row=3, column=1, sticky=W)
        phoneEntry = Entry(inputframe, name="Phone", width=10)
        phoneEntry.grid(row=3, column=2, sticky=W)

        Label(inputframe, text="Address: ").grid(row=4, column=1, sticky=W)
        address1Entry = Entry(inputframe, name="Address1", width=10)
        address1Entry.grid(row=4, column=2, sticky=W)

        Label(inputframe, text="Apt / Unit: ").grid(row=5, column=1, sticky=W)
        addressAptEntry = Entry(inputframe, name="Apt", width=10)
        addressAptEntry.grid(row=5, column=2, sticky=W)

        Label(inputframe, text="Address 2: ").grid(row=6, column=1, sticky=W)
        address2Entry = Entry(inputframe, name="Address2", width=10)
        address2Entry.grid(row=6, column=2, sticky=W)

        Label(inputframe, text="Zip: ").grid(row=7, column=1, sticky=W)
        zipEntry = Entry(inputframe, name="Zip", width=10)
        zipEntry.grid(row=7, column=2, sticky=W)

        Label(inputframe, text="City: ").grid(row=8, column=1, sticky=W)
        cityEntry = Entry(inputframe, name="City", width=10)
        cityEntry.grid(row=8, column=2, sticky=W)

        Label(inputframe, text="State: ").grid(row=9, column=1, sticky=W)
        stateEntry = Entry(inputframe, name="State", width=10)
        stateEntry.grid(row=9, column=2, sticky=W)

        Label(inputframe, text="Country: ").grid(row=10, column=1, sticky=W)
        countryBox = Combobox(inputframe,
                                width=10,
                                name="Country",
                                state="readonly",
                                values=["USA", "Canada"])
        countryBox.grid(row=10, column=2, sticky=W)

        Separator(inputframe, orient=VERTICAL).grid(row=1, column=3, rowspan=10, sticky="ns", padx=3, pady=2)

        Label(inputframe, text="Card Num: ").grid(row=1, column=4, sticky=W)
        cardnumEntry = Entry(inputframe, name="Cardnum", width=10)
        cardnumEntry.grid(row=1, column=5, sticky=W)

        cardmonthBox = Combobox(inputframe,
                                width=3,
                                name="Cardmonth",
                                state="readonly",
                                values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
                                )
        cardmonthBox.grid(row=2, column=4, sticky=W)

        cardyearBox = Combobox(inputframe,
                                width=4,
                                name="Cardyear",
                                state="readonly",
                                values=[str(year) for year in range(self.MINYEAR, self.MAXYEAR+1)])
        cardyearBox.grid(row=2, column=5, sticky=W)

        Label(inputframe, text="CVV: ").grid(row=3, column=4, sticky=W)
        cvvEntry = Entry(inputframe, name="CVV", width=4)
        cvvEntry.grid(row=3, column=5, sticky=W)

        Button(popup,
                text="Add Profile",
                name="button_confirm",
                command=lambda: self.addCardToList(
                                                    nameEntry.get(),
                                                    emailEntry.get(),
                                                    phoneEntry.get(),
                                                    address1Entry.get(),
                                                    addressAptEntry.get(),
                                                    address2Entry.get(),
                                                    zipEntry.get(),
                                                    cityEntry.get(),
                                                    stateEntry.get(),
                                                    countryBox.get(),
                                                    cardnumEntry.get(),
                                                    cardmonthBox.get(),
                                                    cardyearBox.get(),
                                                    cvvEntry.get(),
                                                    popup
                                                    )
                ).grid(row=2, column=1)
        Button(popup, text="Cancel", command=popup.destroy).grid(row=2, column=2)
        return popup

    def editCard(self):
        itemToEdit = self.tree.focus()
        if itemToEdit != "":
            item = self.tree.item(itemToEdit)
            #product = Product(tkTreeValueList=item["values"])

            # re-use the popup created by addproduct()
            popup = self.addProfile()

            # rename the popup
            popup.title("Edit Product")

            # populate the popup widgets with existing data
            '''
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
                                                                ))'''

    def confirmDelete(self, itemID):
        # init popup
        popup = Toplevel()
        popup.title("Confirm Deleti")

        # contents of popup: show the card detail being deleted
        Label(popup, text="Are you sure you want to delete:\n").grid(row=1, column=1, columnspan=2)
        values = self.tree.item(itemID)["values"]
        dataStr = ""
        for value in values:
            if value != "":
                dataStr += str(value)+"\n"

        dataStr+="\n"
        values = self.cardTree.item(itemID)["values"]
        for value in values:
            if value != "":
                dataStr += str(value)+"\n"
        Label(popup, text=dataStr).grid(row=2, column=1, columnspan=2, sticky=W)


        # confirm or cancel
        Button(popup, text="Delete", command=lambda: self._deleteCard(itemID, popup)).grid(row=3, column=1)
        Button(popup, text="Cancel", command=popup.destroy).grid(row=3, column=2)



    def deleteCard(self):
        print(self.tree.focus())
        itemToDelete = self.tree.focus()
        if itemToDelete != "":
            if self.PROMPT_DELETE:
                self.confirmDelete(itemToDelete)
            else:
                self.tree.delete(itemToDelete)

    def getNextCardNum(self):
        if len(self.tree.get_children()) == 0:
            return 1
        else:
            return int(self.tree.get_children()[-1].lstrip("I"))+1


    def _deleteCard(self, itemID, popup=None):
        self.tree.delete(itemID)
        self.cardTree.delete(itemID)
        if popup:
            popup.destroy()
