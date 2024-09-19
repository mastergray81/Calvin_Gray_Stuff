from flask import Flask, request, render_template
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import joblib, pickle, os, sys
import xgboost as xgb
from joblib import load


zipincome = pd.read_csv('totalincomebyzip.csv',low_memory = False)

trimlist = pd.read_csv('trimlist.csv', low_memory = False)


#cars = pd.read_csv('cars.csv', low_memory = False)
cars = pd.read_csv('cars.csv',low_memory = False)
cars = cars.convert_dtypes()

app = Flask(__name__)



@app.route("/")
@app.route('/home')
def home_page():
    return render_template('Home.html', methods=['GET', 'POST'])




def gatherFromTextBox(mileage, year, make, model, trim, transmission, listing_type, zip_code, num_of_cars, avg_price, gross_income):
         


    # keep all inputs in a list
    user_input = [mileage, year, make, model, trim, transmission, listing_type, zip_code, num_of_cars, avg_price, gross_income]


    # Data Frame


    df = pd.DataFrame({'vehicle_mileage':[mileage],'vehicle_specs_year': [year], 'vehicle_specs_make': [make],
         'vehicle_specs_model': [model], 'vehicle_specs_trim': [trim],'vehicle_specs_transmission_type': [transmission],
         'listing_type': [listing_type],'seller_zip': [zip_code], 'num_of_cars': [num_of_cars], 'avg_sale_price':[avg_price],
           'gross_income':[gross_income]})

    input = df.copy()

    cols = ['gross_income',
            'seller_zip',
            'avg_sale_price',
            'num_of_cars',
            'vehicle_specs_year',
            'vehicle_mileage'
           ]
    input[cols] = input[cols].astype('int')
    
    cols =  ['listing_type',
            'vehicle_specs_make',
            'vehicle_specs_model',
            'vehicle_specs_trim',
            'vehicle_specs_transmission_type'
            ]
    
    input[cols] = input[cols].astype('category')


    print(input)
    print(input.info())


    # open pickle file

    #model = open('Grad_Boost_Reg_2500_95_final.pkl','rb')
    model = open('Grad_Boost_Reg_2500_95_final.pkl','rb')

    # load trained model using joblib
    stacked_regressor = joblib.load(model)

    # predict
    prediction = stacked_regressor.predict(input)

    return round(prediction[0], 0)


@app.route('/Top25MakeModel')
def Top25MakeModel_page():
    return render_template('Top25MakeModel.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/cars')
def car_page():
    return render_template('cars.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_page():
    #return render_template('predict.html')

    if request.method == "POST":
            # get form data

            listing_type = request.values.get('listing_type')
            list_type = request.values.get('listing_type')
            year = request.values.get('year')
            make = request.values.get('make')
            model = request.values.get('model')
            trim = request.values.get('trim')
            mileage = request.values.get('mileage')
            transmission = request.values.get('transmission')
            zip_code = request.values.get('zipcode')
            num_of_cars = request.values.get('num_of_cars')
            avg_price = 0
            year = int(year)
            transmission = transmission.title()
            #list_type = listing_type.copy()
            

            # get data from "zipincome"
            # This will avoid crashing the flask web app if a invalid ZipCode is passed to the method.
            try:
                
                zip_code = int(zip_code)
                if zip_code in zipincome['zip'].tolist():
                    zips = zipincome[zipincome['zip'] == zip_code]
                    gross_income = zips['gross_income']
                else:
                    zip_code = 31032
                    gross_income = 447230
            except:
                print('There is an error with the Zip Code')


            if trim in trimlist['trim'].tolist():
                trim == trim
            else:
                trim = 'EX'


            #works with old cars file returns index
            lead = (cars['vehicle_specs_make']==make) & (cars['vehicle_specs_model']==model) & (cars['vehicle_specs_year']==year) & (cars['vehicle_specs_trim']==trim) & (cars['vehicle_specs_transmission_type']==transmission) & (cars['listing_type']==listing_type) 
            
            print("\n-------------------\n lead Sez:", lead[lead].index,'\n---------------------\n')
            
            simp = cars[lead]

            if simp.empty:
                avg_price = avg_price
                

            else:
                avg_price = simp['avg_sale_price']
                

                    
           
           #deprecated....
           
            if listing_type == 'Used':
                listing_type = 0
            else:
                listing_type = 1

           #call gatherfromtextbox and pass inputs


            try:
                price = gatherFromTextBox(mileage, year, make, model, trim, transmission, listing_type, zip_code, num_of_cars, avg_price, gross_income)
                #pass prediction to template
                return render_template('predict.html', list_type=list_type, price=price, year=year, make=make, model=model, trim=trim, transmission=transmission)

            except Exception as e:
                return e.args[0] #print(e) #e.args[0] #"There is no such combination of values. Please try again"

            
    pass

# Run on Correct Port
if __name__ == '__main__':
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host="localhost", port=5000, debug=True)

