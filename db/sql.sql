create table pl_match_db(
    id bigint(20) not null auto_increment,
    match_day datetime not null,
    left_team varchar(255) not null,
    right_team varchar(255) not null,
    score varchar(255),
    primary key (id)
);
