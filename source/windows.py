# ----------- Imports
import curses
from curses import wrapper
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
        self.ww = 45


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

    def get_list(self,list_path):
        self.menu = sys_func.optain_file_list(path_list)

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
        return new_i
    
    def delete_item(self, scr, selected_row):
        scr.clear()
        del_item = self.menu[selected_row]
        sys_func.delete_a_csv(self.list_path, del_item)
        return del_item

    def main(self,scr):
        '''This is the main function of the class, this function initialize the program.
        Params:
            - self --> the class properties, don need entry
            - scr --> the screen, this normally is given by the wrapper
        '''
        self.get_list(self.list_path)
        
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
            self.get_list(self.list_path)
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

            scr.refresh()
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
                    item = self.delete_item(scr,current_row)

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

            scr.refresh()
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

# ---------- Main -----------

if __name__ == "__main__":
    path_list = 'csv_lists'
    todo_list = DisplayList('To Dos List', path_list)
    todo_list.wrapp()
    #input_box = Inpbox('New entry')
    #input_box.wrapp()
    pass
