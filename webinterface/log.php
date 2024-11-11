<?php
    
    echo '<meta http-equiv="refresh" content="5">';

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