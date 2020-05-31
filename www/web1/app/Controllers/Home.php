<?php namespace App\Controllers;

use Config\Database;

class Home extends BaseController
{
    protected $db;

    private function initDB() {
        if ($this->db === null)
        {
            $this->db = Database::connect('default', FALSE);
            $this->db->initialize();
        }

        // Table
        $this->db->query("create table if not exists Members(memid smallint unsigned not null AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(265) NOT NULL, lastname VARCHAR(265) NOT NULL)");

        // Insert
        $this->db->query("INSERT IGNORE INTO Members (memid, firstname, lastname) VALUES (1, 'John', 'Doe'), (2, 'Steve', 'Jobs')");

        $query = $this->db->query('SELECT * FROM Members');
        return $query->getResult();
    }

	public function index()
	{
	    $data['members'] = $this->initDB();
		return view('welcome_message', $data);
	}

	//--------------------------------------------------------------------

}
