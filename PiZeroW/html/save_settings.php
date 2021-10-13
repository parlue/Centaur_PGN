
<?php
$array = file("config.txt");
array_splice($array, 0, 1, "lichesstoken = " . $_GET["lichess_tokken"] . "\n");
array_splice($array, 1, 1, "emailaddress = " . $_GET["email"] . "\n");
array_splice($array, 2, 1, "smtpserver = " . $_GET["smtp_server"] . "\n");
array_splice($array, 3, 1, "smtpuser = " . $_GET["smtp_username"] . "\n");
array_splice($array, 4, 1, "smtp_encryption = " . $_GET["smtp_encrypted"] . "\n");
array_splice($array, 5, 1, "smtppassword = " . $_GET["smtp_password"] . "\n");
array_splice($array, 6, 1, "subject = " . $_GET["email_subject"] . "\n");

$string = implode("", $array);

file_put_contents("config.txt", $string);
echo "Settings saved";
?>