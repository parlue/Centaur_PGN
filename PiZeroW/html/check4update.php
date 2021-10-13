<?php

exec('sudo wget https://serverurlkommtnoch/cent/update/centupdate.gzip');
$existing_file = '/update/centupdate.gzip';
$new_file = '/tmp/centupdate.gzip';
$haschmich = 'md5';

if (hash_file($haschmich, $existing_file) === hash_file($hashmich, $new_file)) {

//blablablub.....Update-Routine muss hier rein.

}

?>