import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        import os, time, sys, glob
        import subprocess as proc
        from termcolor import colored
        from contest.models import Problems as problemData
        from contest.models import Submission as submissionData

        #define macro
        maximal = 2**32
        NORMAL = 0
        UNEXPECTED = maximal - 1
        TLE = maximal - 2
        MLE = maximal - 3
        currentDir = os.getcwd()
        specialChar = '\\'
        endl = '\n'
        newSubmission = submissionData()
        newSubmission.log = str()
        sourceCode = open(event.src_path)
        newSubmission.source_code = sourceCode.read()

        print("Created!")
        os.system('cmd /c "mkdir workspace"')
        exitcode = os.system(f'cmd /c "g++ -std=c++14 \"{event.src_path}\" -pipe -O2 -s -static -lm -Wl,--stack,66060288 -o \"workspace/prog.exe\" "')
        tokens = event.src_path.split('_')
        problemName = tokens[3]
        newSubmission.user = tokens[2]
        newSubmission.problem = problemName
        newSubmission.language = "C++"
        testcasesPath = f"testcase/{problemName}"
        problem = problemData.objects.get(title = problemName)
        maxScore = problem.max_score
        if exitcode != 0:
            print(colored("Compile Error!", "red"))
            newSubmission.log += "Compile Error!\n"
        else:
            print(colored("Compilation Success!", "green"))
            newSubmission.log += "Compilation Success!\n"
            inputFiles = sorted(glob.glob(f"{testcasesPath}/*.inp"))
            acceptedTestcases = 0
            for inputFile in inputFiles:
                testName = ''.join((''.join((''.join(inputFile.split('.')[:-1])).split('/')[-1])).split('\\')[-1])
                #print(testName)
                os.system(f'''cmd /c "copy {inputFile.replace('/', specialChar)} workspace > nul"''')
                exitcode = proc.call(f"AutoJudge.exe workspace/prog.exe {problem.time_limit} {problem.memory_limit} {testName}.inp {testName}.out workspace")
                #print(f"copy {inputFile.replace('/', specialChar)} workspace > nul")
                if exitcode == NORMAL:
                    os.system(f''' cmd /c "copy {testcasesPath.replace('/', specialChar)}{specialChar}{testName}.ans workspace > nul"''')
                    verdict = proc.call(f"wcmp.exe workspace/{inputFile} workspace/{testName}.out workspace/{testName}.ans")
                    if verdict == 0:
                        print(colored(f"Test {testName}: accepted", "green"))
                        newSubmission.log += f"Test {testName}: accepted{endl}"
                    elif verdict == 1:
                        print(colored(f"Test {testName}: wrong answer", "red"))
                        newSubmission.log += f"Test {testName}: wrong answer{endl}"
                    elif verdict == 2:
                        print(colored(f"Test {testName}: fail", "red"))
                        newSubmission.log += f"Test {testName}: fail{endl}"
                    else:
                        print(colored(f"Test {testName}: something is wrong?", "red"))
                        newSubmission.log += f"Test {testName}: something is wrong?{endl}"
                    acceptedTestcases += 1
                elif exitcode == UNEXPECTED:
                    print(colored(f"Test {testName}: unexpected error", "red"))
                    newSubmission.log += f"Test {testName}: unexpected error{endl}"
                elif exitcode == TLE:
                    print(colored(f"Test {testName}: time limit exceeded", "yellow"))
                    newSubmission.log += f"Test {testName}: time limit exceeded{endl}"
                elif exitcode == MLE:
                    print(colored(f"Test {testName}: memory limit exceeded", "yellow"))
                    newSubmission.log += f"Test {testName}: memory limit exceeded{endl}"
                else:
                    print(colored(f"Test {testName}: non-zero exit code", "red"))
                    newSubmission.log += f"Test {testName}: non-zero exit code{endl}"
                os.system(f'''cmd /c "del workspace{specialChar}{testName}.inp > nul"''')
                os.system(f'''cmd /c "del workspace{specialChar}{testName}.out > nul"''')
                os.system(f'''cmd /c "del workspace{specialChar}{testName}.ans > nul"''')
            print(f"The number of accepted test cases: {acceptedTestcases}")
            newSubmission.log += f"The number of accepted test cases: {acceptedTestcases}{endl}"
            finalScore = maxScore / len(inputFiles) * acceptedTestcases
            print(f"Verdict: {finalScore}")
            newSubmission.verdict = finalScore
            newSubmission.log += f"Verdict: {finalScore}"
        
        newSubmission.save()
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
    
