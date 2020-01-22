import sys
import json
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from datetime import timedelta


## The main
def main():

  filename = sys.argv[1]

  with open(filename) as f:
    istr = f.read()

  ijson = json.loads(istr)
  ntot = len(ijson)

  number = [ ijson[i]["node"]["number"] for i in range(0, ntot) ]
  creatDate = [ ijson[i]["node"]["createdAt"] for i in range(0, ntot) ]
  closDate = [ ijson[i]["node"]["closedAt"] for i in range(0, ntot) ]
  state = [ ijson[i]["node"]["state"] for i in range(0, ntot) ]
  author = []
  firstcommentedBy = []
  firstcommentedAt = []
  for i in range(0, ntot):
    auth = ijson[i]["node"]["author"]
    if (auth != None):
        author.append(auth["login"])
    else:
        author.append("")
    comments = ijson[i]["node"]["comments"]["edges"]
    if (len(comments) > 0):
        if (comments[0]["node"]["author"] != None):
            firstcommentedBy.append(comments[0]["node"]["author"]["login"])
        else:
            firstcommentedBy.append("")
        firstcommentedAt.append(comments[0]["node"]["createdAt"])
    else:    
        firstcommentedBy.append("")
        firstcommentedAt.append("")


  crdate = []
  cldate = []
  answdate = []
  duration = []
  reaction = []
  delta = timedelta(days=1)

  for i in range(0, ntot):
    crdate.append(pd.to_datetime(creatDate[i], format='%Y-%m-%dT%H:%M:%SZ'))
    cldate.append(pd.to_datetime(closDate[i], format='%Y-%m-%dT%H:%M:%SZ'))
    if closDate[i] != None:
        duration.append(pd.Timedelta.to_pytimedelta(cldate[i] -
                                                    crdate[i]) / delta )
    else:
        duration.append(None)
    try:
        answdate.append(pd.to_datetime(firstcommentedAt[i],
                                       format='%Y-%m-%dT%H:%M:%SZ'))
        reaction.append(pd.Timedelta.to_pytimedelta(answdate[i] -
                                                    crdate[i]) / delta )
    except:
        answdate.append(None)
        reaction.append(None)

  idata = { "Number" : number, "Author" : author, "CreatedAt" : crdate,
            "ClosedAt" : cldate,
            "Duration" : duration, "FcommAuthor" : firstcommentedBy,
            "FcommDate" : answdate, "AnswerTime" : reaction }
  idf = pd.DataFrame(idata)
  yidf = idf.groupby([idf['CreatedAt'].dt.to_period('Y')]).count().unstack()

  fig = plt.figure()
  n_na = idf["Duration"].count()
  perc = 100 * (ntot - n_na) / ntot 
  sns.distplot(idf["Duration"].dropna(), bins=100, kde=False);
  plt.title("Issue Duration")
  plt.xlabel("days")
  plt.yscale("log")
  percstr = "{0:.2f}% of open issues".format(perc)
  plt.text(1000, 1000, percstr)
  plt.show()

  fig = plt.figure()
  n_na = idf["AnswerTime"].count()
  perc = 100 * (ntot - n_na) / ntot 
  sns.distplot(idf["AnswerTime"].dropna(), kde=False);
  plt.title("Issue First answer")
  plt.xlabel("days")
  plt.yscale("log")
  percstr = "{0:.2f}% of non-answered issues".format(perc)
  plt.text(1000, 1000, percstr)
  plt.show()
  
  gidf = idf.groupby([idf['CreatedAt'].dt.to_period('M')]).count().unstack()
  gidf['CreatedAt'].plot(kind='bar', color='red')
  gidf['ClosedAt'].plot(kind='bar', color='blue')

  plt.show()
  #fig.savefig('plot.png')

if __name__ == "__main__":
    main()
