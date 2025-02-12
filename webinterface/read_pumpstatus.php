<?php

    echo '<meta http-equiv="refresh" content="5">';

    $pumpstatus_raw = file_get_contents('http://localhost:5000/api/pump/status');
    $pumpstatus = json_decode($pumpstatus_raw);
    $pumpstatus = $pumpstatus->status;

    if ($pumpstatus === 'on')
    {
        echo 'Pump is On';
    }
    else if ($pumpstatus === 'off')
    {
        echo 'Pump is Off';
    }
    else
    {
        echo 'Error';
    }

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