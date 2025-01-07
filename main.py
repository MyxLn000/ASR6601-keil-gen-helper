import myxgenfile as mgf
import os
import sys


def judge_pos():
    if not os.path.exists("./keil.bat"):
        print("Please put in project with keil.bat")
        sys.exit(1)
    prePath = ""
    try:
        with open('./keil.bat','r', encoding='utf-8') as k_file:
            while True:
                char = k_file.read(3)
                if (char == '..\\'):
                    prePath = prePath + "../"
                else:
                    break
        prePath = prePath + './'
        folders_check = [
            "tools",
            "projects",
            "drivers",
            "lora",
            "platform"
        ]
        for folder in folders_check:
            if not os.path.isdir(prePath+folder):
                print(f"'{folder}' file not exit ")
                sys.exit(1)
            else:
                continue
        return prePath
    except Exception as e:
        print(f"读取文件时发生错误: {e}")


if __name__ == '__main__':
    prpath=judge_pos()
    mgf.createProj(prpath)
    mgf.rewriteKeilconf(prpath)
    mgf.rewritebat()

    print("[main]Done\n")