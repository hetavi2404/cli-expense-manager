create DATABASE if not exists expense_manager;

use expense_manager;

create table if not exists expenses{
    id int auto_increment primary key,
    category varchar(50),
    amount float,
    note varchar(255),
    date date
};