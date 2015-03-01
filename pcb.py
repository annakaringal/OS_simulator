class PCB:

    def __init__(self, id_num, p_loc="ready"): 
    	self.pid = id_num
    	self.proc_loc = p_loc

    def __repr__(self):
    	return str(pid)

    def __str__(self):
    	return "process #" + str(self.pid)

    def get_pid(self):
    	return self.pid

    def set_proc_loc(self, p_loc):
    	""" Sets location of process, i.e. which queue/device it is in"""
    	self.proc_loc = p_loc

    def status(self):
		return "%s in %s queue" %(self, self.proc_loc)

    ## Setting/clearing system call params

    def set_syst_call_params(self):
        print "##### SET SYSTEM CALL PARAMETERS"
        # TODO: ERROR CHECKING & FORMATTING
        self.file_name = raw_input("File Name: ")
        self.mem_loc = raw_input("Starting Memory Location: ")

    def set_read_write_params(self, dev_type):
        if (dev_type.lower() == "printer"):
            self.read_write = "write"
        else: 
            rw = raw_input("Read or Write?: ")
            if rw.lower() in ["r", "read"]:
                self.read_write = "read"
            elif rw.lower() in ["w", "write"]:
                self.read_write = "write"
            else: #TODO: Loop to get valid input, also EXCEPT HANDLING? 
                print ">>> ERROR: Invalid read/write parameters"

        if self.read_write == "write":
            self.file_length = raw_input ("File Length: ")

    def clear_params(self):
        """ Clears all system call & read/write params """
        self.file_name, self.mem_loc, self.read_write, self.file_length = None



