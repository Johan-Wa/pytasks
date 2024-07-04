# ----------- Imports
import curses
from curses import color_pair, wrapper
import time
import datetime
import threading

import sys_func

#----------- Clases --------
class DisplayList():
    '''This class Display a list in the screen, in form of menu and give a selections funtionalities:
    
    Params:
        - name --> the name (string) of the menu
        - menu_list --> a list with the options of the menu
    '''
    def __init__(self, name:str, list_path):
        self.name = name
        self.list_path = list_path
        self.menu = []
        self.list_range = [0,10]
        self.quit_note = 'Press Esc to QUIT'
        self.arrows_note = 'Use the arrows to move UP and DOWN'
        self.enter_note = 'Press ENTER to select the list'
        self.wh = 0
        self.ww = 60


    def print_list(self,scr,menu_list,selected_row):
        '''this func print the 10 first objects in the menu list
        and show the current object selected

        Params:
            - self --> self class
            - scr --> the screen to show the list
            - menu_list --> the list of menu options
            - selected_row --> the row os the option in the list
        '''
        min = self.list_range[0]
        max = self.list_range[1]
        scr.addstr(0,2,' ' + self.name + ' ' , curses.color_pair(5))

        # Draw text actions
        del_msn_disp = "elete"
        create_msn_disp = "reate"
        
        scr.attron(curses.color_pair(3))
        scr.addstr(self.wh-2,1, " C")
        scr.attroff(curses.color_pair(3))

        scr.addstr(self.wh-2,3, create_msn_disp + ' ')

        scr.attron(curses.color_pair(2))
        scr.addstr(self.wh-2,self.ww-len(del_msn_disp)-4, " D")
        scr.attroff(curses.color_pair(2))
        scr.addstr(self.wh-2,self.ww-len(del_msn_disp)-2, del_msn_disp + ' ')

        pos_y = 2
        pos_count = 0
        
        # Draw list
        for i in enumerate(menu_list):
            if i[0] == selected_row:
                scr.attron(curses.color_pair(4))
                scr.addstr(pos_y + pos_count ,self.ww//8 + 1,i[1])
                scr.attroff(curses.color_pair(4))
                pos_count += 1
            elif i[0] in range(min,max):    
                scr.addstr(pos_y + pos_count, self.ww//8, i[1])
                pos_count += 1

    def get_list(self):
        self.menu = sys_func.optain_file_list(self.list_path)

    def new_item(self, scr):
        '''Creates a new file in the dir of csv lists, and generated a new entry in de list.
        Params:
            - scr --> The parent screen.
        Returns:
            - new_i --> the new item created.
        '''
        w_item = Inpbox('New list')
        new_i = w_item.main(scr)
        if len(new_i) > 0:
            sys_func.create_a_csv(self.list_path, new_i)
            
    def delete_item(self, scr, selected_row):
        ''' Delete a csv file from the list.
        Params:
            - scr --> The screen
            - selected_row --> Is the selected item in the list
        Returns: 
            - del_item --> The name of the delete file without extension
        '''
        scr.clear()
        if len(self.menu) > 0:
            del_item = self.menu[selected_row]
            sys_func.delete_a_csv(self.list_path, del_item)
            return del_item

    def when_press_enter(self, scr, selected_row):
        ''' Displays the next menu.
        Params:
            - scr --> The screen
            - selected_row --> The name of the list to display
        Returns:
            None
        '''
        tasks_window = DisplayTasks(self.menu[selected_row],
                                    list_path=self.list_path,
                                    name=f'{self.menu[selected_row]}: Tasks')

        tasks_window.enter_note = "Press ENTER to select the task's options"
        tasks_window.quit_note = "Press Esc to go back"
        tasks_window.main(scr)
        scr.clear()

    def main(self,scr):
        '''This is the main function of the class, this function initialize the program.
        Params:
            - self --> the class properties, don need entry
            - scr --> the screen, this normally is given by the wrapper
        '''
        self.get_list()
        
        # setting the colors of the app
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)

        curses.curs_set(0)
        current_row = 0
        
        if len(self.menu) <= 10:
            self.wh = len(self.menu) + 4
        else:
            self.wh = 14
        scr.clear()
        scr.nodelay(1)
        scr.timeout(150)
        while True:

            self.get_list()
            win = curses.newwin(self.wh,self.ww, curses.LINES//2 - self.wh//2, curses.COLS//2 - self.ww//2)

            if len(self.menu) <= 10:
                self.wh = len(self.menu) + 5
            else:
                self.wh = 15

            win.clear()
            win.border()
            
            quit_note = self.quit_note
            scr.attron(curses.color_pair(2))
            scr.addstr(curses.LINES//2 - self.wh//2 - 4,curses.COLS//2 - len(quit_note)//2,quit_note)
            scr.attroff(curses.color_pair(2))

            arrows_note = self.arrows_note
            scr.attron(curses.color_pair(3))
            scr.addstr(curses.LINES//2 - self.wh//2 - 2,curses.COLS//2 - len(arrows_note)//2,arrows_note)
            scr.attroff(curses.color_pair(3))

            enter_note = self.enter_note
            scr.addstr(curses.LINES//2 + self.wh//2 + 1,curses.COLS//2 - len(enter_note)//2,enter_note, curses.A_BOLD)

            self.print_list(win, self.menu, current_row)

            win.refresh()
    
            key = scr.getch()
            
            try:
                if key == 27:
                    break
                elif key == curses.KEY_UP and current_row > 0:
                    current_row -= 1
                elif key == curses.KEY_DOWN and current_row < len(self.menu)-1:
                    current_row += 1
                elif chr(key) == 'c' or chr(key) == 'C':
                    self.new_item(scr)
                elif chr(key) == 'd' or chr(key) == 'D':
                    self.delete_item(scr,current_row)
                elif key == curses.KEY_ENTER or key == 10 or key == 13:
                    self.when_press_enter(scr,current_row)

            except:
                pass

            finally:
                if key == curses.KEY_UP and current_row == self.list_range[0] and current_row !=0:
                    self.list_range[0] -= 1
                    self.list_range[1] -= 1
                elif key == curses.KEY_DOWN and current_row == self.list_range[1]:
                    self.list_range[0] += 1
                    self.list_range[1] += 1

            win.clear()
            win.refresh()
            

    def wrapp(self):
        '''This is an auxiliar function that wrapps the main function,
        don't resieve any parameter diferent to self, a this is only invoque
        when the class tha initialize the program is this. 
        if the class isn't initializing the program, will be invoque
        by the main method.
        '''
        wrapper(self.main)
    
class Inpbox():
    '''This class generates a inpbox that optain the user entry, and return it.
    Params:
        - promt --> A promt to show in the inpbox
    Returns: 
        - new_en --> The entry of the user as a string
    '''
    def __init__(self,promt):
        self.promt = promt

    def main(self, scr):
        ''' Show the screen and return the entry
        Params:
            - scr --> The screen to show the box
        Returns:
            - new_en --> The entry of the user
        '''
        width = 42
        height = 2
        top = (curses.LINES - height) // 2
        left = (curses.COLS - width) // 2

        curses.init_pair(4,curses.COLOR_BLACK, curses.COLOR_WHITE)

        box_win = curses.newwin(height, width, top, left)
        scr.clear()
        scr.refresh()

        # Parent Window
        box_win.clear()

        box_win.border()
        box_win.addstr(0,2, ' ' + self.promt + ' ')

        box_win.refresh()

        # Input box
        txt = curses.newwin(1, width - 4, top + height - 1, left + 2)
        txt.bkgd(curses.color_pair(4))
        txt.refresh()
        txt.keypad(1)
        curses.echo()
        new_en = txt.getstr().decode('UTF-8')
        curses.noecho()

        scr.clear()
        scr.refresh()
        return new_en

    def wrapp(self):
        wrapper(self.main)


class DisplayTasks(DisplayList):
    def __init__(self, filename:str,*arg,**kwargs):
        super().__init__(*arg,**kwargs)
        self.filename = filename

    def get_list(self):
        self.menu = sys_func.get_task_list(self.list_path,self.filename)

    def delete_item(self, scr, selected_row):
        ''' Delete a task from the list.
        Params:
            - scr --> The screen
            - selected_row --> row of the task
        Returns:
            - del_task --> name of the task
        '''
        scr.clear()
        del_task = self.menu[selected_row]
        del_task = int(del_task.split('.')[0])
        scr.clear()
        scr.refresh()

        sys_func.del_task(self.list_path,self.filename,del_task)

    def new_item(self, scr):
        scr.clear()
        new_task = CreateTask(self.list_path, self.filename,'New Task', ['','','28-06-2024','0','00:00:00',''])
        new_task.main(scr)
        scr.clear()
        scr.refresh()
       
    def when_press_enter(self, scr, selected_row):
        scr.clear()
        options_list = ListSelect(['Update','View data','Track'], 'Select option')
        option = options_list.main(scr)
        scr.clear()
        scr.refresh()
        selected_task = self.menu[selected_row].split('.')[0]
        file = sys_func.read_csv(self.list_path,self.filename)
        for idx, row in enumerate(file):
            if row[0] == selected_task:
                data = file[idx]
        idx = data.pop(0)
        if option == 'Update':
            update_task = CreateTask(self.list_path, self.filename, 'Update', data,
                                     new = False, id_task=int(idx))
            update_task.main(scr)
            scr.clear()
            scr.refresh()
        elif option == 'View data':
            view_task = ShowTaskInfo(self.list_path, self.filename, int(idx), f'Task: {idx} - {data[0]}')
            view_task.main(scr)
            scr.clear()
            scr.refresh()
        elif option == 'Track':
            track_task = TaskTracker(data[0])
            track_task.main(scr)
            scr.clear()
            scr.refresh()
            


class CreateTask():
    '''This is a form that gets the information given by the user and return a list with the data.
    Params:
        - promt --> the promt to show in the window
    Returns:
        - data --> data list
            - task_name --> string
            - state --> option [no started, completed, canceled, process]
            - create_date --> string (date) D-M-Y
            - finished_date --> string (date) D-M-Y
            - finish_time --> time to finish task (string) H:M:S
            - priority --> option [normal, important, urgent]

    '''
    def __init__(self,list_path, filename, promt:str, data:list, new = True, id_task = 0):
        self.promt = promt
        self.path = list_path
        self.filename = filename
        self.default_data = data
        self.window_objets = [
            'Task name:', 'State:','Create date:',
            'Finished date:','Finish time:',
            'Priority:', ' [Cancel] ', ' [Ok] '
        ]
        self.new = new
        self.id_task = id_task
    def main(self,scr):
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4,curses.COLOR_BLACK,curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.curs_set(0)

        data_list = self.default_data
        wh = 11
        ww = 60
        current_row = 0

        scr.clear()
        win = curses.newwin(wh, ww, curses.LINES//2 - wh//2, curses.COLS//2 - ww//2)
        win.nodelay(1)
        win.timeout(150)
        while True:
            win.border()
            win.addstr(0,2,' ' + self.promt + ' ',color_pair(5))
            
            pos_y = 2

            for idx, row in enumerate(self.window_objets[:6]):
                if idx != current_row:
                    win.addstr(pos_y,ww//6,self.window_objets[idx])
                    win.addstr(pos_y,ww//2,data_list[idx])
                    pos_y +=1
                else:
                    win.attron(color_pair(4))
                    win.addstr(pos_y,ww//6 + 1,self.window_objets[idx])
                    win.attroff(color_pair(4))
                    win.addstr(pos_y,ww//2,data_list[idx])
                    pos_y +=1

            if current_row == 6:
                win.attron(color_pair(4))
                win.addstr(wh - 2, 2,self.window_objets[6])
                win.attroff(color_pair(4))
            else:
                win.attron(color_pair(2))
                win.addstr(wh - 2, 2,self.window_objets[6])
                win.attroff(color_pair(2))

            scr.refresh()
            win.refresh()

            if current_row == 7:
                win.attron(color_pair(4))
                win.addstr(wh - 2, ww - len(self.window_objets[7]) - 2 ,self.window_objets[7])
                win.attroff(color_pair(4))
            else:
                win.attron(color_pair(3))
                win.addstr(wh - 2, ww - len(self.window_objets[7]) - 2,self.window_objets[7])
                win.attroff(color_pair(3))

            scr.refresh()
            win.refresh()

            key = scr.getch()
            
            if key == 27:
               break
            if key == curses.KEY_UP and current_row > 0 and current_row < 7:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < 6:
                current_row += 1
            elif key == curses.KEY_LEFT and current_row == 7:
                current_row -=1
            elif key == curses.KEY_RIGHT and current_row == 6:
                current_row += 1
            elif (key == curses.KEY_ENTER or key == 10 or key == 13) and current_row < 6:
                data_list[current_row] = self.when_press_enter(scr,current_row)
            elif (key == curses.KEY_ENTER or key == 10 or key == 13) and current_row == 6:
                break
            elif (key == curses.KEY_ENTER or key == 10 or key == 13) and current_row == 7:
                data_v, msg = self.validate_values(data_list)
                if not data_v:
                    scr.clear()
                    scr.addstr(curses.LINES//2 + wh//2 + 2,curses.COLS//2 - len(msg)//2,msg,curses.color_pair(2))
                    scr.refresh()
                elif data_v and self.new: 
                    sys_func.new_task(self.path, self.filename, data_list)
                    break
                elif data_v and not self.new: 
                    sys_func.update_task(self.path, self.filename, data_list,
                                         id_task=self.id_task)
                    break
                           
            win.clear()
            win.refresh()
    
    def validate_values(self,data):
        validate = True
        msg = ''
        for i in data:
            if len(i) == 0:
                validate = False
                msg = 'All the data should be completed'

        return validate, msg



    def when_press_enter(self,scr,selected_row):
        item = ''
        match selected_row:
            case 0 | 2 | 3 | 4:
                input = Inpbox(f' {self.window_objets[selected_row].split(':')[0]} ')
                item = input.main(scr)
            case 1:
                input = ListSelect(['no started','completed','canceled','process'], 'State')
                item = input.main(scr)
            case 5:
                input = ListSelect(['normal','important','urgent'], 'Priority')
                item = input.main(scr)

        return item

    def wrapp(self):
        wrapper(self.main)

class ListSelect():
    '''Display a selectable list and returns that selection.
    Params:
        - menu_list --> selectables
        - promt --> promt to show in the window
    Returns:
        - selection --> the item selected
    '''
    def __init__(self,menu_list:list, promt:str):
        self.menu = menu_list
        self.promt = promt
        self.wh = len(self.menu) + 5
        self.ww = 30

    def print_window(self,scr, selected_row):
        scr.clear()
        win_ob = self.menu
        scr.border()
        scr.addstr(0, 2 , ' ' + self.promt + ' ', curses.color_pair(5))
        pos_y = 2

        for idx, row in enumerate(win_ob):
            if idx != selected_row:
                scr.addstr(pos_y + idx, self.ww//2 - len(row)//2, row)
            else:
                scr.attron(color_pair(4))
                scr.addstr(pos_y + idx, self.ww//2 - len(row)//2, row)
                scr.attroff(color_pair(4))

        if selected_row == len(self.menu):
            scr.attron(color_pair(4))
            scr.addstr(self.wh - 2, self.ww//2 - len(' [Cancel] ')//2,' [Cancel] ')
            scr.attroff(color_pair(4))
        else:
            scr.attron(color_pair(2))
            scr.addstr(self.wh - 2, self.ww//2 - len(' [Cancel] ')//2,' [Cancel] ')
            scr.attroff(color_pair(2))

        scr.refresh()


    def main(self,scr):
        curses.init_pair(2, curses.COLOR_RED,curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4,curses.COLOR_BLACK,curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.curs_set(0)

        current_row = 0

        scr.clear()
        scr.refresh()
        win = curses.newwin(self.wh, self.ww, 
                            curses.LINES//2 - self.wh//2, 
                            curses.COLS//2 - self.ww//2
                            )
        win.clear()
        win.border()     
        self.print_window(win, current_row)
        win.refresh()
        while True:

            win.border()
            
            self.print_window(win, current_row)

            win.refresh()

            key = scr.getch()

            if key == curses.KEY_UP and current_row > 0 and current_row <= len(self.menu):
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.menu):
                current_row += 1
            elif (key == curses.KEY_ENTER or key == 10 or key == 13) and current_row < len(self.menu):
                return self.when_press_enter(current_row)
            elif (key == curses.KEY_ENTER or key == 10 or key == 13) and current_row == len(self.menu):
                return ''
            
            win.refresh()


    def when_press_enter(self,selected_row):
        return self.menu[selected_row]

    def wrapp(self):
        wrapper(self.main)

class ShowTaskInfo():
    ''' Show the task info '''
    def __init__(self,path,filename,id_task, promt):
        self.path = path
        self.filename = filename
        self.id_task = id_task
        self.promt = promt

    def print_window(self,scr, data):
        wh = 11
        ww = 60
        curses.curs_set(0)
        curses.init_pair(3,curses.COLOR_GREEN,curses.COLOR_BLACK)
        curses.init_pair(5,curses.COLOR_CYAN,curses.COLOR_BLACK)
        window_objets = ['Task name:', 'State:', 'Create date:', 'Finished date:', 'Finish Time:', 'Priority:']
        win = curses.newwin(wh, ww,
                      curses.LINES//2 - wh//2,
                      curses.COLS//2 - ww//2)
        scr.clear()
        win.clear()
        win.border()
        
        win.addstr(0,1, ' ' + self.promt + ' ', curses.color_pair(5))
        pos_y = 2
        for i in range(len(window_objets)):
            win.addstr(pos_y, ww//6, window_objets[i], curses.color_pair(3))
            win.addstr(pos_y, ww//2, data[i])
            pos_y += 1
        
        scr.refresh()
        win.refresh()
        win.getch()
            
        

    def main(self,scr):
        f_info = sys_func.read_csv(self.path, self.filename)
        info = []
        for idx, l in enumerate(f_info):
            if int(l[0]) == self.id_task:
                info = f_info[idx]

        info.pop(0)
        self.print_window(scr,info)

    def wrapp(self):
        wrapper(self.main)

class TaskTracker():
    def __init__(self, promt) -> None:
        self.promt = promt
        self.task_time = '00:00:00'
        self.wh = 9
        self.ww = 40
        self.chronometer = False
        self.tt = 0
        self.t1 = threading.Thread(name='Hilo_1', target=self.chrono)
        

    def chrono(self):
        while self.chronometer:
            time.sleep(1)
            self.tt += 1
            self.task_time = str(datetime.timedelta(seconds=self.tt))

    def main(self, scr):

        curses.curs_set(0)
        scr.clear()
        win = curses.newwin(curses.LINES//2 - self.wh//2, curses.COLS//2 - self.ww//2, self.wh, self.ww)
        win.nodelay(1)
        scr.nodelay(1)
        scr.timeout(150)
        
        while True:
            win.border()
            win.addstr(0,2, ' ' + self.promt + ' ', curses.color_pair(5))
            win.addstr(self.wh//2, self.ww//2 - len(self.task_time)//2, self.task_time, curses.A_BOLD)
            win.addstr(self.wh - 1, 1, ' S', curses.color_pair(3))
            win.addstr(self.wh - 1, 3, 'tart ')
            win.addstr(self.wh - 1, self.ww - 5, ' Sto')
            win.addstr(self.wh - 1, self.ww - 1, 'p ', curses.color_pair(2))

            scr.refresh()
            win.refresh()
            key = scr.getch()
            
            
            if key == 27:
                self.chronometer = False
                break
            
                
            try:
                ch = chr(key)
            except:
                ch = ''

            if ch == 's' and not self.chronometer:
                self.chronometer = True
                self.t1.start()
            elif ch == 'p' and self.chronometer:
                self.chronometer = False
                

    def wrapp(self):
        wrapper(self.main)

# ---------- Main -----------

if __name__ == "__main__":
    path_list = 'csv_lists'
    #todo_list = DisplayList('To Dos List', path_list)
    #todo_list.wrapp()
    tasks_window = DisplayTasks('nuevo proyecto', list_path=path_list, name='Tasks')
    tasks_window.wrapp()
    #new_task = CreateTask('New task')
    #new_task.wrapp()
    #select_menu = ListSelect(['no started','completed','canceled','process'], 'State')
    #select_menu.wrapp()
    #task_view = ShowTaskInfo(path_list,'frankenpy',1, 'Frankenpy 1')
    #task_view.wrapp()
    #tracker = TaskTracker('task tracker')
    #tracker.wrapp()
    pass
