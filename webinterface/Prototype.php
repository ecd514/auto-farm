<?php
    $status = file_get_contents('pumpstatus.txt');

    if(isset($_POST['status']))
    {
        header('Location:Prototype.php');

        if($status === 'On')
        {
            $status = 'Off';
        }
        elseif($status === 'Off')
        {
            $status = 'On';
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