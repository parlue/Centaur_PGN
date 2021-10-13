<?php

exec('sudo wget https://serverurlkommtnoch/cent/update/centupdate.gz');
$existing_file = '/update/centupdate.gz';
$new_file = '/tmp/centupdate.gz';
$haschmich = 'md5';

if (hash_file($algo, $existing_file) === hash_file($algo, $new_file)) {

//blablablub.....Update-Routine muss hier rein.

}

?>
