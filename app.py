from flask import Flask, render_template, request, redirect, url_for, flash
from excel import leer_stock, actualizar_stock
import os
import re  # Para procesar mensajes de WhatsApp

app = Flask(__name__)
app.secret_key = "demo_secret_key"

# Cargar stock al inicio
stock = leer_stock()

# Obras demo
works = [
    {"obra": "Puerta corrediza López", "estado": "Armado"},
    {"obra": "Ventanas Acosta", "estado": "Corte"},
    {"obra": "Frente Vidriado S.A.", "estado": "Terminado"},
]

# ------------------- Rutas Web -----------------------

@app.route("/")
def dashboard():
    low_stock = [item for item in stock if item["qty"] < 100]
    return render_template("index.html", stock=len(stock), works=len(works), low_stock=low_stock)

@app.route("/stock")
def stock_list():
    global stock
    stock = leer_stock()
    return render_template("stock.html", stock=stock)

@app.route("/ingreso", methods=["GET", "POST"])
def ingreso():
    if request.method == "POST":
        sku = request.form["sku"].strip().upper()
        qty = float(request.form["qty"])
        actualizar_stock(sku, qty, "ingreso")
        flash(f"Ingresados {qty:g} de {sku}", "success")
        return redirect(url_for("stock_list"))
    return render_template("ingreso.html")

@app.route("/egreso", methods=["GET", "POST"])
def egreso():
    if request.method == "POST":
        sku = request.form["sku"].strip().upper()
        qty = float(request.form["qty"])
        try:
            actualizar_stock(sku, qty, "egreso")
            flash(f"Retirados {qty:g} de {sku}", "success")
        except ValueError:
            f
# ------------------- Arranque del servidor -----------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usado por Render
    app.run(host="0.0.0.0", port=port)
