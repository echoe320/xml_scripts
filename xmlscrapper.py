import os
from pathlib import Path, PureWindowsPath
import pandas as pd
from xml.etree import cElementTree as ET

#Empty Cells to keep information:

titles = []
creators = []
keywords = []
rights = []
abstracts = []
datecreated = []
subjects = []
resourcetypes = []
restrictions = []
embargodates = []
pdf_files = []

#Traverse a directory for .xml files

directory_name = r'C:\Users\echoe\Desktop\xml script'

all_files = {}
for root, dirs, files in os.walk(directory_name):
    for file in files:
        if file.endswith('.xml'): 
            all_files[file] = Path(root, file)
        elif file.endswith('.pdf'):
            pdf_files.append(Path(root,file))

'''
def get_info(name, int_id, fin_id):
    for item in root.findall(int_id):
        for item in :
            if (child.tag == fin_id):
                b = item.find(fin_id).text
                name.append(b)
            else:
                get_info(name, child, fin_id)


def get_info(name, id1, id2):
    for a in root.findall(id1):
        b = a.find(id2).text
        name.append(b)

def get_name():
    for a in root.findall('DISS_authorship'):
        for b in a.findall('DISS_author'):
            for c in b.findall('DISS_name'):
                d = c.find('DISS_surname').text
                e = c.find('DISS_fname').text
                f = c.find('DISS_middle').text
                g = c.find('DISS_suffix').text

                n = (g, e, f, d)
                creators.append(n)
'''
#Functions to traverse xml for data

def get_title():
    title = root[1][0].text
    titles.append(title)

def get_name():
    surname = root[0][0][0][0].text
    fname = root[0][0][0][1].text
    middle = root[0][0][0][2].text
    suffix = root[0][0][0][3].text

    n = (suffix, fname, middle, surname)
    creators.append(n)

def get_keywords():
    for kw in root.findall('DISS_description'):
        for a in kw.findall('DISS_categorization'):
            b = a.find('DISS_keyword').text
            if (b == None):
                b = a[0][1].text
            keywords.append(b)

def get_rights():
    rights.append("In Copyright")

def get_abs():
    n = []
    abstract = root[2][0] 
    for child in abstract:
        n.append(child.text)
    abstracts.append(n)

def get_datecreated():
    dc = root[1][1][1].text
    datecreated.append(dc)

def get_subjects():
    sub = root[1][3][2].text
    subjects.append(sub)

def get_resourcetype():
    resourcetypes.append("Dissertation")

def get_restriction():
    if (root[3]):
        rest = root[3][0].attrib
        if (rest['code'] == '0'):
            t = "Open Access" + rest['remove']
            restrictions.append(t)
        else:
            t = "code: " + rest['code'] + ", date: " + rest['remove']
            restrictions.append(t)
    else:
        restrictions.append("None")

def get_embdate():
    embd = root.attrib
    ed = embd['embargo_code']
    if (ed == "0"):
        embargodates.append("no embargo")
    elif (ed == "1"):
        embargodates.append("6 month embargo")
    elif (ed == "2"):
        embargodates.append("1 year embargo")
    elif (ed == "3"):
        embargodates.append("2 year embargo")
    else:
        embargodates.append("Private")
#Function Calls

directpaths = list(all_files.values())
for file in directpaths:
    tree = ET.parse(file)
    root = tree.getroot()
    
    get_title()
    get_name()
    get_keywords()
    get_rights()
    get_abs()
    get_datecreated()
    get_subjects()
    get_resourcetype()
    get_restriction()
    get_embdate()

#putting into CSV file
xml_data = pd.DataFrame({
"Title": titles,
"Creator": creators,
"Keyword": keywords,
"Rights": rights,
"Abstract": abstracts,
"Date Created": datecreated,
"Subject": subjects,
"Resource Type": resourcetypes,
"Restrictions": restrictions,
"Embargo Dates": embargodates,
"PDF Files": pdf_files
})

#save link (change to where you want to save it)
xml_data.to_csv('xml_data.csv')