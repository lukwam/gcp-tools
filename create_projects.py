#!/usr/bin/env python
"""Create Google Cloud Platform projects."""

# import standard libraries
import glob
import re
import sys
import time
import yaml

# update path
sys.path.insert(0, 'lib')

from args import create_arg_parser


def create_project(g, project_id, settings):
    """

    Function: create_project.

    description

    Args:

      g          - [type/description]
      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    organization = str(settings['organization'])
    folder = str(settings['folder'])

    # labels = settings['labels']

    project = {
        'projectId': project_id,
        'name': project_id,
    }

    if organization:
        project['parent'] = {
            'id': organization.replace('organizations/', ''),
            'type': 'organization',
        }
    elif folder:
        project['parent'] = {
            'id': folder.replace('folders/', ''),
            'type': 'folder',
        }

    # if labels:
    #   project['labels'] = labels

    sys.stdout.write('   * creating project: %s...' % project_id)
    sys.stdout.flush()

    result = g.create_project(project)
    if result:
        print 'successful.'


def create_service_accounts(g, project_id, settings):
    """

    Function: create_service_accounts.

    description

    Args:

      g          - [type/description]
      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    service_accounts = settings['serviceAccounts']

    print '   * creating service accounts:'
    for account_id in service_accounts:
        sys.stdout.write('     - %s...' % account_id)
        sys.stdout.flush()
        result = g.create_service_account(project_id, account_id)
        if result:
            print 'successful.'


def display_settings(settings):
    """

    Function: display_settings.

    description

    Args:

      settings - [type/description]

    Returns:

      return description
    """
    print '\nSettings:\n'

    if settings['organization']:
        print '   Parent: organizations/%s...' % settings['organization']
    elif settings['folder']:
        print '   Parent: folders/%s...' % settings['folder']

    if settings['apis']:
        print '   APIs: '
        print '     - ' + '\n     - '.join(settings['apis'])

    if settings['billingAccount']:
        print '   Billing: billingAccounts/%s...' % settings['billingAccount']

    if settings['iamPolicy']:
        print '   IAM Policy:'
        for role in sorted(settings['iamPolicy']):
            print '     %s:' % role
            for i in sorted(settings['iamPolicy'][role]):
                print '      - %s' % i

    if settings['labels']:
        print '   Labels:'
        for l in sorted(settings['labels']):
            print '     %s: %s' % (l, settings['labels'][l])

    if settings['serviceAccounts']:
        print '   Service Accounts:'
        print '     - '+'\n     - '.join(settings['serviceAccounts'])

    if settings['usageBucket']:
        print '   Compute Usage Bucket: %s' % settings['usageBucket']


def enable_billing(g, project_id, settings):
    """

    Function: enable_billing.

    description

    Args:

      g          - [type/description]
      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    billing_account = 'billingAccounts/%s' % settings['billingAccount']

    sys.stdout.write('   * enabling billing: %s...' % billing_account)
    sys.stdout.flush()
    result = g.enable_project_billing(project_id, '%s' % billing_account)
    if result:
        print 'successful.'


def enable_services(g, project_id, settings):
    """

    Function: enable_services.

    description

    Args:

      g          - [type/description]
      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    apis = settings['apis']

    print '   * enabling APIs:'
    for service_name in apis:
        sys.stdout.write('     - %s...' % service_name)
        sys.stdout.flush()
        operation = g.enable_project_service(project_id, service_name)
        if operation:
            while True:
                op = g.get_service_operation(operation['name'])
                if 'done' in op and op['done']:
                    break
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(1)
            print 'successful.'
        else:
            print


