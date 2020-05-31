<?php

include_once "db.php";
$conn = getConnection();

try{

    $sql="create Table if not exists record(id smallint  unsigned not null AUTO_INCREMENT PRIMARY KEY, name VARCHAR(265) NOT NULL,email VARCHAR(265) NOT NULL,department VARCHAR(265) NOT NULL,position varchar(255) NOT NULL)";
    $conn->exec($sql);

    echo "TABLE CREATED"."<br>";

}

catch(PDOException $pd){

    echo "Error Creating Table: " . $pd->getMessage();

}

$conn=null;//close the database connection

?>