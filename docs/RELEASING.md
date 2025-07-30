# Releasing

In the `main` branch, after PRs have been merged:

1. Update the changelog using [`keepachangelog-manager`](https://pypi.org/project/keepachangelog-manager/)
    - `changelog-manager release` - Releases all unreleased changes in changelog
    - `git add CHANGELOG.md && git commit -m "Update changelog for version <version>"`
2. Bump version
    - `uv bump <major/minor/patch>`
3. Create version tag
    - `git tag -a <version> -m "<version>"`
4. Push changes and tags
    - `git push --follow-tags`
