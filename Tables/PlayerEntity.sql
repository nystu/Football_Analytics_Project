CREATE TABLE Player (
    PlayerID INT NOT NULL AUTO_INCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Height INT NOT NULL, -- Height in inches
    College VARCHAR(255), -- Optional field
    Position VARCHAR(255) NOT NULL,
    DOB DATE NOT NULL, -- DOB will be a date
    PRIMARY KEY (PlayerID),
    CHECK (Height > 0) -- Make sure height is greater than 0
);