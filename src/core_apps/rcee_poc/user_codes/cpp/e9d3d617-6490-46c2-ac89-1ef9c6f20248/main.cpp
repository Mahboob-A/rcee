#include <bits/stdc++.h>
using namespace std; 

void sum_of_a_b(int a, int b)
{
    cout << a + b << endl; 
}


int main()
{
    int t, a, b; 
    cin >> t; 
    
    while(t--)
    {
        cin >> a >> b; 
        sum_of_a_b(a, b); 
    }

    return 0;
}