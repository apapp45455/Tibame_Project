from flask import Flask, request, jsonify, render_template

import model
# from test_controller import test_controller

app = Flask(__name__, static_url_path='/resource', static_folder='./myresource')
# app.register_blueprint(test_controller, url_prefix='/controller_a')

@app.route("/hello_post", methods=["GET", "POST"])
def hello_post():
    from datetime import datetime
    request_method = request.method
    if request_method == "GET":
        return render_template('order.html')
    if request_method == "POST":
        customer_id = request.form.get("customer_id")
        product_category = request.form.get("product_category")
        product_name = request.form.get("product_name")
        quantity = request.form.get("quantity")

        data=[customer_id,product_category,product_name,quantity]
        model.writedata(data)
        model.updatestock()
        total_price = model.showtotal()

        return render_template(
        'show_order.html',
        data=data[0],
        total_price=total_price
        )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0' ,port=5001)

