#!/usr/bin/env python

# import standard libraries
import os, sys

# update path
sys.path.insert(0, 'lib')

# import modules
import google as g

def main():

	print 'Getting organizations...'
	organizations = g.getOrganizations()
	print '%s organizations found.' % str(len(organizations))

	print '\nGetting billing accounts...'
	billingAccounts = g.getBillingAccounts()
	print '%s billing accounts found.' % str(len(billingAccounts))

	print '\nGetting projects...'
	projects = g.getProjects()
	print '%s projects found.' % str(len(projects))

if __name__ == "__main__":
	main()
