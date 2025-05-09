<?php
    ob_start();
    date_default_timezone_set("America/New_York");

    // input pump status and decode it into a variable
    $pumpurl = "http://127.0.0.1:5000/api/pump/status";

    $status_raw = file_get_contents($pumpurl);
    $status = json_decode($status_raw);
    $status = $status->status;

    // if the button is pressed
    if(isset($_POST['status']))
    {
        // if the pump is on
        if($status === 'on')
        {
            // encodes a value of off to the api
            $options = [
                "http" => [
                    "header" => "Content-Type: application/json\r\n" . "Accept: application/json\r\n",
                    "method"  => "POST",
                    "content" => json_encode(["status"=>"off"])
                ]
            ];
            
            $context = stream_context_create($options);
            $response = file_get_contents($pumpurl, false, $context);
            
            // writes to the log the date and time, and that the pump is off
            $log = fopen("log.txt", "a");
            if (filesize('log.txt') == 0) {
                fwrite($log, date("m/d/Y,h:ia,") . "Pump Off,");
            }
            else {
                fwrite($log, date("\nm/d/Y,h:ia,") . "Pump Off,");
            }
            fclose($log);
        }
        // if the pump is off
        elseif($status === 'off')
        {            
            // encodes a value of on to the api
            $options = [
                "http" => [
                    "header" => "Content-Type: application/json\r\n" . "Accept: application/json\r\n",
                    "method"  => "POST",
                    "content" => json_encode(["status"=>"on"])
                ]
            ];
            
            $context = stream_context_create($options);
            $response = file_get_contents($pumpurl, false, $context);
            
            // writes to the log the date and time, and that the pump is on
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
            // if button is pressed but the pump status variable is wrong
            // i.e. not on or off
            // nothing happens
        }
       
        // redirects to same page to clear form submission from button
        // prevents erroneous switching of pump status value
        header('Location:Prototype.php');
        exit;
    }
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
            font-size: 24px;
            height: 50px;
            width: 350px;
        }

        .top-right {
            position: absolute;
            top: 10px;
            right: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .middle-right {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: absolute;
            top: 10%;
            right: 5%; 
        }

        .middle-left {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: absolute;
            top: 10%;
            left: 5%;
        }
        
        .center {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center; 
            position: absolute;
            top: 10%;
            left: 50%;
            transform: translateX(-50%);
        }
    </style>
    
    <title>ECD514</title>

</head>

<body>

    <div class="middle-left">
        <h1>Current Pump Status</h1>
        <form method="post">
            <button type="submit" name="status">
                Toggle Pump Status
            </button>
        </form>
        <iframe src="read_pumpstatus.php" height="255" width="350"></iframe>
    </div>

    <div class="top-right">
        <a href="http://rpi-farm.netbird.cloud/grafana/">
            <img src="icons8-grafana-48.png" width="50" height="50">
        </a>

        <a href="http://rpi-farm.netbird.cloud/prometheus/">
            <img src="icons8-prometheus-48.png" width="50" height="50">
        </a>
    </div>

    <div class="center">
        <h1>Recent Events</h1>
        <iframe src="log.php" height="305" width="350"></iframe>
        <a href="log.txt" download>
            <h1>Full Log</h1>
        </a>
    </div>
    
    <div class="middle-right">
        <h1>Weather</h1>
        <iframe src="read_weather.php" height="305" width="350"></iframe>
    </div>
</body>

</html>