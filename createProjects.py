#!/usr/bin/env python

# import GoogleCredentials
from oauth2client.client import GoogleCredentials

# import build
from googleapiclient.discovery import build

# get application default credentials from gcloud
credentials = GoogleCredentials.get_application_default()

def getProjects():

	# build a resource manager service
	crm = build('cloudresourcemanager', 'v1', credentials=credentials)

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

def main():

	projects = getProjects()

if __name__ == "__main__":
	main()
