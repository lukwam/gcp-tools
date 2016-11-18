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

def enableProjectBilling(projectId, billingAccountName):

		body = {
			'projectId': projectId,
			'billingAccountName': billingAccountName,
			'billingEnabled': True,
		}

		return cb.projects().updateBillingInfo(name='projects/'+projectId, body=body).execute()

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
# Compute
#
compute = build('compute', 'v1', credentials=credentials)

def setProjectUsgaeExportBucket(projectId, bucketName):

	body = {
		'bucketName': bucketName,
		'reportNamePrefix': 'usage',
	}

	return compute.projects().setUsageExportBucket(project=projectId, body=body).execute()

#
# Cloud Resource Manager (cloudresourcemanager)
#
crm = build('cloudresourcemanager', 'v1', credentials=credentials)

def createProject(project):

	try:
		return crm.projects().create(body=project).execute()
	except Exception as e:
		print '[%s]' % e._get_reason()
		return {}

def getOrganizations():

	# create a request to list organizations
	response = crm.organizations().search(body={}).execute()

	return response['organizations']

def getProject(projectId):

	# create a request to list projects
	return crm.projects().get(projectId=projectId).execute()

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

def updateProject(projectId, body):
	try:
		return crm.projects().update(projectId=projectId, body=body).execute()
	except Exception as e:
		print '[%s]' % e._get_reason()
		return {}
#
# IAM (Identity and Access Management)
#
iam = build('iam', 'v1', credentials=credentials)

def createServiceAccount(projectId, accountId, displayName=None):

	# set displayName
	if not displayName:
		displayName = accountId

	params = {
		'name': 'projects/'+projectId,
		'body': {
			'accountId': accountId,
			'serviceAccount': {
				'displayName': displayName,
			},
		},
	}

	try:
		return iam.projects().serviceAccounts().create(**params).execute()
	except Exception as e:
		print '[%s]' % e._get_reason().split('/')[-1]
		return {}

#
# Service Management
#
sm = build('servicemanagement', 'v1', credentials=credentials)

def enableProjectService(projectId, serviceName):

	body = {
		'consumerId': 'project:%s' % projectId
	}

	return sm.services().enable(serviceName=serviceName, body=body).execute()

def getServiceOperation(operation):

	return sm.operations().get(name=operation).execute()
