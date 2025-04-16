<?php
    // refresh page every five seconds
    echo '<meta http-equiv="refresh" content="5">';

    // input pump status data and decode it into a variable
    $pumpstatus_raw = file_get_contents('http://127.0.0.1:5000/api/pump/status');
    $pumpstatus = json_decode($pumpstatus_raw);
    $pumpstatus = $pumpstatus->status;

    // initialize background color variable
    $backgroundcolor = '';

    if ($pumpstatus === 'on') // pump is on
    {
        echo 'On';
        $backgroundcolor = 'green';
    }
    else if ($pumpstatus === 'off') // pump is off
    {
        echo 'Off';
        $backgroundcolor = 'red';
    }
    else // pump status is wrong
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