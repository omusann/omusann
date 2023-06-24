# library
import pylab as plt
from matplotlib_venn import venn3, venn3_circles
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd #imported pandas(data frame for manipulation) as pd to use do pd.function 
import datetime
from datetime import date
from datetime import datetime
from matplotlib_venn import venn2,venn3, venn3_circles
from fpdf import FPDF
import os
import psycopg2
!pip install fpdf2
from configparser import ConfigParser
import sendgrid
import os
#!pip install --upgrade pip           # upgrade pip to at least 20.3
#!pip install psycopg
#!pip install psycopg3-binary
#!pip install sendgrid
#pip install sendgrid==6.4.1

def venn_chart(toggle, data_location, data_group_txt, location, dates):

    orig_df = pd.DataFrame(pd.read_csv(data_location,header = 0, nrows = 1400))
    #TODO UPDATE nrows = length of data_location
    values = orig_df.groupby('subset_a')['subset_b'].value_counts()
    
    sub_b = len(orig_df[orig_df['subset_b']].index)
    sub_a =  len(orig_df[orig_df['subset_a']].index)
    print(sub_b, sub_a, len(orig_df))

    if(sub_b != len(orig_df)) and (sub_a != len(orig_df) and 
                                   (sub_a + sub_b < len(orig_df))):
        no_sub_a_sub_b = values[False][False]
    else: 
        no_sub_a_sub_b = 0
  
    
    if(sub_b + sub_a + no_sub_a_sub_b == len(orig_df)):
        sub_a_sub_b = 0
    else:
        sub_bmh = values[True][True]
    
    length = len(orig_df)
    no_sub_a = length - sub_b
    
    v = venn2(subsets = (sub_b - sub_a_sub_b, sub_a - sub_a_sub_b, sub_a_sub_b),
               set_labels = ('Population Classification Subset B',
                              'Population Classification Subset A'))
    plt.title(data_group_txt)
    tablej = plt.table(cellText=[ [length], [sub_b], [sub_a], [sub_a_sub_b],
                                  [no_sub_a_sub_b] ], colWidths = [.5]*9,
                       rowLabels=["Number of Discoveries", 
                                  "Population Classification Subset B","Population Classification Subset A" ,
                                    "Population Classification Subset B AND Population Classification Subset A",
                                  "Number of Discoveries without Population Classification Subset B AND Population Classification Subset A"],
                        loc='left',bbox=[1.0,-0.45,1,.28])
    
    if toggle == 'png':
        title = data_group_txt.replace(" ", "_")
        plt.savefig("graphs/" + dates + "/" + location + "/" + title+'_.png',
                     bbox_inches = "tight", pad_inches = 1/4)  
    
    if toggle == 'print':
        plt.show() 
    
    plt.cla()
    plt.clf()

def age(toggle, orig_df, data_group_txt, location, dates):
    
    orig_df["Age"] = ""
    if(len(orig_df) > 0):
        
        for k in range(0, len(orig_df)):
            todaysDate = date.today()
            date_dob = datetime.strptime(orig_df.iloc[k].dob, '%Y-%m-%d')
            #https://www.geeksforgeeks.org/python-program-to-calculate-age-in-year/
            orig_df.at[k, 'Age'] = todaysDate.year - date_dob.year -((
                todaysDate.month, todaysDate.day) < (date_dob.month, date_dob.day))

        bins = [18, 30, 40, 50, 120]
        mylabely = ['18-29', '30-39', '40-49', '50+']
        orig_df['age_range'] = pd.cut(orig_df.Age, bins, labels = mylabely,include_lowest = True)

        num_18 = len(orig_df[orig_df['age_range'].isin(['18-29'])].index)
        num_30 = len(orig_df[orig_df['age_range'].isin(['30-39'])].index)
        num_40 = len(orig_df[orig_df['age_range'].isin(['40-49'])].index)
        num_50 = len(orig_df[orig_df['age_range'].isin(['50+'])].index)

        length = len(orig_df)
        ages = num_18 + num_30 + num_40 + num_50

        y = np.array([num_18, num_30,num_40,num_50])

        plt.pie(y, startangle = 90)
        y_leg = plt.legend(mylabely, bbox_to_anchor = (1.04,0.5), loc = "center left", borderaxespad = 0)
        plt.title("Variations in Age: \n "+data_group_txt)
        table = plt.table(cellText = [[num_18], [num_30],[num_40],[num_50]],colWidths = [.5]*9,
                          rowLabels = mylabely, loc = 'bottom')

        if length == ages:

            if toggle == 'png':
                title = data_group_txt.replace(" ", "_") 
                plt.savefig("graphs/" + dates + "/" + location + "/" + title + "_age.png",
                            bbox_inches = "tight", pad_inches = 1/4) 

            if toggle == 'print':
                plt.show() 

        if length != ages:

            print("ERROR all ages added up = ", ages, 
                  "all rows of origianal csv = ", length, "check DOB for erronious values")

        plt.cla()
        plt.clf()   
        num_18 = num_30 = num_40 = num_50 = y = length = ages = 0
    else: 
        print("no data")

