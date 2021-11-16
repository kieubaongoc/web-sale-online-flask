from app import app #db
import json
import os
import hashlib
from flask import session
#from app.models import Category, Product

def read_categories():
    with open(os.path.join(app.root_path, "data/categories.json"),
               encoding="utf-8") as f:
         return json.load(f)


def read_accounts():
    with open(os.path.join(app.root_path, "data/account.json"),
               encoding="utf-8") as f:
         return json.load(f)


def read_product_by_id(product_id):
    products = read_products()
    for p in products:
        if p["id"] == product_id:
            return p

    return None


def read_user_by_id(user_id):
    users = read_users()
    for u in users:
        if u["id"] == user_id:
            return u

    return None


def read_products(category_id=0, keyword=None, from_price=None, to_price=None):
    with open(os.path.join(app.root_path, "data/products.json"),
               encoding="utf-8") as f:
         products = json.load(f)

         if category_id > 0:
             products = [p for p in products if p["category_id"] == category_id]

         if keyword:
             products = [p for p in products if p["name"].lower().find(keyword.lower()) >= 0]

         if from_price and to_price:
             products = [p for p in products if p["price"] >= float(from_price) and p["price"] <= float(to_price)]

         return products


def read_users(account_id=0, username=None):
    with open(os.path.join(app.root_path, "data/user.json"),
               encoding="utf-8") as f:
         users = json.load(f)

         if account_id > 0:
             users = [u for u in users if u["account_id"] == account_id]

         if username:
             users = [u for u in users if u["username"].lower().find(username.lower()) >= 0]

         return users


def update_product(product_id, name, description, images, price, category_id):
    products = read_products()
    for idx, p in enumerate(products):
        if p["id"] == int(product_id):
            products[idx]["name"] = name
            products[idx]["description"] = description
            products[idx]["price"] = float(price)
            products[idx]["images"] = images
            products[idx]["category_id"] = int(category_id)

            break
    return update_json(products)


def update_user(user_id, images, password, fullname, sex, address, phone):
    users = read_users()
    for idx, u in enumerate(users):
        if u["id"] == int(user_id):
            users[idx]["password"] = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
           #users[idx]["confirm"] = str(hashlib.md5(confirm.strip().encode("utf-8")).hexdigest())
            users[idx]["images"] = images
            users[idx]["fullname"] = fullname
            users[idx]["sex"] = sex
            users[idx]["address"] = address
            users[idx]["phone"] = phone

            break
    return update_user_json(users)


def update_json(products):
    try:
        with open(os.path.join(app.root_path, "data/products.json"),
                  "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

            return True
    except Exception as ex:
        print(ex)
        return False


def update_user_json(users):
    try:
        with open(os.path.join(app.root_path, "data/user.json"),
                  "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

            return True
    except Exception as ex:
        print(ex)
        return False



def add_products(name, description, price, images, category_id):
    products = read_products()
    product = {
        "id": len(products) +1,
        "name": name,
        "description": description,
        "price": float(price),
        "images": images,
        "category_id": int(category_id)
    }
    products.append(product)

    try:
        with open(os.path.join(app.root_path, "data/products.json"),
                  "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

            return True
    except Exception as ex:
        print(ex)
        return None


def delete_product(product_id):
    products = read_products()
    for idx, product in enumerate(products):
        if product["id"] == int(product_id):
            del products[idx]
            break

    return update_json(products=products)


def delete_user(user_id):
    users = read_users()
    for idx, user in enumerate(users):
        if user["id"] == int(user_id):
            del users[idx]
            break

    return update_user_json(users=user)



def read_admins():
    with open(os.path.join(app.root_path, "data/admin.json"),
              encoding="utf-8") as f:
        return json.load(f)


def validate_admin(username, password):
    admins = read_admins()
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

    for admin in admins:
        if admin["username"].strip() == username.strip() and admin["password"] == password:
            return admin

    return None

def validate_user(username, password):
    users = read_users()
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

    for user in users:
        if user["username"].strip() == username.strip() and user["password"] == password:
            return user

    return None


def load_admins():
    with open(os.path.join(app.root_path, "data/admin.json"),
              encoding="utf-8") as f:
        return json.load(f)


def load_users():
    with open(os.path.join(app.root_path, "data/user.json"),
              encoding="utf-8") as f:
        return json.load(f)


def add_admin(name, username, password):
    admins = read_admins()
    admin = {
        "id": len(admins) + 1,
        "name": name,
        "username": username,
        "password": str(hashlib.md5(password.encode('utf-8')).hexdigest())
    }
    admins.append(admin)

    with open(os.path.join(app.root_path, "data/admin.json"),
              "w", encoding="utf-8") as f:
        json.dump(admins, f, ensure_ascii=False, indent=4)

    return admin


def add_user(name, username, password):
    users = load_users()
    user = {
        "id": len(users) + 1,
        "name": name,
        "username": username,
        "password": str(hashlib.md5(password.encode('utf-8')).hexdigest())
    }
    users.append(user)

    with open(os.path.join(app.root_path, "data/user.json"),
              "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    return user


def cart_stats(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for p in cart.values():
            total_quantity = total_quantity + p["quantity"]
            total_amount = total_amount + p["quantity"] * p["price"]

    return total_quantity, total_amount



if __name__ == "__main__":
    print(read_products())