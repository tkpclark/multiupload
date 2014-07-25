<?php
$upload_file_path = '/home/tkp/multiupload/uploadfiles/';

require_once "./log4php/php/Logger.php";
$logging = Logger::getLogger('recv_logs-0.01');

Logger::configure('./log.xml');



/**** ****/
$upfile=$_FILES["upfile"];


/***** ****/
$logging->info("filename:".$upfile['name']." recv_size:".$upfile["size"]." given_size:".$_POST["filesize"]);


/**** ****/
$error=$upfile["error"];
if($error)
{
	$logging->info("upload failed,error:".$error);
	echo $error;
	exit;
}

if(!isset($_POST['filesize']))
{
	$logging->info("error! no filesize arguments!");
	exit;
}

/***** check whether post file *****/
if(!is_uploaded_file($_FILES['upfile']['tmp_name']))
{
	$logging->info("error! it's not http post file!");
	exit;
}



/**** ****/
$target_file = $upload_file_path."/".$upfile["name"];
if($upfile["size"] == $_POST["filesize"])
{
	move_uploaded_file($upfile["tmp_name"],$target_file);
}


if(file_exists($target_file))
{
	echo "ok";
}
else
{
	echo "fail";
}

?> 
