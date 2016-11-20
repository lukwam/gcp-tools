#!/usr/bin/env python

# import standard libraries
import glob, json, os, re, sys, time, yaml

# update path
sys.path.insert(0, 'lib')

from args import createArgParser

def createProject(g, projectId, settings):

    organization = str(settings['organization'])
    folder = str(settings['folder'])

    labels = settings['labels']

    project = {
        'projectId': projectId,
        'name': projectId,
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

    sys.stdout.write('   * creating project: %s...' % projectId)
    sys.stdout.flush()

    result = g.createProject(project)
    if result:
        print 'successful.'

def createServiceAccounts(g, projectId, settings):

    serviceAccounts = settings['serviceAccounts']

    print '   * creating service accounts:'
    for accountId in serviceAccounts:
        sys.stdout.write('     - %s...' % accountId)
        sys.stdout.flush()
        result = g.createServiceAccount(projectId, accountId)
        if result:
            print 'successful.'

def displaySettings(settings):

    print '\nSettings:\n'

    if settings['organization']:
        print '   Parent: organizations/%s...' % settings['organization']
    elif settings['folder']:
        print '   Parent: folders/%s...' % settings['folder']

    if settings['apis']:
        print '   APIs: '
        print '     - '+'\n     - '.join(settings['apis'])

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

def enableBilling(g, projectId, settings):

    billingAccount = settings['billingAccount']

    sys.stdout.write('   * enabling billing: billingAccounts/%s...' % billingAccount)
    sys.stdout.flush()
    result = g.enableProjectBilling(projectId, 'billingAccounts/%s' % billingAccount)
    if result:
        print 'successful.'

def enableServices(g, projectId, settings):

    apis = settings['apis']

    print '   * enabling APIs:'
    for serviceName in apis:
        sys.stdout.write('     - %s...' % serviceName)
        sys.stdout.flush()
        operation = g.enableProjectService(projectId, serviceName)
        if operation:
            while True:
                op = g.getServiceOperation(operation['name'])
                if 'done' in op and op['done']:
                    break
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(1)
            # print result
            print 'successful.'
        else:
            print

def enableUsageBucket(g, projectId, settings):

    usageBucket = settings['usageBucket']

    sys.stdout.write('   * enabling compute usage export: gs://%s/...' % usageBucket)
    sys.stdout.flush()
    result = g.setProjectUsgaeExportBucket(projectId, usageBucket)
    if result:
        print 'successful.'
    else:
        print

def getBindings(iamPolicyArgs):

    if not iamPolicyArgs:
        return None

    bindings = {}
    for i in iamPolicyArgs.split(','):
        if re.search('=', i):
            (role, identity) = i.split('=')

            if role not in bindings:
                bindings[role] = [ identity ]
            else:
                bindings[role].append(identity)
    return bindings

def getLabels(labelsArgs):

    if not labelsArgs:
        return None

    labels = {}
    for l in labelsArgs.split(','):
        if re.search('=', l):
            (label, value) = l.split('=')
            labels[label] = value
    return labels

def getEffectiveSettings(args):

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
        templateFiles = glob.glob('templates/%s.yml' % args.template)
        if len(templateFiles) < 1:
            print 'ERROR: Template not found: %s' % args.template
            sys.exit(1)

        settings['template'] = args.template

        # open the template file as a stream and process the yaml
        stream = open(templateFiles[0], 'r')
        docs = yaml.load_all(stream)

        # apply template values to settings
        for doc in docs:
            for k,v in doc.items():
                # print k+' --> '+str(v)
                settings[k] = v
            # print

    # print json.dumps(settings, indent=2, sort_keys=True)

    # command line arguments override template default values
    if args.apis:
        settings['apis'] = sorted(args.apis.split(','))
    if args.billingAccount:
        settings['billingAccount'] = args.billingAccount
    if args.folder:
        settings['folder'] = args.folder
    if args.iamPolicy:
        settings['iamPolicy'] = getBindings(args.iamPolicy)
    if args.labels:
        settings['labels'] = getLabels(args.labels)
    if args.organization:
        settings['organization'] = args.organization
    if args.serviceAccounts:
        settings['serviceAccounts'] = sorted(args.serviceAccounts.split(','))
    if args.usageBucket:
        settings['usageBucket'] = args.usageBucket

    return settings

def updateLabels(g, projectId, settings):

    labels = settings['labels']

    sys.stdout.write('   * updating labels: %s...' % labels)
    sys.stdout.flush()

    project = g.getProject(projectId)
    if 'labels' not in project:
        project['labels'] = {}
    for l in labels:
        if re.search('.=.', l):
            (k, v) = l.split('=')
            project['labels'][k.lower()] = v
    result = g.updateProject(projectId, project)
    if result:
        print 'successful.'

def main():

    # create arg parser
    parser = createArgParser()

    # parse the arguments
    args = parser.parse_args()

    # check args
    if args.organization and args.folder:
        print 'ERROR: Provide either an organization or a folder, but not both.'
        sys.exit(1)

    # connect to google
    sys.stdout.write('Connecting to Google with default credentials...')
    sys.stdout.flush()
    import google as g
    print 'successful.'

    # get effective settings
    settings = getEffectiveSettings(args)

    # display effective settings
    displaySettings(settings)

    print '\nCreating Projects:'
    for projectId in args.projectId:

        print '\n %s:' % projectId

        # create the project
        createProject(g, projectId, settings)

        # create project labels
        if settings['serviceAccounts']:
            createServiceAccounts(g, projectId, settings)

        # create project labels
        if settings['labels']:
            updateLabels(g, projectId, settings)

        # enable billing
        if settings['billingAccount']:
            enableBilling(g, projectId, settings)

        # apis
        if settings['apis']:
            enableServices(g, projectId, settings)

        # compute usage bucket
        if settings['usageBucket']:
            enableUsageBucket(g, projectId, settings)

if __name__ == "__main__":
    main()
