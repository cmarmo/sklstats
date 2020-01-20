# An example to get skl issues using the Github GraphQL API.
# from https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad

import sys
import requests
import json

headers = {"Authorization": "Bearer YOUR API KEY"}

# A simple function to use requests.post to make the API call.
# Note the json= section.

def run_query(query, variables):
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query, 'variables': variables},
                            headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}.{}".
                         format(request.status_code, query))


## The main
def main():

  owner = sys.argv[1]
  reponame = sys.argv[2]


  # The GraphQL query (with a few aditional bits included) itself
  # defined as a multi-line string.

  firstquery = """
  query {
    repository(owner: \"""" + owner + """\", name: \"""" + reponame + """\" ) {
      issues(first: 100) {
  """

  loopquery = """
  query($issueCursor: String!) {
    repository(owner: \"""" + owner + """\", name: \"""" + reponame + """\" ) {
      issues(first: 100 after: $issueCursor) {
  """

  query = """
        edges {
          cursor
          node {
            number
            createdAt
            closedAt
            author {
              login
            }
            state
            lastEditedAt
            comments(first: 1) {
              edges {
                node {
                  author {
                    login
                  }
                  createdAt
                }
              }
            }
          }
        }
      }
    }
  }
  """

  firstquery += query 
  variables = {}

  result = run_query(firstquery, variables) # Execute the query
  templist = result["data"]["repository"]["issues"]["edges"]
  issuelist = templist

  myCursor = issuelist[-1]['cursor']

  loopquery += query

  while(len(templist)>1):

          variables = {"issueCursor": myCursor}	

          result = run_query(loopquery, variables) # Execute the query
          templist = result["data"]["repository"]["issues"]["edges"]
          issuelist += templist
          myCursor = issuelist[-1]['cursor']

  fp = open('issues.json', 'w')
  json.dump(issuelist, fp)
  fp.close()

if __name__ == "__main__":
    main()
