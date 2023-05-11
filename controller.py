from PyQt5.QtWidgets import *
from view import *
from pathlib import Path
from typing import TextIO


QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QStackedWidget, Ui_ShoppingTool):
    def __init__(self, *args, **kwargs) -> None:
        '''
        Initializes the controller, widget pages, and the cart dictionary.
        '''
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
  
    def displayCart(self) -> None:
        '''
        Displays the user's items on the cart page.
        '''
        if len(self.__cart) > 0:
            text=""
            for item in self.__cart.keys():
                price, quantity = self.__cart[item]
                text += f"{item:<10} ${price:^5.2f} {quantity:>10}\n"
            self.output_cart.setText(f"Item-----Price-----Quantity\n{text}")
        else:
            self.output_cart.setText("Your cart is empty")
        self.setCurrentIndex(3)
    
    def cartOptions(self) -> None:
        '''
        Changes page from the cart based on radio selected by user
        '''
        if (self.radio_delete.isChecked() or self.radio_mod.isChecked() or self.radio_printBill.isChecked()) and len(self.__cart) == 0:
            self.label_errorCart.setText("Invalid option for an empty cart")
        elif self.radio_add.isChecked():
            self.setCurrentIndex(0)
            self.label_errorCart.setText("")
        elif self.radio_mod.isChecked():
            self.setCurrentIndex(1)
            self.label_errorCart.setText("")
        elif self.radio_delete.isChecked():
            self.setCurrentIndex(2)
            self.label_errorCart.setText("")
        elif self.radio_printBill.isChecked():
            self.setCurrentIndex(4)
            self.label_errorCart.setText("")
        else:
            self.label_errorCart.setText("Option selection required")

    def addItem(self) -> None:
        '''
        Adds a new item to the user's cart.
        '''
        if len(self.input_itemName.text()) and len(self.Input_itemPrice.text()) and len(self.Input_itemQuantity.text()) > 0:
            try:
                name = str(self.input_itemName.text().strip()) 
                price = float(self.Input_itemPrice.text().strip()) 
                quantity = int(self.Input_itemQuantity.text().strip())
                self.__cart[name] = (price, quantity)
                self.label_errorAdd.setText("")
                self.displayCart()
            except:
                self.label_errorAdd.setText("Please enter the price and quantity")
        else:
            self.label_errorAdd.setText("Enter the name, price, and quantity")
        

    def modItem(self) -> None:
        '''
        Changes an existing item in the user's cart.
        '''
        if self.input_itemNameMod.text().strip() in self.__cart.keys():
            try:
                name = str(self.input_itemNameMod.text().strip())
                price = float(self.Input_itemPriceMod.text().strip()) 
                quantity = int(self.Input_itemQuantityMod.text().strip())

                self.__cart[name] = (price, quantity)
                self.label_errorMod.setText("")  
                self.displayCart()
            except:
                self.label_errorMod.setText("Enter the price and quantity")        
        else:
            self.label_errorMod.setText("Please select an item in your cart")

        

    def delItem(self) -> None:
        '''
        Deletes an item from the user's cart.
        '''
        if len(self.input_itemNameDelete.text().strip()) > 0:
            try:
                name = str(self.input_itemNameDelete.text().strip())
                del self.__cart[name]
                self.label_errorDel.setText("")
                self.displayCart()
            except:
                self.label_errorDel.setText("Item is not in cart")
        else:
            self.label_errorDel.setText("Please enter an item's name")
        
    def printBill(self) -> TextIO:
        '''
        Prints the items, their prices and a total
        '''
        if len(self.Input_billName.text()) > 0:
            try:
                fileName = Path("Bills/" + self.Input_billName.text().strip() + ".txt")
                if fileName.is_file():
                    self.label_errorBill.setText("A file with this name already exists")
                else:
                    with open(fileName, 'w') as outputFile:
                        outputFile.write("----Bill----\n")
                        total = 0
                        for item in self.__cart.keys():
                            price, quantity = self.__cart[item]
                            total += (price * quantity)
                            outputFile.write(f"{item} (x{quantity}): ${(price*quantity):.2f}\n")
                        outputFile.write(f"TOTAL: ${total}")

                    self.__cart = {}
                    self.label_errorBill.setText("")
                    self.displayCart()
            except:
                self.label_errorBill.setText("Please enter a valid file name")
        else:
             self.label_errorBill.setText("Please enter a name for the file")