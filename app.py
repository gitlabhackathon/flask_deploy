from flask import Flask, render_template, request, redirect, url_for
import math

app = Flask(__name__,template_folder='flask_deploy')

# Store participants and expenses
participants = {}
expenses = []

@app.route('/')
def index():
    return render_template('index.html', participants=participants, expenses=expenses)

@app.route('/add_participant', methods=['POST'])
def add_participant():
    name = request.form.get('participant_name')
    if name and name not in participants:
        participants[name] = 0.0
    return redirect(url_for('index'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    total_amount = float(request.form.get('total_amount'))
    payer = request.form.get('payer')
    participants_list = request.form.get('participants').split(',')
    participants_list = [p.strip() for p in participants_list]
    
    if payer not in participants:
        return "Payer is not a registered participant", 400
    if any(p not in participants for p in participants_list):
        return "One or more participants are not registered", 400
    
    # Split expense
    share = total_amount / len(participants_list)
    participants[payer] += total_amount
    for participant in participants_list:
        if participant != payer:
            participants[participant] -= share
    
    expenses.append({'amount': total_amount, 'payer': payer, 'participants': participants_list})
    return redirect(url_for('index'))

@app.route('/show_balances')
def show_balances():
    return render_template('balances.html', participants=participants)

@app.route('/show_expenses')
def show_expenses():
    return render_template('expenses.html', expenses=expenses)

if __name__ == "__main__":
    app.run(debug=True)
