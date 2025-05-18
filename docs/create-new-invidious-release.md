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

* Update version in `shard.yml`.
* Update `CHANGELOG.md` to reflect the changes made since the last release.

Each changelog entry is composed of a summary and a list of PRs.

The summary should be simple and concise, and only reflect most important
changes, preferably sorted by impact (new features/breaking changes that the
users will see goes first, changes that affect developers/API users should go
last). Minor changes that are related to repo maintenance can be ignored.

Do not forget to list **ALL** the PRs that have been merged since the last
release, with the proper links.

Note: Maybe this should be done each time a PR is merged?


## Step 2

Commit the changes made in step 1:
```sh
git add CHANGELOG.md shard.yml
git commit -S -m "Release vX.Y.Z"
```

**THEN** tag your release, like so:
```sh
git tag -as vX.Y.Z
```

Git will ask to provide a tag annotation. All you have to do is copy/pasting
the summary from `CHANGELOG.md` and adapt the formatting as required. Do not
include the list of PRs merged.

??? warning Amending your release commit

    If for some reason you need to amend your release commit (e.g you made a typo
    in the changelog), **make sure to retag afterwards!**
    
    Amending a commit will change its hash, but the tag will remain attached to
    the previous (now dangling) commit.

    Here's is how to amend your changes and retag:
    ```sh
    # Amend changes
    git commit --amend --no-edit

    # Retag while reusing the previous tag's annotation
    git tag -l --format='%(contents)' vX.Y.Z > tag_msg.tmp
    git tag -F tag_msg.tmp -as -f vX.Y.Z
    rm tag_msg.tmp
    ```

    Note: **DO NOT** retag if you already pushed you changes. If you made a
    mistake (it happens to everybody), just create a new release.


## Step 3

Check that the release commit is properly tagged:
```sh
# Either with git log (colorful, also shows the branches/tags on the remote)
git log --pretty=oneline -3

# Or using git tag (only shows the tag(s) pointing to HEAD)
git tag --points-at HEAD
```

If not, go back to step 2.


## Step 4

Edit `shard.yml` again to add `-dev` to the version string. If you didn't already, also add a "future version" title line to the
top of the changelog under which future PR will be listed.

[Example commit](https://github.com/iv-org/invidious/commit/98926047586154269bb269d01e3e52e60e044035)

Commit your changes:
```
git add CHANGELOG.md shard.yml
git commit -S -m "Prepare for next release"
```

# Step 5

Once you have checked everything, push to GitHub:
```sh
git push origin master
git push origin vX.Y.Z
```


## Step 6

Got to GitHub to make a new release:
https://github.com/iv-org/invidious/releases/new

Select the tag your previously created, leave `target` set to `master`,
and then copy paste the text you wrote to `CHANGELOG.md` (both the summary and
the list of PRs merged since last release).

And then click "publish"!
