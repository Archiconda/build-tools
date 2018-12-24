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
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import argparse

from time import sleep

def create_aarch64_branch(repo, aarch64_default=True):
    source_branch = 'master'
    target_branch = 'aarch64'
    print(f'Creating branch "{target_branch}" from "{source_branch}"')
    try:
        repo.get_branch(target_branch)
    except GithubException as e:
        if e.status == 404:
            sb = repo.get_branch(source_branch)
            repo.create_git_ref(ref='refs/heads/' + target_branch, sha=sb.commit.sha)
            repo.get_branch(target_branch)
    if aarch64_default:
        print(f"setting fork's default branch to {target_branch}")
        repo.edit(default_branch=target_branch)

def fork_repo(gh, *, org, package_name, source_org):
    forked_repo = gh.get_repo(f'{org.login}/{package_name}-feedstock')
    print('Checking to see if repository exists on Github')
    try:
        # Check that the repo actually exists
        # Printing the name or any property of the repo issues this check
        print(f'{forked_repo.full_name} already exists, not forking it again.')
        return forked_repo
    except UnknownObjectException:
        pass
    
    # Else, now try to fork it from the origin
    feedstock_repo = gh.get_repo(f'{source_org}/{package_name}-feedstock')
    try:
        org.create_fork(feedstock_repo)
    except UnknownObjectException as e:
        if e.status == 404:
            raise RuntimeError(f'Repository not found: {e.data["message"]}')
        else:
            raise e
                               
def get_github_token(token_dir):
    try:
        github_token_filename = (token_dir / 'github.token').expanduser()
        with open(github_token_filename, 'r') as fh:
            github_token = fh.read().strip()
        if not github_token:
            raise ValueError()
        return github_token
    except (IOError, ValueError):
        raise RuntimeError(
            'No github token found for archiconda on Github. \n'
            'Go to https://github.com/settings/tokens/new and generate\n'
            f'a token with repo access. Put it in {github_token_filename}')

def main(package_names, source_org, org_name, token_dir, aarch64_default):
    print(f'Will fork the following feedstocks {package_names}')
    print(f'from: {source_org}')
    print(f'to: {org_name}')
    print(f'using tokens found in: {token_dir}')
    github_token = get_github_token(token_dir)

    gh = Github(github_token)
    org = gh.get_user()
    if org.login != org_name:
        org = gh.get_organization(org_name)

    for package_name in package_names:
        fork_repo(gh, org=org, package_name=package_name, source_org=source_org)
        feedstock_name = f'{package_name}-feedstock'
        forked_repo = gh.get_repo(f'{org.login}/{feedstock_name}')
        create_aarch64_branch(forked_repo, aarch64_default=aarch64_default)
    print('Befeore continuing, please enable the repositories on Shippable')
    print('Go to ')
    print(f'https://app.shippable.com/subs/github/{org_name}/enable')
    print('And enable the repositories:')
    print(f'{[p + "-feedstock" for p in package_names]}')
    input('Press enter to continue...')
          
    for package_name in package_names:
        feedstock_name = f'{package_name}-feedstock'

        repo = Repo.clone_from(forked_repo.ssh_url, f'{feedstock_name}')
        repo.git.checkout('-B', 'aarch64', 'origin/aarch64')
        feedstock_repo = gh.get_repo(f'{source_org}/{package_name}-feedstock')
        repo.create_remote('upstream', feedstock_repo.ssh_url)
        repo.remotes['upstream'].pull('master')
        with open(f'{feedstock_name}/conda-forge.yml') as f:
            y = yaml.load(f)
        y['aarch64'] = True
        with open(f'{feedstock_name}/conda-forge.yml', 'w') as f:
            f.write(yaml.dump(y))
        repo.index.add(['conda-forge.yml'])
        repo.index.commit('Added aarch64 to the conda-forge.yml')
        origin = repo.remotes['origin']
        print('Added the tag ``aarch64: true`` to ``conda-forge.yml``. The repo is now ready to get rerendered.')
        shippable_filename = render_shippable(f'{package_name}-feedstock')
        repo.index.add([shippable_filename.name])
        repo.index.commit('Added shippable.yml')
        origin.push()


def render_shippable(forge_dir):
    content_dir = os.path.abspath(os.path.dirname(__file__))
    env = Environment(loader=FileSystemLoader([content_dir]))
    template = env.get_template('shippable.yml.tmpl')

    p = Path(forge_dir) / '.ci_support'
    config = {'configs': [(f.stem, None) 
                          for f in p.glob('linux*') 
                          if 'gcc' not in f.stem]}
    shippable_config_filename = Path(forge_dir) / 'shippable.yml'
    with open(shippable_config_filename, 'w') as f:
        f.write(template.render(config))
    return shippable_config_filename



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_org', type=str, default='conda-forge',
                        help='The source organization to clone from')
    parser.add_argument('--org', type=str, default='archiconda',
                        help='The destimation organization (or user) where to fork to.')
    parser.add_argument('--token-dir', type=Path, default=Path('~/.archiconda'),
                        help='The directory where to find the tokens.')
    parser.add_argument('package_names', nargs='+', type=str,
                        help='packages to fork and create')
    parser.add_argument('--no-change-master-branch', 
                        dest='aarch64_default', action='store_false',
                        help='If provided, the master branch of the repo will be left unchanged.')    
    parser.set_defaults(aarch64_default=True)
    args = parser.parse_args()
    package_names = args.package_names
    source_org = args.source_org
    org_name = args.org
    token_dir = args.token_dir
    aarch64_default = args.aarch64_default
    main(package_names, source_org, org_name, token_dir, aarch64_default)
