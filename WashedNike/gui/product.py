class Product:
    def __init__(self, TreeValueList=None, dictrow=None):
        if TreeValueList:
            self.cardID = TreeValueList[0]

            self.site = TreeValueList[1]

            self.keywordTildas = self.tilda_keywords(tkTreeValueList[2])

            self.type = tkTreeValueList[3]

            self.size = tkTreeValueList[4]

            self.colorTildas = self.tilda_keywords(tkTreeValueList[5])

            self.keywordList = self.parse_keywords_to_list(tkTreeValueList[1])

            self.colorList = self.parse_keywords_to_list(tkTreeValueList[4])
        if dictrow:
            self.cardID = dictrow["cardID"]
            self.keywordTildas = dictrow["keywords"]
            self.type = dictrow["category"]
            self.size = dictrow["size"]
            self.colorTildas = dictrow["colors"]
            self.site = dictrow["site"]

            self.keywordList = dictrow["keywords"].split("~")
            self.colorList = dictrow["colors"].split("~")

    def tilda_keywords(self, keywordsCommaStr):
        '''
        Converts keyword comma string ("Hanes, Boxers")
        into tilda-delimtied ("Hanes~Boxers")
        '''
        splits = keywordsCommaStr.split(",")
        returnStr = ""
        for keyword in splits:
            returnStr+=keyword.strip()+"~"
        return returnStr[:-1]


    def parse_keywords_to_list(self, keywordsCommaStr):
        '''
        converts keyword comma string ("Hanes, Boxers")
        into a list of strings (["Hanes", "Boxers"])
        '''
        splits = keywordsCommaStr.split(",")
        newList = []
        for keyword in splits:
            newList.append(keyword.strip())
        return newList

    def get_comma_str_keywords(self, kwList):
        returnStr = ""
        for kw in kwList:
            returnStr += kw+", "
        return returnStr[:-2]

    def to_tree_tuple(self):
        '''
        Converts a Product instance into a tuple of strings
        primarily for inserting into tk.Treeview
        '''
        keywordCommaStr = ""
        for keyword in self.keywordList:
            keywordCommaStr += keyword+", "
        keywordCommaStr = keywordCommaStr[:-2]

        colorCommaStr = ""
        for color in self.colorList:
            colorCommaStr += color+", "
        colorCommaStr = colorCommaStr[:-2]

        return (self.cardID, keywordCommaStr, self.type, self.size, colorCommaStr)
