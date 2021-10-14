
<?php
$array = file("config.txt");
if (empty($_GET["lichess_tokken"]))
{
	array_splice($array, 0, 1, "#lichesstoken = " . $_GET["lichess_tokken"] . "\n");
	}
	else
	{
  array_splice($array, 0, 1, "lichesstoken = " . $_GET["lichess_tokken"] . "\n");		
	}
	
if (empty($_GET["email"]))
{
	array_splice($array, 1, 1, "#emailaddress = " . $_GET["email"] . "\n");
	}
	else
	{
  array_splice($array, 1, 1, "emailaddress = " . $_GET["email"] . "\n");		
	}	
	
if (empty($_GET["smtp_server"]))
{
	array_splice($array, 2, 1, "#smtpserver = " . $_GET["smtp_server"] . "\n");
	}
	else
	{
  array_splice($array, 2, 1, "smtpserver = " . $_GET["smtp_server"] . "\n");		
	}	

if (empty($_GET["smtp_username"]))
{
	array_splice($array, 3, 1, "#smtpuser = " . $_GET["smtp_username"] . "\n");
	}
	else
	{
  array_splice($array, 3, 1, "smtpuser = " . $_GET["smtp_username"] . "\n");		
	}
	
if (empty($_GET["smtp_encrypted"]))
{
	array_splice($array, 4, 1, "#smtp_encryption = " . $_GET["smtp_encrypted"] . "\n");
	}
	else
	{
  array_splice($array, 4, 1, "smtp_encryption = " . $_GET["smtp_encrypted"] . "\n");		
	}

if (empty($_GET["smtp_password"]))
{
	array_splice($array, 5, 1, "#smtppassword = " . $_GET["smtp_password"] . "\n");
	}
	else
	{
  array_splice($array, 5, 1, "smtppassword = " . $_GET["smtp_password"] . "\n");		
	}
	
if (empty($_GET["email_subject"]))
{
	array_splice($array, 6, 1, "#subject = " . $_GET["email_subject"] . "\n");
	}
	else
	{
  array_splice($array, 6, 1, "subject = " . $_GET["email_subject"] . "\n");		
	}

$string = implode("", $array);

file_put_contents("config.txt", $string);
echo "Settings saved";


?>