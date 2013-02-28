class Pi_Reader(object):
    """A class to stream out digits of pi.
    """
    def __init__(self):
        #Buffer to store digits of pi
        self.digs = []
        #File to read digits from
        self.pi_file = open("pi.txt")
        #Whether or not there are still digits
        self.has_digits = True
        
    def get_digits(self, n):
        """Outputs a list of the next N digits of pi.
        If not enough digits are available, returns as many as possible.
        """
        #While more digits needed, add more
        while len(self.digs) < n and self.pi_file.:
            self.read()
            
        #Get required digits
        n_digs = self.digs[:n]
        #Remove digits from buffer
        self.digs = self.digs[n:]
        #Return digits
        return n_digs

    def read(self):
        """Reads a line from the pi file and adds it to the digit buffer.
        """
        line = self.pi_file.readline()
        
        digits = []
        
        #Extract all digits from line
        for char in line:
            #If digit, add to list of digits
            if char.isdigit():
                digits.append(int(char))
            #Ignore newlines, spaces, etc.
                
        #Add digits to buffer
        self.digs += digits


#Source of digits of pi
source = Pi_Reader()
old_d = []
cur_d = source.read(1)[0]
next_d = source.read(100)
while True:
