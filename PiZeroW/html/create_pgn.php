<?php
if (isset($_POST['create_pgn']))
{
exec('sudo python /home/pi/v2/createPGN.py');
}
?>


