#include <iostream>
#include <string>
#include <sstream>
#include <dirent.h>
#include <time.h>
#include <windows.h>
#include <psapi.h>
#include <tchar.h>
#define NORMAL (0)
#define UNEXPECTED (-1)
#define TLE (-2)
#define MLE (-3)
using namespace std;

class TestCasesConfig{
public:
    string problemName;
    int timeLimit;
    long long memoryLimit;
    inline TestCasesConfig(string name = "", int tl = 250, long long mem = 256){
        problemName = name;
        timeLimit = tl;
        memoryLimit = mem;
    }
};

class ContestantData{
public:
    int runTime, exitcode;
    long long memoryUsed;
    inline ContestantData(int rt = 0, int mem = 0, int ec = 0){
        runTime = rt;
        memoryUsed = mem;
        exitcode = ec;
    }
};

class Judge: public TestCasesConfig, public ContestantData{
    string testcasesDir, exeDir;
public:
    inline Judge(string name = "", string tcDir = "", string eDir = "", int tl = 250, long long mem = 256){
        //cout << name << '\n';
        problemName = name;
        timeLimit = tl;
        memoryLimit = mem;
        testcasesDir = tcDir;
        exeDir = eDir;
        runTime = 0;
        memoryUsed = 0;
        exitcode = NORMAL;
    }

    int runExe(const string &inputFile, const string &outputFile){
        char* my_appName = NULL;
        char * my_lpCmd = new char[problemName.size() + 1];
        copy(problemName.begin(), problemName.end(), my_lpCmd);
        my_lpCmd[problemName.size()] = '\0';
        //cout << problemName << '\n' << my_lpCmd << '\n';
        //char* my_lpCmd = problemName.c_str();
        SECURITY_ATTRIBUTES secureA;
        secureA.nLength = sizeof(secureA);
        secureA.lpSecurityDescriptor = NULL;
        secureA.bInheritHandle = TRUE;
        LPSECURITY_ATTRIBUTES my_lpProcessAttributes = NULL;
        LPSECURITY_ATTRIBUTES my_lpThreadAttributes = NULL;
        bool my_inheritHandles = true;
        DWORD my_creationFlag = NORMAL_PRIORITY_CLASS;
        LPVOID my_lpEnvironment = NULL;
        char* my_directory = NULL;
        STARTUPINFOA my_startupInfo;
        ZeroMemory(&my_startupInfo, sizeof(STARTUPINFOA));
        my_startupInfo.cb = sizeof(STARTUPINFOA);
        my_startupInfo.hStdInput = CreateFile(_T(inputFile.c_str()),
                                              GENERIC_READ,
                                              0,
                                              &secureA,
                                              OPEN_EXISTING,
                                              FILE_ATTRIBUTE_READONLY,
                                              NULL );
        my_startupInfo.hStdOutput = CreateFile(_T(outputFile.c_str()),
                                              FILE_WRITE_DATA,
                                              FILE_SHARE_WRITE,
                                              &secureA,
                                              OPEN_ALWAYS,
                                              FILE_ATTRIBUTE_NORMAL,
                                              NULL );
        my_startupInfo.dwFlags |= STARTF_USESTDHANDLES;

        PROCESS_INFORMATION my_processInfo;

        //Ref = http://msdn.microsoft.com/library/default.asp?url=/library/en-us/dllproc/base/createprocess.asp
        bool ok = CreateProcess(my_appName, my_lpCmd, my_lpProcessAttributes, my_lpThreadAttributes, my_inheritHandles,
                                my_creationFlag, my_lpEnvironment, my_directory, &my_startupInfo, &my_processInfo);
        if(!ok) return UNEXPECTED;
        int beginTime = clock();
        int endTime = beginTime + timeLimit;
        DWORD exitCode;
        while(clock() < endTime){
            GetExitCodeProcess(my_processInfo.hProcess, &exitCode);
            if(exitCode<256) return exitcode; //Does not MLE or TLE!
            PROCESS_MEMORY_COUNTERS_EX pmc;
            GetProcessMemoryInfo(my_processInfo.hProcess, (PROCESS_MEMORY_COUNTERS*)&pmc, sizeof(pmc));
            SIZE_T curMem = pmc.WorkingSetSize;
            memoryUsed = max(memoryLimit, (long long)curMem / 1024);
            if(memoryUsed / 1024 >= memoryLimit){
                bool terminate = TerminateProcess(my_processInfo.hProcess, 0);
                return MLE; //Memory limit exceed!
            }
            Sleep(10);
        }
        bool terminate = TerminateProcess(my_processInfo.hProcess, 0);
        return TLE; //Time limit exceed!
    }
};

inline int convertToInt(const string &str){
    stringstream ss;
    ss << str;
    int res; ss >> res;
    return res;
}

int main(int argc, char *argv[]){
    if(argc < 2){
        cout << "More agruments are expected!\n";
        return UNEXPECTED;
    }
    Judge judger(argv[1], "", "", convertToInt(argv[2]), convertToInt(argv[3]));
    chdir(argv[6]);
    int exitcode = judger.runExe(argv[4], argv[5]);
    return exitcode;
}
