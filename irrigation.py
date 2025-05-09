def get_irrigation_recommendation(soil_input, temp_input, hum_input, crop_type="Maize"):
    import numpy as np
    import skfuzzy as fuzz
    from skfuzzy import control as ctrl

    # Define fuzzy variables
    soil_moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'soil_moisture')
    temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
    humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
    sprinkling = ctrl.Consequent(np.arange(0, 101, 1), 'sprinkling')

    # Default membership functions
    soil_moisture.automf(3)
    humidity.automf(3)
    temperature['cold'] = fuzz.trimf(temperature.universe, [0, 10, 20])
    temperature['warm'] = fuzz.trimf(temperature.universe, [15, 25, 35])
    temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 50])
    sprinkling['low'] = fuzz.trimf(sprinkling.universe, [0, 25, 50])
    sprinkling['medium'] = fuzz.trimf(sprinkling.universe, [30, 50, 70])
    sprinkling['high'] = fuzz.trimf(sprinkling.universe, [60, 80, 100])

    # Crop-specific fuzzy settings
    crop_configs = {
        "Tomato": {
            "soil": [[0, 15, 35], [30, 50, 70], [60, 80, 100]],
            "humidity": [[0, 20, 40], [35, 55, 75], [70, 85, 100]]
        },
        "Wheat": {
            "soil": [[0, 20, 40], [35, 55, 75], [70, 90, 100]],
            "humidity": [[0, 25, 50], [30, 50, 70], [60, 80, 100]]
        },
        "Potato": {
            "soil": [[0, 25, 50], [30, 50, 70], [60, 80, 100]],
            "humidity": [[0, 25, 50], [45, 60, 75], [70, 85, 100]]
        }
        # Add more crops as needed
    }

    # Override default MFs if crop is supported
    if crop_type in crop_configs:
        s_low, s_med, s_high = crop_configs[crop_type]["soil"]
        h_low, h_med, h_high = crop_configs[crop_type]["humidity"]

        soil_moisture['low'] = fuzz.trimf(soil_moisture.universe, s_low)
        soil_moisture['medium'] = fuzz.trimf(soil_moisture.universe, s_med)
        soil_moisture['high'] = fuzz.trimf(soil_moisture.universe, s_high)

        humidity['low'] = fuzz.trimf(humidity.universe, h_low)
        humidity['medium'] = fuzz.trimf(humidity.universe, h_med)
        humidity['high'] = fuzz.trimf(humidity.universe, h_high)

    # Define rules
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

    # Control system
    irrigation_ctrl = ctrl.ControlSystem(rules)
    simulation = ctrl.ControlSystemSimulation(irrigation_ctrl)

    simulation.input['soil_moisture'] = soil_input
    simulation.input['temperature'] = temp_input
    simulation.input['humidity'] = hum_input

    try:
        simulation.compute()
        result = round(simulation.output['sprinkling'], 2)
    except Exception as e:
        return f"Error during computation: {e}"

    if result < 30:
        rec = "Low sprinkling level. Water lightly."
    elif 30 <= result < 70:
        rec = "Medium sprinkling level. Water moderately."
    else:
        rec = "High sprinkling level. Water thoroughly."

    return f"Recommended sprinkling level: {result}%.\n\n{rec}"
