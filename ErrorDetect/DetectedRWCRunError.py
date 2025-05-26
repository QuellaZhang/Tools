import re
import os

def DetectedRWCRunError(sliceName):

    # 1. Filter build stage, build number, error, snapshot.
    errorList = []
    errorList.append('\n')
    errorList.append(sliceName)
    errorList.append('\n')

    with open(sliceName, 'r+', encoding="utf-8") as file:
        while True:
            line = file.readline()
            if not line:
                break

            # Match setup, build, runtest stage
            if ("Configuring Project: " in line) or ("Building Project: " in line) or ("Testing Project: " in line):
                errorList.append(line)
                continue

            # Build Number
            # BuildNumber = re.search("Valid build number found:", line, re.IGNORECASE)

            # Error Types
            CMakeError = re.search(" CMake Error ", line, re.IGNORECASE)
            Failed = re.search(" Failed ", line)
            Error  = re.search(" error: ", line)
            Cancel = re.search("The operation was canceled.", line)
            ErrorMSB = re.search(" error MSB", line)
            Assertion = re.search(" Assertion failed", line)
            ErrorC = re.search(" error C", line)
            FatalErrorC = re.search("fatal  error C", line)
            FatalErrorC2 = re.search("fatal error C", line)
            ErrorCS = re.search("error CS", line)
            ErrorNETSDK = re.search("error NETSDK", line)
            ErrorWMC = re.search("error WMC", line)
            ICError = re.search("INTERNAL COMPILER ERROR", line)
            CompilerError = re.search("Compiler error", line)
            LINKError = re.search("LINK : fatal error LNK", line)
            LINKError2 = re.search("error LNK2019", line)

            # Useless error message
            ProjectDisabled = re.search("ProjectDisabled", line) # Comment from disabled projects
            FailedToFind1 = re.search(" Failed to find ", line) # cmake info
            FailedToFind2 = re.search(" error: pathspec ", line) # cmake info
            FailedToFind3 = re.search(" error: command ", line) # cmake info
            FailedToFind4 = re.search("Download-File : Failed", line)

            if (not ProjectDisabled) and (CMakeError or (not FailedToFind1 and Failed and not FailedToFind4 and Failed ) \
                    or (not FailedToFind2 and Error and not FailedToFind3 and Error) \
                    or Cancel or ErrorMSB \
                    or Assertion or ErrorC or FatalErrorC or ErrorCS or ErrorNETSDK or ErrorWMC \
                    or ICError or CompilerError or LINKError or FatalErrorC2 or LINKError2):
                errorList.append(line)

    # 2. Filter out the error information corresponding to the project.
    projectErrorList = []

    for i in range(0, len(errorList) - 1):

        currentLine = errorList[i]
        nextLine = errorList[i + 1]

        if (("Configuring Project: " in currentLine) and ("Building Project: " in nextLine)) \
                or (("Building Project: " in currentLine) and ("Testing Project: " in nextLine)) \
                or (("Building Project: " in currentLine) and ("Configuring Project: " in nextLine)) \
                or (("Testing Project: " in currentLine) and ("Configuring Project: " in nextLine)):
            continue
        else:
            if ("Configuring Project: " in currentLine) or ("Building Project: " in currentLine) or ("Testing Project: " in currentLine):
                projectErrorList.append('\n')

            projectErrorList.append(currentLine)

    with open(r'result_error_list.txt', 'a+', encoding='utf-8') as file:
        file.writelines(errorList)
    with open(r'result_project_error_list.txt', 'a+', encoding='utf-8') as file:
        file.writelines(projectErrorList)

if __name__ == '__main__':
    if os.path.exists(r'result_error_list.txt'):
        os.remove(r'result_error_list.txt')
    if os.path.exists(r'result_project_error_list.txt'):
        os.remove(r'result_project_error_list.txt')

    for i in range(1, 11):
        sliceName = str(i) + "_RWC slice " + str(i) + ".txt"

        print(sliceName)
        DetectedRWCRunError(sliceName)
