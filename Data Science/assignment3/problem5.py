import MapReduce
import sys

mr = MapReduce.MapReduce()
seq=set()
# =============================
# Do not modify above this line

def mapper(record):
    key = record[0]
    value = record[1]
    value = value[0:len(value)-10]
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    for v in list_of_values:
        if v not in seq:
            seq.add(v)
            mr.emit(v)


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
__author__ = 'ATX'
