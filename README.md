## Why this repo

See https://opensource.guide/metrics/#maintainer-activity

## Notes on data retrieving 

~~_Github API v3_

~~List all the issues (curl -i if header needed)

~~See the [issue parameters](https://developer.github.com/v3/issues/#parameters)
```
curl https://api.github.com/repos/scikit-learn/scikit-learn/issues/events
```

~~List all the PRs

~~See the [PR parameters](https://developer.github.com/v3/pulls/#parameters)
```
curl https://api.github.com/repos/scikit-learn/scikit-learn/pulls
```


_[Github API v4](https://developer.github.com/v4/)_

From the [Explorer interface](https://developer.github.com/v4/explorer/)

Retrieve the last hundred Pull Requests

See the [GraphQL Pull Request schema](https://developer.github.com/v4/object/pullrequest/)

Retrieve the last hundred Issues

See the [GraphQL Issue schema](https://developer.github.com/v4/object/issue/)
