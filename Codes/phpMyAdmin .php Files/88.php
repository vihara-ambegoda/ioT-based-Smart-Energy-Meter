<?php
class Asc712{
 public $link='';
 function __construct($CURRENT, $VOLTAGE){
  $this->connect();
  $this->storeInDB($CURRENT, $VOLTAGE);
  MYSQL *conn = "COM1";  //virtual   
 }
 
 function connect(){
  $this->link = mysqli_connect('localhost','root','') or die('Cannot connect to the DB');
  mysqli_select_db($this->link,'<Your Database Name>') or die('Cannot select the DB');
 }
 
 function storeInDB($CURRENT, $VOLTAGE){
  $query = "insert into Asc712 set VOLTAGE='".$VOLTAGE."', CURRENT='".$CURRENT."'";   //table name
  $result = mysqli_query($this->link,$query) or die('Errant query:  '.$query);
 }
 
}
if($_GET['CURRENT'] != '' and  $_GET['VOLTAGE'] != ''){
 $Asc712=new Asc712($_GET['CURRENT'],$_GET['VOLTAGE']);
}

?>