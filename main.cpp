#include <iostream>

using namespace std;

int main(){

    int num1, num2;
    cout << "Enter two Number : ";
    cin >> num1 >> num2;

    if(!cin.fail()){
        cout << "Original order\n";
        cout << num1 << " " << num2 << endl;
        num1 = num2 - num1;
        num2 = num2 - num1;
        num1 = num2 + num1;
        cout << "Updated Order\n"<< num1 << " "<< num2 << endl;
}
    return 0;
}