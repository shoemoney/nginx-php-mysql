<?php

function getConnection() {
    $db_string = $_SERVER['web2'];
    $db_values = explode(":", $db_string, 4);

    $dsn = "mysql:host=".$db_values[0].";port=3306;dbname=".$db_values[1];
    $username = $db_values[2];
    $password = $db_values[3];

    try{
        $conn = new PDO( $dsn, $username, $password );
        $conn->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
        return $conn;
    }
    catch(PDOException $pd){
        echo $pd->getMessage();
    }
}

?>