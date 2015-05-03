# OS_Simulator

Simulates how an operating system manages processes and process queues.

**Author:** Anna Karingal

**Date Created:** February 27, 2015

**Last Modified:** May 3, 2015

## Usage

**Python Version:** 2.7.6

The program is run from the command line using `python main.py` in the working directory.

Once you run the program, it will enter system generation (Sys Gen) mode and prompt you for information about the system, including how many devices are in the system, how many cylinders there are for each disk drive and some parameters for CPU scheduling like the history parameter (alpha) and intial burst estimate (Tau(0)). 

**CPU Scheduling** is implemented using a history-based shortest job first approximation algorithm using the formula

    Tau(next) = (alpha * Tau(previous)) + ((1-alpha) + t(previous))

where `t(previous)` is the actual previous CPU burst and `Tau` is the estimated burst. All processes are initialized with an estimated next burst of `Tau(0)`.

**Disk Scheduling** is implemented using an FLOOK algorithm. 

Once the program exits sys gen mode, the user can input commands to simulate system calls and new processes coming into the system. The user will also be prompted to enter how much time has elapsed between system calls, so that CPU scheduling can properly be implemented.

## Commands

`a`  -- Activates a new process

`t`  -- Terminates current process in CPU

`s`  -- Enters snapshot mode. Enter the prefix of the device type to see a list of processes in devices of that type.

`p1` -- enter the name of any device in lowercase to simulate the active process in the CPU requesting that device via a system call

`P1` -- enter the name of any device in uppercase to simulate the active process in  that device is finished and wants to go back into the ready queue.

`h`  -- Help to see a list of commands

`q` or `Ctrl+D` to quit

## Coming soon

- Memory management simulation using paging
- Kill command to kill any process
