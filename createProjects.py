#!/usr/bin/env python

# import standard libraries
import argparse, os, sys

# update path
sys.path.insert(0, 'lib')

def createProject(projectId, organization=None, folder=None):
	sys.stdout.write('   * creating project: %s...' % projectId)
	sys.stdout.flush()
	print

def enableBilling(projectId, billingAccount):
	sys.stdout.write('   * enabling billing: billingAccounts/%s...' % billingAccount)
	sys.stdout.flush()
	print

def enableServices(projectId, apis):
	sys.stdout.write('   * enabling APIs: %s...' % apis)
	sys.stdout.flush()
	print

def enableUsageBucket(projectId, usageBucket):
	sys.stdout.write('   * enabling compute usage export: gs://%s/...' % usageBucket)
	sys.stdout.flush()
	print

def setLabels(projectId, labels):
	sys.stdout.write('   * setting project labels: %s...' % labels)
	sys.stdout.flush()
	print

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
	usageBucket = None

	# check for template
	if args.template:
		print '\nLoading template: %s...' % args.template

		# default organization

		# default folder

		# default labels

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
		print '   * creating project...'
		if organization:
			createProject(projectId, organization=organization)
		elif folder:
			createProject(projectId, folder=folder)
		else:
			createProject(projectId)

		# create project labels
		if labels:
			setLabels(projectId, labels)

		# enable billing
		if billingAccount:
			enableBilling(projectId, billingAccount)

		# apis
		if apis:
			enableServices(projectId, apis)

		# compute usage bucket
		if usageBucket:
			enableUsageBucket(projectId, usageBucket)

if __name__ == "__main__":
	main()
