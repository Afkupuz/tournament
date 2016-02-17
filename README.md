# tournament
The second project as part of Udacity's Full Stack NanoDegree program  
  
The project: 
1. Install Vagrant and VirtualBox  
2. Clone the fullstack-nanodegree-vm repository  
3. Launch the Vagrant VM  
4. Write SQL database and table definitions in a file (tournament.sql)  
5. Write Python functions filling out a template of an API (tournament.py)  
6. Run a test suite to verify your code (tournament_test.py)  
  
Grading:  
Grading was based on functionality, table design, code quality and documentation  
  
Extra Credit:
Account for an uneven number of players (possible bye game)  
Add functionality for a tie
Have no re-matches
Add functionality for multiple tournaments


My Project:

To run program:
Have vagrant installed and launch an instance where the tournament folder is accessable  
Example from the OSX terminal:   
$ vagrant up (launches the vagrant server)  
$ vagrant ssh (ssh login to that server)  
$ cd /vagrant/tournament  
  
From this folder calling $ python tournament_test.py will return the results of the tournament.py 
This is an easy way of seeing that the code works.  
The database can be seen by calling $ psql tournament  
other psl commands:  
/i to import   
/? for help  
/dt lists tables  

Expected results:  
The test file will show that python functions in tournament.py are running properly  
The code present in the test file will give an overview of the underlying functionality.  

What to look for:  
functionality for an uneven number of players in the tournament   
functionality for A bye  
functionality for A tie  
functionality for players not rematching  
functionality for pLayers to be ranked based on points  
functionality for multiple tournements  
