# save this as app.py
from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/prediction.html', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])
        
        #new feature

        Previous_loan_amount=float(request.form['Previous_loan_amount'])
        profession = request.form['profession']
        Paid_amount=float(request.form['Paid_amount'])

        


        #new feature

        # gender
        if (gender == "Male"):
            male=1
        else:
            male=0
        
        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # dependents
        if(dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif(dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif(dependents=="3+"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (employed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if(area=="Semiurban"):
            semiurban=1
            urban=0
        elif(area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0

        #new change in logic

        #biasing based on profession
        
        if profession == "Farming":
            ApplicantIncome += 100
        elif profession == "Teaching":
            ApplicantIncome += 300
        elif profession == "Banking":
            ApplicantIncome += 800
        elif profession == "Doctor":
            ApplicantIncome += 500
        elif profession == "Other":
            ApplicantIncome += 50


        #biasing based on education
        if education == "Graduate":
            ApplicantIncome += 50


        #biasing based on previous loan amount
        Left_amount=Previous_loan_amount-Paid_amount
        if Left_amount >= 2500:
            Applicant_income = 0
        elif 1500 <= Left_amount < 2500:
            Applicant_income -= Left_amount
        if Applicant_income <= 0:
            Applicant_income = 0
        elif 500 < Left_amount < 1500:
            Applicant_income -= 500








        








        #new change 


        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = model.predict([[credit, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban, urban ]])

        # print(prediction)

        if(prediction=="N"):
            prediction="No" 
            return render_template("prediction.html", prediction_text="{}, You are not eligible for loan.".format(prediction))
        else:
            prediction="Yes"
            return render_template("prediction.html", prediction_text="{}, You are eligible for loan.".format(prediction))

        




    else:
        return render_template("prediction.html")



if __name__ == "__main__":
    app.run(debug=True)