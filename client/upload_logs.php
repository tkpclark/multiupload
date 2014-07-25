<?php
//0.01
ini_set('display_errors', 1);
error_reporting(E_ALL);

require('HttpRequest.class.php');  
  
$config = array(  
            'ip' => '42.62.78.248', // 如空则用host代替  
            'host' => '127.0.0.1',  
            'port' => 80,  
            'errno' => '',  
            'errstr' => '',  
            'timeout' => 30,  
            'url' => '/mul/server/recv_logs.php',  
            //'url' => '/postapi.php',  
            //'url' => '/multipart.php'  
);  
  
$folder="/root/logs/";


echo 'entering '.$folder;
chdir($folder);
$fp=opendir(".");
$i=0;
while(false!=$file=readdir($fp))
{	
    if($file!='.' && $file!='..')
    {	
		echo "===$file===";
		$ext_name = substr($file,strrpos($file, '.')+1);
		$today = date("Y-m-d",time());
		if(false===strpos($file,$today))//not today
		{
			
			//compress !gz file
			if($ext_name != 'gz')
			{
				exec('gzip '.$file);
				$gzfile=$file.".gz";
			}
			else
			{
				$gzfile=$file;
			}
			echo "gzfile name: $gzfile";
			
			//check whether gzfile exist
			/*
			if(file_exists($gzfile))
			{
				
			}
			*/
			//$file="$file";
			$size = filesize($gzfile); 
			$formdata = array(  
				'filesize' => $size
			); 
			$filedata=array(
				array( 
					'name' => 'upfile',  
					'filename' => $gzfile,  
					'path' => $gzfile 
				)
			);
			//print_r($filedata);exit;
			$obj = new HttpRequest();  
			$obj->setConfig($config);  
			$obj->setFormData($formdata);
			$obj->setFileData($filedata);    
			$result = $obj->send('multipart');  
			echo $result;
			$i++;
			//exit;
		}
	}
	
}
closedir($fp);
echo $i;



  


?>
