This is a database implementation for a Swiss - style tournament application.

The database is defined in the tournament.sql file and the db operations are defined in the tournament.py file in order to satisfy the test needs defined in the tournament_test.py. The db operations are considered functional and upto specification if all the test cases defined in the unit test successfully passes. The following output is expected.

1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!


Steps to setup
- Clone or download the entire implementation
- In the terminal navigate to the tournament folder and setup vagrant (VM)
    - First up use the command "vagrant up" to start the VM
    - Once all the dependencies are installed then use the command "vagrant ssh" to log into the VM
- In the VM you will want to "cd /vagrant" to change directory to the synced folders in order to work on your project.
- Then "cd tournament" to work in the tournament project.
- Enter the PSQL command line interface by typing "psql"
- Run the tournament.sql file which will setup the database and necessary tables
- Quit from the PSQL command line interface and then run the tournament_test.py file
- Make sure that all the tests have passed successfully
