#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# 
# Author:			Anna Cristina Karingal
# Name:				main.py
# Created: 			February 27, 2015
# Last Updated: 	March 1, 2015
# Description: 		Demonstrates how an operating system manages processes  
# 						and process queues for the different devices in a 
#						system
# Run using: 		python main.py

import sys
import commands

def main():

	# Call system command loop to generate system and prompt user for input
	sys_comm = commands.SysCommand()
	sys_comm.cmdloop()

if __name__ == '__main__':
	main()