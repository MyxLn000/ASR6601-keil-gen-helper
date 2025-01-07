import os
import shutil
import sys
import re

def createProj(pre_path):
    print("[mgf]Create new project...\n")
    if not os.path.exists("./project"):
        os.makedirs("./project/incs")
    else:
        print("Poject is already exist!")
        sys.exit(1)
    basefilelist = [
        "./inc",
        "./src",
        "./cfg",
        "./utils"
    ]
    usedforincs = [
        "drivers",
        "lora",
        "platform"
    ]
    for file in basefilelist:
        shutil.copytree(file,"./project/"+file)
    for file in usedforincs:
        shutil.copytree(pre_path + file, "./project/incs/"+file)
    shutil.copy('./keil.bat','./project/keil.bat')

def genKeilconf(pre_path):
    print('[mgf]rewrite the new file "keil_config.ini"...\n')
    keil_config_file_path = "./project/utils/keil_config.ini"
    try:
        pre_path = pre_path[:-2]
        with open(keil_config_file_path, encoding='utf-8') as conf:
            content = conf.read()

        # split content to use
        datas = content.split('\n')
        src_paths = datas[1][5:-2].split("', '")
        inc_paths = datas[3][14:-2].split("; ")

        # replace the paths
        changeRule_src = [
            (pre_path + r"projects/.*/examples/.*/src/(.*?)", "./src/"),
            (pre_path + r"platform/(.*?)", "./incs/platform/"),
            (pre_path + r"drivers/peripheral/(.*?)", "./incs/drivers/peripheral/")
        ]
        changeRule_inc = [
            (pre_path + r"projects/.*/examples/.*/inc", "./inc"),
            (pre_path + r"platform/(.*?)", "./incs/platform/"),
            (pre_path + r"drivers/peripheral/(.*?)", "./incs/drivers/peripheral/")
        ]

        for i, path in enumerate(src_paths):
            for pattern, replacement in changeRule_src:
                st = re.sub(pattern, replacement, path)
                if not src_paths[i] == st:
                    src_paths[i] = st
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
        print("can not open generate file in ./project/utils/keil_config.in")
        sys.exit(1)
