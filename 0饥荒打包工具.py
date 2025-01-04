import re
import shutil
import os
from PIL import Image
import subprocess
import glob  

# BUILD
    
# 获取当前目录
currentdir = os.getcwd()
#简单图片打包目录
current_dir = currentdir+"/1/1"

working_directory = "D:/Program Files/Steam/steamapps/common/Don't Starve Mod Tools/mod_tools"

# 设置系统区域和编码设置
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["LANG"] = "zh_CN.UTF-8"


# 打开CMD窗口
# stdin=subprocess.PIPE表示将标准输入流作为管道输入，stdout=subprocess.PIPE表示将标准输出流作为管道输出，stderr=subprocess.PIPE表示将标准错误流作为管道输出。
# 如果你需要获取CMD窗口输出的结果，可以在subprocess.Popen()中使用stdout=subprocess.PIPE来配置标准输出流，并使用cmd.stdout.read()来读取输出结果。
# cmd = subprocess.Popen(f'cmd.exe /K cd /D {working_directory}', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
cmd = subprocess.Popen(f'cmd.exe /K cd /D {working_directory}', shell=True, stdin=subprocess.PIPE)



# 创建一个空列表
commandscml = []
assets = []

# 遍历当前目录下的文件和文件夹
# for root, dirs, files in os.walk(current_dir):
    # for file in files:
        # print("文件",os.path.join(root, file))
    # for dir in dirs:
        # print("目录",dir,os.path.join(root, dir))


# 创建物品栏图片文件夹
inventoryimages = current_dir+"/inventoryimages"
if not os.path.exists(inventoryimages):
    os.mkdir(inventoryimages)

# 遍历目录下的文件, 简单的图片生成动画，文件夹1里面
for filename in os.listdir(current_dir):
    full_filepath = os.path.join(current_dir, filename)
    # 判断文件扩展名是否为 .png
    if os.path.isfile(full_filepath) and filename.lower().endswith('.png'):
        print(full_filepath)
        # 获取文件名（不包含后缀）
        name = os.path.splitext(filename)[0]   
        new_folder_path = current_dir + "/" + name
        # 检查文件夹是否已经存在
        if not os.path.exists(new_folder_path):

            # 使用 mkdir() 函数创建新文件夹
            os.mkdir(new_folder_path)  #创建放scml的文件夹
            new_folder_path1 = new_folder_path + "/" + name
            os.mkdir(new_folder_path1)  #创建放图片的文件夹
            
            # copy() 只复制文件内容，并不保留文件的元数据。(文件权限、时间戳等）
            # copy2() 复制文件内容，并尽可能保留源文件的元数据。
            # shutil.copy2(full_filepath, new_folder_path1+"/"+filename)
            
            # 打开图片
            image = Image.open(full_filepath)
            # 获取图片的长宽
            width, height = image.size
            # 计算缩放比例
            # scale = min(64 / original_width, 64 / original_height)
            # 计算缩放后的分辨率
            # new_width, new_height = int(width * scale), int(height * scale)
            
            # 等比例缩放图片分辨率到64
            image.thumbnail((64, 64))
            # 保存缩放后的图片
            image.save(inventoryimages+"/"+filename)
            
            assets.append(f'Asset("IMAGE", "images/inventoryimages/{name}.tex"),')
            assets.append(f'Asset("ATLAS", "images/inventoryimages/{name}.xml"),')
            assets.append(f'Asset("ANIM", "anim/{name}.zip"),')
    
            # 使用 move() 函数移动文件
            shutil.move(full_filepath, new_folder_path1) 
            with open(new_folder_path1+".scml", "w") as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('    <spriter_data scml_version="1.0" generator="BrashMonkey Spriter" generator_version="r7">\n')
                file.write(f'        <folder id="0" name="{name}">\n')
                file.write(f'            <file id="0" name="{name}/{filename}" width="{width}" height="{height}" pivot_x="0" pivot_y="1"/>\n')
                file.write('        </folder>\n')
                file.write(f'        <entity id="0" name="{name}">\n')
                file.write('            <animation id="0" name="idle" length="1000" interval="100">\n')
                file.write('                <mainline>\n')
                file.write('                    <key id="0">\n')
                file.write('                        <object_ref id="0" timeline="0" key="0" z_index="0"/>\n')
                file.write('                    </key>\n')
                file.write('                </mainline>\n')
                file.write(f'                <timeline id="0" name="{name}">\n')
                file.write('                    <key id="0" spin="0">\n')
                file.write(f'                        <object folder="0" file="0" x="-{width/2}" y="{height}"/>\n')
                file.write('                    </key>\n')
                file.write('                </timeline>\n')
                file.write('            </animation>\n')
                file.write('        </entity>\n')
                file.write('    </spriter_data>')
            
            # 打开 CMD 并执行命令, shell=True 参数将确保命令在 CMD 中执行。
            # subprocess.call(command, shell=True)
            # 我们使用 subprocess.call() 函数来打开 CMD 并在指定路径下执行指定的命令。cmd /C 表示在 CMD 中执行命令，cd /D {working_directory} 是切换到指定路径的命令，&& 表示在同一个命令行中执行多个命令，{command} 是要执行的命令本身。
            # 打开 CMD，并在指定路径下执行命令
            # subprocess.call(f'cmd /C "cd /D {working_directory} && scml {new_folder_path1}.scml {current_dir}"')
            
            commandscml.append(f'png "{inventoryimages}/{filename}" "{inventoryimages}"')
            commandscml.append(f'scml "{new_folder_path1}.scml" "{current_dir}"')


