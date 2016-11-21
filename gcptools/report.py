#!/usr/bin/env python
"""Display a report of GCP resources."""

# import modules
from lib.google import Google


def main():
    """Main function."""
    # authenticate to google
    print 'Authenticating to Google...'
    google = Google()
    google.auth()

    print 'Getting data from GCP...'

    print '   * organizations...'
    organizations = google.get_organizations()
    print '   * billing accounts...'
    billing_accounts = google.get_billing_accounts()
    print '   * projects...'
    projects = google.get_projects()

    print '\nOrganizations (%s)' % str(len(organizations))
    print 'Billing Accounts (%s)' % str(len(billing_accounts))
    print 'Projects (%s)' % str(len(projects))


if __name__ == "__main__":
    main()
