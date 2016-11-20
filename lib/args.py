#!/usr/bin/env python
"""Default functions for working with command-line arguments."""


def create_arg_parser():
    """Return an parser that handles all the arguments."""
    import argparse

    # create a new argument parser
    parser = argparse.ArgumentParser(
        description='Create projects'
    )

    apis_example = 'compute_component,storage-component-json.googleapis.com'
    parser.add_argument(
        '-a',
        '--apis',
        action='store',
        default=None,
        help='API services to enable (ex. %s)' % apis_example,
    )

    parser.add_argument(
        '-b',
        '--billing_account',
        action='store',
        default=None,
        help='Billing account (ex. ABCDEF-012345-6789FE)',
    )

    parser.add_argument(
        '-f',
        '--folder',
        action='store',
        default=None,
        help='Folder (ex. 123456789098)'
    )

    iam_policy_example = 'owner=user:email@domain.com'
    iam_policy_example += ',editor=group:group@domain.com'

    parser.add_argument(
        '-i',
        '--iam_policy',
        action='store',
        default=None,
        help='IAM Policy (ex. %s)' % iam_policy_example
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
        '--service_accounts',
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
        '--usage_bucket',
        action='store',
        default=None,
        help='Usage Bucket for Compute (ex. my-compute-usage-bucket)'
    )

    # at least project_id is required
    parser.add_argument('project_id', nargs='+')

    return parser
