<html>
	
<form action="check4update.php" method="post">
	<table>
		<tr><td>Check for Software-Update:</td><td><input type="submit" name="update_check" value="Update" /></td></tr>
  </table>
</form>	
	
<form action="create_pgn.php" method="post">
	<table>
		<tr><td>Create PGN:</td><td><input type="submit" name="create_pgn" value="new" /></td></tr>
  </table>
</form>


<form action="create_pgn.php" method="post">
	<table>
		<tr><td>PGN-Datei erstellen:</td><td><input type="submit" name="create_pgn" value="new" /></td></tr>
  </table>
</form>

<br><br>
PGN-Files Download<br>
<?php
$ftype = filetype( $file );
$verzeichnis = "/home/pi/www/pgn/";
echo "<ol>";


if ( is_dir ( $verzeichnis ))
{
   
    if ( $handle = opendir($verzeichnis) )
    {
      
        while (($file = readdir($handle)) !== false)
        {
            
            echo "<li>Dateiname: ";
            echo "<a href=\"$file\">$file</a> ";
            echo "<ul><li>Dateityp: ";
            echo filetype( $file );
            echo "</li></ul>\n";
           
        }
        closedir($handle);
    }
}
echo "</ol>";
?>
<br><br>
	
<form action="save_settings.php" method="get">
	
	<table>
   <tr><td>Lichess Tokken:</td><td><input type="text" name="lichess_tokken" /></td></tr>
   <tr><td>Email:</td><td><input type="text" name="email" /></td></tr>
   <tr><td>SMTP Server:</td><td><input type="text" name="smtp_server" /></td></tr>
   <tr><td>SMTP Username:</td><td><input type="text" name="smtp_username" /></td></tr>
   <tr><td>SMTP encrypted?</td><td><input type="radio" name="smtp_encrypted" value="yes" />Yes <input type="radio" name="smtp_encrypted" value="no" />No<br /></td></tr>
   <tr><td>SMTP Password:</td><td><input type="password" name="smtp_password" /></td></tr>
   <tr><td>Email Subject:</td><td><input type="text" name="email_subject" /></td></tr>
   <tr><td></td><td></td></tr>
   <tr><td><input type="reset" value="Reset" /></td><td><input type="submit" value="Save" /></td></tr>
  </table>
</form>
</html>
