<?php
class Database
{
    private $host = 'mysql';
    private $username = 'demo';
    private $password = '123123';
    private $database = 'company';
    private $connection;

    public function __construct()
    {
        $this->connection = new mysqli($this->host, $this->username, $this->password, $this->database);

        if ($this->connection->connect_error) {
            die('Error en la conexión a la base de datos: ' . $this->connection->connect_error);
        }
    }

    public function getConnection()
    {
        return $this->connection;
    }
}
