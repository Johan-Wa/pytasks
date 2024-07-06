import os
import sys
from pathlib import Path

rute = Path(os.path.abspath(__file__)).parent
sys.path.append(str(rute))

from source import sys_func
from source import windows as wc

def main():
    app_name = 'Pytasks'
    path = rute / 'source/csv_lists'

    app = wc.DisplayList(app_name,path)
    app.wrapp()

if __name__ == "__main__":
    main()

