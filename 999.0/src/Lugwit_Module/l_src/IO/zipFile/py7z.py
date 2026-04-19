import subprocess
import re,os
curDir=os.path.dirname(__file__)

def get_element(lst, index):
    if 0 <= index < len(lst):
        return lst[index]
    else:
        return None  # 或者其他默认值

class ExtractCallback:
    def __init__(self):
        self.processing_file_path = None
        self.processing_bytes = 0
        self.output = ''

    def report_start_preparation(self):
        print("Starting extraction...")

    def report_start(self, processing_file_path, processing_bytes):
        self.processing_file_path = processing_file_path
        self.processing_bytes = processing_bytes

    def report_end(self, processing_file_path, wrote_bytes):
        print(f'Finished extracting {processing_file_path}, {wrote_bytes} bytes written')

    def report_postprocess(self):
        print("Finished extraction")

    def report_warning(self, message):
        print(f"Warning: {message}")

    def report_progress(self, char):
        self.output += char
        match_process = re.search('\d{1,3}%.+\r', self.output, flags=re.M | re.S | re.I)
        process, filesize, filename='','',''
        if match_process:
            match_process = match_process.group()
            split_match_process = match_process.replace('\r','').split(' ')
            process, filesize, filename = get_element(split_match_process, 0), \
                                          get_element(split_match_process, 1), \
                                          get_element(split_match_process, 3)
            #print(f'Progress: {process}, Filesize: {filesize}, Filename: {filename}')
            self.output = ''
        return process, filesize, filename

def extract(zipExePath=r"", zipfile='',
            outDir='',callback='',modifyFucn=''):
    '''
    modifyFucn#返回值process, filesize, filename
    '''
    if not zipExePath:
        zipExePath=curDir+'/7za.exe'
    cmd=f'"{zipExePath}" x "{zipfile}" -o{outDir} -aoa -bsp1 -y'
    if not callback:
        callback = ExtractCallback()
    st=subprocess.STARTUPINFO()
    st.dwFlags=subprocess.STARTF_USESHOWWINDOW
    st.wShowWindow=subprocess.SW_HIDE
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,startupinfo=st)
    callback.report_start_preparation()
    extract_finish=False
    while True:
        line = p.stdout.readline()
        if line:
            while True:
                char = p.stdout.read(1).decode("gbk", errors="ignore")
                if p.poll() is not None:
                    print (u'提取完成')
                    extract_finish=True
                    callback.report_postprocess()
                process, filesize, filename=callback.report_progress(char)
                if extract_finish:
                    process='100%'
                if process:
                    #print(f'Progress: {process}, Filesize: {filesize}, Filename: {filename}')
                    if modifyFucn:
                        modifyFucn(process, filesize, filename)
                        if extract_finish:
                            return True

def modifyFucn(*args):
    #返回值process, filesize, filename
    print (args)
    
if __name__ == "__main__":
    callback = ExtractCallback()
    extract(modifyFucn=modifyFucn)
