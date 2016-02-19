.output part_a.txt

select count(*) from Frequency
where docid='10398_txt_earn';

.output part_b.txt
select count(*) from Frequency 
where docid='10398_txt_earn' AND count=1;

.output part_c.txt

create view [part_1] AS
select term from frequency
where docid='10398_txt_earn' AND count=1;

create view [part_2] AS
select term from frequency
where docid='925_txt_trade' AND count=1;

select count(*) from (
select * from [part_1]
union
select * from [part_2]);
drop view [part_1];
drop view [part_2];


.output part_d.txt

select count(distinct docid) 
from frequency 
where term='law' OR term='legal';

.output part_e.txt

select count(*) from 
(select f.docid, count(*)
from frequency f
group by f.docid
having count(f.count)>300);

.output part_f.txt

create view [part_1] AS
select distinct docid from frequency
where term='transactions';

create view [part_2] AS
select distinct docid from frequency
where term='world';

select count(*) from (
select * from [part_1]
intersect
select * from [part_2]);
drop view [part_1];
drop view [part_2];




