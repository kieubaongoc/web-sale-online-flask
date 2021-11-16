from flask import render_template, request, redirect, jsonify, url_for, session
from app import app, dao
#from app.models import *
import hashlib, json, os
from app.decorator import login_required, login_admin_required


@app.route("/")
def index():
    return render_template("index.html",
                           products=dao.read_products())

@app.route("/mobile")
def mobile():
    return render_template("body/mobile.html")

@app.route("/tablet")
def tablet():
    return render_template("body/tablet.html")

@app.route("/admin-page")
def admin_page():
    return render_template("admin/admin.html")


@app.route("/login-admin", methods=["get", "post"])
def login_admin():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = dao.validate_admin(username=username, password=password)
        if admin:
            session["admin"] = admin

            if "next" in request.args:
                return redirect(request.args["next"])

            return render_template("admin/about-us.html")
        else:
            err_msg = "Đăng nhập không thành công"

    return render_template("admin/login-admin.html", err_msg=err_msg)


@app.route("/login", methods=["get", "post"])
def login():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.validate_user(username=username, password=password)
        if user:
            session["user"] = user

            if "next" in request.args:
                return redirect(request.args["next"])

            return redirect(url_for("index"))
        else:
            err_msg = "Đăng nhập không thành công"

    return render_template("login.html", err_msg=err_msg)


@app.route("/api/products")
def get_product_list():
    with open("data/categories.json", encoding="utf-8") as f:
        products = json.load(f)

        return jsonify({"data": products})


@app.route("/api/users")
def get_user_list():
    with open("data/account.json", encoding="utf-8") as f:
        users = json.load(f)

        return jsonify({"data": users})


@app.route("/products")
def product_list():
    kw = request.args.get("keyword", None)
    from_price = request.args.get("from_price", None)
    to_price = request.args.get("to_price", None)
    return render_template("products.html",
                           products=dao.read_products(keyword=kw, from_price=from_price, to_price=to_price))


@app.route("/users")
def user_list():
    un = request.args.get("username", None)
    return render_template("admin/mgr-user.html",
                           users=dao.read_users(username=un))


@app.route("/products/<int:category_id>")
def products_by_cate_id(category_id):
    return render_template("products.html",
                           products=dao.read_products(category_id=category_id))


@app.route("/users/<int:account_id>")
def users_by_cate_id(account_id):
    return render_template("admin/mgr-user.html",
                           users=dao.read_users(account_id=account_id))


@app.route("/products/add", methods=["get", "post"])
@login_admin_required
def add_or_update_product():
    err = ""
    product_id = request.args.get("product_id")
    product = None
    if product_id:
        product = dao.read_product_by_id(product_id=int(product_id))

    if request.method.lower() == "post":
        #name = request.form.get("name")
        #price = request.form.get("price", 0)
        #images = request.form.get("images")
        #description = request.form.get("description")
        #category_id = request.form.get("category_id", 0)
        #import pdb  # thư viện debug
        #pdb.set_trace() #debug

        # viết tường minh
        # if dao.add_products(name=name, price=price, images=images,
        #                    description=description, category_id=category_id):
        if product_id:  # Cập nhật
            data = dict(request.form.copy())
            data["product_id"] = product_id
            if dao.update_product(**data):
                return redirect(url_for("product_list"))
        else: # Thêm
            if dao.add_products(**dict(request.form)):
                return redirect(url_for("product_list"))

        err = "Something went wrong! Please back later."

    return render_template("product-add.html",
                           categories=dao.read_categories(),
                           product=product,
                           err=err)


@app.route("/users/update", methods=["get", "post"])
def update_user():
    err = ""
    user_id = request.args.get("user_id")
    user = None
    if user_id:
        user = dao.read_user_by_id(user_id=int(user_id))

    if request.method.lower() == "post":
        #name = request.form.get("name")
        #price = request.form.get("price", 0)
        #images = request.form.get("images")
        #description = request.form.get("description")
        #category_id = request.form.get("category_id", 0)
        #import pdb  # thư viện debug
        #pdb.set_trace() #debug

        # viết tường minh
        # if dao.add_products(name=name, price=price, images=images,
        #                    description=description, category_id=category_id):
        if user_id:  # Cập nhật
            data1 = dict(request.form.copy())
            data1["user_id"] = user_id
            if dao.update_user(**data1):
                return redirect(url_for("login"))

        err = "Something went wrong! Please back later."

    return render_template("user_update.html",
                           accounts=dao.read_accounts(),
                           user=user,
                           err=err)

