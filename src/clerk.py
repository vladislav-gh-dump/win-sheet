import os
import sys


def make_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def make_file(dir):
    if not os.path.isfile(dir):
        with open(dir, "w", encoding="UTF-8") as file:
            ...


def write_to_file(dir, text):
    with open(dir, "w", encoding="UTF-8") as file:
        file.write(text)


def get_text_from_file(dir):
    text = ""
    with open(dir, "r", encoding="UTF-8") as file:
        text = file.read()
    return text


class Clerk:
    
    def __init__(self):
        self.__cur_text = ""
        self.__text_list = [self.__cur_text]
        self.__index_cur_text = 0

        self.__data_file_dir = ""
        self.__data_file_dir_init()
        
    def __data_file_dir_init(self):
        # создание директории для хранения файла с текстом
        cur_dir = os.path.dirname(os.path.abspath(sys.argv[0])) 
        data_dir = f"{cur_dir}\\clerk-data"
        make_dir(data_dir)
        
        # создание файла для хранения текста
        self.__data_file_dir = f"{data_dir}\\clerk-text.data"
        make_file(self.__data_file_dir)
    
    def __is_index_cur_text_exist(self, index):
        return index >= 0 and index <= len(self.__text_list) - 1
    
    def drop_text(self):
        self.__cur_text = ""
        self.__text_list = [self.__cur_text]
        self.__index_cur_text = 0
    
    def get_text(self):
        return self.__text_list[self.__index_cur_text]
    
    def go_prev_text(self):
        index_cur_text = self.__index_cur_text - 1
        if self.__is_index_cur_text_exist(index_cur_text):
            self.__index_cur_text = index_cur_text
            
    def go_next_text(self):
        index_cur_text = self.__index_cur_text + 1
        if self.__is_index_cur_text_exist(index_cur_text):
            self.__index_cur_text = index_cur_text
    
    def write(self, text):
        self.__cur_text = text
        self.__text_list.append(self.__cur_text)
        self.__index_cur_text = len(self.__text_list) - 1 
        
    def save(self):
        self.__data_file_dir_init()
        
        write_to_file(self.__data_file_dir, self.__text_list[self.__index_cur_text])
            
    def load(self):
        self.__data_file_dir_init()
        
        text = get_text_from_file(self.__data_file_dir)
        self.write(text)
        
    