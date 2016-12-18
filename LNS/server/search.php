<!DOCTYPE html>
<html>
<body>
<?php
include_once 'article_class.php';
//
$query = $_GET["query"];
//echo $query;
//echo exec("python /var/www/html/AI/LNS/server/main.py Donald Trump");

/*
 * TODO:
 * Replace path according to DEMO PC
 * Update the execution limit in php.ini
 */

$art = new Article($query);
echo $art->getTweets();
echo "<br><br><br><br> Summaries <br><br><br><br>";
echo $art->getSummaries();
//echo $ret;
echo "<br>";
//echo "$python $codefile $args";

?>
</body>
</html>
