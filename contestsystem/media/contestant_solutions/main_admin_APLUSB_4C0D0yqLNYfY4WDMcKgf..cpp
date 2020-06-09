#include <bits/stdc++.h>
using namespace std;

int main(){
	string folderName="D:/MyCode/FacebookHackerCup/Round1/";
	string taskname="GraphsAsAService";
	string extend="cpp";
	string fileName=taskname+'.'+extend;
    system(("g++ -std=c++14 "+folderName+fileName+" -pipe -O2 -s -static -lm -Wl,--stack,66060288 -x c++ -o "+folderName+taskname).c_str());
    system("Untitled1.exe");
    return 0;
}