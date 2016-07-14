#!/usr/bin/python

### THIS FILE SUPPLIES CONSTANTS TO webapp.wsgi ###

if (__name__=="__main__"):
    print("This file is imported by webapp.wsgi")
    print("and is not intended to be run.")
    print("Exiting...")
    exit()

csvFilename = "txe1_node_hwtab.csv"

adminEmail = "admin"

# the downloaded zipped keys file will use the cluster name
clusterName = "engaging"

# will suppress sending mail to additional receivers
devMode = False
