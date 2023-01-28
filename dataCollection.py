#######################
### CSV FILE FORMAT ###
#######################
# Name (String) opt, TimeStamp (Date format), Drug name (String), Location (String), Particulates found (Boolean), Concetration of particulates (Float) opt

# Given drug test input data from user, add to database (csv file)

# Import needed libraries
import pandas as pd


# From javascript message (from website -> javaScript -> this script), format the data according to csv file
# Make sure that Name is compared uncapitalized
# Have a dict of names it can belong to
burroughDict = {
    ""
}