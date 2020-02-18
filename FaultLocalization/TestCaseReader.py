class ReadFile:

    def importResultsFile(self):
        testCaseResuts = []
        results = {}
        tests = []
        totalPassed = 0
        totalFailed = 0
        resultsFileName = "D:\docu\KL\Test\midTestCase"
        with open(resultsFileName, 'r') as file:
            while True:
                line = file.readline()
                # print line
                try:
                    numbers = tuple([int(num) for num in line.split(',')])
                    tests.append(numbers)
                except ValueError:
                    break
                line2 = file.readline()
                # print line2
                if line2 == 'F\n' or line2 == 'F':
                    totalFailed += 1
                    results[numbers] = False
                if line2 == 'P\n' or line2 == 'P':
                    totalPassed += 1
                    results[numbers] = True
                testCaseResuts.append((line.rstrip(), line2.rstrip()))
        return results,testCaseResuts,tests,totalPassed,totalFailed


if __name__ == '__main__':
    rf = ReadFile()
    testtest = rf.importResultsFile()
    print(testtest)