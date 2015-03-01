import sys

class PCB:

    def __init__(self, id_num, p_loc="ready"): 
    	self.pid = id_num
    	self.proc_loc = p_loc
        self.param_fields = ["file_name","mem_loc","rw","file_len"]
        self.params = dict.fromkeys(self.param_fields)

    def set_proc_loc(self, p_loc):
        """ Sets location of process, i.e. which queue/device it is in"""
        self.proc_loc = p_loc


    ## Methods to print out contents/properties of PCB

    def __repr__(self):
    	return "process #" + str(self.pid) 

    def __str__(self):
    	return "process #" + str(self.pid)

    def status(self):
		return "%s in %s queue" %(self, self.proc_loc)

    ## Setting/clearing system call params for pcb

    def set_syst_call_params(self):
        print "##### SET SYSTEM CALL PARAMETERS"
        # TODO: ERROR CHECKING & FORMATTING
        self.params["file_name"] = raw_input("File Name: ")
        self.params["mem_loc"] = raw_input("Starting Memory Location: ")

    def set_read_write_params(self, dev_type):
        if (dev_type.lower() == "printer"):
            self.params["rw"] = "w"
        else: 
            rw = raw_input("Read or Write?: ")
            if rw.lower() in ["r", "read"]:
                self.params["rw"] = "r"
            elif rw.lower() in ["w", "write"]:
                self.params["rw"] = "w"
            else: # TODO: Loop to get valid input, also EXCEPT HANDLING? 
                print "ERROR: Invalid read/write parameters"

        if self.params["rw"] == "w":
            self.params["file_len"] = raw_input ("File Length: ")

    def clear_params(self): # TODO: FIGURE OUT WHEN NEED TO DO THIS
        """ Clears all system call & read/write params """
        for p in self.params:
            self.params[p] = None



