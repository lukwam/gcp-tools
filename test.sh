#!/bin/sh

./run.sh createProjects.py \
	-t karlsson \
	-o 548622027621 \
	-b 00A539-93294F-AC9B6F \
	-i owner=user:karlsson@broadinstitute.org,editor=group:devops@broadinstitute.org \
	-a compute_component,storage-component-json.googleapis.com \
	-l costobject=broad-1234567,billingAccount=master \
	-u karlsson-compute-usage \
	-s cloudhealth,terraform \
	ltk-test-01 ltk-test-02 ltk-test-03

