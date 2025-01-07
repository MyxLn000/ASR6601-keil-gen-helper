# ASR6601 keil GEN helper

## Brief

用于给ASR6601的sdk生成可移动keil工程例程

测试过的版本： [ASR6601_LoRaWAN 1.0.3 SDK](https://github.com/asrlora/asr_lora_6601)

> 本程序需要sdk里面的工具包tools等，解压sdk后不要改变文件结构！

----

Generate movable keil project for ASR6601 in sdk

Used for ASR6601 Keil project generate to a movable file

suitable version: ASR6601_LoRaWAN 1.0.3 SDK

> you can download this file by this :  [ASR_lora_6601](https://github.com/asrlora/asr_lora_6601)
>
> this function need the "tools" file from the sdk, do not change the file structure after you unzip the sdk

## Usage 

1、解压SDK文件，打开"projects"文件夹找到你要打开的文件

2、直接复制Genhelper.exe程序到目标文件夹下，放在keil.bat文件一起，双击运行.

>如果你有环境，可以直接把main.py和myxgenfile.py复制到文件夹下，打开bash窗口用
> 
> ```
> python.exe main.py
> ```

3、此时会生成一个Project文件夹下面是生成好的可移动文件
_____

1.unzip the SDK zip file, open the direct "projects" and find the project you want

2.Copy the Genhelper.exe to the project file which you want to use, and put it with the "keil.bat" file,click it.

>if you have the python env，you can copy main.py and myxgenfile.py to the file，open bash and:
> 
> ```
> python.exe main.py
> ```
> 
3.there will generate a file 'project' and you can move it to anywhere

------

## Notice

生成工程的main.c不在user文件夹下，在src下。但是生成的项目以及可以用了，而且我也不会改（才不是懒（doge ）

----
the main.c in ./src instead of ./user , but the project is works and i have no ideas fix it ( not lazy :] )


write in 2025.1.7 CN
