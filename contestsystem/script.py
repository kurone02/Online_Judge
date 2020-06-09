import os, time, sys, glob
import subprocess as proc
from termcolor import colored
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from contest.models import Problems as problemData

testcasesPath = ""

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print("Created!")
        os.system('cmd /c "mkdir workspace"')
        exitcode = os.system(f'cmd /c "g++ -std=c++14 \"{event.src_path}\" -pipe -O2 -s -static -lm -Wl,--stack,66060288 -o \"workspace/prog.exe\" "')
        tokens = event.src_path.split('_')
        problemName = tokens[2]
        testcasesPath = f"testcase/{problemName}"
        if exitcode != 0:
            print(colored("Compile Error!", "red"))
        else:
            print(colored("Compilation Success!", "green"))
            inputFiles = sorted(glob.glob("*.inp"))
            counter = 0
            acceptedTestcases = 0
            for inputFile in inputFiles:
                counter += 1
                testName = ''.join(inputFile[:-1])
                exitcode = proc.call(f"runExe.exe workspace/prog.exe {problemData.time_limit} {problemData.memory_limit} {inputFile} {testName}.out")
                if exitcode == 0:
                    print(colored(f"Test {counter}: accepted"), "green")
                    print(colored(f"Test {counter}: wrong answer"), "red")
                    acceptedTestcases += 1
                elif exitcode == -1:
                    print(colored(f"Test {counter}: unexpected error"), "red")
                elif exitcode == -2:
                    print(colored(f"Test {counter}: time limit exceeded"), "yellow")
                elif exitcode == -3:
                    print(colored(f"Test {counter}: memory limit exceeded"), "yellow")
                else:
                    print(colored(f"Test {counter}: non-zero exit code"), "red")
            print(f"The number of accepted test cases: {acceptedTestcases}")
        
        print("Deleted!")
        os.system('cmd /c "rmdir /s /q workspace"')


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path = 'media/contestant_solutions', recursive = False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
    
