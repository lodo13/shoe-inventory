"""The app is designed for a shoe store, it gets shoes from the inventory and displays them by item, quantity and cost"""


# ========Imports==========
from tabulate import tabulate
import os


# ========The beginning of the class==========
class Shoe:
    """this class defines the object shoe"""

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        cost = self.cost
        return cost

    def get_quantity(self):
        quantity = self.quantity
        return quantity

    def __str__(self):
        return (f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}")


# =============Shoe list===========
shoe_list = []

# ==========Functions outside the class==============


def read_shoes_data():
    '''loads the shoes from the inventory file'''
    inv_list = []
    try:
        with open("inventory.txt", "r") as inventory:
            for line in inventory:
                line = line.strip("\n")
                line = line.split(",")
                inv_list.append(line)
        inv_list.pop(0)
        for i in inv_list:
            shoe_list.append(Shoe(i[0], i[1], i[2], int(i[3]), int(i[4])))
    except FileNotFoundError:
        print("The inventory file was not found.")
        quit()


def capture_shoes():
    """adds a new shoe"""
    while True:
        select = input("Would you like to add a new shoe? Y/n: ").lower()
        if select == "y":
            country = input("Enter the country of provenance: ").capitalize()
            code = input("Enter the SKU code (eg. SKU00000): ").upper()
            product = input("Enter the name of the product: ").title()
            cost = int(input("Enter the price of the product: "))
            quantity = int(input("Enter the quantity of the product: "))

            with open("inventory.txt", "r") as inventory:
                reading = inventory.read()
            with open("inventory.txt", "a") as inventory:
                if reading[-1] == "\n":
                    inventory.write(
                        f"{country}, {code}, {product}, {cost}, {quantity}\n")
                else:
                    inventory.write(
                        f"\n{country}, {code}, {product}, {cost}, {quantity}")

            shoe_list.append(Shoe(country, code, product, cost, quantity))

            break

        elif select == "n":
            break

        else:
            print("Wrong selection:")


def view_all():
    """shows all the shoes in the inventory"""
    print(tabulate([[obj.country, obj.code, obj.product, obj.cost, obj.quantity]
          for obj in shoe_list], headers=["Country", "Code", "Product", "Cost", "Quantity"]))


def re_stock():
    """changes the quantity of a selected item"""
    to_restock = []
    new_file = []
    high_quant = min(obj.quantity for obj in shoe_list)

    for obj in shoe_list:
        if obj.quantity == high_quant:
            to_restock.append(obj)
    print(tabulate([[obj.country, obj.code, obj.product, obj.cost, obj.quantity]
          for obj in to_restock], headers=["Country", "Code", "Product", "Cost", "Quantity"]))

    while True:
        sku = input("Select the SKU number or write back to exit: ").upper()
        if sku == "BACK":
            break
        select = input("Would you like to restock this item? Y/n: ").lower()

        if select == "y":
            new_quantity = int(input("Please insert a new quantity: "))

            for x in shoe_list:
                if x.code == sku:
                    x.quantity = new_quantity
            with open("inventory.txt", "r") as file:
                for line in file:
                    line = line.strip("\n")
                    line = line.split(",")
                    new_file.append(line)

                for line in new_file:
                    if line[1] == sku:
                        line[4] = new_quantity

            with open("inventory.txt", "w+") as newfile:
                for line in new_file:
                    newfile.write(
                        f"{line[0]},{line[1]},{line[2]},{line[3]},{line[4]}\n")

            break
        if select == "n":
            break


def search_shoe():
    """searches shoes among the inventory"""
    search_result = []
    while True:
        sel = input(
            "Search by code, name, country or back to previous menu: ").lower()
        if sel == "code":
            shoecode = input("Insert SKU number: ").upper()
            for obj in shoe_list:
                if obj.code == shoecode:
                    search_result.append(obj)
            clear()
            print(tabulate([[obj.country, obj.code, obj.product, obj.cost, obj.quantity]
                  for obj in search_result], headers=["Country", "Code", "Product", "Cost", "Quantity"]))
            print()

        elif sel == "name":
            shoename = input("Insert name of product: ").title()
            for obj in shoe_list:
                if shoename in obj.product:
                    search_result.append(obj)
            print(tabulate([[obj.country, obj.code, obj.product, obj.cost, obj.quantity]
                  for obj in search_result], headers=["Country", "Code", "Product", "Cost", "Quantity"]))
            print()

        elif sel == "country":
            shoecountry = input("Insert country of provenance: ").capitalize()
            for obj in shoe_list:
                if obj.country == shoecountry:
                    search_result.append(obj)
            print(tabulate([[obj.country, obj.code, obj.product, obj.cost, obj.quantity]
                  for obj in search_result], headers=["Country", "Code", "Product", "Cost", "Quantity"]))
            print()

        elif sel == "back":
            break

        else:
            print("Wrong selection.")
            continue

        break


def clear():
    """it simply clears the screen"""
    os.system('cls')


def value_per_item():
    """prints out the value for each shoe in stock"""
    print(tabulate([[obj.country, obj.code, obj.product, (obj.get_cost() * obj.get_quantity())]
          for obj in shoe_list], headers=["Country", "Code", "Product", "Cost", "Quantity"]))


def highest_qty():
    """prints out the highest quantity shoes in stock"""
    on_sale = []
    high_quant = max(obj.quantity for obj in shoe_list)

    for obj in shoe_list:
        if obj.quantity == high_quant:
            on_sale.append(obj)
    print(tabulate([[obj.country, obj.code, obj.product, obj.cost, obj.quantity]
          for obj in on_sale], headers=["Country", "Code", "Product", "Cost", "Quantity"]))
    print("\nThis shoes are on discount 30%!\n")


# ==========Main Menu=============
read_shoes_data()

while True:
    selection = input("""

Please select an option:
    
A: Add a new shoe.
V: View all shoes in the catalogue.
T: Value per item.
H: Show highest quantity shoe.
M: Show the item with lower quantity.
S: Search product.
E: Close the program.

""").lower()

    if selection == "a":
        clear()
        capture_shoes()
        continue
    elif selection == "v":
        clear()
        view_all()
    elif selection == "t":
        clear()
        value_per_item()
    elif selection == "h":
        clear()
        highest_qty()
    elif selection == "m":
        clear()
        re_stock()
    elif selection == "s":
        clear()
        search_shoe()
    elif selection == "e":
        clear()
        print("Goodbye.")
        quit()
    else:
        clear()
        print("Wrong selection.")
        continue
