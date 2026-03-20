"""
File: voter_analytics/models.py
author: Jerry Teixeira (jerrybt@bu.edu), 03/20/26
Description: Data model for registered Newton voters and CSV import loader.
"""

from django.db import models

# Voter model and CSV import helper for this app.

class Voter(models.Model):
    '''
    Store/represent one registered voter record for Newton, MA.
    '''
    # Core identity fields used in list/detail output.
    # identification
    voter_id_number = models.TextField(blank=True, null=True)
    first_name = models.TextField()
    last_name = models.TextField()
    residential_address_street_number = models.TextField()
    residential_address_street_name = models.TextField()
    residential_address_apartment_number = models.TextField(blank=True, null=True)
    residential_address_zip_code = models.TextField()

    # participation / voter info
    date_of_birth = models.TextField()
    date_of_registration = models.TextField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()

    # elections
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    # election score
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.precinct_number})'


def load_data():
    '''Function to load voter records from CSV file into Django model instances.'''
    # Clear previous records before bulk re-load.
    # VERY DANGEROUS!
    Voter.objects.all().delete()

    filename = '/Users/jerryteixeira/Desktop/CS412/newton_voters.csv'
    # Open the assignment data file and skip header row.
    f = open(filename, 'r')
    f.readline()  # discard headers

    for line in f:
        try:
            # Parse one CSV row and map each column to a model field.
            fields = line.strip().split(',')

            # 0 = Voter ID Number (not required, but preserved)
            # 1 = Last Name
            # 2 = First Name
            # 3 = Residential Address - Street Number
            # 4 = Residential Address - Street Name
            # 5 = Residential Address - Apartment Number
            # 6 = Residential Address - Zip Code
            # 7 = Date of Birth
            # 8 = Date of Registration
            # 9 = Party Affiliation
            # 10 = Precinct Number
            # 11 = v20state
            # 12 = v21town
            # 13 = v21primary
            # 14 = v22general
            # 15 = v23town
            # 16 = voter_score

            voter = Voter(
                voter_id_number = fields[0],
                last_name = fields[1],
                first_name = fields[2],
                residential_address_street_number = fields[3],
                residential_address_street_name = fields[4],
                residential_address_apartment_number = fields[5],
                residential_address_zip_code = fields[6],
                
                date_of_birth = fields[7],
                date_of_registration = fields[8],
                party_affiliation = fields[9],
                precinct_number = fields[10],

                v20state = fields[11].strip().lower() == 'true',
                v21town = fields[12].strip().lower() == 'true',
                v21primary = fields[13].strip().lower() == 'true',
                v22general = fields[14].strip().lower() == 'true',
                v23town = fields[15].strip().lower() == 'true',

                voter_score = fields[16],
            )
            voter.save() # Commit this voter to the database.
        except:
            # Skip malformed rows while continuing the import batch.
            print("Something went wrong!")
            print(f"Skipped={fields}")

    print(f"Done. Created {len(Voter.objects.all())} voters")
