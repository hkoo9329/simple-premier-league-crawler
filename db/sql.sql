create table pl_match_db(
    id bigint(20) not null auto_increment,
    match_day datetime not null,
    left_team varchar(255) not null,
    right_team varchar(255) not null,
    score varchar(255),
    primary key (id)
);
-- 스코어가 없는 상위 row 한개를 가져온다. -> update때 사용
select id from pl_match_db where score is null limit 1;
