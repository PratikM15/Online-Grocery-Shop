create database grocery;

use grocery;




CREATE TABLE customer(
  customer_id int NOT NULL,
  customer_name varchar(100) NOT NULL,
  address varchar(100) NOT NULL,
  contact varchar(100) NOT NULL,
  username varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  constraint customer_pk primary key(customer_id)
);

insert into customer(customer_name,address,contact) values
	('Yash','Bhandara',6786787898),
    ('Pratik','Nahpur',7245465768),
    ('Kunal','Hingna',3435675872),
    ('Anurag','Morshi',3345468883),
    ('Harshal','Amravati',7218023412);



/*create table lose(
vege_name varchar(50),
vege_price varchar(50) not null,
vege_quantity int not null,
fruit_name varchar(50),
fruit_price varchar(50) not null,
fruit_quantity int not null
);*/

create table vege(
vproduct_id int not null auto_increment,
vege_name varchar(50),
vege_price varchar(50) not null,
vegetotal_quantity int not null,
constraint vproduct_pk primary key(vproduct_id)
);


insert into vege(vege_name,vege_price,vegetotal_quantity) values
	('Brinjal','50kg',30),
    ('Cauliflower','40kg',20),
    ('Cabage','20kg',30),
    ('Potato','70kg',40),
    ('Onion','100kg',60),
    ('Spinach','25kg',50);


create table fruit(
fproduct_id int not null auto_increment,
fruit_name varchar(50),
fruit_price varchar(50),
fruittotal_quantity int not null,
constraint fproduct_pk primary key(fproduct_id)
);

insert into fruit(fruit_name,fruit_price,fruittotal_quantity) values
	('Apple','50kg',30),
    ('Banana','40kg',20),
    ('Grapes','20kg',30),
    ('Cherry','70kg',40),
    ('Orange','10kg',60),
    ('Chickoo','25kg',50);
    


create table cart(
cart_id int not null,
vege_name varchar(50),
vegeqty_taken int not null,
fruit_name varchar(50),
fruitqty_taken int not null,
vproduct_id int,
fproduct_id int,
constraint cart_pk primary key(cart_id),
foreign key(vproduct_id) references vege(vproduct_id),
foreign key(fproduct_id) references fruit(fproduct_id)
);



create table purchase(
product_id int not null,
products varchar(200),
total_amount int not null,
constraint product_pk primary key(product_id)
);


  
    
alter table customer
	modify customer_id int not null auto_increment;
    



alter table cart
	modify cart_id int not null auto_increment,auto_increment=1000;
    
alter table purchase
	modify product_id int not null auto_increment;
    
    
    









