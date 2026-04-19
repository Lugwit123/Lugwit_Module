import os
import re
import subprocess
import threading
import fire

def decompile(filepath):
    """
    Decompile .pyc file or all .pyc files in a directory and its subdirectories.

    Parameters:
    filepath (str): The path to the .pyc file or directory to decompile

    Returns:
    None
    """
    def decompile_pyc_file(filepath):
        out_path = os.path.splitext(filepath)[0] + '.py'
        py_exists = os.path.isfile(out_path)
        if py_exists:
            print(u"Python file {} already exists. Skipping decompiling.".format_map(out_path))
        else:
            print ('----- Decompiling:', filepath, '-----')
            cmd = u'D:\\ProgramFiles\\miniconda3\\envs\\py2\\Scripts\\uncompyle6.exe --encoding GBK {} > {}'.format(filepath,out_path)
            thread = threading.Thread(target=subprocess.run, args=(cmd,), kwargs={'shell': True})
            thread.start()
            thread.join()

            with open(out_path, 'r', encoding='GBK') as f:
                lines = f.readlines()

            if lines[0].strip() == '# -*- coding: GBK -*-':
                lines[0] = '# -*- coding: utf8 -*-\n'

            for i, line in enumerate(lines):
                unicode_strs = re.findall(r'\\u....', line) 
                for unicode_str in unicode_strs:
                    try:
                        unicode_char = unicode_str.encode('ascii').decode('unicode_escape')
                        line = line.replace(unicode_str, u'"{}"'.format(unicode_char))
                    except:
                        break 
                lines[i] = line

            with open(out_path, 'w', encoding='utf8') as f:
                f.writelines(lines)

    if os.path.isdir(filepath):
        for dirpath, dirnames, filenames in os.walk(filepath):
            for filename in filenames:
                if filename.endswith('.pyc'):  
                    decompile_pyc_file(os.path.join(dirpath, filename))
    elif filepath.endswith('.pyc'):
        decompile_pyc_file(filepath)
    else:
        print("The path provided is neither a .pyc file nor a directory. Please provide a valid path.")

if __name__ == '__main__':
    fire.Fire(decompile)
