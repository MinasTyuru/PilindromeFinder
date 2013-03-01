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

def pal_str(center, branch):
    """Convert a palindrome as a central element (possibly None) and a list to
    a string and return it.

    >>> pal_to_int(1, [2, 3, 4])
    4321234
    >>> pal_to_int(None, [2, 3, 4])
    432234
    """
    #Get left branch
    pal = branch[::-1]
    #Middle
    if center:
        pal.append(center)
    #Right branch
    pal += branch

    pal = [str(dig) for dig in pal]
    return ''.join(pal)
        

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

def search_palindromes(src_file, min_len):
    """Searches for palindromes in the file with filename SRC_FILE of at least
    length MIN_LEN. Returns a list of the palindromes found as
    (palindrome, position).
    """
    #Get digit source
    source = NumReader(src_file)
    #Old digits. Should always be length 100-200, unless there aren't enough digits.
    old_d = []
    #Current digit (possibly None)
    cur_d = source.read(1)[0]
    #Future digits. Should always be length 100-200, unless there aren't enough digits.
    next_d = source.read(100)
    #List of accumulated palindromes as strings
    pals = []

    #Keep running until out of digits
    while source.has_digits:
        #Look for palindrome centered at current digit
        branch_len = pal_length(old_d, next_d)
        cur_length = 1 + 2 * branch_len
        #If long enough, add to list
        if cur_length >= min_len:
            p = pal_str(cur_d, old_d[:branch_len])
            pals.append((p, source.digits_read - len(next_d)))

        #Look for "even" palindrome centered at current digit
        #Shift current digit into old buffer
        old_d.insert(0, cur_d)
        cur_d = None
        branch_len = pal_length(old_d, next_d)
        cur_length = 2 * branch_len
        #If long enough, add to list
        if cur_length >= min_len:
            p = pal_str(cur_d, old_d[:branch_len])
            pals.append((p, source.digits_read - len(next_d)))

        #Pull next digit
        cur_d = next_d.pop(0)

        #Maintain buffers
        if len(old_d) > 50:
            old_d = old_d[:50]
        if len(next_d) < 50:
            next_d += source.read(50)
    return pals

"""Process to find longest palindrome in the first million digits of pi:

Note: I knew 10 was a good minimum length because I found the answer in a
previous version of this code, which just searched for the maximum instead of
returning a list.
>>> pi_pals = search_palindromes('pi.txt', 10)
>>> pi_pals.sort(key = lambda pal_tup: len(pal_tup[0]))
>>> pi_pals
[('0136776310', 16066), ('5783993875', 397922), ('0045445400', 506352), ('6282662826', 552087), ('3517997153', 593129), ('8890770988', 693442), ('7046006407', 760405), ('1112552111', 831549), ('7264994627', 842171), ('21348884312', 247152), ('49612121694', 268803), ('28112721182', 307753), ('53850405835', 370727), ('04778787740', 619574), ('09577577590', 745892), ('84995859948', 913585), ('41428782414', 939282), ('450197791054', 273846), ('9475082805749', 879333)]
>>> pi_pals[-1]
('9475082805749', 879333)

So the longest palindrome in the first million digits of pi is 9475082805749
centered at position 879333.

Process to find longest palindrome in both pi and e:

Note: The number 7 was discovered by experimentation, by increasing the
number until only a few remained.

>>> pi_pals = search_palindromes('pi.txt', 7)
>>> pi_set = set()
>>> for pal, pos in pi_pals:
	pi_set.add(pal)
>>> e_pals = search_palindromes('e.txt', 7)
>>> both_pals = []
>>> for pal, pos in e_pals:
	if pal in pi_set:
		both_pals.append(pal)
>>> both_pals.sort(key = lambda pal: len(pal))
>>> both_pals
['369963', '429924', '790097', '956659', '839938', '606606', '493394', '602206', '606606', '768867', '696696', '2404042', '9973799', '6848486', '1532351', '4272724', '6695966', '5163615', '6254526', '8285828', '2823282', '6443446', '0429240', '5883885', '2475742', '9225229', '1177711', '4696964', '2891982', '2978792', '5893985', '0715170', '0338330', '2199912', '4152514', '4149414', '6064606', '7511157', '8791978', '9023209', '0187810', '8964698', '0902090', '7299927', '4712174', '0158510', '4046404', '8935398', '8653568', '4965694', '2271722', '7826287', '5067605', '0902090', '8255528', '2488842', '0492940', '3781873', '3301033', '6109016', '1624261', '1596951', '5718175', '6172716', '1973791', '4263624', '7412147', '8831388', '75711757']
>>> both_pals[-1]
'75711757'
>>> [p for p in pi_pals if p[0]=='75711757']
[('75711757', 44791)]
>>> [p for p in e_pals if p[0]=='75711757']
[('75711757', 296628)]

So the longest palindrome in both e and pi is 75711757, centered at position 44791 in pi, and 296628 in e.
"""
