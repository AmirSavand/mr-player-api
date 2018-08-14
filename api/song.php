<?php

require "include/requirements.php";

if ($method === "GET") {

    if (require_params(["key", "value", "last", "limit"], $_GET)) {

        $key = $db->escape($_GET["key"]);
        $value = $db->quote($_GET["value"]);
        $last = $db->escape($_GET["last"]);
        $limit = $db->escape($_GET["limit"]);

        response($db->select("SELECT id, url FROM song WHERE $key=$value AND id > $last LIMIT $limit"), 200);
    }
}

else if ($method === "POST") {

    if (require_params(["user", "party", "url"], $_POST)) {

        $user = $db->quote($_POST["user"]);
        $party = $db->quote($_POST["party"]);
        $url = $db->quote(get_youtube_id($_POST["url"]));

        $db->query("INSERT INTO song (user, party, url) VALUE ($user, $party, $url)");

        response($db->select("SELECT id, url FROM song WHERE id={$db->insert_id()}")[0], 201);
    }
}

else if ($method === "DELETE") {

    if (require_params(["id", "user"], $_POST)) {

        $id = $db->escape($_POST["id"]);
        $user = $db->quote($_POST["user"]);

        $db->query("DELETE FROM song WHERE id=$id AND user=$user");

        response(null, 200);
    }
}
