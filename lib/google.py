#!/usr/bin/env python
"""Classes for calling Google APIs."""

# import modules
from apiclient import http as apihttp
import io
import json
import logging

# import discovery.build, errors
from googleapiclient.discovery import build
from googleapiclient import errors

# import GoogleCredentials
from oauth2client.client import GoogleCredentials

# enable logging
logging.basicConfig(filename='logs/debug.log', level=logging.DEBUG)


# Google Class
class Google(object):
    """Class with methods for working with Google APIs."""

    def __init__(self):
        """Initialize."""
        self.billing = None
        self.compute = None
        self.crm = None
        self.iam = None
        self.smgt = None
        self.storage = None

    def auth(self):
        """Athenticate with gcloud application-default credentials."""
        # get application-default credentials from gcloud
        credentials = GoogleCredentials.get_application_default()

        #
        # build the various services that we'll need
        #

        # build a cloud billing API service
        self.billing = build('cloudbilling', 'v1', credentials=credentials)

        # build a compute API service
        self.compute = build('compute', 'v1', credentials=credentials)

        # build a cloud resource manager API service
        self.crm = build('cloudresourcemanager', 'v1', credentials=credentials)

        # build an iam API service
        self.iam = build('iam', 'v1', credentials=credentials)

        # build a service management API service
        self.smgt = build('servicemanagement', 'v1', credentials=credentials)

        # build a service management API service
        self.storage = build('storage', 'v1', credentials=credentials)

    #
    # Cloud Billing API (cloudbilling)
    #
    def enable_project_billing(self, project_id, billing_account_name):
        """

        Function: enable_project_billing.

        Google Cloud Billing API - projects().updateBillingInfo()

        Parameters:

          project_id         - [type/description]
          billing_account_name - [type/description]

        Returns:

          return response
        """
        body = {
            'project_id': project_id,
            'billingAccountName': billing_account_name,
            'billingEnabled': True,
        }

        params = {
            'name': 'projects/%s' % project_id,
            'body': body,
        }

        return self.billing.projects().updateBillingInfo(**params).execute()

    def get_billing_accounts(self):
        """

        Function: get_billing_accounts.

        Google Cloud Billing API - billingAccounts().list()

        Returns:

          return list of billing accounts
        """
        # create a request to list billingAccounts
        billing_accounts = self.billing.billingAccounts()
        request = billing_accounts.list()

        # create a list to hold all the projects
        billing_accounts_list = []

        # page through the responses
        while request is not None:

            # execute the request
            response = request.execute()

            # add projects to the projects list
            if 'billingAccounts' in response:
                billing_accounts_list.extend(response['billingAccounts'])

            request = billing_accounts.list_next(request, response)

        return billing_accounts_list

    #
    # Compute
    #
    def set_project_usgae_export_bucket(self, project_id, bucket_name):
        """

        Function: set_project_usgae_export_bucket.

        description

        Parameters:

          project_id  - [type/description]
          bucket_name - [type/description]

        Return:

          return description
        """
        body = {
            'bucketName': bucket_name,
            'reportNamePrefix': 'usage',
        }

        params = {
            'project': project_id,
            'body': body,
        }

        return self.compute.projects().setUsageExportBucket(**params).execute()

    #
    # Cloud Resource Manager (cloudresourcemanager)
    #
    def create_project(self, project):
        """Return a created project."""
        try:
            return self.crm.projects().create(body=project).execute()
        except errors.HttpError, httperror:
            error = json.loads(httperror.content)['error']
            print '[%s]' % error['message']
            return {}

    def get_organizations(self):
        """Return a list of organizations."""
        # create a request to list organizations
        org_search = self.crm.organizations().search(body={})
        response = org_search.execute()

        return response['organizations']

    def get_project(self, project_id):
        """Return a project."""
        # create a request to list projects
        return self.crm.projects().get(projectId=project_id).execute()

    def get_projects(self):
        """

        Function: get_projects.

        description

        Returns:

          return description
        """
        # create a request to list projects
        request = self.crm.projects().list()

        # create a list to hold all the projects
        projects = []

        # page through the responses
        while request is not None:

            # execute the request
            response = request.execute()

            # add projects to the projects list
            if 'projects' in response:
                projects.extend(response['projects'])

            request = self.crm.projects().list_next(request, response)

        return projects

    def update_project(self, project_id, body):
        """Return an updated project resource."""
        params = {
            'projectId': project_id,
            'body': body,
        }
        projects_update = self.crm.projects().update(**params)
        try:
            return projects_update.execute()
        except errors.HttpError as httperror:
            error = json.loads(httperror.content)['error']
            print '[%s]' % error['message']
            return {}

    #
    # IAM (Identity and Access Management) API (iam)
    #
    def create_service_account(
            self,
            project_id,
            account_id,
            display_name=None
    ):
        """

        Function: create_service_account.

        description

        Parameters:

          project_id   - [type/description]
          account_d    - [type/description]
          display_name - [type/description]

        Returns:

          return description
        """
        # set displayName
        if not display_name:
            display_name = account_id

        params = {
            'name': 'projects/'+project_id,
            'body': {
                'accountId': account_id,
                'serviceAccount': {
                    'displayName': display_name,
                },
            },
        }

        iam_service_accounts = self.iam.projects().serviceAccounts()
        try:
            return iam_service_accounts.create(**params).execute()
        except errors.HttpError as httperror:
            error = json.loads(httperror.content)['error']
            print '[%s]' % error['message'].split('/')[-1]
            return {}

    #
    # Service Management API (servicemanagement)
    #
    def enable_project_service(self, project_id, service_name):
        """Return an enabled project service response."""
        body = {
            'consumerId': 'project:%s' % project_id
        }
        params = {
            'serviceName': service_name,
            'body': body,
        }
        return self.smgt.services().enable(**params).execute()

    def get_service_operation(self, operation):
        """Return an operation."""
        return self.smgt.operations().get(name=operation).execute()

    #
    # Storage API (storage)
    #
    def get_bucket_object(self, bucket_name, object_name):

        params = {
            'bucket': bucket_name,
            'object': object_name,
        }

        # get the storage object media
        request = self.storage.objects().get_media(**params)

        # The BytesIO object may be replaced with any io.Base instance.
        media = io.BytesIO()

        # create downloader
        downloader = apihttp.MediaIoBaseDownload(media, request, chunksize=1024*1024)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        return media
