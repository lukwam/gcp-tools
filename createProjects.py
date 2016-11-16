#!/usr/bin/env python

# import standard libraries
import argparse, json, os, re, sys

# update path
sys.path.insert(0, 'lib')

def createProject(g, projectId, organization=None, folder=None, labels=None):
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

	sys.stdout.write('   * creating project: %s...' % projectId)
	sys.stdout.flush()

	result = g.createProject(project)
	if result:
		print 'successful.'

def createServiceAccounts(g, projectId, serviceAccounts):
	print '   * creating service accounts:'
	for accountId in serviceAccounts.split(','):
		sys.stdout.write('     - %s...' % accountId)
		sys.stdout.flush()
		result = g.createServiceAccount(projectId, accountId)
		if result:
			print 'successful.'

def enableBilling(g, projectId, billingAccount):
	sys.stdout.write('   * enabling billing: billingAccounts/%s...' % billingAccount)
	sys.stdout.flush()
	print

def enableServices(g, projectId, apis):
	sys.stdout.write('   * enabling APIs: %s...' % apis)
	sys.stdout.flush()
	print

def enableUsageBucket(g, projectId, usageBucket):
	sys.stdout.write('   * enabling compute usage export: gs://%s/...' % usageBucket)
	sys.stdout.flush()
	print

def setLabels(g, projectId, labels):
	sys.stdout.write('   * updating labels: %s...' % labels)
	sys.stdout.flush()

	project = g.getProject(projectId)
	if 'labels' not in project:
		project['labels'] = {}
	for l in labels.split(','):
		if re.search('.=.', l):
			(k, v) = l.split('=')
			project['labels'][k.lower()] = v
	result = g.updateProject(projectId, project)
	if result:
		print 'successful.'

def main():

	# create a new argument parser
	parser = argparse.ArgumentParser(
		description='Create projects'
	)

	parser.add_argument(
		'-a',
		'--apis',
		action='store',
		default=None,
		help='API services to enable (ex. compute_component,storage-component-json.googleapis.com)'
	)

	parser.add_argument(
		'-b',
		'--billingAccount',
		action='store',
		default=None,
		help='Billing account (ex. ABCDEF-012345-6789FE)'
	)

	parser.add_argument(
		'-f',
		'--folder',
		action='store',
		default=None,
		help='Folder (ex. 123456789098)'
	)

	parser.add_argument(
		'-l',
		'--labels',
		action='store',
		default=None,
		help='Labels (ex. label1=value1,label2=value2)'
	)

	parser.add_argument(
		'-o',
		'--organization',
		action='store',
		default=None,
		help='Organization (ex. 123456789098)'
	)

	parser.add_argument(
		'-s',
		'--serviceAccounts',
		action='store',
		default=None,
		help='Service Accounts (ex. account1,account2)'
	)

	parser.add_argument(
		'-t',
		'--template',
		action='store',
		default=None,
		help='Template (ex. my-template)'
	)

	parser.add_argument(
		'-u',
		'--usageBucket',
		action='store',
		default=None,
		help='Usage Bucket for Compute (ex. my-compute-usage-bucket)'
	)

	# at least projectId is required
	parser.add_argument('projectId', nargs='+')

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

	# set defaults
	apis = None
	billingAccount = None
	folder = None
	labels = None
	organization = None
	serviceAccounts = None
	usageBucket = None

	# check for template
	if args.template:
		print '\nLoading template: %s...' % args.template

		# default organization

		# default folder

		# default labels

		# default service accounts

		# default billing account

		# default apis

		# usage bucket

	# command line arguments override template defaults
	if args.apis:
		apis = args.apis
	if args.billingAccount:
		billingAccount = args.billingAccount
	if args.folder:
		folder = args.folder
	if args.labels:
		labels = args.labels
	if args.organization:
		organization = args.organization
	if args.serviceAccounts:
		serviceAccounts = args.serviceAccounts
	if args.usageBucket:
		usageBucket = args.usageBucket

	# display settings
	print '\nSettings:'
	if organization:
		print '   * Parent: organizations/%s...' % organization
	elif folder:
		print '   * Parent: folders/%s...' % folder

	if labels:
		print '   * Labels:'
		print '     - '+'\n     - '.join(sorted(labels.split(',')))

	if serviceAccounts:
		print '   * Service Accounts:'
		print '     - '+'\n     - '.join(sorted(serviceAccounts.split(',')))

	if billingAccount:
		print '   * Billing: billingAccounts/%s...' % billingAccount

	if apis:
		print '   * APIs: '
		print '     - '+'\n     - '.join(sorted(apis.split(',')))

	if usageBucket:
		print '   * Compute Usage Bucket: %s' % usageBucket


	for projectId in args.projectId:

		print '\n%s:' % projectId

		# create the project
		if organization:
			createProject(g, projectId, organization=organization, labels=labels)
		elif folder:
			createProject(g, projectId, folder=folder, labels=labels)
		else:
			createProject(g, projectId, labels=labels)

		# create project labels
		if serviceAccounts:
			createServiceAccounts(g, projectId, serviceAccounts)

		# create project labels
		if labels:
			setLabels(g, projectId, labels)

		# enable billing
		if billingAccount:
			enableBilling(g, projectId, billingAccount)

		# apis
		if apis:
			enableServices(g, projectId, apis)

		# compute usage bucket
		if usageBucket:
			enableUsageBucket(g, projectId, usageBucket)

if __name__ == "__main__":
	main()
