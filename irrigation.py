import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def get_irrigation_recommendation(soil_input, temp_input, hum_input, crop_type="maize"):
    # Define fuzzy variables
    soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
    temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
    humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
    sprinkling = ctrl.Consequent(np.arange(0, 101, 1), 'sprinkling')

    # Standard membership functions for temperature & sprinkling
    temperature['cold'] = fuzz.trimf(temperature.universe, [0, 10, 20])
    temperature['warm'] = fuzz.trimf(temperature.universe, [15, 25, 35])
    temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 50])

    sprinkling['low'] = fuzz.trimf(sprinkling.universe, [0, 25, 50])
    sprinkling['medium'] = fuzz.trimf(sprinkling.universe, [30, 50, 70])
    sprinkling['high'] = fuzz.trimf(sprinkling.universe, [60, 80, 100])

    # Standard/default for maize (and fallback)
    if crop_type.lower() in ["maize", "default"]:
        soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 25, 50])
        soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [30, 50, 70])
        soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [60, 80, 100])

        humidity['low'] = fuzz.trimf(humidity.universe, [0, 25, 50])
        humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
        humidity['high'] = fuzz.trimf(humidity.universe, [60, 80, 100])

    elif crop_type.lower() == "tomato":
        soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 15, 35])
        soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [30, 50, 70])
        soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [60, 80, 100])

        humidity['low'] = fuzz.trimf(humidity.universe, [0, 20, 40])
        humidity['medium'] = fuzz.trimf(humidity.universe, [35, 55, 75])
        humidity['high'] = fuzz.trimf(humidity.universe, [70, 85, 100])

    elif crop_type.lower() == "wheat":
        soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 20, 40])
        soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [35, 55, 75])
        soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [70, 90, 100])

        humidity['low'] = fuzz.trimf(humidity.universe, [0, 25, 50])
        humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
        humidity['high'] = fuzz.trimf(humidity.universe, [60, 80, 100])

    elif crop_type.lower() == "potato":
        soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 25, 50])
        soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [30, 50, 70])
        soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [60, 80, 100])

        humidity['low'] = fuzz.trimf(humidity.universe, [0, 25, 50])
        humidity['medium'] = fuzz.trimf(humidity.universe, [45, 60, 75])
        humidity['high'] = fuzz.trimf(humidity.universe, [70, 85, 100])

    else:
        # fallback: same as maize
        soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, [0, 25, 50])
        soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, [30, 50, 70])
        soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, [60, 80, 100])

        humidity['low'] = fuzz.trimf(humidity.universe, [0, 25, 50])
        humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
        humidity['high'] = fuzz.trimf(humidity.universe, [60, 80, 100])

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

    irrigation_ctrl = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(irrigation_ctrl)

    sim.input['soil_moisture'] = soil_input
    sim.input['temperature'] = temp_input
    sim.input['humidity'] = hum_input

    try:
        sim.compute()
        result = round(sim.output['sprinkling'], 2)
    except Exception as e:
        return f"Error in fuzzy computation: {e}"

    if result < 30:
        msg = "Low sprinkling level. Water lightly."
    elif result < 70:
        msg = "Medium sprinkling level. Monitor and water moderately."
    else:
        msg = "High sprinkling level. Strong irrigation recommended."

    return f"Recommended sprinkling: {result}%.\n\n{msg}"
