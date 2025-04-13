from prometheus_client import start_http_server, Gauge
import random
import math
import time

# Create metrics
SOIL_TEMPERATURE = Gauge('soil_data_temp_c',
                         'Current soil temperature from the field', ['sensor'])
SOIL_PH = Gauge('soil_data_ph', 'Current soil PH from the field', ['sensor'])
SOIL_MOISTURE = Gauge('soil_data_moisture_perc',
                      'Current soil moisture percentage from the field', ['sensor'])

# Precompute constants
PI = math.pi
HALF_PI = math.pi / 2
SENSOR_IDS = ['0', '1', '2', '3']
PHASE_SHIFTS = [0, HALF_PI, PI, -HALF_PI]


def generate_metrics(sine_wave_iteration):
    # Update pH metrics
    for sensor_id in SENSOR_IDS:
        SOIL_PH.labels(sensor_id).set(random.uniform(1, 14))

    # Calculate base sine value
    base_val = 0.1 * PI * sine_wave_iteration

    # Update temperature metrics
    for sensor_id, phase_shift in zip(SENSOR_IDS, PHASE_SHIFTS):
        temp_value = 20 * math.sin(base_val + phase_shift) + 20
        SOIL_TEMPERATURE.labels(sensor_id).set(temp_value)
        temp_value = 50 * math.sin(base_val + phase_shift) + 50
        SOIL_MOISTURE.labels(sensor_id).set(temp_value)


if __name__ == '__main__':
    start_http_server(8000)
    count = 0

    while True:
        start_time = time.time()
        generate_metrics(count)
        count += 1

        execution_time = time.time() - start_time
        sleep_time = max(0, 5 - execution_time)

        print(f"Execution time: {
              execution_time:.6f}s, Sleeping for: {sleep_time:.6f}s")
        time.sleep(sleep_time)