def gender(toggle, orig_df, data_group_txt,location,dates):
    
    ##creation of variables for chart 
    male = len(orig_df[orig_df['gender'].isin(['M'])].index)
    female = len(orig_df[orig_df['gender'].isin(['F'])].index)
    other =  len(orig_df[orig_df['gender'].isin(['O'])].index)
    non_binary = len(orig_df[orig_df['gender'].isin(['NB'])].index)
    
    ##data manipulation of what total is 
    # the length of the DF for checks of data 
    length = len(orig_df)
    if length > 0:
        genders = male + female + other + non_binary

        #array creation for graph of variables
        y = np.array([male, female, other, non_binary])
        mylabely = ["Male", "Female","Other", "N/B"]

      #creation of table with title, pie chart, legend, table 
        plt.title("Variations in Gender: \n "+data_group_txt)
        plt.pie(y, startangle = 90)
        y_leg = plt.legend(mylabely,bbox_to_anchor=(1.04,0.5), 
                           loc="center left", borderaxespad=0)
        tabley = plt.table(cellText=[[male],[female],[other], 
                                     [non_binary]],colWidths = [.5]*9,
                           rowLabels = mylabely,loc='bottom')

        #if length of DF == genders print everything as in toggle 
        if length == genders:

            if toggle == 'png':
                title = data_group_txt.replace(" ", "_")
                plt.savefig("graphs/"+dates+"/"+location+"/"+
                            title+"_gender.png", 
                            bbox_inches="tight", pad_inches=1/4) 

            if toggle == 'print':
                plt.show() 

        #if length of df =! genders add error statment 
        if length != genders:
            print("ERROR all genders added up = ",length,
                   "all rows of origianal csv = ", genders, 
                   "check gender for NA values")

        #clear data
        plt.cla()
        plt.clf()
        male = female = other = y = mylabely = length = genders = non_binary = 0
    else: 
        print("no data")

