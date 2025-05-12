from flask import Flask, render_template, request
import joblib
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

# Fix for using Matplotlib with Flask (ensure it uses the correct backend)
matplotlib.use('Agg')

app = Flask(__name__)
model = joblib.load("model/energy_model.pkl")

# Function to generate line graph
def generate_line_graph(hour, day, temperature, appliance):
    hours = [hour - 2, hour, hour + 2]  # Example hours to show a small range around the current hour
    predictions = [model.predict(np.array([[h, day, temperature, appliance]]))[0] for h in hours]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hours, predictions, label='Energy Consumption', color='b', marker='o')
    ax.set(xlabel='Hour of the Day', ylabel='Energy Consumption (kWh)', title='Energy Consumption vs Time of Day')
    ax.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url

# Function to generate pie chart
def generate_pie_chart(hour, day, temperature, appliance):
    appliance_usages = [100, 500, 1000, 1500, 2000]  # Different appliance usage values
    predictions = [model.predict(np.array([[hour, day, temperature, appliance_usage]]))[0] for appliance_usage in appliance_usages]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(predictions, labels=appliance_usages, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
    ax.axis('equal')
    ax.set_title('Energy Consumption by Appliance Usage')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url

# Function to generate bar graph with proper bars
def generate_bar_graph(hour, day, temperature, appliance):
    appliance_usages = [100, 500, 1000, 1500, 2000]  # Different appliance usage values
    predictions = [model.predict(np.array([[hour, day, temperature, appliance_usage]]))[0] for appliance_usage in appliance_usages]
    
    # Create a larger bar plot with proper bars
    fig, ax = plt.subplots(figsize=(10, 5))  # Adjusting the figure size
    ax.bar(appliance_usages, predictions, label='Energy Consumption', color='g', width=300)  # Added width for bars
    ax.set(xlabel='Appliance Usage (W)', ylabel='Energy Consumption (kWh)', title='Energy Consumption by Appliance Usage')
    ax.grid(True)

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    return plot_url

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    line_graph_url = None
    pie_chart_url = None
    bar_graph_url = None

    if request.method == "POST":
        hour = int(request.form["hour"])
        day = int(request.form["day"])
        temperature = float(request.form["temperature"])
        appliance = float(request.form["appliance"])

        # Debugging step: Print received data
        print(f"Received input - Hour: {hour}, Day: {day}, Temperature: {temperature}, Appliance: {appliance}")
        
        features = np.array([[hour, day, temperature, appliance]])

        # Debugging step: Check if features are passed correctly to the model
        print(f"Features passed to model: {features}")

        try:
            # Get prediction from the model
            prediction = model.predict(features)[0]

            # Debugging step: Print out the prediction
            print(f"Prediction: {prediction}")
        except Exception as e:
            print(f"Error during prediction: {e}")
        
        # Generate graphs
        line_graph_url = generate_line_graph(hour, day, temperature, appliance)
        pie_chart_url = generate_pie_chart(hour, day, temperature, appliance)
        bar_graph_url = generate_bar_graph(hour, day, temperature, appliance)

    return render_template("index.html", prediction=prediction, 
                           line_graph_url=line_graph_url,
                           pie_chart_url=pie_chart_url,
                           bar_graph_url=bar_graph_url)

if __name__ == "__main__":
    app.run(debug=True)

