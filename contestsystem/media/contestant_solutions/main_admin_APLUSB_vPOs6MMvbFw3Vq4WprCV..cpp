#include <iostream>
#include <cstdio>
#include <cmath>
#define taskname "CANDLE"
using namespace std;

int main(){
	ios_base::sync_with_stdio(false);
	cin.tie(0); cout.tie(0); if(fopen(taskname".INP", "r"))
	freopen(taskname".INP", "r", stdin),
	freopen(taskname".OUT", "w", stdout);
	int n; cin >> n;
	cout << 2 * n + int(ceil(2 * sqrt(n)));
	return 0;
}