# An example to get skl issues using the Github GraphQL API.
# from https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad

import requests

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

        
# The GraphQL query (with a few aditional bits included) itself
# defined as a multi-line string.       

query = """
query($issueCursor: String!) {
  repository(owner: "scikit-learn", name: "scikit-learn") {
    issues(last: 10 after: $issueCursor) {
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
        }
      }
    }
  }
}
"""

variables = {"issueCursor": myCursor}	

result = run_query(query, variables) # Execute the query
