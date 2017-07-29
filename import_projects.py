#!/usr/bin/env python
"""Import Google Cloud Platform projects into an organization."""

import argparse
import re
import sys

from lib.google import Google


def add_project_to_org(admin, project):
    """Add the project to the organization."""
    output = []
    project_id = project['projectId']

    body = project.copy()
    del body['bindings']
    del body['google']
    del body['owner']

    body['parent'] = {
        'type': 'organization',
        'id': admin.organization_id
    }

    params = {
        'projectId': project_id,
        'body': body,
    }

    # connect as service account
    sa = Google()
    sa.auth(service_account_file='serviceaccount.json')

    try:
        sa.crm.projects().update(**params).execute()
        text = '      + added project to organization %s.' % (
            admin.organization_id,
        )
        output.append(text)

    except Exception as e:
        print 'ERROR adding project %s to organization %s!' % (
            project_id,
            admin.organization_id,
        )
        print e

    return output


def add_serviceaccount_owner(admin, project_id, project):
    """Add our service account as an owner on the project."""
    sa_email = admin.credentials.service_account_email

    newbindings = []
    update = False

    for b in project['bindings']:
        user = 'serviceAccount:%s' % (sa_email)
        if b['role'] == 'roles/owner' and user not in b['members']:
            b['members'].append(user)
            update = True
        newbindings.append(b)

    body = {
        'policy': {
            'bindings': newbindings
        }
    }
    params = {
        'resource': project_id,
        'body': body,
    }

    output = []
    if update:
        g = project['google']

        try:
            g.crm.projects().setIamPolicy(**params).execute()
            text = '      + added %s as project owner.' % (
                sa_email
            )
            output.append(text)

        except Exception as e:
            print 'ERROR: Failed to add service account to %s!' % (
                project_id
            )
            print e

    return output


def display_projects(projects):
    """Display the list of projects to import."""
    if projects:
        print '\nFound %s projects to import:' % (len(projects))
        for project_id in projects:
            owner = projects[project_id]['owner']
            print '   * %s (%s)' % (project_id, owner)


def get_domain_users(admin):
    """Return all users in the domain."""
    # get users as superadmin
    print 'Retrieving users from Google Admin SDK Directory API...'
    users = admin.get_users()
    print 'Found %s users in domain.' % (len(users))
    return users


def get_args():
    """Return the arguments from argparse."""
    parser = argparse.ArgumentParser()
    parser.add_argument('superadmin')
    return parser.parse_args()


def get_domain_projects(users):
    """Return a dict of all domain projects that have no parent."""
    domain_projects = {}

    # scan all users and get all their projects
    print '\nScanning all users for projects without a parent...'
    for user in users:
        email = user['primaryEmail']

        # authenticate as the user
        g = Google()
        g.auth(
            service_account_file='serviceaccount.json',
            sub_account=email,
        )

        # retrieve the user's projects
        try:
            projects = g.get_projects()
        except Exception as e:
            print 'ERROR retrieving %s: %s' % (
                email, e
            )
            continue

        # scan the projects
        user_projects = scan_user_projects(g, email, projects)
        domain_projects.update(user_projects)

    return domain_projects


def get_organization_id(admin):
    """Return the organization_id based on the super admin email."""
    organization_id = None

    # get list of organizations
    organizations = admin.get_organizations()

    # find the correct organization
    for o in organizations:
        domain = o['displayName']
        if domain == admin.domain:
            name = o['name']
            organization_id = name.replace('organizations/', '')

            print 'Organization: %s [%s] (customer: %s)\n' % (
                domain,
                organization_id,
                o['owner']['directoryCustomerId'],
            )

    return organization_id


def move_projects(admin, projects):
    """Update and move projects into the organization."""
    for project_id in sorted(projects):
        project = projects[project_id]

        # add service account as project owner
        output = add_serviceaccount_owner(admin, project_id, project)

        # add project to organization
        output += add_project_to_org(admin, project)

        if output:
            print '   * %s:' % (project_id)
            print '\n'.join(output)
            print


def scan_user_projects(g, email, projects):
    """Return the list of projects to import."""
    user_projects = {}

    output = []
    for p in sorted(projects, key=lambda x: x['name']):

        # skip projects that are not active
        if p['lifecycleState'] != 'ACTIVE':
            continue

        # look for projects that have no parent
        if 'parent' not in p or not p['parent']:
            project_id = p['projectId']
            params = {
                'resource': project_id,
                'body': {},
            }

            # retrieve the iam policy for the project
            policy = g.crm.projects().getIamPolicy(**params).execute()

            owner = None

            # scan each of the bindings to see if user is owner
            bindings = policy.get('bindings', [])
            for b in bindings:

                # skip bindings other than owner
                if b['role'] != 'roles/owner':
                    continue

                # see if user is one of the owners
                if 'user:%s' % (email) in b['members']:
                    owner = email

            # skip projects where the user is not the owner
            if not owner:
                continue

            # create some text to output about the user's project
            text = '    * %s: %s [%s] (%s)' % (
                p['name'],
                p['projectId'],
                p['projectNumber'],
                p['lifecycleState'],
            )
            output.append(text)

            # add bindings, google auth and owner to the project data
            p['bindings'] = bindings
            p['google'] = g
            p['owner'] = email

            # add project to list of projects to import
            user_projects[project_id] = p

    # display the output for this user
    if output:
        print '  %s:' % (email)
        print '\n'.join(output)

    return user_projects


def main():
    """Main function."""
    # get arguments
    args = get_args()

    # create google class object
    admin = Google(superadmin=args.superadmin)

    # authenticate with the service account
    admin.auth(
        service_account_file='serviceaccount.json',
        sub_account=args.superadmin,
    )

    # get domain users
    users = get_domain_users(admin)

    # get domain-owned projects that have no parent
    projects = get_domain_projects(users)

    # exit if there are no projects to import
    if not projects:
        sys.exit(0)

    # display the list of all projects we can import
    display_projects(projects)

    # ask if we are sure we want to continue
    print '\nPreparing to move %s projects into org: %s...' % (
        len(projects),
        admin.domain,
    )

    prompt = "   ---> Are you sure you want to continue? [y/N]: "
    confirm = raw_input(prompt)

    # continue if Yes or yes or Y or y
    if not re.search('y|Y', confirm):
        print 'Exiting.'
        sys.exit(1)
    print

    # get the oranization ID based on the super admin email
    admin.organization_id = get_organization_id(admin)

    # fail if the organization_id is not set
    if not admin.organization_id:
        print 'ERORR: organization_id not found!'
        sys.exit(1)

    # move projects into the organization
    move_projects(admin, projects)


if __name__ == "__main__":
    main()
