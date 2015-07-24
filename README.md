# Project-2---FSD---Tournament

How to test:
--------------
Download git repository and have it in location readily available
*All without quotes

- 1) Have vagrant installed
- 2) In shell, testing using git shell, navigate to the folder location, cd into vagrant, 
	 and then cd into tournament folder
- 3) Run without quotes - 'vagrant up'
- 4) Run 'vagrant ssh' to connect
- 5) Run 'cd vagrant' then 'cd tournament'
- 6) Run 'psql'
- 7) Run '\i tournament.sql' this will create database and tables
- 8) Run '\q' to exit postgres cli
- 9) Run 'python tournament_test.py' to run test cases.
- 10) tournament.py contains methods to intereact with database.
