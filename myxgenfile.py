import os
import shutil
import sys
import re
import subprocess

def judge_pos():
    print("[mgf]checking sdk...\n")
    if not os.path.exists("./keil.bat"):
        print("Please put in project with keil.bat")
        errorhandle()
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
                errorhandle()
            else:
                continue
        return prePath
    except Exception as e:
        print(f"读取文件时发生错误: {e}")


def createProj(pre_path):
    print("[mgf]Create new project...\n")
    if os.path.exists("./project"):
        print("Poject is already exist!")
        errorhandle()
    basefilelist = [
        "./inc",
        "./src",
        "./cfg",
        "./utils"
    ]
    usedforincs = [
        "drivers",
        "lora",
        "platform",
        "tools"
        ""
    ]
    for file in basefilelist:
        shutil.copytree(file,"./project/"+file)
    for file in usedforincs:
        shutil.copytree(pre_path + file, "./project/"+file)
    shutil.copy('./keil.bat','./project/keil.bat')


def rewriteKeilconf(pre_path):
    print('[mgf]rewrite the new file "keil_config.ini"...\n')
    keil_config_file_path = "./project/utils/keil_config.ini"
    try:
        pre_path = pre_path[:-2]
        with open(keil_config_file_path, encoding='utf-8') as conf:
            content = conf.read()

        # split content to use
        datas = content.split('\n')
        src_paths = datas[1][5:-2].split("', '")
        lib_paths = datas[2][5:-2].split("', '")
        inc_paths = datas[3][14:-2].split("; ")

        # replace the paths
        changeRule_src = [
            (pre_path + r"projects/.*/examples/.*/src/(.*?)", "./src/"),
            (pre_path + r"platform/(.*?)", "./platform/"),
            (pre_path + r"drivers/(.*?)", "./drivers/"),
            (pre_path + r"lora/(.*?)", "./lora/")
        ]
        changeRule_inc = [
            (pre_path + r"projects/.*/examples/.*/inc", "./inc"),
            (pre_path + r"platform/(.*?)", "./platform/"),
            (pre_path + r"drivers/(.*?)", "./drivers/"),
            (pre_path + r"lora/(.*?)", "./lora/")
        ]
        changeRule_lib = [
            (pre_path + r"platform/(.*?)", "./platform/"),
            (pre_path + r"drivers/(.*?)", "./drivers/"),
            (pre_path + r"lora/(.*?)", "./lora/")
        ]

        for i, path in enumerate(src_paths):
            for pattern, replacement in changeRule_src:
                st = re.sub(pattern, replacement, path)
                if not src_paths[i] == st:
                    src_paths[i] = st
                    break

        for i, path in enumerate(lib_paths):
            for pattern, replacement in changeRule_lib:
                st = re.sub(pattern, replacement, path)
                if not lib_paths[i] == st:
                    lib_paths[i] = st
                    break

        for i, path in enumerate(inc_paths):
            for pattern, replacement in changeRule_inc:
                st = re.sub(pattern, replacement, path)
                if not inc_paths[i] == st:
                    inc_paths[i] = st
                    break

        # merge the changes and write to file
        st = ""
        for path in src_paths:
            st = st + "'" + path + "', "
        datas[1] = "src=" + st

        st = ""
        for path in lib_paths:
            st = st + "'" + path + "', "
        datas[2] = "lib=" + st

        st = "'"
        for path in inc_paths:
            st = st + path + '; '
        datas[3] = "include_path=" + st + "'"
        st = ''
        for i in datas:
            st = st + i + '\n'

        # 将替换后的内容写回文件
        with open(keil_config_file_path, 'w') as file:
            file.write(st)
    except:
        print("can not open generate file in ./project/utils/keil_config.ini")
        errorhandle()


def rewritebat(pre_path):# this function change the keil.bat and ./utils/genbinary.bat
    print('[mgf]rewrite the new file "keil.bat"...\n')
    keil_bat_path = './project/keil.bat'
    genbinary_path = './project/utils/genbinary.bat'
    pre_path = pre_path[:-2]
    try:
        with open(keil_bat_path,encoding='utf-8') as keil:
            cont = keil.read()
        cont = cont.split(' ')
        cont[0] = '..\\'+cont[0]
        cont[1] = '..\\'+cont[1]
        newcon = ''
        for i in cont:
            newcon = newcon + i + ' '

        with open(keil_bat_path, 'w') as file:
            file.write(newcon)
    except:
        print("can not open generate file in ./project/keil.bat")
        errorhandle()

    print('[mgf]rewrite the new file "genbinary.bat"...\n')
    try:
        with open(genbinary_path, encoding='utf-8') as genbin:
            cont = genbin.read()
        a = len(pre_path)
        cont = '.\\'+cont[a:]

        with open(genbinary_path, 'w') as file:
            file.write(cont)

    except:
        print("can not open generate file in ./project/utils/genbinary.bat")
        errorhandle()

def finishedgen():
    print("[mgf]generate the keil project...\n")
    bat_path = '.\\keil.bat'
    utils_path = './utils/'
    os.chdir("./project")
    try:
        subprocess.run([bat_path], shell=True, check=True)
        print(f"[mgf]{bat_path} done. project has been gen\n")

    except subprocess.CalledProcessError as e:
    # 运行失败时的处理
        print(f"文件 {bat_path} 运行失败,请手动点击./project/keil.bat生成工程，返回码: {e.returncode}")
        errorhandle()
    except FileNotFoundError:
        # 文件不存在时的处理
        print(f"文件 {bat_path} 不存在.")
        errorhandle()
    except PermissionError:
        # 没有权限运行文件时的处理
        print(f"没有权限运行文件 {bat_path},请手动点击./project/keil.bat生成工程.")
        errorhandle()
    except Exception as e:
        # 其他异常的处理
        print(f"运行文件时发生错误: {e},请手动点击./project/keil.bat生成工程")
        errorhandle()

    try:
        os.remove(bat_path)
    except FileNotFoundError:
        print(f"文件 {bat_path} 不存在.")
    except PermissionError:
        print(f"没有权限删除文件 {bat_path}.")
        errorhandle()
    except Exception as e:
        print(f"删除文件时发生错误: {e}")
        errorhandle()





def errorhandle():
    print("some thing error..\n")
    input("Press any key to exit...")
    sys.exit(1)
