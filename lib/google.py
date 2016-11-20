#!/usr/bin/env python
"""Functions for calling Google APIs."""

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

def enable_project_billing(project_id, billing_account_name):
    """

    Function: enable_project_billing

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

    return cb.projects().updateBillingInfo(**params).execute()

def get_billing_accounts():
    """

    Function: get_billing_accounts

    Google Cloud Billing API - billingAccounts().list()

    Returns:

      return list of billing accounts
    """
    # create a request to list billingAccounts
    request = cb.billingAccounts().list()

    # create a list to hold all the projects
    billing_accounts = []

    # page through the responses
    while request is not None:

        # execute the request
        response = request.execute()

        # add projects to the projects list
        if 'billingAccounts' in response:
            billing_accounts.extend(response['billingAccounts'])

        request = cb.billingAccounts().list_next(request, response)

    return billing_accounts

#
# Compute
#
compute = build('compute', 'v1', credentials=credentials)

def set_project_usgae_export_bucket(project_id, bucket_name):
    """

    Function: set_project_usgae_export_bucket

    description

    Parameters:

      project_id  - [type/description]
      bucket_name - [type/description]

    Returns:

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

    return compute.projects().setUsageExportBucket(**params).execute()

#
# Cloud Resource Manager (cloudresourcemanager)
#
crm = build('cloudresourcemanager', 'v1', credentials=credentials)

def create_project(project):
    """Returns a created project."""
    try:
        return crm.projects().create(body=project).execute()
    except Exception as exception:
        print '[%s]' % exception._get_reason()
        return {}

def get_organizations():
    """Returns a list of organizations."""
    # create a request to list organizations
    response = crm.organizations().search(body={}).execute()

    return response['organizations']

def get_project(project_id):
    """Returns a project."""
    # create a request to list projects
    return crm.projects().get(projectId=project_id).execute()

def get_projects():
    """

    Function: get_projects

    description

    Returns:

      return description
    """
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

def update_project(project_id, body):
    """Returns an updated project."""
    try:
        return crm.projects().update(projectId=project_id, body=body).execute()
    except Exception as exception:
        print '[%s]' % exception._get_reason()
        return {}
#
# IAM (Identity and Access Management)
#
iam = build('iam', 'v1', credentials=credentials)

def create_service_account(project_id, account_id, display_name=None):
    """

    Function: create_service_account

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

    try:
        return iam.projects().serviceAccounts().create(**params).execute()
    except Exception as exception:
        print '[%s]' % exception._get_reason().split('/')[-1]
        return {}

#
# Service Management
#
sm = build('servicemanagement', 'v1', credentials=credentials)

def enable_project_service(project_id, service_name):
    """Returns an enabled project service response."""
    body = {
        'consumerId': 'project:%s' % project_id
    }

    return sm.services().enable(serviceName=service_name, body=body).execute()

def get_service_operation(operation):
    """Returns an operation."""
    return sm.operations().get(name=operation).execute()
