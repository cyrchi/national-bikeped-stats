# +
import zipfile
import urllib
import io
import pandas
import bs4
import requests
import re
import os
import sys


## input functions


def find_filename(name_list, file_list):
    """
    Output the exact name of a file by checking
    against a predefined list of filenames. Used to
    deal with different filename cases across years
    in FARS data.
    
    - name_list: predefined list of names
    - file_list: list of file names to search through
    """
    filename = "None" # initialize a filename variable
    
    # run through list of files
    for file in file_list:
        if file in name_list: # check if list of file is in predefined list
            filename = file # if so, set filename
    if filename == "None": # if not, raise error
        raise ValueError(
            'There were no matches between the predefined list {} and list {}'.format(name_list, file_list))
        
    return filename


def get_zip(url):
    """
    Modified from:
    citation: https://andrewpwheeler.com/2022/02/28/downloading-geo-files-from-census-ftp-using-python/
    """
    
    webpage = requests.get(url, verify=False)
    soup = bs4.BeautifulSoup(webpage.content,"html.parser")
    zip_files = soup.find_all("a", href=re.compile(r"zip")) # find anchor elements on page whose href contain "zip"
    zip_urls = [os.path.join(url, i["href"]) for i in zip_files] # join the webpage url to the file name for each file
    
    return zip_urls


def fetch_multi_csv_zip_from_url(url, filenames=[], *args, **kwargs):
    """
    Modified from:
    https://stackoverflow.com/questions/48843761/how-to-scrape-csv-
    files-from-a-url-when-they-are-saved-in-a-zip-file-in-pytho
    
    Uses the find_filename() function from this module.
    """
    assert kwargs.get('compression') is None
    
    req = urllib.request.urlopen(url)
    
    zip_file = zipfile.ZipFile(io.BytesIO(req.read()))
    
    names = zip_file.namelist() # get a list of files in the archive
    
    filename = find_filename(filenames, names) # find the right filename
    
    # check that the specified file names are actually in the zip
    if filename not in names:
        raise ValueError(
            'filename {} not in {}'.format(filename, names))
    
    # read the file into a dataframe
    df = pandas.read_csv(zip_file.open(filename), *args, **kwargs)
    return df



## cleaning & engineering functions


def remap_PER_TYP(person_file, year, combine=True):
    """
    This function remaps values in the person.csv file's
    PER_TYPE column across all years in NHTSA's Fatality 
    Analysis and Reporting System (FARS). The remapped
    values are based on the table on C-40 (PDF p.565) of
    the 2022 User Manual. Input:
    
     - person_file: a dataframe of the person.csv file
     - year: integer value of the year the file is from
    
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
    
    # replace per_typ column values with dictionary values based on year range
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
    
    
    if combine==True:
        
        # dict mapping multiple per_typs to one
        combine_dict = {
            "Other non-occupant": 'Other/unknown non-occupant', 
            "Unknown non-occupant type": 'Other/unknown non-occupant', 
            "Unknown person type": 'Other/unknown non-occupant'
        }
        
        # combine categories in per_typ column
        df["PER_TYP"].replace(
            to_replace=combine_dict,
            inplace=True
        )

    return  df


def join_count(points, polygons, groupby_col, count_col, unique_id):
    """
    This function counts the number of points in each polygon. If
    points lie on the boundaries of multiple polygons, the function
    assigns them based on the default args of pandas.drop_duplicates()
    
    - points: geodataframe of points
    - polygons: geodataframe of polygons
    - groupby_col: the unique ID of polygons
    - count_col: the name assigned to the count column in the output
    - unique_id: the unique ID (string or list-like) of points
    
    WARNING: this function returns modified input as output.
    """
    
    # spatial join polygon attributes to the points
    join = points.sjoin(polygons, how="left", predicate="intersects")
    
    # find and drop duplicates based on unique ID field(s)
    # any duplicates are likely the result of points on the boundary 
    # between two polygons
    join.drop_duplicates(subset=unique_id, inplace=True)  
    
    # group points by specified column
    grouped = join.groupby(by=groupby_col)
    
    # count the number of points in each group, and convert to dataframe
    counts = grouped.size().reset_index()
    
    # rename the count column to specified value
    counts.rename(columns={0: count_col}, inplace=True)
    
    # merge count column to polygons, maintaining polygons with no count
    polygons = polygons.merge(counts, on=groupby_col, how="left")
    
    # replace NaN in count column with 0
    polygons.fillna(value={count_col: 0}, inplace=True)
    
    return polygons
