from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import random  # Import the random module
import os

app = Flask(__name__, template_folder='template')
port = int(os.environ.get('PORT', 5000))
    

model1 = pickle.load(open('model1.pkl', 'rb'))
model2 = pickle.load(open('model2.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_model = request.form['model_select']
        if selected_model == 'model1':
            return redirect(url_for('input_page', model='model1'))
        elif selected_model == 'model2':
            return redirect(url_for('input_page', model='model2'))
    return render_template('index.html')

@app.route('/input_page/<model>', methods=['GET', 'POST'])
def input_page(model):
    if request.method == 'POST':
        aggregate = request.form['Aggregate']
        source = request.form['source']
        viscosity = float(request.form['viscosity'])  # Assuming viscosity is a float
        dag = request.form['DAG']
        air_voids = request.form['air_voids']
        
        # Convert input data to a format that the model expects
        input_data = np.array([[aggregate, source, viscosity, dag, air_voids]])
        
        # Initialize prediction variable
        pred = None
        
        # Make prediction using the selected model
        if model == 'model1':
            pred = model1.predict(input_data)
        elif model == 'model2':
            pred = model2.predict(input_data)
        else:
            pred = "Invalid model selection"

        
        # Ensure prediction is extracted correctly
        if isinstance(pred, np.ndarray):
            pred = pred[0]

        # Modify the prediction value within a range of ±5 if it is numeric
        if isinstance(pred, (int, float)):  # Ensure the prediction is a numeric type
            formatted_pred = f"{pred:.3f}"
            pred = formatted_pred
            pred = float(pred)
            # formatted_pred = f"{pred:.3f}"


        return render_template('result.html', pred=pred)
    return render_template('input_page.html', model=model)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port,debug=True)
