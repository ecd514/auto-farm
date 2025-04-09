<?php

    echo '<meta http-equiv="refresh" content="5">';

    $weather_raw = file_get_contents('http://127.0.0.1:5000/api/weather/forecast');
    $weather = json_decode($weather_raw);
    $temperature = $weather->temperature;
    $percentage_of_rain = $weather->percentage_of_rain;
    $detailed_forecast = $weather->detailed_forecast;
?>

<!DOCTYPE html>
<head>
<style>
    body {
        font-family: "Arial", sans-serif;
        font-size: 24px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
</style>
</head>
<body>
<div>
    <?php echo "Temperature: $temperature&deg;F"; ?> <br> <br>
    <?php echo "Chance of rain: $percentage_of_rain%"; ?> <br> <br>
    <?php echo "Detailed forecast: $detailed_forecast%"; ?> 
</div>
</body>
</html>