from datetime import datetime, date
import csv

def AnalyzeOneChunk(file):

    # 1. Filter projects and timestamp
    buildingProjects = []
    timeList = []
    lenth = len("2022-04-25T22:39:24.7129845Z ##[section] 2022-04-25T15:39:24.7000663-07:00  Building Projects: ")

    with open(file, 'r+', encoding="utf-8") as f:
        while True:
            line = f.readline()
            #print(line)
            if not line:
                break

            if "Building Projects" in line:
                line = (line[lenth:]).replace(',', ' ')
                buildingProjects = line.split()

            # Match setup, build, runtest stage
            if line.endswith("::Setup\n") or line.endswith("::Build\n") or line.endswith("::RunTests\n") or line.endswith("::Summarize\n"):
                timeList.append(line)

    # 2. Match projects and timestamp: such as ['UnrealEngine', '2022-04-27 18:48:25', '2022-04-27 19:45:02', '2022-04-28 04:12:50', '2022-04-28 04:12:50']
    projectsTimeList = []
    lenth = len(timeList)
    n = 0

    for name in buildingProjects:
        oneProject = []
        oneProject.append(name)

        while n < lenth:
            line = timeList[n]
            if name in line:
                oneProject.append((line[:19]).replace('T', ' '))
            else:
                break
            n += 1

        projectsTimeList.append(oneProject)

    # 3. Calculating time: such as ['UnrealEngine', 57, 508, 0, 565]
    results = []
    failedProjects = []

    for project in projectsTimeList:
        oneResult = []
        oneResult.append(project[0])

        # Filter failed project and skip it
        if len(project) > 5:
            failedProjects.append(project[0])
            continue

        sum = 0
        for i in range(1, 4):
            start = project[i + 1]
            end = project[i]
            start_struct = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            end_struct = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            seconds = (start_struct - end_struct).seconds

            minutes = 0

            if seconds % 60 < 30:
                minutes = seconds // 60
            else:
                minutes = seconds // 60 + 1

            oneResult.append(minutes)
            sum += minutes

        # If the time less than 1 minute, count as 1 minute
        if sum == 0:
            sum = 1

        oneResult.append(sum)
        results.append(oneResult)

    return results, failedProjects

def TakeFirst(elem):
    return elem[0]

def AnalyzeOneRunLog():
    results = []
    failedProjects = []

    # Analyze one run log, collect info from 1-8 build chunks.
    for i in range(1, 9):
        fileName = str(i) + "_Build Chunk" + str(i) + ".txt"
        #print(fileName)
        oneChunkResult, failedProject = AnalyzeOneChunk(fileName)

        results += oneChunkResult
        failedProjects += failedProject

    # Sorted(A-Z) and show projects
    projectsCount  = 0
    results.sort(key=TakeFirst)
    for i in results:
        projectsCount += 1
        print(i)
    print(projectsCount)

    # Write to csv file
    with open('TimeCost.csv', 'w', newline='') as csvfile:
        fieldnames = ['ProjectName', 'SetupTime', 'BuildTime', 'RunTestTime', 'TotalTime']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in results:
            writer.writerow({'ProjectName': i[0], 'SetupTime': i[1], 'BuildTime': i[2], 'RunTestTime': i[3], 'TotalTime': i[4]})

AnalyzeOneRunLog()
