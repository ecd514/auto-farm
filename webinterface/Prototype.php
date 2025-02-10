<?php
    date_default_timezone_set("America/New_York");

    $status_raw = file_get_contents('http://localhost:5000/api/pump/status');
    // http://localhost:5000/api/pump/status
    $status = json_decode($status_raw);
    $status = $status->status;
    echo $status;
    if(isset($_POST['status']))
    {
        header('Location:Prototype.php');

        if($status === 'on')
        {
            $status = 'off';
            $log = fopen("log.txt", "a");

            // if statement to check if file is empty
            // if it is, the first newline is not added
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
            $status = 'on';
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

    <h1>Recent Events</h1>

    <iframe src="log.php" height="225"></iframe>
    
    <a href="log.txt" download>
        <h1>Full Log</h1>
    </a>

</body>

</html>