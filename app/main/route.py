from flask import Flask, render_template, flash, redirect, request, url_for, jsonify,  Blueprint
from ..app import db,Customer

main = Blueprint('main', __name__)

db.create_all()

@main.route('/', methods=['GET', 'POST'])
def index():

    data = request.get_json()
    username = data["username"]
    email = data["email"]

    user = User(username, email)
    print(user.username)

    db.session.add(user)
    db.session.commit()

    db_data = User.query.all()

    for name_user in db_data:
        print("======>:  " + name_user.username)

    return jsonify({"username": name_user.username, "email": name_user.email})

    # return "hello world"

#GET all accounts
@main.route('/accounts', methods =['GET'])
def getAllAccounts():

    all_customers = {'Customers':  [customer for customer in Customer.query.all()]}
    
    return jsonify(all_customers) ,404

    
#GET account by ID
@main.route('/accounts/<int:Id>',methods =['GET'])
def getAccoutByID(Id):

    customer = Customer.query.filter(Customer.id==Id).first()
   

    return jsonify({'Customer account': [customer]}) if customer else jsonify({'message': 'Customer not found'}),404 
    
#GET account balance
@main.route('/accounts/<int:Id>/balance',methods =['GET'])
def getAccountBalance(Id):
    
    customer = Customer.query.filter(Customer.id==Id).first()
    
    return jsonify({'Account balance': [customer.balance]}) if customer else jsonify({'message': 'Customer not found'}) 
 
#GET account number
@main.route('/accounts/<int:Id>/accountnumber',methods =['GET'])
def getAccountNumber(Id):

    customer = Customer.query.filter(Customer.id==Id).first()

    return jsonify({'Account number': [customer.account_no]}) if customer else jsonify({'message': 'Customer not found'}) 
 
#GET account consumption statement
@main.route('/accounts/<int:Id>/consumption',methods =['GET'])
def getAccountConsumptionStatement(Id):
    
    cons = Consumption.query.filter(Customer.id==Id)

    return jsonify({'Consumption': [cons.to_json()]}) if cons else jsonify({'message': 'Consumption not found'}) 
 
#GET account topup statement
@main.route('/accounts/<int:Id>/balance',methods =['GET'])
def getAccountTopUpStatement(Id):
    
    topUp = TopUp.query.filter(Customer.id==Id)
    return jsonify({'TopUp': [topUp.to_json()]}) if topUp else jsonify({'message': 'TopUp not found'}) 
 
