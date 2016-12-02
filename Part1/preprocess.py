import re
from string import digits

data = []
temp = []
# http://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def preprocess_data(i):
    temp[:] = []
    f = open(i, 'r')
    x = f.read()
    # x = f.read()
    f.close()
    x = cleanhtml(x)
    x = x.split()


    for i in x:
        temp.append(re.findall(r"\b\w+\b",i))

    data = [item for sublist in temp for item in sublist]

    data = [word.lower() for word in data]

    # https://github.com/Alir3z4/stop-words/blob/master/english.txt
    g = open("english.txt",'r')
    stopWords = g.read().split('\n')
    data = ' '.join([word for word in data if word not in stopWords])

    char_Remove = "[!@#$).\_%^&*()#@|-](){}+\n:<>?;,='"
    char_Remove1 = '"'
    data =  data.translate(None, char_Remove)
    data =  data.translate(None, char_Remove1)
    data =  data.translate(None,digits)

    # Remove url links
    # data = re.sub(r'http\S+', '', data)

    data = data.split()
    data = data[1:]

    return data




