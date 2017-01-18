#!/usr/bin/env python
"""Create Google Cloud Platform projects."""

# import standard libraries
import glob
import re
import sys
import time
import yaml

# update path
# sys.path.insert(0, 'lib')

from lib.args import create_arg_parser
from lib.google import Google

google = Google()


def get_parent(settings):
    """

    Function: get_parent.

    description

    Args:

      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    organization = settings['organization']
    folder = settings['folder']
    parent = None

    if organization:
        parent = {
            'id': str(organization).replace('organizations/', ''),
            'type': 'organization',
        }
    elif folder:
        parent = {
            'id': str(folder).replace('folders/', ''),
            'type': 'folder',
        }
    return parent


def create_project(project_id, settings):
    """

    Function: create_project.

    description

    Args:

      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    organization = settings['organization']
    folder = settings['folder']

    # labels = settings['labels']

    project = {
        'projectId': project_id,
        'name': project_id,
    }

    project['parent'] = get_parent(settings)

    # if labels:
    #   project['labels'] = labels

    sys.stdout.write('   * creating project: %s...' % project_id)
    sys.stdout.flush()

    result = google.create_project(project)
    if result:
        time.sleep(1)
        print 'successful.'
    return result


def create_service_accounts(project_id, settings):
    """

    Function: create_service_accounts.

    description

    Args:

      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    service_accounts = settings['service_accounts']

    print '   * creating service accounts:'
    for account_id in service_accounts:
        sys.stdout.write('     - %s...' % account_id)
        sys.stdout.flush()
        result = google.create_service_account(project_id, account_id)
        if result:
            print 'successful.'


def create_usage_bucket(project_id, settings):
    """

    Function: create_usage_bucket.

    description

    Args:

      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    usage_bucket = settings['usage_bucket']
    try:
        google.get_bucket(usage_bucket)
    except:
        sys.stdout.write('   * creating usage bucket: %s...' % usage_bucket)
        sys.stdout.flush()
        result = google.create_bucket(project_id, usage_bucket)
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
    for key in sorted(settings):

        if key in ['organization'] and settings[key]:
            print '   Organization: %s...' % settings[key]

        elif key in ['folder'] and settings[key]:
            print '   Folder: %s...' % settings[key]

        elif key in ['apis'] and settings[key]:
            print '   APIs: '
            print '     - ' + '\n     - '.join(settings[key])

        elif key in ['billing_account'] and settings[key]:
            print '   Billing Account: %s...' % settings[key]

        elif key in ['iam_policy'] and settings[key]:
            print '   IAM Policy:'
            for role in sorted(settings[key]):
                print '     %s:' % role
                for i in sorted(settings[key][role]):
                    print '      - %s' % i

        elif key in ['labels'] and settings[key]:
            print '   Labels:'
            for label in sorted(settings[key]):
                print '     %s: %s' % (label, settings[key][label])

        elif key in ['service_accounts'] and settings[key]:
            print '   Service Accounts:'
            print '     - '+'\n     - '.join(settings[key])

        elif key in ['usage_bucket'] and settings[key]:
            print '   Usage Bucket: %s' % settings[key]

        elif key in ['region'] and settings[key]:
            print '   Region: %s' % settings[key]

        elif key in ['zone'] and settings[key]:
            print '   Zone: %s' % settings[key]


def enable_billing(project_id, settings):
    """

    Function: enable_billing.

    description

    Args:

      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    billing_account = 'billingAccounts/%s' % settings['billing_account']

    sys.stdout.write('   * enabling billing: %s...' % billing_account)
    sys.stdout.flush()
    result = google.enable_project_billing(project_id, '%s' % billing_account)
    if result:
        print 'successful.'


def enable_services(project_id, settings):
    """

    Function: enable_services.

    description

    Args:

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
        response = google.enable_project_service(project_id, service_name)
        if response:
            while True:
                operation = google.get_service_operation(response['name'])
                if 'done' in operation and operation['done']:
                    break
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(1)
            print 'successful.'
        else:
            print
    return sorted(apis)


