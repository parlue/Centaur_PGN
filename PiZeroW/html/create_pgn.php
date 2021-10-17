<?php
if (isset($_POST['create_pgn']))
{
exec('python /home/pi/v2/createPGN.py');
}
?>


