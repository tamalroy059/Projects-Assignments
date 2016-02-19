import MapReduce
import sys

b_matrix={}
mr = MapReduce.MapReduce()
# =============================
# Do not modify above this line

def mapper(record):

    if record[0]=='a':
        key=record[1];
        value = record
        mr.emit_intermediate(key,value)
    if record[0]=='b':
        if not record[2] in b_matrix.keys():
            temp=[]
            temp.append(record)
            b_matrix[record[2]]=temp
        else:
            temp=b_matrix[record[2]]
            temp.append(record)
            b_matrix[record[2]]=temp




def reducer(key, list_of_values):

    for k in b_matrix.keys():
        result=0
        b_temp=b_matrix[k]
        for i in list_of_values:
            for j in b_temp:
                if(i[2]==j[1]):
                    result=result+i[3]*j[3]
                    break
        if result!=0:
            mr.emit((key,k,result))
        result=0

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])

  mr.execute(inputdata, mapper, reducer)
__author__ = 'ATX'
