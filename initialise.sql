PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS User (
    UtorID VARCHAR(32) NOT NULL PRIMARY KEY,
    First_Name VARCHAR(128) NOT NULL,
    Middle_Name VARCHAR(128),
    Last_Name VARCHAR(128),
    Status NOT NULL CHECK (Status in ('Instructor', 'Student')),
    Password VARCHAR(256) NOT NULL,
    Instructor VARCHAR(32),
    FOREIGN KEY(Instructor) REFERENCES User(UtorID)
);

CREATE TABLE IF NOT EXISTS Assignment (
    Name VARCHAR(256),
    Description VARCHAR(1024),
    Instructor VARCHAR(32) NOT NULL,
    PRIMARY KEY (Name, Instructor),
    FOREIGN KEY (Instructor) REFERENCES User(UtorID)
);

CREATE TABLE IF NOT EXISTS Grade (
    Assignment VARCHAR(256),
    Student_Id VARCHAR(32),
    Grade FLOAT,
    PRIMARY KEY(Assignment, Student_Id),
    FOREIGN KEY(Student_Id) REFERENCES User(UtorID),
    FOREIGN KEY (Assignment) REFERENCES Assignment(Name)
);

CREATE TABLE IF NOT EXISTS Feedback (
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Content VARCHAR(1024),
    Instructor VARCHAR(32) NOT NULL,
    FOREIGN KEY (Instructor) REFERENCES Instructor(UtorID)
);

CREATE TABLE IF NOT EXISTS Regrade_Request (
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Grade_Id INTEGER,
    Content VARCHAR(1024),
    FOREIGN KEY (Grade_Id) REFERENCES Grade(Id)
);