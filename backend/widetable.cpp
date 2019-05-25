// Program to illustrate the working of objects and class in C++ Programming
#include <iostream>
using namespace std;

class Test
{
    private:
        int data1;
        float data2;

    public:

       void insertIntegerData(int d)
       {
          data1 = d;
          cout << "Number: " << data1;
        }

       float insertFloatData()
       {
           cout << "\nEnter data: ";
           cin >> data2;
           return data2;
        }
};

 int main()
 {
      Test o1, o2;
      float secondDataOfObject2;

      o1.insertIntegerData(12);
      secondDataOfObject2 = o2.insertFloatData();

      cout << "You entered " << secondDataOfObject2;
      return 0;
 }
