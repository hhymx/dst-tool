import xml.etree.ElementTree as ET 

inventoryimages = {}

def loadimg(path):
    root = ET.parse(path).getroot() 
    for element in root.findall('.//Element'):  
        name = element.get('name')  
        inventoryimages[name[:-4]] = path
loadimg("E:\\jihuangmod\\scripts\\images\\inventoryimages.xml")
loadimg("E:\\jihuangmod\\scripts\\images\\inventoryimages1.xml")
loadimg("E:\\jihuangmod\\scripts\\images\\inventoryimages2.xml")
loadimg("E:\\jihuangmod\\scripts\\images\\inventoryimages3.xml")



chinese = {}
# 打开文件并逐行读取  
with open("E:\\jihuangmod\\scripts\\languages\\chinese_s.po", 'r', encoding='utf-8') as file:  
    chinese_key = None
    for line in file:  
        if line.startswith('#. STRINGS.NAMES.'):
            chinese_key = line[17:].strip().lower() #.strip()去掉可能的换行空白符
            if chinese_key not in inventoryimages:
                chinese_key = None
        elif chinese_key != None and line.startswith('msgstr'):
            chinese[chinese_key] = line[8:-2].strip()
            chinese_key = None


# 下面不需要了，设置null，应该会回收内存把
inventoryimages = None
# 使用with语句打开文件，这样可以确保文件在使用后会被正确关闭  
# 'w'模式表示写入模式，如果文件已存在则会被覆盖  
# with open('chinese_s.po', 'w') as file:  
    # for k, v in chinese.items(): 
        # file.write("#. STRINGS.ACTIONS.")  
        # file.write(k)  
        # file.write("\n")  
        # file.write('msgstr "')  
        # file.write(v)  
        # file.write("\n")  

# 网页配方表打印
for k, v in chinese.items(): 
    print(f'"{v}":"{k}",')
input("{xx:x}")

# Ingredient = {}
# while True:
    # a = input("输入配方: 木头*1 草*2\n")
    # for b in a.split(' '):
        # c = b.split('*')
        # for k, v in chinese.items(): 
            # if k not in Ingredient:
                # if c[0] == v:
                    # Ingredient[k] = c[1]
                # elif c[0] in v:
                    # print(v, f'Ingredient("{k}", {c[1]}),')
    
    # istr = "{"
    # for k, v in Ingredient.items():  
        # istr = istr + f'Ingredient("{k}", {v}),'
    # istr = istr[:-1] + '}' 
    # print("\n")
    # print('AddRecipe2("mod",'+istr+',TECH.NONE, {atlas ="images/inventoryimages/mod.xml",image = "mod.tex"})')
    # print("\n")
    # print('AddRecipe2("mod",'+istr+',TECH.NONE, {builder_tag = "",atlas ="images/inventoryimages/mod.xml",image = "mod.tex"},{"CHARACTER"})')
    # print("\n")
