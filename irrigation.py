import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def get_irrigation_recommendation(soil_input, temp_input, hum_input, crop_type="Maize"):
    # Define fuzzy variables
    soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
    temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
    humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
    sprinkling = ctrl.Consequent(np.arange(0, 101, 1), 'sprinkling')

    # Default membership functions (used if crop is not customized)
    soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 25, 50])
    soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [30, 50, 70])
    soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [60, 80, 100])

    humidity['low'] = fuzz.trimf(humidity.universe, [0, 25, 50])
    humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
    humidity['high'] = fuzz.trimf(humidity.universe, [60, 80, 100])

    # Membership functions for temperature (common to all)
    temperature['cold'] = fuzz.trimf(temperature.universe, [0, 10, 20])
    temperature['warm'] = fuzz.trimf(temperature.universe, [15, 25, 35])
    temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 50])

    # Membership functions for sprinkling
    sprinkling['low'] = fuzz.trimf(sprinkling.universe, [0, 25, 50])
    sprinkling['medium'] = fuzz.trimf(sprinkling.universe, [30, 50, 70])
    sprinkling['high'] = fuzz.trimf(sprinkling.universe, [60, 80, 100])

    # Customize membership functions based on crop type
    if crop_type.lower() == "tomato":
        # Tomatoes need more moisture
        soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 15, 35])
        soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [30, 50, 70])
        soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [60, 80, 100])
        humidity['low'] = fuzz.trimf(humidity.universe, [0, 20, 40])
        humidity['medium'] = fuzz.trimf(humidity.universe, [35, 55, 75])
        humidity['high'] = fuzz.trimf(humidity.universe, [70, 85, 100])

    elif crop_type.lower() == "wheat":
        # Wheat tolerates dryness
        soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 20, 40])
        soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [35, 55, 75])
        soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [70, 90, 100])

    elif crop_type.lower() == "potato":
        # Potatoes need consistent moisture
        humidity['low'] = fuzz.trimf(humidity.universe, [0, 25, 50])
        humidity['medium'] = fuzz.trimf(humidity.universe, [45, 60, 75])
        humidity['high'] = fuzz.trimf(humidity.universe, [70, 85, 100])

    # Debug: Print terms (optional)
    # print("Soil terms:", soil_moisture.terms)
    # print("Humidity terms:", humidity.terms)

    # Define fuzzy rules
    rules = [
        ctrl.Rule(soil_moisture['low'] & temperature['hot'] & humidity['low'], sprinkling['high']),
        ctrl.Rule(soil_moisture['low'] & temperature['warm'] & humidity['medium'], sprinkling['medium']),
        ctrl.Rule(soil_moisture['medium'] & temperature['warm'] & humidity['medium'], sprinkling['medium']),
        ctrl.Rule(soil_moisture['medium'] & temperature['hot'], sprinkling['high']),
        ctrl.Rule(soil_moisture['high'] | humidity['high'], sprinkling['low']),
        ctrl.Rule(temperature['cold'] & soil_moisture['medium'], sprinkling['low']),
        ctrl.Rule(soil_moisture['medium'] & humidity['low'], sprinkling['medium']),
        ctrl.Rule(temperature['hot'] & humidity['high'], sprinkling['medium']),
        ctrl.Rule(temperature['cold'] & humidity['low'], sprinkling['low']),
    ]

    # Create and simulate control system
    irrigation_ctrl = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(irrigation_ctrl)

    # Provide input values
    simulation.input['soil_moisture'] = soil_input
    simulation.input['temperature'] = temp_input
    simulation.input['humidity'] = hum_input

    try:
        simulation.compute()
        result = round(simulation.output['sprinkling'], 2)
    except Exception as e:
        return f"Error in computation: {e}"

    # Interpret result
    if result < 30:
        recommendation = "Low sprinkling level. Your soil is likely well-moisturized or the weather is not too hot. It's recommended to water your crops lightly."
    elif 30 <= result < 70:
        recommendation = "Medium sprinkling level. Your soil could use moderate irrigation due to the current weather and humidity. Keep an eye on soil moisture."
    else:
        recommendation = "High sprinkling level. The current conditions indicate the need for substantial irrigation. Make sure to water thoroughly, especially if it's hot and dry."

    return f"Recommended sprinkling level: {result}%.\n\n{recommendation}"
