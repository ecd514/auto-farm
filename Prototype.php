<!DOCTYPE html>
<head>
    <title>ECD514</title>

    <meta http-equiv="refresh" content="5">

</head>

<body>
    <h1>Current Pump Status</h1>

    <?php

        $pumpstatus = file_get_contents('pumpstatus.txt');

        if ($pumpstatus === 'On')
        {
            echo 'Pump is On';
        }
        else if ($pumpstatus === 'Off')
        {
            echo 'Pump is Off';
        }
        else
        {
            echo 'Error';
        }

    ?>

    <h1>Recent Events</h1>

    <?php
    
        // import log text file
        $log = file_get_contents('log.txt');
    
        // Split log into array by new line
        $logarray = explode("\n", $log);

        // most recent ten lines 
        $mostrecentten = array_slice($logarray, -10);
        
        // display each line using foreach
        foreach ($mostrecentten as $mostrecent)
        {
            echo $mostrecent;
            echo "<br/>";
        }

    ?>
    
    <a href="log.txt" download>
        <h1>Full Log</h1>
    </a>

</body>

</html>