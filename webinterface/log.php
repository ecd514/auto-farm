<?php
    
    echo '<meta http-equiv="refresh" content="5">';

    // import log text file
    $log = file_get_contents('log.txt');
    
    // Split log into array by new line
    $logarray = explode("\n", $log);

    // most recent thirty lines 
    // ten dates, times, and events
    $mostrecentthirty = array_slice($logarray, -30);

    // display each line using foreach
    /*foreach ($mostrecentten as $mostrecent)
    {
        echo $mostrecent;
        echo "<br/>";
    }*/
?>

<!DOCTYPE html>
<head>
<style>
    body {
        font-family: "Arial", sans-serif;
        text-align: center;
    }
    table {        
        border-collapse: collapse;
        text-align: center;
        width: 100%;
    }
    td {
        border: 1px solid;
    }
</style>
</head>
<body>
    <table>
        <tr>
            <th>Date</th>
            <th>Time</th>
            <th>Event</th>
        </tr>
        <?php
            // using php to fill the table
            foreach ($mostrecentthirty as $mostrecent) {
                // split each row of date into three columns
                $element = explode(",", $mostrecent);
                
                // if the log is empty, say that
                if (empty($element[1]) == TRUE) {
        ?>
        <tr> 
            <td> Log </td>
            <td> Is </td>
            <td> Empty </td>
        </tr>
        <?php // close the if and create the else case
                }
                else {
        ?>
        <tr> 
            <td> <?php echo $element[0]; ?> </td>
            <td> <?php echo $element[1]; ?> </td>
            <td> <?php echo $element[2]; ?> </td>
        </tr>
        <?php }}; //end the else and the foreach ?>
            

    </table>
</body>
</html>