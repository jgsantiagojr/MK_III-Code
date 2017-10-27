'''
The official build chain for the 2017-2018 Olin Electric Motorsports FSAE Formula Team
For more information on the team: https://www.olinelectricmotorsports.com/

@author: Peter Seger '20

Released under MIT License 2017
'''


import glob
import os
import re
import sys
import subprocess


CC = 'gcc'
PROGRAMMER = 'avrispmkII'
PORT = 'usb'
AVRDUDE = 'avrdude'
OBJCOPY = 'avr-objcopy'
MCU = 'atmega16m1'
F_CPU = '4000000UL'
COMPILER = 'gnu99'
FUSE = '0x62'

CFLAGS = '-Os -g -mmcu=' + MCU + ' -std=' + COMPILER + ' -Wall -Werror -ff'
LDFLAG = '-mmcu=' + MCU + '-lm'
AVRFLAGS = '-p ' + MCU + ' -v -c ' + PROGRAMMER + ' -p ' + PORT

possible_boards = ['Dashboard','BMS','Blinky']


def get_input():
    board = input("Board (i.e. Dashboard): ")
    flash = input("Flash (y/n): ")

    # Test Inputs
    if board not in possible_boards:
        print("Not a possible board -%s-"%(board))
        quit()
    if flash != 'y' and flash !='n':
        print("Not a possible flash setting -" + flash)
        quit()

    return board, flash


def build_boards_list(boards, head):
    '''
    Goes through the /boards directory and adds each board to a list
    '''
    os.chdir(boards)
    boards = []
    bds = glob.glob('*')
    for el in bds:
        boards.append(el)
    os.chdir(head)
    return boards


def make_libs():
    libs = os.listdir('./lib/')
    return libs


def ensure_setup(board, test, head):
    t = os.listdir(test)
    if 'outputs' not in t:
        os.chdir(test)
        os.system('mkdir outs')
        os.chdir(head)


def make_elf(board, test, libs, head):
    os.chdir(test)
    c_files = glob.glob('*.c')
    h_files = glob.glob('*.h')
    out = 'cc '
    for item in c_files:
        out = out + str(item) + (' ')
    out = out + '-o ' + board + '.elf'
    print(out)
    outs = 'outs/'
    os.chdir(outs)
    file = open('test', 'a')    #DEBUG
    file.write(out+"\n")        #DEBUG
    file.close()                #DEBUG
    # os.system(out)            #Write command to system
    os.chdir(head)


def make_hex(board, test, libs, head):
    '''
    Takes the elf output files and turns them into hex output
    '''
    # $(BUIDIR)/%.hex: $(BUIDIR)/%.elf
    # $(OBJCOPY) -O ihex -R .eeprom $< $@
    outs = 'outs/'
    os.chdir(test)
    os.chdir(outs)
    elf = glob.glob('*.elf')
    out = OBJCOPY + ' -O ihex -R .eeprom ' + elf[0] + ' ' + board +'.hex'
    file = open('test', 'a')    #DEBUG
    file.write(out+"\n")        #DEBUG
    file.close()                #DEBUG
    # os.system(out)            #Write command to system
    os.chdir(head)



def flash_board(board, test, libs, head):
    '''
    Takes hex files and uses ARVDUDE w/ ARVFLAGS to flash code onto board
    '''
    # flash: $(BUIDIR)/$(TARGET).hex
    # sudo $(AVRDUDE) $(AVRFLAGS) -U flash:w:$<
    os.chdir(test)
    hex_file = glob.glob('*.hex')
    out = 'sudo ' + AVRDUDE + ' ' + AVRFLAGS + ' -U flash:v:' + hex_file
    print(out)          #DEBUG
    # os.system(out)      #Write command to systems


def set_fuse():
    '''
    Uses ARVDUDE w/ ARVFLAGS to set the fuse
    '''
    out = 'sudo ' + AVRDUDE + ' ' + AVRFLAGS + ' -U hfuse:w:' + FUSE + ':m'
    print(out)          #DEBUG
    # os.system(out)            #Write command to system


if __name__ == "__main__":
    # TODO
    '''
    -Make argc input when file called and setup logic flow for flashing, clean, and board building
    '''
    cwd = os.getcwd()

    board, flash = get_input()

    boards = './boards/'
    boards_list = build_boards_list(boards, cwd)    # Get a list of all boards

    test = './boards/%s/'%board

    ensure_setup(board, test, cwd)
    libs = make_libs()
    make_elf(board, test, libs, cwd)
    make_hex(board, test, libs, cwd)
    # make_hex(board)

    # if(flash == 'y'):
        # flash_board()


    # test = './boards/%s/'%board
    # t = os.listdir(test)


    '''
    os.chdir(test)
    os.system('ls')
    os.system('make clean')
    os.chdir('..')
    os.system('ls')
    '''
    # os.chdir('boards/')
    # os.system('mkdir hello')
