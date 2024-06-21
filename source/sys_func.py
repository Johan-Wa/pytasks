# --------------- Imports -------------
import os
import subprocess

# --------------- Functions ------------
def create_a_csv(path,name):
    '''Creates a csv file in path given.
    Params:
        - path --> the path to the directory
        - name --> name of the file
    Returns:
        None
    '''
    subprocess.run(['touch',f'{path}/{name}.csv'])

def delete_a_csv(path,name):
    '''Deletes a csv file in the given path.
    Params:
        - path --> the path of the directory
        - name --> name of the file
    Returns:
        None
    '''
    subprocess.run(['rm',f'{path}/{name}.csv'])
    return f'{name}.csv'

def optain_file_list(path):
    '''Scan a directory, get a list of the files, and returns the names.
    Params:
        - path --> path of the directory to scan
    Returns:
        - file_names --> list of the file names without extension.
    '''
    files = os.scandir(path)
    files_names = []
    for i in files:
        if not i.name.startswith('.') and i.is_file():
            files_names.append(i.name)

    files_names = [i.split('.')[0] for i in files_names]

    return files_names
# --------------- Main -----------------
if __name__ == "__main__":
    path = 'csv_lists'
    print(delete_a_csv(path,'Archivo 1'))
