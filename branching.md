# SMIRK Git Branching Model

Our branching model closely resembles the model used by Dr. Melanie E. Rose's [Biological Compuation Lab](https://github.com/BCLab-UNM) which in turn is based on Vincent Driessen's "[A successful Git branching model](http://nvie.com/posts/a-successful-git-branching-model/)."

External pull requests are welcome. Pull requests adding new features shall target the `develop` branch. Critical fixes, on the other hand, shall target `master` directly.  

## Overall description

The SMIRK branching model uses two *infinite* branches (`master` and `develop`) and two types of supporting branches (`feature` and `hotfix` branches). Supporting branches shall be *ephemeral*, i.e., they should only last as long as the feature or hotfix itself is in development. Once completed, they shall be merged back into one of the infitine branches and/or discarded.

- `master` - the main branch where the source code of HEAD always reflects a production-ready state.
- `develop` - where the main development is reflected. Merges into `master`.
- `feature-x` - used to develop new features for the upcoming release. Merges into `develop`.
-	`hotfix-x` - used when it is necessary to act immediately upon an undesired state of a live production version. Merges into `master`.

The following examples describe how to work according to the SMIRK branching model. In the examples, `feature-foo` or `hotfix-foo` should be replaced with a short phrase describing the feature or hotfix.

## Feature branches

Feature branches are used to implement new enhancements for upcoming releases. Once the feature is completed, it must be merged back into the `master` branch and/or discarded.

Consider an example in which we to implement a new feature called `feature-foo`:

Begin by switching to a new branch `feature-foo`, branching off of `master`:

```
$ git checkout -b feature-foo master
```

You should use `feature-foo` to implement and commit all changes required for your new feature.

- Make many small commits so that the history of development for your feature branch is clear and so that it is easy to pinpoint and edit or cherry-pick specific commits if necessary.
- Avoid merging your feature branch with other feature branches being developed in parallel. This *MIGHT* cause a lot of problems down the line when doing a pull request to merge your feature back into the master branch.

When your feature is complete, push it to the remote repo to prepare for a pull request.

```
$ git push -u origin feature-foo
```

Next, you will want to [create a pull request](https://help.github.com/articles/creating-a-pull-request/), so that the repository administrator can review and merge your feature. You will want to create the following pull request:

* base: `master`, compare: `feature-foo`

Finally, after your pull request is accepted, clean up your local repositories by deleting your local feature branch:

```
$ git branch -d foo
```

The repository administrators are responsible for deleting the remote copy of the feature branch.

All pull requests must be reviewed before they can be merged into the `master` branch. Reviewers may ask questions or make suggestions for edits and improvements before your feature can be merged. If your feature branch pull request is not accepted, make the necessary adjustments or fixes as indicated by the repository administrator and redo the pull request.

## Hotfix branches

Hotfix branches are used to implement critical bug fixes in the *production version* of your code, i.e., code that is currently being used in released versions of SMIRK. As such, they should always originate from the `master` branch.

Now, consider an example in which we discover a critical bug in the current production release of your code:
Begin by switching to a new branch `hotfix-foo`, branching off of `master`:

```
$ git checkout -b hotfix-foo master
```

Implement your bug fix in `hotfix-foo`, commit your changes, then push your hotfix branch back into the remote repository to prepare it for a pull request:

- Make many small commits so that the history of development for your hotfix branch is clear and so that it is easy to pinpoint and edit or cherry-pick specific commits if necessary.

```
$ git push -u origin hotfix-foo
```

Next, you will want to [create a pull request](https://help.github.com/articles/creating-a-pull-request/), so that the repository administrator can review and merge your hotfix:

* base: `master`, compare: `hotfix-foo`

Finally, after your pull request is accepted, clean up your local repositories by deleting your hotfix branch:

```
$ git branch -d hotfix-foo
```

The repository administrators are responsible for deleting the remote copy of the hotfix branch and updating the version tag for the `master` branch.

All pull requests must be reviewed before they can be merged into the `master` branch. Reviewers may ask questions or make suggestions for edits and improvements before your feature can be merged. If your feature branch pull request is not accepted, make the necessary adjustments or fixes as indicated by the repository administrator and redo the pull request.
