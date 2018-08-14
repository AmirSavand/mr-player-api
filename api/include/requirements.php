<?php

// Request method (GET, POST, etc...)
$method = $_SERVER["REQUEST_METHOD"];

// Get $_POST content
$_POST = json_decode(file_get_contents("php://input"), true);
$_PUT  = json_decode(file_get_contents("php://input"), true);

// Envirement variables
$is_localhost = $_SERVER["REMOTE_ADDR"] === "127.0.0.1";
$envs = parse_ini_file("env.ini", true);
$env = $envs["prod"];

// Get current env
if ($is_localhost) {
    $env = $envs["dev"];
}

// Load requirements
require "connection.php";

// Database
$db = new Db();

// Header
header("Content-Type: application/json");

// No CORS for localhost
if ($is_localhost) {
    header("Access-Control-Allow-Origin: *");
    header("Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS");
    header("Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token, Authorization");
}

/**
* Prints the API data with status code
*
* @param array $data API response
* @param number $status HTTP response status code
*/
function response($data, $status=200) {
    http_response_code($status);
    if ($data != null) {
        print(json_encode($data));
    }
}

/**
* Check (and handle) if all required params are given
*
* @param array $params Required params
* @param array $method_variable
*/
function require_params($params, $method_variable) {
    foreach ($params as $param) {
        if (!isset($method_variable[$param])) {
            response([$param => "This field is required"], 400);
            return false;
        }
    }
    return true;
}

/**
* Check (and handle) if hidden input is filled
*
* @param array $method_variable
*/
function validate_hidden($method_variable) {
    if (isset($method_variable["hidden"])) {
        response(["error" => "Something went wrong, try again later."], 400);
        return false;
    }
    return true;
}

/**
* Get the YouTube video ID from its URL
*
* @param string $url YouTube video address
*/
function get_youtube_id($url) {
    if (stristr($url, "youtu.be/")) {
        preg_match("/(https:|http:|)(\/\/www\.|\/\/|)(.*?)\/(.{11})/i", $url, $final_id);
        return $final_id[4];
    } else {
        @preg_match("/(https:|http:|):(\/\/www\.|\/\/|)(.*?)\/(embed\/|watch.*?v=|)([a-z_A-Z0-9\-]{11})/i", $url, $idd);
        return $idd[5];
    }
}
