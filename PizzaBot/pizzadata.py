from pizzapy import *
import data

def storedata(ctx, addr):
    address = Address(*addr.split(', '))
    near=address.closest_store()
    if not near:
        return False
    else:
        return near

def menudata(ctx, addr):
    address = Address(*addr.split(', '))
    store=address.closest_store()
    if not store:
        return False
    else:
        menu=store.get_menu().display()
        return menu

def getmenu(ctx, addr):
    address = Address(*addr.split(', ')) 
    store=address.closest_store()
    if not store:
        return False
    else:
        menu=store.get_menu()
        return menu

def storeopen(ctx, addr):
    address = Address(*addr.split(', '))
    store=address.closest_store()
    if not store:
        return False
    else:
        return True

def orderprice(ctx, vals):
    customer = Customer(vals[1], vals[2], vals[4], vals[3], vals[5])
    store = StoreLocator.find_closest_store_to_customer(customer)
    order = Order.begin_customer_order(customer, store)
    items=data.showorder(ctx)
    if not items:
        return False
    else:
        for item in items:
            order.add_item(item)
        x=order.pay_with()
        return x['Order']['Amounts']['Customer']

def placeorder(ctx, vals, card=''):
    customer = Customer(vals[1], vals[2], vals[4], vals[3], vals[5])
    store = StoreLocator.find_closest_store_to_customer(customer)
    order = Order.begin_customer_order(customer, store)
    items=data.showorder(ctx)
    if not items:
        return False
    else:
        for item in items:
            order.add_item(item)
        if order.validate():
            if card=='':
                x=order.place()
                return x
            else:
                val=card.split(', ')
                crd=CreditCard(val[0], val[1], val[2], val[3])
                x=order.place(crd)
                return x

        else:
            return False