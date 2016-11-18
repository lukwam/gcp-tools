#!/usr/bin/env python

import argparse

def createArgParser():

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
		'-i',
		'--iamPolicy',
		action='store',
		default=None,
		help='IAM Policy (ex. owner=user:email@domain.com,editor=group:group@domain.com)'
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

	return parser
