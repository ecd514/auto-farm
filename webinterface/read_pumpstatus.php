<?php

    echo '<meta http-equiv="refresh" content="5">';

    $pumpstatus_raw = file_get_contents('http://127.0.0.1:5000/api/pump/status');
    $pumpstatus = json_decode($pumpstatus_raw);
    $pumpstatus = $pumpstatus->status;

    $backgroundcolor = '';

    if ($pumpstatus === 'on')
    {
        echo 'On';
        $backgroundcolor = 'green';
    }
    else if ($pumpstatus === 'off')
    {
        echo 'Off';
        $backgroundcolor = 'red';
    }
    else
    {
        echo 'Error';
        $backgroundcolor = 'grey';
    }

?>

<!DOCTYPE html>
<head>
<style>
    body {
        background-color: <?php echo $backgroundcolor; ?>;
        font-family: "Arial", sans-serif;
        font-size: 96px;
        text-align: center;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
</head>
</html>