def ethnicity(toggle, orig_df, data_group_txt, location, dates):
    
    AA = len(orig_df[orig_df['ethnicity'].isin(['AA'])].index)
    BA = len(orig_df[orig_df['ethnicity'].isin(['BA'])].index)
    HS = len(orig_df[orig_df['ethnicity'].isin(['HS'])].index)
    NAT = len(orig_df[orig_df['ethnicity'].isin(['NAT'])].index)
    NH = len(orig_df[orig_df['ethnicity'].isin(['NH'])].index)
    ME = len(orig_df[orig_df['ethnicity'].isin(['ME'])].index)
    WA = len(orig_df[orig_df['ethnicity'].isin(['WA'])].index)
    O = len(orig_df[orig_df['ethnicity'].isin(['O'])].index)
    #N_A = 0
    
    length = len(orig_df)
    if length>0:
        ethnicities = AA + BA + HS + NAT + NH + ME + WA + O
        N_A = length - ethnicities
        
        y = np.array([AA, BA, NAT, HS, NH, ME, WA, O, N_A])
        mylabely = ["Asian American: ", "Black/African American: ", 
                    "Native American: ", "Hispanic/Latino: ", 
                    "White American: ", "Other: ", "N/A: "]

        y_pie = plt.pie(y, startangle = 90)
        y_title = plt.title("Variations in Ethnicity: \n " + data_group_txt)
        y_leg = plt.legend(mylabely, bbox_to_anchor = (1.04,0.5), 
                           loc = "center left", borderaxespad=0)
        y_table = table = plt.table(cellText = [[AA], 
                                                [BA], [NAT], [HS], 
                                                [WA], [O], [N_A]],
                      colWidths = [.5]*9,rowLabels = mylabely)
        #plt.show() 
        if length == ethnicities + N_A:
            if toggle == 'png':
                title = data_group_txt.replace(" ", "_")
                plt.savefig("graphs/" + dates + "/" + location + "/" + 
                            title + "_ethnicity.png", 
                            bbox_inches = "tight", pad_inches = 1/4) 
                            
                
            if toggle == 'print':
                plt.show()   

        if length != ethnicities + N_A:
            print("ERROR all ethnicities added up = ",ethnicity, 
                  "all rows of origianal csv = ", length, 
                  "check Native american NA for erronious values")

        plt.cla()
        plt.clf()
        AA = BA = HS = NAT = WA = O = N_A = 0
        y = mylabely = length = ethnicities = 0
    else: 
        print("no data")

def png_main(toggle, data_location, title_txt,location,dates,venn_toggle):

    print(toggle)
    print(data_location)
    #this main begins the program to make 3 report pie charts 
    #manually converts text file into DF 
    #calls each graph to print or png
    
    orig_df = pd.DataFrame(pd.read_csv(data_location,header=0,nrows=1400))
    #TODO UPDATE nrows = length of data_location 
    
    ethnicity(toggle, orig_df, title_txt, location, dates)
    gender(toggle, orig_df, title_txt, location, dates)
    age(toggle, orig_df, title_txt,location, dates)
    
    if venn_toggle == 'ven_on' and (title_txt == 'Population Classification'):
        venn_chart(toggle, data_location, title_txt, location, dates)
        
def create_directory(Month_year, location_names):

    # Get the current working directory
    cwd = os.getcwd()
    #if running first name make folders datasets graphs 
    # and finished reports where this code is held 
    path_datasets = os.path.join(cwd, 'datasets/' + Month_year)
    path_graphs = os.path.join(cwd, 'graphs/'+ Month_year)
    path_finished = os.path.join(cwd, 'Finished Reports/'+ Month_year) 
    
    os.mkdir(path_finished)
    os.mkdir(path_datasets)
    os.mkdir(path_graphs)

    for x in location_names:
        path = os.path.join(path_graphs,x)
        os.mkdir(path)
        
    for x in location_names:
        path = os.path.join(path_datasets,x)
        os.mkdir(path)
        
def call_png_report(Month_year, location_names, title_txt):
    
    cwd = os.getcwd()
    path = os.path.join(cwd, 'datasets/' + Month_year)
    
    for x in location_names:
        #venn may give issues
        print(x)
        venn_chart('png', path + '/' + x + '/Population Classification.csv'
                   , 'Population Classification',x , Month_year)
       
        for y in title_txt: 
            path2 = os.path.join(path,x  )
            print(path+'/'+x)
            png_main("png",path+'/'+x+'/' + y +'.csv',y ,x ,
                     Month_year, "ven_off")

