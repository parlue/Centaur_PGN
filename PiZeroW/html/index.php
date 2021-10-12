<?php
// Der Punkt steht für das Verzeichnis, in der auch dieses
// PHP-Programm gespeichert ist
$verzeichnis = "./pgn/";
echo "<ol>";

// Test, ob es sich um ein Verzeichnis handelt
if ( is_dir ( $verzeichnis ))
{
    // öffnen des Verzeichnisses
    if ( $handle = opendir($verzeichnis) )
    {
        // einlesen der Verzeichnisses
        while (($file = readdir($handle)) !== false)
        {
            echo "<li>Dateiname: ";
            echo $file;

            echo "<ul><li>Dateityp: ";
            echo filetype( $file );
            echo "</li></ul>\n";
        }
        closedir($handle);
    }
}
echo "</ol>";
?>