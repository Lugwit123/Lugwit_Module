from tqdm import tqdm

def copy_filtered_files(src, dst, exclude_exts=['.py', '.pyc', '.bat', '.ipynb'], exclude_dirs=['venv', '__pycache__']):
    src = os.path.normpath(src)
    dst = os.path.normpath(dst)
    if not os.path.exists(src):
        print("Source path does not exist.")
        return

    if not os.path.exists(dst):
        os.makedirs(dst)

    files_to_copy = []

    for root, dirs, files in os.walk(src):
        if root.startswith(dst):
            continue

        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if not any(fnmatch.fnmatch(file, '*' + ext) for ext in exclude_exts):
                files_to_copy.append((os.path.join(root, file), os.path.join(dst, os.path.relpath(os.path.join(root, file), src).replace(src, '').lstrip(os.sep))))

    for src_file_path, dst_file; path in tqdm(files_to_copy, desc='Copying files'):
        try:
            subprocess.Popen(u'cmd /c echo F| xcopy /y/r/D "{}" "{}"'.format(src_file_path, dst_file_path))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    src_path = r"D:\bb\TestCopy\src"
    dst_path = r"D:\bb\TestCopy\src\tgt"

    copy_filtered_files(src_path, dst_path)
