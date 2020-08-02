
<?php
define('HOST','sih2020.cfafpwsc4oxl.us-east-2.rds.amazonaws.com');
define('USER','admin');
define('PASS','sih2020agnels');
define('DB','sih2020');



 
$con = mysqli_connect(HOST,USER,PASS,DB);
$var  = $_GET['mob_no'];
$name="Name: ";
 
$sql = "select * from beneficiary_beneficiary_register where  u_phone =$var";
 
$res = mysqli_query($con,$sql);

 
$result = array();
 
while($row = mysqli_fetch_array($res)){
array_push($result,array('u_fname'=>$row[1],
'u_phone'=>$row[12],
'u_status'=>$row[8],
'id'=>$row[0]

));
}
 
echo json_encode(array("result"=>$result));
 
mysqli_close($con);
 
?>