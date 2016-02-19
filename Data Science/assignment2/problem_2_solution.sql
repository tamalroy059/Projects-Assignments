.output part_g.txt

create view [part_1] as
select a.row_num as row_a, a.col_num as col_a, a.value as value_a,
b.row_num as row_b, b.col_num as col_b, b.value as value_b
from a,b
where a.col_num=b.row_num
order by a.row_num asc, b.col_num asc;

create view [part_2] as 
select row_a, col_b, value_a*value_b as value
from [part_1];

select value from
(select row_a,col_b, sum(value) as value
from part_2
group by row_a, col_b)
where row_a=2 AND col_b=3;
