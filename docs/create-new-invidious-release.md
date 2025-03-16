# How to make a new Invidious release

## Preamble

In the following document, `vX.Y.Z` is the release version, which should follow
the pattern `v<MAJOR>.<YYYY><MM><DD>.<PATCH>`

The major component is only updated on breaking changes (database migrations,
incompatible config changes). The minor component is the current UTC date.
The patch component is updated if a second release is done the same day.


## Step 0

Make sure you're synced with upstream:
```sh
git checkout master
git remote update
git pull origin master
```


## Step 1

Update CHANGELOG.md to reflect the changes made since the last release.

Each changelog entry is composed of a summary and a list of PRs (~= diff).

The summary should be simple and concise, and only reflect most important
changes, preferably sorted by impact (new features/breaking changes that the
users will see goes first, changes that affect developers/API users should go
last). Minor changes that are related to repo maintenance can be ignored.

Do not forget to list **ALL** the PRs that have been merged since the last
release, with the proper links.

Note: Maybe this should be done each time a PR is marged?


## Step 2

Commit the changes made to `CHANGELOG.md`:
```sh
git commit -S -m "Release vX.Y.Z"
```

**THEN** tag your release, like so:
```sh
git tag -as vX.Y.Z
```

Git will ask to provide a tag message. All you have to do is copy/pasting the
summary from `CHANGEMLOG.md` and adapt a the formatting as required. Do not
include the list of PRs merged.


## Step 3

Once you have checked everything, push to GitHub:
```sh
git push origin master
git push upstream vX.Y.Z
```


## Step 4

Got to GitHub to make a new release:
https://github.com/iv-org/invidious/releases/new

Select the tag your previously created, leave `target` set to `master`,
and then copy paste the text you wrote to `CHANGELOG.md` (both the summary and
the list of PRs merged since last release).

And then click "publish"!