def query_db(Month_year, location_names, title_txt,month_on):
    #using: https://www.psycopg.org/docs/cursor.html
    #using https://kb.objectrocket.com/postgresql/from-postgres-to-csv-with-python-910 
    #https://www.psycopg.org/docs/usage.html
    #https://www.psycopg.org/docs/cursor.html#cursor-iterable
    #https://www.pythontutorial.net/python-basics/python-write-csv-file/
    #https://www.pythontutorial.net/python-basics/python-write-csv-file/
    import sys
    import calendar
    import datetime
    import csv
     
    monthDict={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,'May':5,'Jun':6, 
               'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    
    if month_on != 'other':
        currmonth = Month_year[0]+Month_year[1]+Month_year[2]

        month_num = monthDict[currmonth]

        yrlen = len(Month_year)

        year_num = Month_year[yrlen-4] + Month_year[yrlen-3] + Month_year[yrlen-2] + Month_year[yrlen-1]

        print(year_num)

        date = datetime.date(2023,month_num,1)

        max_days = "%s" % calendar.monthrange(date.year, date.month)[1]

        print(max_days)

        month_num = "%s" % month_num
 
    conn = None
    cwd = os.getcwd()
        # read connection parameters
    params = config()

        # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

        # create a cursor
    cur = conn.cursor()

	# execute a statement        
    select = 'dob, gender, ethnicity, Population Classification Subset A, Population Classification Subset B '
    header = ['dob','gender','ethnicity','Population Classification Subset A','Population Classification Subset B']  
    
    if month_on == 'yes':
        
        dates =  '''created_at BETWEEN '2023-'''+month_num+'''-1 00:00:00.00' AND '2023-'''+month_num+'''-''' +max_days+''' 23:59:00.00' '''
    
    if month_on == 'other':
        dates = '''created_at BETWEEN '2023-'''+ '2' +'''-1 00:00:00.00' AND '2022-'''+ '3' +'''-''' + '30' +''' 23:59:00.00' '''
    
    if month_on == 'no':
        
        dates =   '''created_at BETWEEN '2022-'''+month_num+'''-1 00:00:00.00' AND '2023-'''+month_num+'''-''' + '1' +''' 00:00:00.00' '''

    for x in location_names:
        
        for y in title_txt:
            
            s =  "SELECT " + select + " FROM DISCOVERY WHERE location = '" + x + "' AND " + dates
           
            if y == "Population Classification Subset A":
                s += " AND Population Classification Subset A =  'true'"
                    
            if y == "Population Classification Subset B":  
                s += " AND Population Classification Subset B = 'true'"
            
            if y == "Population Classification Subset A AND Population Classification Subset B":
                s += " AND Population Classification Subset A = 'true' AND Population Classification Subset B = 'true'"
            

            SQL_for_file_output = s+';'
                      
            path_datasets = os.path.join(cwd, 'datasets/' + Month_year+'/'+ x + '/' + y + '.csv')
            print(path_datasets + '\n')
               
            #csv_file = open(path_datasets, 'w')
            #with closes file 
            with open(path_datasets, 'w') as f_output:
               
                cur.execute(SQL_for_file_output)
                test = cur.fetchall()
                myfile = csv.writer(f_output)
                myfile.writerow(header)
                myfile.writerows(test)
                
            
            path_datasets = 0    
            s = 0
                
    cur.close()
    conn.close()
            
    print('Database connection closed.')
    
"""main report controlls program 

    creates variables and sets up data to send to other functions 

    Args:
        to invoke simplicity the first few and last 
        few char of one arg are significant in the 
        format (monthyear) where month is the name and 
        year is a number

    Returns:
       print statment of finished 

    Raises:
        nothing
    """
def main_report(Month_year):
    
    month_year = Month_year
    
    location_names = ['location_1', 'location_2', 'location_3']
    
    title_txt = ['Population Classification', 
                 'Population Classification Subset A', 
                 'Population Classification Subset B',
                 'Population Classification Subset A and B']
    month_on = 'yes'
    
    create_directory(Month_year, location_names)
    
    query_db(Month_year, location_names, title_txt,month_on)
    
    call_png_report(Month_year, location_names, title_txt)
    
    cwd = os.getcwd()
    path = os.path.join(cwd, 'graphs/' + Month_year)
    path_data = os.path.join(cwd,'datasets/'+Month_year)
    
    for x in location_names:
        length = len(pd.DataFrame
                     (pd.read_csv(path_data + '/' +x 
                                  +'/Population_Classification.csv',
                                  header = 0, nrows = 1400)))
    return(print("finished!"))
    

    