@app.route("/api/products/<int:product_id>", methods=["delete"])
def delete_product(product_id):
    if dao.delete_product(product_id=product_id):
        return jsonify({
             "status": 200,
             "message": "Delete successful",
             "data": {"product_id": product_id}
                        })

    return jsonify({
        "status": 500,
        "message": "Delete failed",
    })


@app.route("/api/users/<int:user_id>", methods=["delete"])
def delete_user(user_id):
    if dao.delete_user(user_id=user_id):
        return jsonify({
             "status": 200,
             "message": "Delete successful",
             "data": {"user_id": user_id}
                        })

    return jsonify({
        "status": 500,
        "message": "Delete failed",
    })


@app.route("/logout")
def logout():
    session["user"] = None
    return redirect(url_for("index"))

@app.route("/logout-admin")
def logout_admin():
    session["admin"] = None
    return redirect(url_for("index"))


@app.route("/register-admin", methods=["get", "post"])
def register_admin():
    if session.get("admin"):
        return redirect(request.url) #trang hiện tại

    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "Mật khẩu không khớp!"
        else:
            if dao.add_admin(name=name, username=username, password=password):
                return redirect(url_for('login_admin'))
            else:
                err_msg = "Something wrong!!!"

    return render_template("admin/register-admin.html", err_msg=err_msg)


@app.route("/register", methods=["get", "post"])
def register():
    if session.get("user"):
        return redirect(request.url) #trang hiện tại

    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "Mật khẩu không khớp!"
        else:
            if dao.add_user(name=name, username=username, password=password):
                return redirect(url_for('login'))
            else:
                err_msg = "Something wrong!!!"

    return render_template("register.html", err_msg=err_msg)


@app.route("/feedback", methods=["get", "post"])
@login_required
def feedback():
    msg = ""
    err_msg = ""
    """err_msg = ""
        if request.args.get("feedback"):
            msg = "%s" % (request.args["feedback"])
        return "%s" % msg"""
    if request.method == "POST":
        msg = request.form.get("feedback")
    else:
        err_msg = "Đã xảy ra lỗi!"

    return render_template("feedback.html", msg=msg, err_msg=err_msg)


@app.route("/user-info")
def user_info():
    return render_template("user-info.html")


@app.route("/cart")
@login_required
def cart():
    total_quan, total_amount = dao.cart_stats(session.get('cart'))
    cart_pay = {
        "total_quantity": total_quan,
        "total_amount": total_amount
    }
    return render_template("cart.html", cart_pay=cart_pay)


@app.route("/api/cart", methods=['get', 'post'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    if id in cart: #co sp trong gio
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else: #chua co sp trong gio
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    total_quan, total_amount = dao.cart_stats(cart)

    return jsonify({
        "total_quantity": total_quan,
        "total_amount": total_amount,
        "cart": cart
    })


@app.route("/api/cart/<item_id>", methods=['delete'])
def delete_item(item_id):
    if 'cart' in session:
        cart = session['cart']
        if item_id in cart:
            del cart[item_id]
            session['cart'] = cart

            return jsonify({
                'message': 'successful',
                'status': 200,
                'item_id': item_id
            })

        return jsonify({
            'status': 500,
            'message': 'failed'
        })


@app.route("/api/cart/<item_id>", methods=['post'])
def update_item(item_id):
    if 'cart' in session:
        cart = session['cart']
        data = request.json
        if item_id in cart and 'quantity' in data:
            cart[item_id]['quantity'] = int(data['quantity'])
            session['cart'] = cart
            total_quan, total_amount = dao.cart_stats(session.get('cart'))

            return jsonify({
                'message': 'successful',
                'status': 200,
                'total_quantity': total_quan,
                'total_amount': total_amount
            })

        return jsonify({
            'status': 500,
            'message': 'failed'
        })



if __name__ == "__main__":
    app.run(debug=True, port=5050)