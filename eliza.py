#----------------------------------------------------------------------
# eliza.py
#
#Rough implementation of eliza done as a college project.
#CSI/ACM rocks.
#----------------------------------------------------------------------
import string
import re
import random
from dict import *

class eliza:
  def __init__(self):
    #Creating a re object using the data dictionary present.

    self.keys = map(lambda x:re.compile(x[0], re.IGNORECASE),gPats)
    self.values = map(lambda x:x[1],gPats)

  #----------------------------------------------------------------------
  # translate: take a string, replace any words found in dict.keys()
  # with the corresponding dict.values()
  #----------------------------------------------------------------------
  def translate(self,str,dict):
    words = string.split(string.lower(str))
    #keys = dict.keys();
    for i in range(0,len(words)):
      if words[i] in dict.keys():
        words[i] = dict[words[i]]
    return string.join(words)

  #----------------------------------------------------------------------
  #  Choice: giving skewed probability to each answer in self.values
  #  Probability is given exponentially
  #----------------------------------------------------------------------
  def choice(self, i):
    rand = random.randint(1,100)
    #print rand
    j = -1
    for str in self.values[i]:
      j+=1
      if rand > 100/(2**(j+1)):
        return self.values[i][j]
    return self.values[i][0]

  #----------------------------------------------------------------------
  #  respond: take a string, a set of regexps, and a corresponding
  #    set of response lists; find a match, and return a randomly
  #    chosen response from the corresponding list.
  #----------------------------------------------------------------------
  def respond(self,str):
    # find a match among keys
    for i in range(0,len(self.keys)):
      match = self.keys[i].match(str)
      if match:
        # found a match ... stuff with corresponding value
        # chosen randomly from among the available options
        #resp = random.choice(self.values[i])
        resp = self.choice(i)
        # we've got a response... stuff in reflected text where indicated
        pos = string.find(resp,'%')
        #print (pos)
        while pos > -1:
          num = string.atoi(resp[pos+1:pos+2])
          #print (resp)
          resp = resp[:pos] + \
            self.translate(match.group(num),gReflections) + \
            resp[pos+2:]
          pos = string.find(resp,'%')
          #pos = -2
        # fix munged punctuation at the end
        if resp[-2:] == '?.': resp = resp[:-2] + '.'
        if resp[-2:] == '??': resp = resp[:-2] + '?'
        return resp

#----------------------------------------------------------------------
#  command_interface/UI
#----------------------------------------------------------------------
def command_interface():
  print "Fuggachio\n---------"
  print "Talk to the program by typing in plain English, using normal upper"
  print 'and lower-case letters and punctuation.  Enter "quit" when done.'
  print '='*72
  print "Hello.  How are you feeling today?"
  s = ""
  therapist = eliza();
  while s != "quit":
    try: s = raw_input(">")
    except EOFError:
      s = "quit"
      print s
    while s[-1] in "!.#@$^&*()": 
      try: s = s[:-1]
      except IndexError:
        print "English  please!!"
        s = "quit"
    print therapist.respond(s)


if __name__ == "__main__":
  command_interface()