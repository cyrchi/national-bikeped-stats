def remap_PER_TYP(person_file, year):
    """
    This function remaps values in the person.csv file's
    PER_TYPE column across all years in NHTSA's Fatality 
    Analysis and Reporting System (FARS). The remapped
    values are based on the table on C-40 (PDF p.565) of
    the 2022 User Manual. Input:
    
     - person_file: a dataframe of the person.csv file
     - year: numeric value of the year the file is from
    
    """
    per_typ_75_81 = {
        1: "Driver",
        2: "Passenger",
        9: "Passenger",
        5: "Other non-occupant",
        3: "Pedestrian",
        4: "Bicyclist", # changed from pedalcyclist
        8: "Other/unknown non-occupant"
    }

    per_typ_82_93 = {
        1: "Driver",
        2: "Passenger",
        9: "Passenger",
        3: "Other non-occupant",
        4: "Other non-occupant",
        5: "Pedestrian",
        6: "Bicyclist", # changed from pedalcyclist
        7: "Bicyclist", # changed from pedalcyclist
        8: "Other/unknown non-occupant"
    }

    per_typ_94_04 = {
        1: "Driver",
        2: "Passenger",
        9: "Passenger",
        3: "Other non-occupant",
        4: "Other non-occupant",
        5: "Pedestrian",
        6: "Bicyclist", # changed from pedalcyclist
        7: "Bicyclist", # changed from pedalcyclist
        8: "Other non-occupant",
        19: "Unknown non-occupant type",
        99: "Unknown person type"
    }

    per_typ_05_06 = {
        1: "Driver",
        2: "Passenger",
        9: "Passenger",
        3: "Other non-occupant",
        4: "Other non-occupant",
        5: "Pedestrian",
        6: "Bicyclist", # changed from pedalcyclist
        7: "Bicyclist", # changed from pedalcyclist
        8: "Other non-occupant",
        19: "Unknown non-occupant type",
    }

    per_typ_07_19 = {
        1: "Driver",
        2: "Passenger",
        9: "Passenger",
        3: "Other non-occupant",
        4: "Other non-occupant",
        5: "Pedestrian",
        6: "Bicyclist", # changed from pedalcyclist
        7: "Bicyclist", # changed from pedalcyclist
        8: "Other non-occupant",
        10: "Other non-occupant",
        19: "Unknown non-occupant type",
        88: "Unknown person type"
    }

    per_typ_20_plus = {
        1: "Driver",
        2: "Passenger",
        9: "Passenger",
        3: "Other non-occupant",
        4: "Other non-occupant",
        5: "Pedestrian",
        6: "Bicyclist", # changed from pedalcyclist
        7: "Bicyclist", # changed from pedalcyclist
        8: "Other non-occupant",
        10: "Other non-occupant",
        11: "Other non-occupant",
        12: "Other non-occupant",
        13: "Other non-occupant",
        19: "Unknown non-occupant type",
    }
    
    
    df = person_file.copy() # copy the dataframe to avoid pandas SetWithCopy error

    if year in range(1975, 1982):
        df["PER_TYP"].replace(to_replace=per_typ_75_81, inplace=True)
    elif year in range(1982, 1994):
        df["PER_TYP"].replace(to_replace=per_typ_82_93, inplace=True)
    elif year in range(1994, 2005):
        df["PER_TYP"].replace(to_replace=per_typ_94_04, inplace=True)
    elif year in range(2005, 2007):
        df["PER_TYP"].replace(to_replace=per_typ_05_06, inplace=True)
    elif year in range(2007, 2020):
        df["PER_TYP"].replace(to_replace=per_typ_07_19, inplace=True)
    else:
        df["PER_TYP"].replace(to_replace=per_typ_20_plus, inplace=True) # may need to modified annually
    
    return  df
