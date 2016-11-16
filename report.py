#!/usr/bin/env python

# import standard libraries
import os, sys

# update path
sys.path.insert(0, 'lib')

# import modules
import google as g

def main():

	print 'Getting data from GCP...'

	print '   * organizations...'
	organizations = g.getOrganizations()
	print '   * billing accounts...'
	billingAccounts = g.getBillingAccounts()
	print '   * projects...'
	projects = g.getProjects()

	print '\nOrganizations (%s)' % str(len(organizations))
	print 'Billing Accounts (%s)' % str(len(billingAccounts))
	print 'Projects (%s)' % str(len(projects))

if __name__ == "__main__":
	main()
