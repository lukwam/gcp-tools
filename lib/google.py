#!/usr/bin/env python

# import build
from googleapiclient.discovery import build

# import GoogleCredentials
from oauth2client.client import GoogleCredentials

# get application default credentials
credentials = GoogleCredentials.get_application_default()

# import logging
import logging

# enable logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

#
# Cloud Billing (cloudbilling)
#

# build a resource manager service
cb = build('cloudbilling', 'v1', credentials=credentials)

def getBillingAccounts():

	# create a request to list billingAccounts
	request = cb.billingAccounts().list()

	# create a list to hold all the projects
	billingAccounts = []

	# page through the responses
	while request is not None:

		# execute the request
		response = request.execute()

		# add projects to the projects list
		if 'billingAccounts' in response:
			billingAccounts.extend(response['billingAccounts'])

		request = cb.billingAccounts().list_next(request, response)

	return billingAccounts

#
# Cloud Resource Manager (cloudresourcemanager)
#

# build a resource manager service
crm = build('cloudresourcemanager', 'v1', credentials=credentials)

def getOrganizations():

	# create a request to list organizations
	response = crm.organizations().search(body={}).execute()

	return response['organizations']

def getProjects():

	# create a request to list projects
	request = crm.projects().list()

	# create a list to hold all the projects
	projects = []

	# page through the responses
	while request is not None:

		# execute the request
		response = request.execute()

		# add projects to the projects list
		if 'projects' in response:
			projects.extend(response['projects'])

		request = crm.projects().list_next(request, response)

	return projects
