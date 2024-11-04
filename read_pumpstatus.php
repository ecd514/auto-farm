<?php

    echo '<meta http-equiv="refresh" content="5">';

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