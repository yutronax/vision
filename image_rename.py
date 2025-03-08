import os
path=r"C:\Users\MONSTER\3D Objects\yazprojeler\klasor4\nesneler\domates\sağlıklı"
def rename_files(directory, new_name):
    for i, filename in enumerate(os.listdir(directory)):
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, f'{new_name}{i}.jpg')
        os.rename(src, dst)


rename_files(path, 'new_health_tomato_name')
