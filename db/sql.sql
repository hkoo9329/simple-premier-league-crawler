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

-- 테이블이 비어 있는지 확인하는 쿼리
SELECT EXISTS (SELECT 1 FROM table);

-- 현재 시간에서 앞 5경기 뒤의 3경기를 반환하는 쿼리
select * from (
    select * from pl_match_db
    where match_day < NOW()
    order by match_day desc
    limit 3
)CNT union (
    select * from pl_match_db
    where match_day >= NOW()
    limit 5
) order by id;

--- 해당 팀의 앞 5경기 뒤의 3경기를 반환하는 쿼리
select * from (
    select * from pl_match_db
    where match_day < NOW() and (left_team = '토트넘' or right_team = '토트넘')
    order by match_day desc
    limit 3
)CNT union (
    select * from pl_match_db
    where match_day >= NOW() and (left_team = '토트넘' or right_team = '토트넘')
    limit 5
) order by id;
