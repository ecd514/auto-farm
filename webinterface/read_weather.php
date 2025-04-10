<?php

    echo '<meta http-equiv="refresh" content="5">';

    $weather_raw = file_get_contents('http://localhost:5000/api/weather/forecast');
    $weather = json_decode($weather_raw);
    $temperature = $weather->temperature;
    $percent_rain = $weather->percent_rain;
    //$detailed_forecast = $weather->detailed_forecast;
    //$weather_icon_url = $weather->weather_icon_url;
    //$generated_at = $weather->generated_at;

    echo "Temperature: $temperature\n";
    echo "Chance of rain: $percent_rain"
?>

<!DOCTYPE html>
<head>
<style>
    body {
        font-family: "Arial", sans-serif;
        text-align: center;
    }
</style>
</head>
</html>