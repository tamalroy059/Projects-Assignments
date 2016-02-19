.header ON
.mode columns
.output part_h.txt
create view [part1] as 
select a.docid as docid_a, a.term as term_a, a.count as count_a,
b.term as term_b, b.docid as docid_b, b.count as count_b
from frequency a, frequency b
where a.term=b.term AND a.docid='10080_txt_crude' AND
b.docid='17035_txt_earn'
order by a.docid asc, b.docid asc;


create view [part2] as
select docid_a, docid_b, sum(count_a*count_b) as sum_value
from part1
group by docid_a, docid_b;

select sum_value from part2;

drop view part1;
drop view part2;


.output part_i.txt

create view freq as
select * FROM frequency 
UNION
select 'q' as docid, 'washington' as term, 1 as count
UNION 
select 'q' as docid, 'taxes' as term, 1 as count
UNION
select 'q' as docid, 'treasury' as term, 1 as count;

create view target as

select 'q' as docid, 'washington' as term, 1 as count
UNION 
select 'q' as docid, 'taxes' as term, 1 as count
UNION
select 'q' as docid, 'treasury' as term, 1 as count;


create view [part1] as 
select a.docid as docid_a, a.term as term_a, a.count as count_a,
b.term as term_b, b.docid as docid_b, b.count as count_b
from frequency a, target b
where a.term=b.term
order by a.docid asc, b.docid asc;


create view [part2] as
select docid_a, docid_b, term_b, sum(count_a*count_b) as sum_value
from part1
group by docid_a, docid_b;

select maxvalue from
(select docid_a, max(sum_value) as maxvalue
from part2
group by term_b);

