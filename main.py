#! /usr/bin/env python3
# main.py 
# programmed by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last updated: 15 August 2020

import playmode
import readmode

settings = {'turnmode_play': True, 'turnmode_read': False, 'reverse_read': False}

def resetting():
    ON_OFF = ['OFF', 'ON']

    while True:
        print('''
    PLAY MODE
        BOARD ROTATION IN BLACK'S TURN: {}

    READ MODE
        BOARD ROTATION IN BLACK'S TURN: {}

        '''.format(ON_OFF[settings['turnmode_play']], ON_OFF[settings['turnmode_read']]))
        command = input("ENTER A COMMAND (P to change playmode / R to change readmode / X to exit) >>> ")
        if command in ['P', 'p', 'PLAY', 'play', 'Play', 'PLAYMODE', 'PlayMode', 'Playmode', 'playmode', 'PLAY MODE', 'Play Mode', 'Play mode', 'play mode']:
            print('''
            BOARD ROTATION IN BLACK'S TURN IN PLAY MODE: {}
            '''.format(ON_OFF[settings['turnmode_play']]))
            while True:
                command = input("ENTER A COMMAND (ON / OFF / EXIT) >>> ")
                if command in ['ON', 'on', 'On']:
                    settings['turnmode_play'] = True
                    break
                elif command in ['OFF', 'Off', 'off']:
                    settings['turnmode_play'] = False
                    break
                elif command in ['EXIT', 'Exit', 'exit', 'X', 'Ex', 'EX', 'ex']:
                    break
        elif command in ['R', 'r', 'READ', 'Read', 'read', 'READMODE', 'ReadMode', 'Readmode', 'readmode', 'READ MODE', 'Read Mode', 'Read mode', 'read mode']:
            print('''
            BOARD ROTATION IN BLACK'S TURN IN READ MODE: {}
            '''.format(ON_OFF[settings['turnmode_read']]))
            while True:
                command = input("ENTER A COMMAND (ON / OFF / EXIT) >>> ")
                if command in ['ON', 'on', 'On']:
                    settings['turnmode_read'] = True
                    settings['reverse_read'] = True
                    break
                elif command in ['OFF', 'Off', 'off']:
                    settings['turnmode_read'] = False
                    settings['reverse_read'] = False
                    break
                elif command in ['EXIT', 'Exit', 'exit', 'X', 'Ex', 'EX', 'ex']:
                    break
        elif command in ['X', 'x', 'Exit', 'EXIT', 'exit', 'EX', 'Ex', 'ex']:
            return



if __name__ == "__main__":
    while True:
        print("\n\nWELCOME TO CHESS\n")
        command = input("ENTER A COMMAND (P to PLAYMODE / R to READMODE / S to SETTINGS / X to EXIT) >>> ")
        if command in ['P', 'p', 'PLAY', 'play', 'Play', 'PLAYMODE', 'PlayMode', 'Playmode', 'playmode', 'PLAY MODE', 'Play Mode', 'Play mode', 'play mode']:
            playmode.playmode(settings['turnmode_play'])
            break

        elif command in ['R', 'r', 'READ', 'Read', 'read', 'READMODE', 'ReadMode', 'Readmode', 'readmode', 'READ MODE', 'Read Mode', 'Read mode', 'read mode']:
            readmode.readmode(settings['turnmode_read'], settings['reverse_read'])
            break

        elif command in ['S', 's', 'SETTINGS', 'settings', 'Settings', 'SETTING', 'Setting', 'setting']:
            resetting()
            
        elif command in ['X', 'x', 'Exit', 'EXIT', 'exit', 'EX', 'Ex', 'ex']:
            break