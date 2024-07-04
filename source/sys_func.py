# --------------- Imports -------------
import os
import subprocess
import csv
import datetime

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

def read_csv(path,filename):
    ''' Read the csv and returns the reader.
    Params:
        - path --> The dir path
        - filename --> Name of the file
    Returns: 
        - reader --> The csv.reader
    '''

    with open(f'{path}/{filename}.csv') as f:
        reader = csv.reader(f)
        reader = list(reader)

    return reader

def get_task_list(path,filename):
    '''Read a csv file and reurns a lis of tasks in the file.
    Params:
        - path --> The dir path
        - filename --> the file name of the file
    Returns:
        - new_list --> a list of strings
    '''
    tasks_data = read_csv(path,filename)
    state_dict = {
        'no started': '_',
        'completed': '#',
        'canceled': 'X',
        'process': '%',
    }
    priority_dict = {
        'normal': '-',
        'important': '!',
        'urgent': '*!'
    }
    
    tasks_list = [f'{i[0]}. {i[1]}          [{state_dict[i[2]]}][{priority_dict[i[6]]}]' for i in tasks_data]

    return tasks_list

def new_task(path, filename, data):
    '''Create a new task in the file.
    Params:
        - path --> Dir path
        - filename --> name of the file
        - data --> a list with the data to get in
            - task_name --> name of the task
            - state --> state of the tasks [no started, completed, canceled, process]
            - create_date --> date of creation
            - finished_date --> when finished the task
            - finish_time --> Time that takes finish the task
            - priorityt --> the priority of the task [normal, important, urgent]
    Returns:
        None
    '''
    actual_list = read_csv(path,filename)
    if len(actual_list) > 0:
        last_i = int(actual_list[-1][0])
        write_task(path,filename,data, last_i+1)
    else:
        write_task(path,filename,data)

def update_task(path, filename, data, id_task):
    ''' Update the data of a task.
    Params:
        - path --> path of the lists
        - filename --> name of the file
        - data --> data tu update
        - id_task --> index of the task
    Returns:
        None
    '''
    file = read_csv(path,filename)
    for idx, l in enumerate(file): 
        if int(l[0]) == id_task:
            data.insert(0,id_task)
            file[idx] = data

    with open(f'{path}/{filename}.csv', 'w') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(file)

def write_task(path, filename, data, id_task=1):
    '''Write a csv file.
    Params:
        - path --> path of the lists
        - filename --> name of the file
        - data --> data tu update
        - id_task --> index of the task, by default = 1
    Returns:
        None
    '''
    data.insert(0,id_task)
    with open(f'{path}/{filename}.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(data)

def del_task(path, filename, id_t):
    ''' Delete a task in the file.'''
    actual_list = read_csv(path, filename)
    actual_list = list(actual_list)
    print(actual_list)
    if len(actual_list) > 0:
        for idx, row in enumerate(actual_list):
            if int(row[0]) == id_t:
                actual_list.pop(idx)
                print(actual_list)
    with open(f'{path}/{filename}.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(actual_list)

def str_to_senconds(str_time:str):
    ''' Conver a string with the time in seconds
    Params
        - str_time --> string with the format H:M:S
    Return:
        - seconds --> integer with the seconds
    '''
    if str_time == '0':
        h = 0
        m = 0
        s = 0
    else:
        h , m , s = str_time.split(':')

    seconds = datetime.timedelta(hours=int(h),minutes=int(m), seconds=int(s)).seconds

    return seconds

def get_date():
    ''' Optain the actual date and returns it like a string
    Params:
        None
    Return:
        - date --> the formated date in a string D-M-Y
    '''
    
    str_date = datetime.datetime.today()
    str_date = str(str_date.strftime('%d-%m-%Y'))

    return str_date
# --------------- Main -----------------
if __name__ == "__main__":
    pass
