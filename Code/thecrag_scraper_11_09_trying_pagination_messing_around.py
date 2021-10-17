from bs4 import BeautifulSoup, SoupStrainer
import requests
import time
import re
import xlsxwriter
import os

print(os.getcwd())

list_of_ascents = []
#boulder_grades = ['v1', 'V1', 'v2', 'V2','v3', 'V3','v4', 'V4','v5', 'V5','v6', 'V6','v7', 'V7','v9', 'V9','v10', 'V10','v11', 'V11','v12', 'V12','v13', 'V13', 'v14', 'V14', 'v15', 'V15']
number_of_routes_counter = 0
number_of_routes_list = []
#counter_route_loop = 0

######### initialise stuff for xlsx writer
row = 1 # Due to heading
column = 0
workbook = xlsxwriter.Workbook('C:/Users/Declan/.atom/BlueMountainsRoutes_1starmin_grade_23_39_length_5_45m_sport_and_trad_appendv3.xlsx') #"C:\Users\Declan\.atom\thecrag_scraper_11_09_trying_pagination.py"
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'KeywordsS')

route_finder_url = ['https://www.thecrag.com/en/climbing/australia/blue-mountains/routes/with-stars/1/with-grade/AU:23:39/with-gear-style/trad+sport/length-between/5+10/?sortby=at,desc&page=1',
                    'https://www.thecrag.com/en/climbing/australia/blue-mountains/routes/with-stars/1/with-grade/AU:23:39/with-gear-style/trad+sport/length-between/10+20/?sortby=at,desc&page=1',
                    'https://www.thecrag.com/en/climbing/australia/blue-mountains/routes/with-stars/1/with-grade/AU:23:39/with-gear-style/trad+sport/length-between/20+45/?sortby=at,desc&page=1']

for m in range(0,len(route_finder_url)):

    page_number = 0
    number_of_routes = 0
    page = requests.get(route_finder_url[m])
    data = page.text
    soup = BeautifulSoup(data, "html.parser")
    max_routes = soup.findAll("div", {"class":"page-chooser center"})

    start_of_routes = str(max_routes)
    if "out of" in start_of_routes:
        out_of = start_of_routes.find('out of')
        end_of = start_of_routes.find(' routes')
        number_of_routes =  start_of_routes[(out_of)+len('out of '):end_of] #248
        print('number_of_routes', number_of_routes)
    else:
        "Showing all" in start_of_routes
        start = start_of_routes.find('Showing all')
        end = start_of_routes.find(' routes')
        number_of_routes =  start_of_routes[start+len('Showing all '):end]
        print('number_of_routes', number_of_routes)

    number_of_routes_counter = int(number_of_routes_counter) + int(number_of_routes)
    number_of_routes_list.append(int(number_of_routes))

    exit_condition = True

    while exit_condition:
        try:
            page_number += 1
            url = route_finder_url[m][:-1]+str(page_number)
            page = requests.get(url)
            data = page.text
            soup = BeautifulSoup(data, "html.parser")

            for link in soup.find_all('a'):

                if "/ascents" in str(link):
                    if "route" in str(link):
                        list_of_ascents.append('https://thecrag.com'+link.get('href'))

                        if int(len(list_of_ascents)) == sum(number_of_routes_list) or str(len(list_of_ascents)) ==number_of_routes_list:

                            print("finished list")
                            exit_condition = False
                            break

        except Exception as ex:
            print(ex)
            print('probably last page')
            break

    #print('starting route text analysis')
    print('\n')


#print(list_of_ascents)

print('total number of routes = ', len(list_of_ascents))
################################################################################
for route in range(0,len(list_of_ascents)):

    num_of_links = 0
    keyword_list = [] # used for comment keywords later on
    url_route = list_of_ascents[route].strip("''")
    page_route = requests.get(url_route)
    data_route = page_route.text
    soup_route = BeautifulSoup(data_route, "html.parser")
    route_text_raw = soup_route.findAll("div", {"class":"markdown"})

    ################################################################
    # looking for route name
    ################################################################
    url_route_main_page = list_of_ascents[route].strip("''")
    url_route_main_page = url_route_main_page.strip('/ascents')
    page_route_main_page = requests.get(url_route_main_page)
    data_route_main_page = page_route_main_page.text
    soup_route_main_page = BeautifulSoup(data_route_main_page, "html.parser")
    route_text_main_name = soup_route_main_page.findAll("span", {"itemprop":"name"})
    route_name = str(route_text_main_name)[len('[<span itemprop="name">'):str(route_text_main_name).find('</span>]')]

    ################################################################
    ################ looking for comment keywords## ################
    ################################################################
    comment_keywords = soup_route_main_page.findAll("div", {"class":"keywords cloud"})
    comment_keywords = str(comment_keywords)
    comment_keywords = comment_keywords.replace('</span>\n</span>',"</span>")

    for keyword in range(1,comment_keywords.count('em">')+1):
        comment_start = comment_keywords.find('em">')
        comment_end = comment_keywords.find('</span>')
        keyword = comment_keywords[comment_start+4:comment_end]

        fontsize_start = comment_keywords.find('font-size: ')
        fontsize_end =  comment_keywords.find('em">')
        fontsize = comment_keywords[fontsize_start+len('font-size: '):fontsize_end]
        fontsize = fontsize[0:5]#4 is 2 digits
        fontsize = float(fontsize)
        fontsize = round(fontsize,2)
        fontsize = str(fontsize)

        if keyword == "":
            continue

        # finding font size

        #print('fontsize ', fontsize)
        keyword_list.append(keyword+ " "+fontsize)

        comment_keywords = comment_keywords[comment_end+len('</span>')::]
        #keyword_list.append(fontsize)

        #comment_keywords = comment_keywords[comment_end+len('</span>')::]

    #
    #print(route+1, 'Route name', route_name, 'Grade AU', route_grade_AU, 'Route length', route_length, 'Quality', route_text_quality_final)
    print(route+1, 'Route name')
    print('\n')


    column = 0
    worksheet.write(row, column, str(keyword_list).replace("''","").replace('""',"")) #a
    column +=1

    row +=1

workbook.close()
