#!/usr/bin/env python
"""Display a report of GCP resources."""

# import modules
from lib.google import Google


def display_billing_accounts(google):
    """Display the billing accounts for the authenticated user."""
    billing_accounts = google.get_billing_accounts()
    print '\nBilling Accounts (%s)' % str(len(billing_accounts))
    for ba in sorted(billing_accounts, key=lambda x: x['displayName']):
        display_name = str(ba['displayName'])
        name = str(ba['name'])
        print '   * %s [%s]' % (display_name, name)


def display_folders(google, parent, depth=0):
    """Display the folders for the given parent."""
    folders = google.get_folders(parent)
    for folder in sorted(folders, key=lambda x: x['displayName']):
        display_name = str(folder['displayName'])
        name = str(folder['name'])
        indent = '  ' * depth
        print '     %s- %s [%s]' % (indent, display_name, name)
        display_folders(google, name, depth+1)


def display_orgs(google):
    """Display the organizations for the authenticated user."""
    organizations = google.get_organizations()
    print '\nOrganizations (%s)' % str(len(organizations))
    for org in sorted(organizations, key=lambda x: x['displayName']):
        customerId = str(org['owner']['directoryCustomerId'])
        display_name = str(org['displayName'])
        name = str(org['name'])
        print '\n   * %s [%s] (%s)' % (display_name, name, customerId)
        display_folders(google, name)


def display_projects(google):
    """Display the projects for the authenticated user."""
    projects = google.get_projects()
    print '\nProjects (%s)' % str(len(projects))
    for project in sorted(projects, key=lambda x: x['name']):
        name = str(project['name'])
        projectId = str(project['projectId'])
        print '   * %s [%s]' % (name, projectId)


def main():
    """Main function."""
    # authenticate to google
    print 'Authenticating to Google...'
    google = Google()
    google.auth()

    display_orgs(google)
    # display_billing_accounts(google)
    # display_projects(google)


if __name__ == "__main__":
    main()
