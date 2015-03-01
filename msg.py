#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:           Anna Cristina Karingal
# Name:             msg.py
# Created:          March 1, 2015
# Last Updated:     March 1, 2015
# Description:      Contains methods to display formatted output to terminal

screen_width = 78

def ruler(len=screen_width): 
	return "{:-^{l}}".format("", l=len)

def sys_mode(mode_name, len=screen_width):
	return "\n" + "{:#^{l}}".format(" " + mode_name.upper() + " ", l=len) + "\n"

def err(err_msg):
	return "ERROR: " + err_msg 

def invalid_command():
	return "ERROR: Invalid command"

def nothing_in_cpu():
	return "ERROR: No active process in CPU"

def nothing_in_ready():
	return "ERROR: Ready queue is empty"



