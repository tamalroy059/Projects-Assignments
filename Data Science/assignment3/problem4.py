import MapReduce
import sys

mr = MapReduce.MapReduce()
people=set()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    people.add(key)
    people.add(value)
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    for v in list_of_values:
        if v in dict.keys(mr.intermediate):
            temp=mr.intermediate[v]
            if not key in temp:
                mr.emit((v,key))
                mr.emit((key,v))
        else:
            mr.emit((v,key))
            mr.emit((key,v))


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
__author__ = 'ATX'
