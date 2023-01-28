from flask import Flask,render_template,request,redirect
import json
from web3 import Web3,HTTPProvider

def connect_blockchain_register(wallet):
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if wallet==0:
        wallet=web3.eth.accounts[0]
    web3.eth.defaultAccount=wallet
    artifact_path='../build/contracts/register.json'
    contract_address='0x9dcD0B1e944d405E0e4b50Ad93E5A3FDD72C9A1E'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('Home.html')

@app.route('/description')
def descriptionpage():
    return render_template('description.html')

@app.route('/head')
def headpage():
    return render_template('Head.html')

@app.route('/loginbidder')
def loginbidderpage():
    return render_template('loginbidder.html')

@app.route('/logintender')
def logintenderpage():
    return render_template('logintender.html')

@app.route('/registrationbidder')
def registrationbidderpage():
    return render_template('registrationbidder.html')

@app.route('/registrationtender')
def registrationtenderpage():
    return render_template('registrationtender.html')

@app.route('/registerbidder',methods=['POST'])
def registerbidder():
    username=request.form['username']
    password=request.form['password']
    email=request.form['email']
    print(username,password,email)
    contract,web3=connect_blockchain_register(0)
    tx_hash=contract.functions.registerbiduser(username,int(password),email).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/loginbidder')

@app.route('/loginbidderform', methods=['POST'])
def loginbidderform():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_blockchain_register(0)
    state=contract.functions.loginbiduser(username,int(password)).call()
    if state==True:
        return('Success')
    else:
        return('Fail')

@app.route('/registertender',methods=['POST'])
def registertender():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_blockchain_register(0)
    tx_hash=contract.functions.registeruser(username,int(password)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/logintender')

@app.route('/logintenderform',methods=['POST'])
def logintenderform():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_blockchain_register(0)
    state=contract.functions.loginuser(username,int(password)).call()
    if state==True:
        return('Success')
    else:
        return('Fail')
    
if __name__=="__main__":
    app.run(debug=True)