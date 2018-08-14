<?php
class Db {
    protected static $connection;
    /**
    * @return bool false on failure / mysqli MySQLi object instance on success
    */
    public function connect() {
        global $env;
        if (!isset(self::$connection)) {
            self::$connection = new mysqli($env["host"], $env["username"], $env["password"], $env["database"]);
        }
        if (self::$connection === false) {
            return false;
        }
        return self::$connection;
    }
    /**
    * @param $query The query string
    * @return mixed The result of the mysqli::query() function
    */
    public function query($query) {
        return $this->connect()->query($query);
    }
    /**
    * @param $query The query string
    * @return bool False on failure / array Database rows on success
    */
    public function select($query) {
        $rows = array();
        $result = $this->query($query);
        if ($result === false) {
            return false;
        }
        while ($row = $result->fetch_assoc()) {
            $rows[] = $row;
        }
        return $rows;
    }
    /**
    * @return string Database error message
    */
    public function error() {
        return $this->connect()->error;
    }
    /**
    * @param string $value The value to be escaped
    * @return string The escaped string
    */
    public function escape($value) {
        return $this->connect()->real_escape_string($value);
    }
    /**
    * @param string $value The value to be quoted and escaped
    * @return string The quoted and escaped string
    */
    public function quote($value) {
        return "'" . $this->connect()->real_escape_string($value) . "'";
    }
    /**
    * @param string $value The value to be quoted and escaped (to boolean)
    * @return boolean The quoted and escaped string (to boolean)
    */
    public function quote_bool($value) {
        return $value == "true" ? "true" : "false";
    }
    /**
    * @return number Number of affected rows
    */
    public function affected() {
        return $this->connect()->affected_rows;
    }
    /**
    * @return number Last insert id
    */
    public function insert_id() {
        return $this->connect()->insert_id;
    }
}
