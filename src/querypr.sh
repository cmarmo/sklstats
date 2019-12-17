curl -H "Authorization: bearer token" -X POST -d " \
 { \
   \"query\": \"query { \
    repository(owner:\\\"scikit-learn\\\", name:\\\"scikit-learn\\\") { \
    pullRequests(last: 100) { \
      edges { \
        node { \
          number \
          createdAt \
          closedAt \
          author { \
            login \
            } \
          } \
        } \
      } \
    } \
  }\" \
 } \
" https://api.github.com/graphql
