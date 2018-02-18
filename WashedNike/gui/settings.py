from pathlib import Path
from tkinter import ttk
from tkinter import *

DEFAULTMINREFRESH = 0.35
DEFAULTMAXREFRESH = 0.75
DEFAULTCHECKOUTDELAY = 0.0

class Settings:
    def __init__(self, MINREFRESH=DEFAULTMINREFRESH, MAXREFRESH=DEFAULTMAXREFRESH, 
                    CHECKOUTDELAY=DEFAULTCHECKOUTDELAY):
        self.MINREFRESH = MINREFRESH
        self.MAXREFRESH = MAXREFRESH
        self.CHECKOUTDELAY = CHECKOUTDELAY

    def resetToDefault(self, filePath, minRefreshEntry, maxRefreshEntry, checkoutDelayEntry):
        minRefreshEntry.delete(0, END)
        minRefreshEntry.insert(0, DEFAULTMINREFRESH)

        maxRefreshEntry.delete(0, END)
        maxRefreshEntry.insert(0, DEFAULTMAXREFRESH)

        checkoutDelayEntry.delete(0, END)
        checkoutDelayEntry.insert(0, DEFAULTCHECKOUTDELAY)

        self.saveToFile(filePath, "", "", "")

    def loadFromFile(self, filePath):
        minrefresh = DEFAULTMINREFRESH
        maxrefresh = DEFAULTMAXREFRESH
        checkoutdelay = DEFAULTCHECKOUTDELAY

        setingsFilePath = Path(filePath)
        if setingsFilePath.is_file():
            with setingsFilePath.open() as f:
                try:
                    minrefresh = float(f.readline())
                    
                except:
                    None

        return Settings(minrefresh, maxrefresh, checkoutdelay)

    def saveToFile(self, filePath, minrefresh, maxrefresh, checkoutdelay):
        settingsFilePath = Path(filePath)
        with settingsFilePath.open(mode="w") as f:
            if minrefresh == "":
                f.write(str(DEFAULTMINREFRESH)+"\n")
            else:
                f.write(minrefresh+"\n")

            if maxrefresh == "":
                f.write(str(DEFAULTMAXREFRESH)+"\n")
            else:
                f.write(maxrefresh+"\n")
            if checkoutdelay == "":
                f.write(str(DEFAULTCHECKOUTDELAY)+"\n")
            else:
                f.write(checkoutdelay+"\n")