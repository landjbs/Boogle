import numpy as np
duoList = ['julien/ryan', 'ethan/nick', 'harrison/landon']
roomList = [1,2,3]
assignments = np.random.choice(roomList, size=len(duoList), replace=False)
print('\n\n')
for (duo, assignment) in zip(duoList, assignments):
    print(f'{"-"*40}\nRoom {assignment} goes to {duo}\n{"-"*40}')
print('\n\n')
