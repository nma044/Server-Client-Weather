How to run:
1. Change username and password and clustername manually in storage.py to your own database
(We could have solved this with dotenv, but we were not able to install the packages.)
2. First run the storage.py script, this acts as the server.
3. Then run the wrapper.py script to get the data into the database.
4. Run fmi.py and check the box of the desired data to retrieve the data from the database.

Known bugs:
-If a checkmark is removed in the application then it will not be cleared and still be shown.
-If there is too much data for the application then not all data will be shown.(
	The fix is adding a scrollbar, however we ran out of time, therefore 
	it prints everything in the terminal.
)

Extensions:
We chose to use a cloudbased MongoDB database and a simple GUI.

What we have done:

-fmi.py
	Sets up a UDP connection with storage.py, after sending its address it then recieves the entire database.
	After the user have chosen which data to show it prints the chosen columns of data.

-wrapper.py
	Sets up a TCP connection with storage.py. 
	Gathers current weatherdata on an interval and sends the data to storage.py.

-storage.py
	Runs two threads simultaneously 
		-Thread1: recieveDataConnection()
			-This thread sets up a TCP connection with wrapper.py.
			-It then connects to the database and creates a new collection if it's not there beforehand.
			-Recieves data from wrapper.py and sends it to the database.
		-Thread2: retrieveDataConnection()
			-This thread sets up a UDP connection with fmi.py .
			-It then connects to the database and finds the correct collection.
			-Sends number of rows and then the data.

