<html>
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
</html>