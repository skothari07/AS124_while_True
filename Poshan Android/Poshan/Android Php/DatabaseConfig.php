<?php

//Define your host here.
$db_name="sih2020";
$mysql_username="admin";
$mysql_password="sih2020agnels";
$server_name="sih2020.cfafpwsc4oxl.us-east-2.rds.amazonaws.com";



$con=mysqli_connect($server_name,$mysql_username,$mysql_password,$db_name);
if($con){
echo "Connection success";
}
else{
echo "Connection not success";
}

?>