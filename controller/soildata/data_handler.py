import requests
import time
from datetime import datetime
import pandas as pd


def get_prometheus_data(query, prometheus_url):
    """
    Query Prometheus and return the result.

    Args:
        query (str): PromQL query
        prometheus_url (str): URL of Prometheus server

    Returns:
        dict: Response from Prometheus
    """
    response = requests.get(
        f"{prometheus_url}/api/v1/query",
        params={
            "query": query,
            "time": time.time()
        }
    )

    if response.status_code != 200:
        raise Exception(f"Query failed with status code {
                        response.status_code}. Response: {response.text}")

    return response.json()


def get_active_sensors(prometheus_url):
    """
    Get all active sensors sending soil_data_moisture_perc metrics.

    Args:
        prometheus_url (str): URL of Prometheus server

    Returns:
        list: List of sensor names
    """
    query = "count by (sensor) (soil_data_moisture_perc)"
    result = get_prometheus_data(query, prometheus_url)

    sensors = []
    if result["status"] == "success" and result["data"]["resultType"] == "vector":
        for metric in result["data"]["result"]:
            if "sensor" in metric["metric"]:
                sensors.append(metric["metric"]["sensor"])

    return sensors


def get_sensor_average(sensor, prometheus_url, minutes=2):
    """
    Get average moisture percentage for a specific sensor over the past X minutes.

    Args:
        sensor (str): Name of the sensor
        prometheus_url (str): URL of Prometheus server
        minutes (int): Time range in minutes

    Returns:
        float: Average moisture percentage
    """
    query = f'avg_over_time(soil_data_moisture_perc{{sensor="{
        sensor}"}}[{minutes}m])'
    result = get_prometheus_data(query, prometheus_url)

    if result["status"] == "success" and result["data"]["resultType"] == "vector":
        if result["data"]["result"]:
            return float(result["data"]["result"][0]["value"][1])

    return None


def main():
    prometheus_url = "http://localhost:9090"

    print(f"Checking active sensors at {
          datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    try:
        # Get all active sensors
        sensors = get_active_sensors(prometheus_url)

        if not sensors:
            print("No active sensors found.")
            return

        print(f"Found {len(sensors)} active sensors.")
        print("")

        # Create a data structure for the results
        results = []

        # Get average for each sensor
        for sensor in sensors:
            avg_moisture = get_sensor_average(sensor, prometheus_url)

            if avg_moisture is not None:
                print(f"Sensor: {sensor}")
                print(f"Average moisture (past 2 min): {avg_moisture:.2f}%")
                print("-" * 30)

                results.append({
                    "sensor": sensor,
                    "average_moisture": avg_moisture
                })

        # Create a summary DataFrame
        if results:
            df = pd.DataFrame(results)
            print("\nSummary:")
            print(df.sort_values("average_moisture", ascending=False))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
