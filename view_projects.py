#!/usr/bin/env python
"""Create Google Cloud Platform projects."""

# import standard libraries
import argparse

# update path
# sys.path.insert(0, 'lib')

from lib.args import create_arg_parser
from lib.google import Google

google = Google()
google.auth()

folders = {}

project_url = 'https://console.cloud.google.com/iam-admin/iam/project?project='


def main():
    """Main function."""
    import argparse

    # create a new argument parser
    parser = argparse.ArgumentParser(
        description='View projects'
    )

    parser.add_argument('projects', nargs='+')
    args = parser.parse_args()

    for project_id in sorted(args.projects):
        print '%s:' % (project_id)

        try:
            project = google.get_project(project_id)

        except:
            print '   ERROR: not found!\n'
            continue

        created = project['createTime']
        labels = google.display_labels(project['labels'])
        name = project['name']
        number = project['projectNumber']
        pid = project['projectId']
        status = project['lifecycleState']

        parent_id = project['parent']['id']
        # parent_type = project['parent']['type']

        if parent_id in folders:
            org_path = folders[parent_id]
        else:
            org_path = google.display_parents(project['parent'])
            folders[parent_id] = org_path

        print '   Created:  %s' % created
        print '   ID:       %s' % (pid)
        print '   Name:     %s' % (name)
        print '   Number:   %s' % (number)
        print '   Status:   %s' % (status)
        print '   Labels:   %s' % (labels)
        print '   Org Path: %s' % (org_path)
        print '   URL:      %s%s' % (project_url, project_id)
        print


if __name__ == "__main__":
    main()
