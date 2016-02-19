import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    key = record[1]
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    order=None
    for v in list_of_values:
        if v[0]=='order':
            order=v
            list_of_values.remove(v)

    final_output=[]

    if order is not None:
        for v in list_of_values:
            mr.emit(order+v)


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
__author__ = 'ATX'
