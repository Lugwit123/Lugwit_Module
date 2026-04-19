import os
import codecs
import re
import fire
def modify_OCIOSeting(add=True):
    for MayaVersion in range(2018,2025):
        input_file_path = os.path.join(os.path.expandvars("%USERPROFILE%"), 'Documents', 'maya', str(MayaVersion), 'Maya.env')
        input_file_Dir=os.path.dirname(input_file_path)
        print (input_file_Dir,MayaVersion,os.path.exists(input_file_Dir))
        if os.path.exists(input_file_Dir) == False:
            continue
        search_string = r'OCIO = A:\\TD\database\\dccData\\Maya\\aces_1.2\\config.ocio'
        print(f'input_file_path:\n{input_file_path}\n')

        # 读取文件内容
        with codecs.open(input_file_path, 'a+', encoding='utf-8') as file:
            file.seek(0,0)
            file_content = file.read()
            print(f'file_content:\n{file_content}\n')
            #不管之前有没有icio设置都先删除
            remove_ocio_content = re.sub('\n.+config.ocio', '', file_content, flags=re.I)
            print(f'remove_ocio_content:\n{remove_ocio_content}\n')
            if add:
                updated_content=remove_ocio_content+'\n'+search_string
            else:
                updated_content=remove_ocio_content
            print(f'updated_content:\n{updated_content}\n')
            file.seek(0,0)
            file.truncate()
            file.write(updated_content.replace('\\\\','\\'))
        #break
if __name__ == '__main__':
    fire.Fire()