exported = []
exported1 = 0

for item in os.listdir('.'):
    if os.path.isdir(item): #是文件夹
        if os.path.isdir(item+"/exported"):
            exported.append(item)
            print(f"{exported1}: {item}")
            exported1+=1

# 判断文件名是不是包含中文, 中文字符主要位于Unicode编码范围\u4e00至\u9fff之间 
def contains_chinese(filename):
    for char in filename:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

input_number = int(input("请输入序号(输入其他退出): \n"))
if input_number < len(exported):
    # 遍历当前文件夹
    for folder_name in os.listdir(exported[input_number]):
        if folder_name == "exported" or folder_name == "bigportraits" or folder_name == "images":
            for root, dirs, files in os.walk(exported[input_number]+"\\"+folder_name):
                for file in files:
                    # 获取文件的完整路径
                    file_path = os.path.join(root, file)
                    # 获取文件的后缀名
                    name, ext = os.path.splitext(file_path)
                    # 判断后缀名是否为png或scml
                    if folder_name == "exported":
                        if ext.lower() == ".scml" :
                            assets.append(f'Asset("ANIM", "anim/{os.path.splitext(file)[0]}.zip"),')
                            commandscml.append(f'scml "{currentdir}\\{file_path}" "{currentdir}\\{exported[input_number]}"')
                            for png in glob.glob(os.path.join(root, '*.png')): #打包scml旁边的图片
                                name1 = os.path.splitext(os.path.basename(png))[0].replace("\\","/")
                                if not contains_chinese(name1):
                                    # if not os.path.exists(name1+".xml"):
                                    assets.append(f'Asset("IMAGE", "images/inventoryimages/{name1}.tex"),')
                                    assets.append(f'Asset("ATLAS", "images/inventoryimages/{name1}.xml"),')
                                    commandscml.append(f'png "{currentdir}\\{png}" "{currentdir}\\{root}"')
                    elif ext.lower() == ".png" and not os.path.exists(name+".xml"): #没有xml文件说明没有被打包
                        #name为相对路径,使用字符串去掉mod文件夹exported[input_number]名字
                        name1 = name.replace(exported[input_number]+"\\", "").replace("\\","/")
                        assets.append(f'Asset("IMAGE", "{name1}.tex"),')
                        assets.append(f'Asset("ATLAS", "{name1}.xml"),')
                        commandscml.append(f'png "{currentdir}\\{file_path}" "{currentdir}\\{root}"')


# 关闭CMD窗口
# cmd.stdin.close()
# cmd.wait()



print("开始打包scml")
for command in commandscml:
    print(command)
    # cmd.stdin.write(command.encode('utf-8') + b'\n')
    # 将指令进行编码并写入CMD进程
    cmd.stdin.write(command.encode('gbk') + b'\n')
    cmd.stdin.flush()  # 刷新缓冲区


# 关闭CMD进程的标准输入
cmd.stdin.close()

# 等待CMD进程执行完毕
cmd.wait()

print("\n==================================")
for asset in assets:
    print(asset)
print("==================================")
    
input("按任意键退出...")
