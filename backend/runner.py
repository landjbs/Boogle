x = [1,2,3]
y = ['a','b','c']

dataList = [x,y]

resultList = []
counter = 0
while len(resultList) < 20:
    for data in dataList:
        print(data[counter])
    counter +=1
