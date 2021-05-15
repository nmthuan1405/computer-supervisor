import win32gui
import win32api
import win32process
import tabulate
import itertools

import subprocess
def getResultCMD( cmd, headers):
    lines = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    firstLine = lines.stdout.readline().decode().rstrip()
    align = []
    for header in headers:
        align.append(firstLine.find(header))
    align.append(len(firstLine) + 1)
    
    result = []
    for l in lines.stdout:
        if l.rstrip():
            line = l.decode().rstrip()
            row = []
            for i in range(len(align) - 1):
                row.append(line[align[i] : align[i + 1] - 1].rstrip())
            result.append(row)

    return result

def getAllWindows(hwnd, param):
    result, child = param
    name = win32gui.GetWindowText(hwnd)
    isWindows = win32gui.IsWindow(hwnd)
    isEnable = win32gui.IsWindowEnabled(hwnd)
    isVisible = win32gui.IsWindowVisible(hwnd)
    nID = win32process.GetWindowThreadProcessId(hwnd)

    win32gui.EnumChildWindows(hwnd, getAllWindows, (result, nID[1]))

    if name != '':
        result.append([name, isWindows, isEnable, isVisible, nID[1], nID[0], child])
    return True


result = []
process_data = getResultCMD('wmic process get description, processid, threadcount', ['Description', 'ProcessId', 'ThreadCount'])

win32gui.EnumWindows(getAllWindows, (result, None))

pro = []
for i in result:
    for j in process_data:
        if str(i[4]) == j[1]:
            pro.append(i + j)

def take(li):
    return li[4]
    
pro.sort(key=take)
print(tabulate.tabulate(pro, headers=['name', 'isWindows', 'isEnable', 'isVisible', 'procID', 'threadID', 'child', 'name', 'id', 'threaad']))