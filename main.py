from source import windows as wc
from source import sys_func

def main():
    app_name = 'Pytasks'
    path = 'source/csv_lists'

    app = wc.DisplayList(app_name,path)
    app.wrapp()

if __name__ == "__main__":
    main()