def enable_usage_bucket(project_id, settings):
    """

    Function: enable_usage_bucket.

    description

    Args:

      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    usage_bucket = settings['usage_bucket']
    message = 'enabling compute usage export'
    sys.stdout.write('   * %s: gs://%s/...' % (message, usage_bucket))
    sys.stdout.flush()
    result = google.set_project_usgae_export_bucket(project_id, usage_bucket)
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
    for label in labels_args.split(','):
        if re.search('=', label):
            (name, value) = label.split('=')
            labels[name] = value
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
        'billing_account': None,
        'folder': None,
        'iam_policy': None,
        'labels': None,
        'organization': None,
        'service_accounts': None,
        'template': None,
        'usage_bucket': None,
    }

    # print json.dumps(settings, indent=2, sort_keys=True)

    # check for template
    if args.template:
        print '\nLoading template: %s...' % args.template

        # check if file is a gs:// path
        if re.match('gs:', args.template):
            # print args.template
            bucket_name = args.template.split('/')[2]
            object_name = '/'.join(args.template.split('/')[3:])
            print google.get_bucket_object(bucket_name, object_name)

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
            for key, value in doc.items():
                # print k+' --> '+str(v)
                settings[key] = value
            # print

    # print json.dumps(settings, indent=2, sort_keys=True)

    # command line arguments override template default values
    if args.apis:
        settings['apis'] = sorted(args.apis.split(','))
    if args.billing_account:
        settings['billing_account'] = args.billing_account
    if args.folder:
        settings['folder'] = args.folder
    if args.iam_policy:
        settings['iam_policy'] = get_bindings(args.iam_policy)
    if args.labels:
        settings['labels'] = get_labels(args.labels)
    if args.organization:
        settings['organization'] = args.organization
    if args.service_accounts:
        settings['service_accounts'] = sorted(args.service_accounts.split(','))
    if args.usage_bucket:
        settings['usage_bucket'] = args.usage_bucket

    return settings


def set_iam_policy(project_id, settings):
    """

    Function: set_iam_policy.

    description

    Args:

      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    iam_policy = settings['iam_policy']

    policy = {
        'bindings': []
    }

    for role in iam_policy:
        binding = {
            'role': 'roles/%s' % (role),
            'members': [],
        }
        for member in iam_policy[role]:
            binding['members'].append(member)
        policy['bindings'].append(binding)

    sys.stdout.write('   * updating IAM policy...')
    sys.stdout.flush()

    result = google.set_iam_policy(project_id, policy)
    if result:
        print 'successful.'


def update_labels(project_id, settings):
    """

    Function: update_labels.

    description

    Args:

      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    labels = settings['labels']
    labels_list = []
    for label in sorted(labels):
        labels_list.append('%s=%s' % (label, labels[label]))

    sys.stdout.write('   * updating labels: %s...' % ','.join(labels_list))
    sys.stdout.flush()

    project = google.get_project(project_id)
    if 'labels' not in project:
        project['labels'] = {}
    for label in labels:
        if re.search('.=.', label):
            (key, value) = label.split('=')
            project['labels'][key.lower()] = value
    result = google.update_project(project_id, project)
    if result:
        print 'successful.'


def update_project_metadata(project_id, settings):
    """

    Function: update_project_metadata.

    description

    Args:

      project_id - [type/description]
      settings   - [type/description]

    Returns:

      return description
    """
    region = settings['region']
    zone = settings['zone']

    project = google.get_compute_project(project_id)

    metadata = None
    update = False

    if 'commonInstanceMetadata' in project:
        metadata = project['commonInstanceMetadata']

        metadata_dict = {}
        if 'items' in metadata:
            for item in metadata['items']:
                key = item['key']
                value = item['value']
                metadata_dict[key] = value

        if region and (
            ('google-compute-default-region' in metadata_dict
                and metadata_dict['google-compute-default-region'] != region)
            or 'google-compute-default-region' not in metadata_dict
        ):
            update = True

        if zone and (
            ('google-compute-default-zone' in metadata_dict
                and metadata_dict['google-compute-default-zone'] != zone)
            or 'google-compute-default-zone' not in metadata_dict
        ):
            update = True

    else:
        update = True

    if update:
        metadata_items = {
            'items': []
        }
        if region:
            metadata_items['items'].append({
                'key': 'google-compute-default-region',
                'value': region,
            })
        if zone:
            metadata_items['items'].append({
                'key': 'google-compute-default-zone',
                'value': zone,
            })
        if metadata:
            metadata_items['fingerprint'] = metadata['fingerprint']

        sys.stdout.write('   * updating common instance metadata...')
        sys.stdout.flush()

        result = google.set_common_instance_metadata(
            project_id,
            metadata_items
        )
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

    # authenticate via the gcloud application-default credentials
    google.auth()
    print 'successful.'

    # get effective settings
    settings = get_effective_settings(args)

    # display effective settings
    display_settings(settings)

    print '\nCreating Projects:'
    for project_id in args.project_id:

        print '\n %s:' % project_id

        # create the project
        project = create_project(project_id, settings)

        # check if project aready exists
        if not project:
            project = google.get_project(project_id)

            # check parent
            current_parent = None
            if 'parent' in project:
                current_parent = project['parent']

            parent = get_parent(settings)

            if current_parent != parent:
                parent_string = '%ss/%s' % (parent['type'], parent['id'])
                sys.stdout.write('   * updating parent: %s...' % parent_string)
                sys.stdout.flush()
                update = google.update_project(project_id, {'parent': parent})
                if update:
                    print 'successful.'

        # create service accounts
        if settings['service_accounts']:
            create_service_accounts(project_id, settings)

        # set IAM policies
        if settings['iam_policy']:
            set_iam_policy(project_id, settings)

        # create project labels
        if settings['labels']:
            update_labels(project_id, settings)

        # enable billing
        if settings['billing_account']:
            enable_billing(project_id, settings)

        # enable apis
        apis = []
        if settings['apis']:
            apis = enable_services(project_id, settings)

        # check if compute api is enabled
        if 'compute_component' in apis:

            # compute usage bucket
            if settings['usage_bucket']:
                create_usage_bucket(project_id, settings)
                enable_usage_bucket(project_id, settings)

        # update project metadata
        if settings['region'] or settings['zone']:
            update_project_metadata(project_id, settings)

        base = 'https://console.cloud.google.com/home/dashboard?project='
        print '   * console: %s%s' % (base, project_id)


if __name__ == "__main__":
    main()
