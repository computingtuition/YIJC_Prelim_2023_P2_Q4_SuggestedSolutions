import sqlite3

db = sqlite3.connect('Taxi.db') # existing db file

# clear the Feedback table if it exists (to avoid conflict)
db.execute('''DROP TABLE IF EXISTS Feedback''')

# create the Feedback table according to question
db.execute('''
    CREATE TABLE `Feedback` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`DriverID`	INTEGER,
	`Date`	TEXT,
	`Comment`	TEXT,
	FOREIGN KEY(`DriverID`) REFERENCES `Driver`(`ID`)
);
''')

db.commit()

# read data from Feedback.TXT and insert into the db
file = open('Feedback.TXT', 'r')

# skip header line
header = file.readline()

for line in file:
    line = line.strip().split(',')
    
    # no need to insert to ID column as it is autoincrement
    db.execute('''
        INSERT INTO Feedback(DriverID, Date, Comment)
        VALUES(?, ?, ?)
    ''', (line[0], line[1], line[2]))
    
    db.commit()
file.close()

db.close()