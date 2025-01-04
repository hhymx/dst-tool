import os
import xml.etree.ElementTree as Et
from PIL import Image
import re

folder_path = "D:\\Program Files\\Steam\\steamapps\\common\\Don't Starve Together\\mods\\"



# folder_path = folder_path + "Plume_Wolf\\exported\\剑气槽+技能"
# input("输入目录\n")
# scmlname = "plumewolf_skill_bar"
# input("输入scml名称\n")

手持动画 = { #做手持动画的文件夹
    "swap",
}

# folder_path = folder_path + "tz\\exported\\尾巴"
folder_path = input("输入目录\n")
scmlname = "tz_fh_dushenzhe"
动画信息 = { #单位毫秒
    "tz_fh_dushenzhe":{"a":50,"x":0.5,"y":0.5}
}



# scml的红点y计算和显示的需要计算差值,虽然不知道为什么
for k, v in 动画信息.items():
    v["y"] = 1-v["y"]

scml = Et.Element("spriter_data")
scml.set("scml_version", "1.0")
scml.set("generator", "BrashMonkey Spriter")
scml.set("generator_version", "r7")

anims = []

def custom_sort_key(name):
    # 使用正则表达式匹配文件名中的数字部分
    match = re.search(r'(\d+)', name)
    if match:
        # 将匹配到的数字部分转换为整数
        return int(match.group(0)), name
    else:
        # 如果没有找到数字，则直接按文件名排序
        return 0, name

# 遍历文件夹
for root, dirs, files in os.walk(folder_path):
    # 遍历目录
    for i, item in enumerate(dirs):
        item_path = str(os.path.join(root, item))
        # print("文件夹：",item_path)
        print("文件夹：",item)
        # 创建子元素并添加到根元素，导入文件夹信息
        folder = Et.SubElement(scml, "folder")
        folder.set("id", str(i))
        folder.set("name", item)
        width, height = 0, 0
        # 遍历文件夹里面的图片
        files = os.listdir(item_path)
        红点x = 0.5
        红点y = 0.5
        if item in 动画信息: 
            红点x = 动画信息[item].get("x", 0.5)
            红点y = 动画信息[item].get("y", 0.5)
        for j, f in enumerate(sorted(files, key=custom_sort_key)): # 排序图片
            print("序列帧：",f)
            file = Et.SubElement(folder, "file")
            image = Image.open(os.path.join(item_path, f))# 打开图片
            width, height = image.size # 获取图片的长宽
            file.set("id", str(j))
            file.set("name", item+"/"+f)
            file.set("width", str(width))
            file.set("height", str(height))
            file.set("pivot_x", str(红点x))
            file.set("pivot_y", str(红点y))
        if item in 手持动画 :
            anims.append({"name": item, "folder": i, "x": 0, "y": 0, "file": len(files)})
        else:
            # 动画里面的文件信息, 并计算坐标，让图片处于中心x轴的中心，y轴的上上面
            anims.append({"name": item, "folder": i, "x": width*红点x-width/2, "y": height*红点y, "file": len(files)})

entity = Et.SubElement(scml, "entity")

entity.set("id", "0")
entity.set("name", scmlname)
for i, e in enumerate(anims):
    file = e["file"]
    间隔 = 50
    if e["name"] in 动画信息: 
        间隔 = 动画信息[e["name"]]["a"]
    animation = Et.SubElement(entity, "animation")
    animation.set("id", str(i))
    animation.set("name", e["name"])
    animation.set("length", str(file*间隔))
    animation.set("interval", "100")
    mainline = Et.SubElement(animation, "mainline")
    timeline = Et.SubElement(animation, "timeline")
    timeline.set("id", "0")
    timeline.set("name", e["name"])
    for j in range(file):
        # 
        mainlinekey = Et.SubElement(mainline, "key")
        mainlinekey.set("id", str(j))
        mainlinekey.set("time", str(j*间隔))
        mainlineobject_ref = Et.SubElement(mainlinekey, "object_ref")
        mainlineobject_ref.set("id", "0")
        mainlineobject_ref.set("timeline", "0")
        mainlineobject_ref.set("key", str(j))
        mainlineobject_ref.set("z_index", "0")
        # timeline 动画切换图片
        timelinekey = Et.SubElement(timeline, "key")
        timelinekey.set("spin", "0")
        timelinekey.set("id", str(j))
        timelinekey.set("time", str(j*间隔))
        timeline_object = Et.SubElement(timelinekey, "object")
        timeline_object.set("folder", str(e["folder"]))
        timeline_object.set("file", str(j))
        timeline_object.set("x", str(e["x"]))
        timeline_object.set("y", str(e["y"]))


# 创建ElementTree对象，并写入文件
tree = Et.ElementTree(scml)
with open(folder_path + "//" + scmlname + ".scml", "wb") as file:
    tree.write(file, encoding="utf-8", xml_declaration=True)

input("...")