number: the issue number on github
createdAt: the creation date
closedAt: when the issue has been closed (null if OPEN)
author: { login: the github login of the author }
reviews(last:50) { totalCount: the total number of the reviews
                   state: the state of the reviews (PENDING, COMMENTED, APPROVED, CHANGES_REQUESTED, DISMISSED) for each review }
state: the state of the PR (OPEN, CLOSED, MERGED)
lastEditedAt: the time of the last edition
