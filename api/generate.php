<?php

require "include/requirements.php";

response([
    "party" => strtoupper(substr(str_shuffle(sha1(microtime())), 0, 6)),
    "user"  => strtoupper(str_shuffle(sha1(microtime())))
]);
