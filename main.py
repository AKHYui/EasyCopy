import time
import PySimpleGUI as sg
from pathlib import Path
import os
import _thread


def gui():
    sg.theme('Dark Blue 3')
    layout = [
        [sg.Text('源目录：'), sg.Input(disabled=True), sg.FolderBrowse()],
        [sg.Text('新目录：'), sg.Input(disabled=True), sg.FolderBrowse()],
        [sg.Text('读入/输出块大小(k)'), sg.InputText('18')],
        [sg.Button('开始复制'), sg.Button('关闭')],
        [sg.Output(size=(80, 10), key='_output_')]
    ]

    window = sg.Window('EasyCopy', layout)

    while True:
        event, values = window.read()
        if event in (None, '关闭'):
            break
        if event == '开始复制':
            olddir = values[0]
            newdir = values[1]
            bs = values[2]
            if olddir == '' or newdir == '':
                sg.Popup('请先选择目录')
            elif olddir == newdir:
                sg.Popup('两路径不允许一致')
            else:
                print(tm() + '----正在读取目录文件')
                _thread.start_new_thread(scan_file, (olddir, newdir, bs,))

    window.close()


def tm():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def scan_file(path, newdir, bs):
    if bs == '':
        bs = '18'
    files = []
    for fpathe, dirs, fs in os.walk(path):
        for f in fs:
            file = os.path.join(fpathe, f).replace("/", os.sep)
            files.append(file)
    print(tm() + '----共发现：' + str(len(files)) + '个文件')
    # print(files[1])
    path = path.replace("/", os.sep)
    newdir = newdir.replace("/", os.sep)
    # print(files[1].replace(path, newdir + path.split(os.sep)[-1]))
    remaining = len(files)
    for i in files:
        oldfile = i
        newfile = i.replace(path, newdir + path.split(os.sep)[-1])
        # print(newfile.replace(newfile.split(os.sep)[-1], ''))
        isExists = os.path.exists(
            newfile.replace(newfile.split(os.sep)[-1], ''))
        if not isExists:
            os.makedirs(newfile.replace(newfile.split(os.sep)[-1], ''))
        else:
            pass
        if os.path.exists(newfile):
            remaining = remaining - 1
            carried = len(files) - remaining
            per = carried/len(files) * 100
            per = ("%.2f" % per)
            print(str(carried) + '/' + str(len(files)) +
                  ' | ' + str(per) + '%')
        else:
            # print('dd if=' + oldfile + ' of=' + newfile + ' bs=' + bs + 'k')
            os.system('dd if=' + oldfile + ' of=' +
                      newfile + ' bs=' + bs + 'k')
            remaining = remaining - 1
            carried = len(files) - remaining
            per = carried/len(files) * 100
            per = ("%.2f" % per)
            print(str(carried) + '/' + str(len(files)) +
                  ' | ' + str(per) + '%')
    print(tm() + '----复制结束')


def main():
    gui()


if __name__ == '__main__':
    main()
