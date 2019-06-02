from sklearn.preprocessing import OneHotEncoder

enc = OneHotEncoder(n_values=15)

testList = ['Computers', 'World', 'Business']

testList = testList.transform([['Computers', 1],
                                ['World', 2],
                                ['Business, 2']])

print(testList)

testVector = enc.fit_transform(testList)

print(testVector)
