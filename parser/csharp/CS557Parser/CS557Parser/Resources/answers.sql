CREATE TABLE answer (
	id INT NOT NULL AUTO_INCREMENT,
	answerId INT NOT NULL,
	parentId INT NOT NULL,
	creationDate DATETIME,
	score INT,
	code TEXT,
	ownerUserId INT,
	lastEditorUserId INT,
	lastEditorDisplayName VARCHAR(40) NOT NULL,
	lastEditDate DATETIME,
	lastActivityDate DATETIME,
	commentCount INT,
	communityOwnedDate DATETIME,
	PRIMARY KEY(id)
);