
try:
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    from IPython.display import clear_output
    from IPython.display import Audio, display

except ModuleNotFoundError:
    print("Module or modules not found!")
    
URL = "https://brightlinkprep.com/all-the-600-gre-words-you-must-know/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "lxml")
table = soup.find('table', id="tablepress-43")
headers = []
for i in table.find_all('th'):
 title = i.text
 headers.append(title)
df = pd.DataFrame(columns = headers)
for j in table.find_all('tr')[1:]:
 row_data = j.find_all('td')
 row = [i.text for i in row_data]
 length = len(df)
 df.loc[length] = row
df.Words = df.Words.str.capitalize()
def printquestion(wordtest,deftest, answerIndex, total):
  wordarr = np.array([x for x in wordtest])
  index = ["A. ", "B. ", "C. ", "D. ", "E. ", "F. ", "G. ", "H. ", "I. ", "J. "]
  print( str(total) + '.',deftest.loc[answerIndex].capitalize(),'\n')
  for x in zip(index, wordarr):
    print(x[0] + x[1])
  print('\n')
  return

def getAnswerIndex(deftest):
  return deftest.sample(1).index[0]

def Evaluate(wordtest, deftest, answerIndex, userInput, total, correct):
  total +=1
  if(wordtest.loc[answerIndex].lower() == userInput.lower()):
    print("Correct! \n")
    correct +=1
  else:
    print("Incorrect! \n")
  for x in wordtest.index:
    print(wordtest.loc[x], " - ", deftest.loc[x])
  print("\n")
  return total, correct

def getSample(df):
  Sample = df.sample(n = 10)
  wordtest = Sample.Words
  deftest = Sample.Meanings
  return wordtest, deftest

def exitText(total, correct):
  clear_output(wait = True)
  print("Total : ", total, "\nCorrect : ", correct)
  if(total != 0):
    print("Accuracy: ", round(correct/total*100, 2))
  print("Goodbye")


def play(total = 0,correct = 0):
  while(True):
    wordtest, deftest = getSample(df)
    answerIndex = getAnswerIndex(deftest)
    printquestion(wordtest, deftest, answerIndex, total+1)
    print("Type the correct word which matches this definition:")
    x = input()

    if(x.lower().strip() == 'exit'):
      exitText(total, correct)
      break

    total, correct = Evaluate(wordtest, deftest, answerIndex, x, total, correct)
    print("Press Enter to advance to the next question, or type Exit to exit.")
    y = input()
    if(y.lower().strip() == 'exit'):
      exitText(total, correct)
      break

    clear_output(wait = True)

play()
