curl -H "Authorization: bearer token" -X POST -d " \
 { \
   \"query\": \"query { \
    repository(owner:\\\"scikit-learn\\\", name:\\\"scikit-learn\\\") { \
    issues(last: 100) { \
      edges { \
        node { \
          number \
          createdAt \
          closedAt \
          author { \
            login \
            } \
          state \
          lastEditedAt \
          } \
        } \
      } \
    } \
  }\" \
 } \
" https://api.github.com/graphql
