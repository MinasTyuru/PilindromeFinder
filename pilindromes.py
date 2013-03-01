from doctest import run_docstring_examples

def rde(fn):
    run_docstring_examples(fn, None, verbose=True)
    
class NumReader(object):
    """A class to stream out digits of a number stored in a text file.
    Text file must not contain any numerical digits that are not the number
    itself (e.g. timestamps). Newlines, spaces, etc. are allowed.

    >>> src = NumReader("pi.txt", 7)
    >>> src.read(5)
    [3, 1, 4, 1, 5]
    >>> src.read(5) #Limit reached
    [9, 2]
    """
    def __init__(self, filename, limit=1000000):
        #Max number of digits to read out
        self.limit = limit
        #Number of digits read so far
        self.digits_read = 0
        #File to read digits from
        self.file = open(filename)
        
    def read(self, n):
        """Outputs a list of the next N digits of pi.
        If not enough digits are available, returns as many as possible.
        """
        buffer = [] #Buffer for storing digits to output
        
        #While more digits needed (and limit not reached), add more digits
        while len(buffer) < n and self.digits_read < self.limit:
            #Get the next character
            char = self.file.read(1)
            #If out of characters, end search
            if char == '':
                self.file.close()
                self.file = None
                break
            #Only add numerical digits to the buffer
            if char.isdigit():
                buffer.append(int(char))
                self.digits_read += 1
            
        #Return digits
        return buffer

    @property
    def has_digits(self):
        """Report whether you still have digits left to read or not."""
        #Reached digit limit
        if self.digits_read == self.limit:
            return False
        #File closed
        if self.file is None:
            return False
        #Otherwise should be ok
        return True

def pal_length(past, future):
    """Given a list PAST and a list FUTURE, determine the length of a
    palindrome extending outwards into the past/future.

    >>> pal_length([1, 2, 3, 4], [1, 2, 3, 5])
    3
    >>> pal_length([1, 2], [1, 2, 3, 5]) #hello => eh, l, lo
    2
    >>> pal_length(['e', 'h'], ['l', 'o']) #racecar => car, e, car
    0
    >>> pal_length(['c', 'a', 'r'], ['c', 'a', 'r'])
    3
    """
    max_length = min(len(past), len(future))
    pal_length = 0
    #Look through all available characters
    for ch_i in range(max_length):
        #If palindrome broken, end
        if past[ch_i] != future[ch_i]:
            break
        #If palindrome continues, increment length counter
        pal_length += 1
    return pal_length
        
"""Plan of attack: Stream digits from a NumReader. Keep past digits, current
digit, and next digits in lists like this:
3141592 =>
Past: 4, 1, 3
Cur: 1
Next: 5, 9, 2

Cur might be None. To search for a palindrome, expand outwards on Past and
Next until you find nonmatching digits; in this case there is no palindrome
centered at 1, so it would stop immediately.
512343211
Past: 3, 2, 1, 5
Cur: 4
Next: 3, 2, 1, 1
This would expand outwards 3 times until finding 5 != 1.

We also search for palindromes with even lengths, e.g.
51233214
Past: 3, 2, 1, 5
Cur: None
Next: 3, 2, 1, 4
Expands outwards 3 times.
"""
#Source of digits of pi
source = NumReader("pi.txt")
#Old digits. Should always be length 100-200, unless there aren't enough digits.
old_d = []
#Current digit (possibly None)
cur_d = source.read(1)[0]
#Future digits. Should always be length 100-200, unless there aren't enough digits.
next_d = source.read(100)

#Keep running until out of digits
max_length = 0
max_pos = None
while source.has_digits:
    #Look for palindrome centered at current digit
    cur_length = 1 + 2 * pal_length(old_d, next_d)
    if cur_length > max_length:
        max_length = cur_length
        max_pos = source.digits_read - len(next_d)
        print("New max length " + str(cur_length) + " at " + str(max_pos))

    #Look for "even" palindrome centered at current digit
    #Shift current digit into old buffer
    old_d.insert(0, cur_d)
    cur_d = None
    cur_length = 2 * pal_length(old_d, next_d)
    if cur_length > max_length:
        max_length = cur_length
        max_pos = source.digits_read - len(next_d)
        print("New max length " + str(cur_length) + " at " + str(max_pos))

    #Pull next digit
    cur_d = next_d.pop(0)

    #Maintain buffers
    if len(old_d) > 50:
        old_d = old_d[:50]
    if len(next_d) < 50:
        next_d += source.read(50)
