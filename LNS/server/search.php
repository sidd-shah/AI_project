<!DOCTYPE html>
<html>
<body>
<?php

//
//$query = $_GET["query"];
//echo $query;
//echo exec("python /var/www/html/AI/LNS/server/main.py Donald Trump");

/*
 * TODO:
 * Replace path according to DEMO PC
 * Update the execution limit in php.ini
 */

set_time_limit(5000);
error_reporting(E_ALL);
$python = "/home/d1810/anaconda3/envs/machinelearningpython2/bin/python";
$codefile = "/home/d1810/Documents/Extra/AI/github/AI_project/src/main.py";
$args = "Donald";

echo "HELLO!";
$ret = 0;
ob_start();
// passthru('/usr/bin/python2.7 test.py');
passthru("$python $codefile $args", $ret);
$output = ob_get_clean();
echo $output;
echo $ret;
echo "<br>";
echo "$python $codefile $args";

?>
</body>
</html>