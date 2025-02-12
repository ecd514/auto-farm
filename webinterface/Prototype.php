<?php
    date_default_timezone_set("America/New_York");

    $pumpurl = "http://localhost:5000/api/pump/status";

    $status_raw = file_get_contents($pumpurl);
    $status = json_decode($status_raw);
    $status = $status->status;

    if(isset($_POST['status']))
    {
        header('Location:Prototype.php');

        if($status === 'on')
        {
            $options = [
                "http" => [
                    "header" => "Content-Type: application/json\r\n" . "Accept: application/json\r\n",
                    "method"  => "POST",
                    "content" => json_encode(["status"=>"off"])
                ]
            ];
            
            $context = stream_context_create($options);
            $response = file_get_contents($pumpurl, false, $context);
            
            echo "Response: " . $response;

            $log = fopen("log.txt", "a");
            if (filesize('log.txt') == 0) {
                fwrite($log, date("m/d/Y,h:ia,") . "Pump Off,");
            }
            else {
                fwrite($log, date("\nm/d/Y,h:ia,") . "Pump Off,");
            }
            fclose($log);
        }
        elseif($status === 'off')
        {            
            $options = [
                "http" => [
                    "header" => "Content-Type: application/json\r\n" . "Accept: application/json\r\n",
                    "method"  => "POST",
                    "content" => json_encode(["status"=>"on"])
                ]
            ];
            
            $context = stream_context_create($options);
            $response = file_get_contents($pumpurl, false, $context);
            
            echo "Response: " . $response;

            $log = fopen("log.txt", "a");
            if (filesize('log.txt') == 0) {
                fwrite($log, date("m/d/Y,h:ia,") . "Pump On,");
            }
            else {
                fwrite($log, date("\nm/d/Y,h:ia,") . "Pump On,");
            }
            fclose($log);

        }
        else
        {
            echo $status;
        }
    }

    file_put_contents('pumpstatus.txt', $status);

?>

<!DOCTYPE html>
<head>
    <style>
        body {
            background-color: whitesmoke;
        }
        
        h1 {
            color: black;
            font-family: "Arial", sans-serif;
        }

        iframe {
            background-color: lightgrey;
            border-radius: 25px;
        }

        button {
            border-radius: 25px;
        }

        .top-right {
            position: fixed;
            top: 10px;
            right: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
    </style>
    
    <title>ECD514</title>

</head>

<body>
    <h1>Current Pump Status</h1>

    <form method="post">
        <button type="submit" name="status">
            Toggle Pump Status
        </button>
    </form>

    <div>
        <iframe src="read_pumpstatus.php" width="200" height="35"></iframe>
    </div>

    <div class="top-right">
        <a href="http://rpi-farm.netbird.cloud/grafana/">
            <img src="icons8-grafana-48.png" width="50" height="50">
        </a>

        <a href="http://rpi-farm.netbird.cloud/prometheus/">
            <img src="icons8-prometheus-48.png" width="50" height="50">
        </a>
    </div>

    <h1>Recent Events</h1>

    <iframe src="log.php" height="225"></iframe>
    
    <a href="log.txt" download>
        <h1>Full Log</h1>
    </a>

    <iframe src="https://forecast.weather.gov/MapClick.php?lat=42.1242647&lon=-75.9280673#current-conditions" height="225" width="1000"></iframe>

</body>

</html>