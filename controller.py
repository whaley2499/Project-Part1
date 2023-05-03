from PyQt5.QtWidgets import *
from view import *
import csv

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QStackedWidget, Ui_ShoppingTool):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.__cart = {}
        self.displayCart()

        self.Button_submitUser.clicked.connect(lambda: self.cartOptions())

        self.Button_submitAdd.clicked.connect(lambda: self.addItem())
        self.Button_cancelAdd.clicked.connect(lambda: self.displayCart())

        self.Button_submitMod.clicked.connect(lambda: self.modItem())
        self.Button_cancelMod.clicked.connect(lambda: self.displayCart())

        self.Button_submitDelete.clicked.connect(lambda: self.delItem())
        self.Button_cancelDel.clicked.connect(lambda: self.displayCart())

        self.Button_submitPrintBill.clicked.connect(lambda: self.printBill())
        self.Button_cancelPrintBill.clicked.connect(lambda: self.displayCart())
        self.__cart['item'] = (2.50,3)

#TODO: Fix output formatting    
#TODO: Impliment error displays
    def displayCart(self) -> None:
        '''
        Displays the user's items on the cart page.
        '''
        if len(self.__cart) > 0:
            self.output_cart.setText(f"{sorted(self.__cart.values(), key = lambda item: item[1])}")
        else:
            self.output_cart.setText("Your cart is empty")
        self.setCurrentIndex(3)
    
    def cartOptions(self) -> None:
        '''
        Changes page from the cart based on radio selected by user
        '''
        if self.radio_add.isChecked():
            self.setCurrentIndex(0)
        elif self.radio_mod.isChecked() and len(self.__cart) > 0:
            self.setCurrentIndex(1)
        elif self.radio_delete.isChecked() and len(self.__cart) > 0:
            self.setCurrentIndex(2)
        elif self.radio_printBill.isChecked() and len(self.__cart) > 0:
            self.setCurrentIndex(4)
        else:
            self.output_cart.setText("Error")

    def addItem(self) -> None:
        '''
        Adds a new item to the user's cart.
        '''
        try:
            name = str(self.input_itemName.text()) 
            price = float(self.Input_itemPrice.text()) 
            quantity = int(self.Input_itemQuantity.text())
        except:
            self.label_addToCart.setText("Please enter the price and quantity")
            return
        self.__cart[name] = (price, quantity)
        self.displayCart()

    def modItem(self) -> None:
        '''
        Changes an existing item in the user's cart.
        '''
        if self.input_itemNameMod.text() in self.__cart.keys():
            try:
                name = str(self.input_itemNameMod.text()) 
                price = float(self.Input_itemPriceMod.text()) 
                quantity = int(self.Input_itemQuantityMod.text())
            except:
                self.label_modItem.setText("Please enter the price and quantity")        
        else:
            self.label_modItem.setText("Please select an item in your cart")

        self.__cart[name] = (price, quantity)
        self.displayCart()

    def delItem(self) -> None:
        '''
        Deletes an item from the user's cart.
        '''
        if len(self.input_itemNameDelete.text()) > 0:
            try:
                name = str(self.input_itemNameDelete.text())
            except:
                self.label_delItem.setText("Item is not in cart")
        else:
            self.label_delItem.setText("You need to type an Item's name")
        del self.__cart[name]
        self.displayCart()
    
    def printBill(self) -> None:
        if len(self.Input_billName.text()) > 0:
            try:
                fileName = self.Input_billName.text().strip() + ".csv"
            except:
                self.label_errorBill.setText("File name invalid")
        else:
             self.label_errorBill.setText("Please enter a name for the file")
             return
#TODO: Change to formatted text instead of csv
        with open(fileName, 'w', newline='') as outfile:
            bill = csv.writer(outfile, delimiter=',')
            for item in self.__cart.keys():
                price, quantity = self.__cart[item]
                bill.writerow([item, f"{price:.2f}", quantity])
        self.__cart = {}
        self.displayCart()