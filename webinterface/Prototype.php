<?php
    date_default_timezone_set("America/New_York");

    $status = file_get_contents('pumpstatus.txt');

    if(isset($_POST['status']))
    {
        header('Location:Prototype.php');

        if($status === 'On')
        {
            $status = 'Off';
            $log = fopen("log.txt", "a");
            fwrite($log, date("m/d/Y h:ia") . " Pump Off\n");
            fclose($log);
        }
        elseif($status === 'Off')
        {
            $status = 'On';
            $log = fopen("log.txt", "a");
            fwrite($log, date("m/d/Y h:ia") . " Pump On\n");
            fclose($log);
        }
        else
        {
            echo 'Error';
        }
    }

    file_put_contents('pumpstatus.txt', $status);

?>

<!DOCTYPE html>
<head>
    <title>ECD514</title>

    <!--<meta http-equiv="refresh" content="5">-->

</head>

<body>
    <h1>Current Pump Status</h1>

    <form method="post">
        <button type="submit" name="status">
            Toggle Pump Status
        </button>
    </form>



    <div>
        <iframe src="read_pumpstatus.php" width="115" height="35"></iframe>
    </div>

    <h1>Recent Events</h1>

    <iframe src="log.php" height="210"></iframe>
    
    <a href="log.txt" download>
        <h1>Full Log</h1>
    </a>

</body>

</html>