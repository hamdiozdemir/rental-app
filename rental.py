from flask import Flask, render_template, redirect, url_for, session, request, flash
import numpy as np
# from flask_sqlalchemy import SQLAlchemy
# from wtforms import Form, StringField, IntegerField, validators
# from wtforms.validators import InputRequired, ValidationError



app = Flask(__name__)
app.secret_key = "housesare2muchexpensive"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/rental"

# db = SQLAlchemy(app)


# ------ DATABASES -------------------
"""
class Expences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_tax_m = db.Column(db.Integer)
    insurance_m = db.Column(db.Integer)
    gas_elec_m = db.Column(db.Integer)
    water_m = db.Column(db.Integer)
    sewer_m = db.Column(db.Integer)
    garbage_m = db.Column(db.Integer)
    lawn_snow = db.Column(db.Integer)
    management = db.Column(db.Float)
    vacancy = db.Column(db.Float)
    maintenance = db.Column(db.Float)


class Mortgage(db.Model):
    downpayment = db.Column(db.Float)
    interest_rate = db.Column(db.Float)
    loan_term = db.Column(db.Integer)
    cloasing_costs = db.Column(db.Integer)

"""

# ------------ FORMs ------------------




# --------------- VIEWS --------------------

@app.route("/", methods=["GET", "POST"])
def index():
    values = {
        "salesprice": 70000,
        "propertytax":1400,
        "insurance":35,
        "gaselectric":0,
        "water":0,
        "sewer":0,
        "garbage":0,
        "lawnsnow":0,
        "management":10.00,
        "vacancy":5.00,
        "maintenance":10.00,
        "downpayment":20.00,
        "interestrate":3.75,
        "loanterm":25,
        "closingcosts":0
    }
    if request.method == "GET":
        return render_template("index.html", values=values)
    else:
        values = {
        "salesprice": request.form["salesprice"],
        "propertytax":request.form["propertytax"],
        "insurance":request.form["insurance"],
        "gaselectric":request.form["gaselectric"],
        "water":request.form["water"],
        "sewer":request.form["sewer"],
        "garbage":request.form["garbage"],
        "lawnsnow":request.form["lawnsnow"],
        "management":request.form["management"],
        "vacancy":request.form["vacancy"],
        "maintenance":request.form["maintenance"],
        "downpayment":request.form["downpayment"],
        "interestrate":request.form["interestrate"],
        "loanterm":request.form["loanterm"],
        "closingcosts":request.form["closingcosts"]
    }




        gross_rent = rentmo_total()
        proformaItem = CurrentProforma(gross_rent)
        currentMortgage = CurrentMortgage(request.form["salesprice"], gross_rent)
        



        return render_template("index.html", values=values, proformaItem=proformaItem, currentMortgage=currentMortgage)



# ------------------------ UTILS -------------------------------------

def rentmo_total():
    inputs = [request.form["rentmo1"], request.form["rentmo2"], request.form["rentmo3"], request.form["rentmo4"], request.form["rentmo5"], request.form["rentmo6"]]
    results = []
    for item in inputs:
        if item == "":
            item = 0
            results.append(item)
        else:
            item = int(item)
            results.append(item)
    rent_total = sum(results)
    return rent_total

def marketrent_total():
    try:
        marketrent_total = int(request.form["rentmarket1"])+int(request.form["rentmarket2"])+int(request.form["rentmarket3"])+int(request.form["rentmarket4"])+int(request.form["rentmarket5"])+int(request.form["rentmarket6"])
        return marketrent_total
    except:
        return 0


class CurrentProforma():

    def __init__(self, gross_rent):
        self.gross_rent = round(gross_rent, 2)
        
    def gross_rents(self):
        return round(self.gross_rent, 2)

    def marketrent_total(self):
        marketrent_total = int(request.form["rentmarket1"])+int(request.form["rentmarket2"])+int(request.form["rentmarket3"])+int(request.form["rentmarket4"])+int(request.form["rentmarket5"])+int(request.form["rentmarket6"])
        return marketrent_total

    def property_management(self):
        return round(self.gross_rent * float(request.form["management"]) / 100, 2)

    def property_tax(self):
        return round(int(request.form["propertytax"]) / 12, 2)

    def insurance(self):
        return round(int(request.form["insurance"]), 2)
    
    def op_utilities(self):
        return round(int(request.form["gaselectric"])+int(request.form["water"])+int(request.form["sewer"])+int(request.form["garbage"])+int(request.form["lawnsnow"]), 2)
        
    def vacancy_reserve(self):
        return round(self.gross_rent * float(request.form["vacancy"]) / 100, 2)

    def maintenance_reserve(self):
        return round(self.gross_rent * float(request.form["maintenance"]) / 100, 2)
        
    def total_operating_expences(self):
        return round(self.property_management() + self.property_tax() + self.insurance() + self.op_utilities() + self.vacancy_reserve() + self.maintenance_reserve(), 2)

    
    def monthly_noi(self):
        return round(self.gross_rent - self.total_operating_expences(), 2)
    
    def annualized_noi(self):
        return round(self.monthly_noi() * 12, 2)

    def capitalization_rate(self):
        return round(self.annualized_noi() / int(request.form["salesprice"]) * 100, 2)

class CurrentMortgage():
    
    def __init__(self, salesprice, gross_rent):
        self.salesprice = int(salesprice)
        self.gross_rent = round(gross_rent, 2)
    
    def saleprice(self):
        return self.salesprice
    
    def loan_to_value_ratio(self):
        return 100 - float(request.form["downpayment"])

    def down_payment(self):
        return self.salesprice * (float(request.form["downpayment"]) / 100)
    
    def closing_costs(self):
        return float(request.form["closingcosts"])
    
    def principal(self):
        return self.salesprice * self.loan_to_value_ratio() / 100
    
    def interest_rate(self):
        return float(request.form["interestrate"])

    def term(self):
        return int(request.form["loanterm"])
    
    def monthly_mortgage(self):
        monthly = np.pmt(self.interest_rate() / 100 / 12, self.term() * 12, self.principal())
        monthly = abs(monthly)
        monthly = round(monthly, 2)
        return monthly

    def monthly_net(self):
        return CurrentProforma(self.gross_rent).monthly_noi() - self.monthly_mortgage()

    def annualized_net(self):
        return self.monthly_net() * 12
    
    def annualized_roi(self):
        return self.annualized_net() / (self.down_payment() + self.closing_costs()) * 100



@app.template_filter()
def currencyFormat(value):
    return format(int(value), ',d')


if __name__ == "__main__":
    app.run(debug=True)