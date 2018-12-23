#!/usr/bin/env python3
# To get the user token
import os

# To interact with github
import github
from github import Github
from github.GithubException import GithubException
from github.Organization import Organization
from github import UnknownObjectException

# To modify the git repository using sane tools
from git import Repo
import yaml


def main():
    try:
        with open(os.path.expanduser('~/.archiconda/github.token'), 'r') as fh:
            github_token = fh.read().strip()
        if not github_token:
            raise ValueError()
    except (IOError, ValueError):
        print('No github token found for archiconda on Github. \n'
              'Go to https://github.com/settings/tokens/new and generate\n'
              'a token with repo access. Put it in ~/.archiconda/github.token')

    gh = Github(github_token)

    org_name = 'archiconda'
    org = gh.get_organization(org_name)

    # TODO: Make this a loop so that we can fork multiple packages at once
    source_org = 'conda-forge'
    package_name = 'pip'
    feedstock_repo = gh.get_repo(f'{source_org}/{package_name}-feedstock')
    try:
        org.create_fork(feedstock_repo)
        print('Repository already found. Aborting')
        return
    except UnknownObjectException as e:
        if e.status == 404:
            raise RuntimeError(f'Repository not found: {e.data["message"]}')
        else:
            raise e

    forked_repo = gh.get_repo(f'{org.login}/{package_name}-feedstock')

    source_branch = 'master'
    target_branch = 'aarch64'
    print(f'Creating branch "{target_branch}" from "{source_branch}"')
    try:
        forked_repo.get_branch(target_branch)
    except GithubException as e:
        if e.status == 404:
            sb = forked_repo.get_branch(source_branch)
            forked_repo.create_git_ref(ref='refs/heads/' + target_branch, sha=sb.commit.sha)
            forked_repo.get_branch(target_branch)

    print(f"setting fork's default branch to {target_branch}")
    forked_repo.edit(default_branch=target_branch)

    r = Repo.clone_from(forked_repo.ssh_url, f'{package_name}-feedstock')
    with open(f'{package_name}-feedstock/conda-forge.yml') as f:
        y = yaml.load(f)
    y['aarch64'] = True
    with open(f'{package_name}-feedstock/conda-forge.yml', 'w') as f:
        f.write(yaml.dump(y))
    r.index.add(['conda-forge.yml'])
    r.index.commit('Added aarch64 to the conda-forge.yml')
    origin = r.remote()
    origin.push()
    print('Added the tag ``aarch64: true`` to ``conda-forge.yml``. The repo is now ready to get rerendered.')


if __name__ == '__main__':
    main()
