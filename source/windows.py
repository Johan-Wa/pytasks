# ----------- Imports
import curses
from curses import wrapper

#----------- Clases --------
class DisplayList():
    '''This class Display a list in the screen, in form of menu and give a selections funtionalities:
    
    Params:
        - name --> the name (string) of the menu
        - menu_list --> a list with the options of the menu
    '''
    def __init__(self, name:str, menu_list:list):
        self.name = name
        self.menu = menu_list


    def print_list(self,scr,menu_list, heigth, weight,selected_row):
        '''this func print the 10 first objects in the menu list
        and show the current object selected

        Params:
            - self --> self class
            - scr --> the screen to show the list
            - menu_list --> the list of menu options
            - heigth --> the height of the screen
            - weight --> the weight of the screnn
            - selected_row --> the row os the option in the list
        '''
        if selected_row > 9:
            max = selected_row + 1
            min = selected_row - 9
        else: 
            max = 10
            min = 0

        scr.addstr(0,2,' ' + self.name + ' ' , curses.color_pair(5))
        pos_y = heigth//2-len(self.menu)//2
        
        for i in enumerate(menu_list):
            if i[0] == selected_row:
                scr.attron(curses.color_pair(4))
                scr.addstr(pos_y + i[0] ,weight//8 + 1,i[1])
                scr.attroff(curses.color_pair(4))
            elif i[0] in range(min,max):    
                scr.addstr(pos_y + i[0], weight//8, i[1])

    def main(self,scr):
        '''This is the main function of the class, this function initialize the program.
        Params:
            - self --> the class properties, don need entry
            - scr --> the screen, this normally is given by the wrapper
        '''
        # setting the colors of the app
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)

        curses.curs_set(0)
        
        scr.clear()

        current_row = 0
        if len(self.menu) <= 10:
            wh = len(self.menu) + 4
        else:
            wh = 14
        ww = 35
        win = curses.newwin(wh,ww, curses.LINES//2 - wh//2, curses.COLS//2 - ww//2)
        win.clear()
        win.border()
        
        self.print_list(win,self.menu, wh, ww, current_row)

        scr.refresh()
        win.refresh()
        scr.getch()

    def wrapp(self):
        '''This is an auxiliar function that wrapps the main function,
        don't resieve any parameter diferent to self, a this is only invoque
        when the class tha initialize the program is this. 
        if the class isn't initializing the program, will be invoque
        by the main method.
        '''
        wrapper(self.main)
    

# ---------- Main -----------

if __name__ == "__main__":
    menu_list = ['list1','list2','list3','list4','list5','list6','list7','list8','list9','list10','list11']
    todo_list = DisplayList('To Dos List', menu_list)
    todo_list.wrapp()
