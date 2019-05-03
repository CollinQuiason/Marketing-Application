create table IF NOT EXISTS Categories(Category_ID varchar(3) not NULL, 
CatName varchar(20) not NULL, 
constraint pk_Category_ID primary key(Category_ID));
create table IF NOT EXISTS Status_Type
 (Status_ID varchar(2) not NULL,
  StatusName varchar(20) not NULL,
  constraint pk_Status_ID primary key(Status_ID)
 );
create table IF NOT EXISTS Users
 (User_ID varchar(20) not NULL, 
  UserFirstName varchar(20) not NULL,
  UserLasrName varchar(20) not NULL,
  constraint pk_Users_ID primary key(User_ID) 
 );
CREATE TABLE IF NOT EXISTS Moderators
 (User_ID varchar(20) not NULL,
  constraint pk_Users_ID primary key(User_ID),
  constraint fk_Moderators_Users foreign key (User_ID) references Users(User_ID) ON DELETE RESTRICT
 );
create table IF NOT EXISTS Advertisements
 (Advertisements_ID integer unsigned not NULL auto_increment,
  AdvTitle varchar(30) not NULL,
  AdvDetails varchar(50) not NULL,
  AdvDateTime DateTime not NULL,
  price FLOAT4 not NULL,
  User_ID varchar(20) not NULL, 
  Moderator_ID varchar(20),
  Category_ID varchar(10) not NULL,
  Status_ID varchar(2) not NULL,
  constraint pk_Advertisements_ID primary key(Advertisements_ID),
  constraint fk_Advertisements_Users 
  	FOREIGN KEY (User_ID) REFERENCES Users (User_ID) ON DELETE CASCADE,
  constraint fk_Advertisements_Moderators 
  	FOREIGN KEY (Moderator_ID) REFERENCES Moderators(User_ID) ON DELETE SET NULL,
  constraint fk_Advertisements_Categories 
  	FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID) ON DELETE RESTRICT,
  constraint fk_Advertisements_Status_Type 
  	FOREIGN KEY (Status_ID) REFERENCES Status_Type(Status_ID) ON DELETE RESTRICT
 );

/* End table creation */

/* begin data population */

/* Categories data */
insert into Categories (Category_ID, CatName)
values ('CAT','Cars and Trucks'),('HOU','Houseing'),('ELC','Electronics'),('CCA', 'Child Care');

/* Status_Type data*/ 
insert into Status_Type (Status_ID, StatusName)
values ('PN','Pending'),('AC','Active'),('DI','Disapproved');

/* Users Data */ 
insert into Users (User_ID, UserFirstName, UserLasrName)
values ('clarson','Connor','Larson'), ('Jsmith', 'John', 'Smith');

/* Moderators Data */
insert into Moderators(User_ID)
	VALUES ((SELECT User_ID FROM Users where UserFirstName = 'Connor' and UserLasrName = 'Larson' ));


/* Advertisements Data */ 
INSERT into Advertisements (AdvTitle, AdvDetails, AdvDateTime, price, User_ID, Moderator_ID, Category_ID, Status_ID)
	VALUES ('2010 Sedan Subaru', '2010 sedan car in great shape for sale','2017-02-10', 6000,
		(SELECT User_ID FROM Users WHERE  UserFirstName = 'John' and UserLasrName = 'Smith'),
		(SELECT User_ID FROM Moderators WHERE User_ID = 'clarson'), 
		(SELECT Category_ID FROM Categories WHERE CatName = 'Cars and Trucks'), 
		(SELECT Status_ID FROM Status_Type WHERE StatusName = 'Active')
		),
		('Nice Office Desk', ' Nice office desk for sale','2017-02-15', 50.25,
		(SELECT User_ID FROM Users WHERE  UserFirstName = 'John' and UserLasrName = 'Smith'),
		(SELECT User_ID FROM Moderators WHERE User_ID = 'clarson'), 
		(SELECT Category_ID FROM Categories WHERE CatName = 'Houseing'), 
		(SELECT Status_ID FROM Status_Type WHERE StatusName = 'Active')
		), 
		('Smart LG TV for $200 ONLY', 'Smart LG TV 52 inches! Really cheap!','2017-03-15', 200,
		(SELECT User_ID FROM Users WHERE  UserFirstName = 'John' and UserLasrName = 'Smith'),
		(SELECT User_ID FROM Moderators WHERE User_ID = 'clarson'), 
		(SELECT Category_ID FROM Categories WHERE CatName = 'Electronics'), 
		(SELECT Status_ID FROM Status_Type WHERE StatusName = 'Active')
		), 
		(
		'HD Tablet for $25 only', 'Amazon Fire Tablet HD','2017-03-20', 25,
		(SELECT User_ID FROM Users WHERE  UserFirstName = 'John' and UserLasrName = 'Smith'),
		null, 
		(SELECT Category_ID FROM Categories WHERE CatName = 'Electronics'), 
		(SELECT Status_ID FROM Status_Type WHERE StatusName = 'Pending')
		), 
		(
		'Laptop for $100', 'Amazing HP laptop for $100','2017-03-20', 100,
		(SELECT User_ID FROM Users WHERE  UserFirstName = 'John' and UserLasrName = 'Smith'),
		null, 
		(SELECT Category_ID FROM Categories WHERE CatName = 'Electronics'), 
		(SELECT Status_ID FROM Status_Type WHERE StatusName = 'Pending')
		);

