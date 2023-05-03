
# You can store items however you wish, this is just an example, 
# However, I recommend a dictionary so the starter code is structured around using a dictionary 'items'
 
# string -> (price, quantity)
items = dict()

def add_item():
    name = input("Enter the name of the item to add: ")
    price = float(input("Enter the price of the item: "))
    quantity = int(input("Enter the quantity: "))
    
    items[name] = (price, quantity)

def update_item():
    # TODO: implement the update function
    name = input("Enter the name of the item to update: ")
    price = float(input("Enter the updated price of the item: "))
    quantity = int(input("Enter the updated quantity: "))

    items[name] = (price, quantity)

def delete_item():
    # TODO: implement the delete function
    #       HINT: You can use 'del' statement "del items['name']" or "items.pop('name')"
    name = input("Enter the name of the item to delete: ")
    del items[name]

def display_by_name():
    # TODO: implement the display by name function
    #       HINT: use the 'sorted()' function built-in.
    print(sorted(items))

def display_by_price():
    # TODO: implement the display by price function
    #       HINT: this may be tricky, you can use this: 
    #             https://realpython.com/sort-python-dictionary/#using-the-key-parameter-and-lambda-functions 
    #            (use items.values())
    #
    print(sorted(items.values(), key = lambda item: item[1]))

######################################

def display_menu():
    print("Welcome to Generic E-Commerce Store!")
    print("Which of the following would you like to do?")
    print("1. Add Item")
    print("2. Update Item")
    print("3. Delete Item")
    print("4. Display Items by Name")
    print("5. Display Items by Total Price")
    print("6. Quit")

def get_validated_main_menu_input():
    while True:
        choice = int(input("Enter the number of your choice: "))

        if choice in range(1, 6 + 1):
            return choice # This exits the entire function whith the value
        
        print("Invalid Input.")

while True:
    display_menu()
    choice = get_validated_main_menu_input()
    
    if choice == 1:
        add_item()
        
    elif choice == 2:
        update_item()

    elif choice == 3:
        delete_item()
    
    elif choice == 4:
        display_by_name()
    
    elif choice == 5:
        display_by_price()
  
    else:
        break