def enable_usage_bucket(g, project_id, settings):
    """

    Function: enable_usage_bucket.

    description

    Args:

      g          - [type/description]
      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    usage_bucket = settings['usageBucket']
    message = 'enabling compute usage export'
    sys.stdout.write('   * %s: gs://%s/...' % (message, usage_bucket))
    sys.stdout.flush()
    result = g.set_project_usgae_export_bucket(project_id, usage_bucket)
    if result:
        print 'successful.'
    else:
        print


def get_bindings(iam_policy_args):
    """

    Function: get_bindings.

    description

    Args:

      iam_policy_args - [type/description]

    Returns:

      return description
    """
    if not iam_policy_args:
        return None

    bindings = {}
    for i in iam_policy_args.split(','):
        if re.search('=', i):
            (role, identity) = i.split('=')

            if role not in bindings:
                bindings[role] = [identity]
            else:
                bindings[role].append(identity)
    return bindings


def get_labels(labels_args):
    """

    Function: get_labels.

    description

    Args:

      labelsArgs - [type/description]

    Returns:

      return description
    """
    if not labels_args:
        return None

    labels = {}
    for l in labels_args.split(','):
        if re.search('=', l):
            (label, value) = l.split('=')
            labels[label] = value
    return labels


def get_effective_settings(args):
    """

    Function: get_effective_settings.

    description

    Args:

      args - [type/description]

    Returns:

      return description
    """
    # set defaults
    settings = {
        'apis': None,
        'billingAccount': None,
        'folder': None,
        'iamPolicy': None,
        'labels': None,
        'organization': None,
        'serviceAccounts': None,
        'template': None,
        'usageBucket': None,
    }

    # print json.dumps(settings, indent=2, sort_keys=True)

    # check for template
    if args.template:
        print '\nLoading template: %s...' % args.template

        # look for template in templates directory
        template_files = glob.glob('templates/%s.yml' % args.template)
        if len(template_files) < 1:
            print 'ERROR: Template not found: %s' % args.template
            sys.exit(1)

        settings['template'] = args.template

        # open the template file as a stream and process the yaml
        stream = open(template_files[0], 'r')
        docs = yaml.load_all(stream)

        # apply template values to settings
        for doc in docs:
            for k, v in doc.items():
                # print k+' --> '+str(v)
                settings[k] = v
            # print

    # print json.dumps(settings, indent=2, sort_keys=True)

    # command line arguments override template default values
    if args.apis:
        settings['apis'] = sorted(args.apis.split(','))
    if args.billing_account:
        settings['billingAccount'] = args.billing_account
    if args.folder:
        settings['folder'] = args.folder
    if args.iam_policy:
        settings['iamPolicy'] = get_bindings(args.iam_policy)
    if args.labels:
        settings['labels'] = get_labels(args.labels)
    if args.organization:
        settings['organization'] = args.organization
    if args.service_accounts:
        settings['serviceAccounts'] = sorted(args.service_accounts.split(','))
    if args.usage_bucket:
        settings['usageBucket'] = args.usage_bucket

    return settings


def update_labels(g, project_id, settings):
    """

    Function: update_labels.

    description

    Args:

      g          - [type/description]
      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    labels = settings['labels']

    sys.stdout.write('   * updating labels: %s...' % labels)
    sys.stdout.flush()

    project = g.get_project(project_id)
    if 'labels' not in project:
        project['labels'] = {}
    for l in labels:
        if re.search('.=.', l):
            (k, v) = l.split('=')
            project['labels'][k.lower()] = v
    result = g.update_project(project_id, project)
    if result:
        print 'successful.'


def main():
    """Main function."""
    # create arg parser
    parser = create_arg_parser()

    # parse the arguments
    args = parser.parse_args()

    # check args
    folder_error = 'Provide either an organization or a folder, but not both.'
    if args.organization and args.folder:
        print 'ERROR: %s' % folder_error
        sys.exit(1)

    # connect to google
    sys.stdout.write('Connecting to Google with default credentials...')
    sys.stdout.flush()
    import google as g
    print 'successful.'

    # get effective settings
    settings = get_effective_settings(args)

    # display effective settings
    display_settings(settings)

    print '\nCreating Projects:'
    for project_id in args.project_id:

        print '\n %s:' % project_id

        # create the project
        create_project(g, project_id, settings)

        # create project labels
        if settings['serviceAccounts']:
            create_service_accounts(g, project_id, settings)

        # create project labels
        if settings['labels']:
            update_labels(g, project_id, settings)

        # enable billing
        if settings['billingAccount']:
            enable_billing(g, project_id, settings)

        # apis
        if settings['apis']:
            enable_services(g, project_id, settings)

        # compute usage bucket
        if settings['usageBucket']:
            enable_usage_bucket(g, project_id, settings)


if __name__ == "__main__":
    main()
