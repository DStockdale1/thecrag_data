'''
Thecrag scraper is now completely updated with modifcications from the other messing around file as of 28-09
Only issue is how keywords are printed as l have no idea how I want to parse them for analysis

To do
- Run code on nowra/shoalhaven area
- Run code on arapilies and grampians
- Run code on other climbing areas (maybe metro sydney)
'''

from bs4 import BeautifulSoup, SoupStrainer
import requests
import time
import re
import xlsxwriter
import os

print(os.getcwd())

list_of_ascents = []
boulder_grades = ['v1', 'V1', 'v2', 'V2','v3', 'V3','v4', 'V4','v5', 'V5','v6', 'V6','v7', 'V7','v9', 'V9','v10', 'V10','v11', 'V11','v12', 'V12','v13', 'V13', 'v14', 'V14', 'v15', 'V15']
number_of_routes_counter = 0
number_of_routes_list = []

######### initialise stuff for xlsx writer
row = 1 # Due to heading
column = 0
workbook = xlsxwriter.Workbook('C:/Users/Declan/.atom/BlueMountainsRoutes_1starmin_grade_23_39_length_5_45m_sport_and_trad.xlsx') #"C:\Users\Declan\.atom\thecrag_scraper_11_09_trying_pagination.py"
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Route Name')
worksheet.write('B1', 'Grade')
worksheet.write('C1', 'Style')
worksheet.write('D1', 'Route length (m)')
worksheet.write('E1', 'Quality')
worksheet.write('F1', 'Popularity')
worksheet.write('G1', 'Description')
worksheet.write('H1', 'Total number of rankings')
worksheet.write('I1', 'Mega classic')
worksheet.write('J1', 'Classic')
worksheet.write('K1', 'Very good')
worksheet.write('L1', 'Good')
worksheet.write('M1', 'Average')
worksheet.write('N1', "Don't bother")
worksheet.write('O1', 'Crap')
worksheet.write('P1', 'Number of ascents')
worksheet.write('Q1', 'Onsight')
worksheet.write('R1', 'Flash')
worksheet.write('S1', 'Red Point')
worksheet.write('T1', 'Pink Point')
worksheet.write('U1', 'Attempt')
worksheet.write('V1', 'Tick')
worksheet.write('W1', 'Keywords')     #worksheet.write('T1', 'Location')


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
    # looking for route style
    ################################################################
    route_style_text = soup_route_main_page.findAll("div", {"class":"headline__guts"})

    route_style = 'not listed'

    if "SPORT" in str(route_style_text):
        route_style = 'sport'

    if "TRAD" in str(route_style_text):
        route_style = 'trad'
    ################################################################
    # looking for route location # want e.g. Blue mountians - Mount vic -  Bardens lookout - Jean genie area
    ################################################################

    route_location = []
    route_text_location = soup_route_main_page.findAll( "div", {"class":"crumbs__all"}) # was __all
    route_text_location = str(route_text_location)
    route_text_location = route_text_location.replace('</i></span>',"")

    for location in range(1, route_text_location.count('itemprop="title">')+1):
        location_start = route_text_location.find('itemprop="title">')
        location_end = route_text_location.find('</span>')
        location_total = route_text_location[location_start+len('itemprop="title">'):location_end]
        if len(location_total) == 0:
            pass
        else:
            a = 1 #placeholder
            location_total = location_total.replace(' &amp',"")
            route_location.append(location_total)
            #print('location_total', location_total)

        route_text_location = route_text_location[location_end+6::]

    if soup_route_main_page.findAll("span", {"class":"gb4"}):
        route_text_grade_AU = soup_route_main_page.findAll("span", {"class":"gb4"})
    elif soup_route_main_page.findAll("span", {"class":"gb3"}):
        route_text_grade_AU = soup_route_main_page.findAll("span", {"class":"gb3"})
    else:
        print("couldn't find grade")

    route_text_grade_AU_start = str(route_text_grade_AU).find('Set using AU grade config">')
    route_grade_AU = str(route_text_grade_AU)[route_text_grade_AU_start+len('Set using AU grade config">'):route_text_grade_AU_start+len('Set using AU grade config">')+2]

    #################################################################
    ############### looking for route length### #####################
    #################################################################
    route_text_length = soup_route_main_page.findAll("div", {"class":"headline__guts"})
    route_text_length_find = str(soup_route_main_page).find('<li><strong>Length:</strong>')
    route_length = str(soup_route_main_page)[route_text_length_find+len('<li><strong>Length:</strong> '):route_text_length_find+len('<li><strong>Length:</strong>')+3].replace('m',"")

    #################################################################
    ############### looking for route popularity#####################
    #################################################################
    route_text_popularity= soup_route_main_page.findAll("span", {"class":"heading__t"})
    route_text_popularity = str(route_text_popularity).encode('ascii','ignore').decode('ascii')
    route_text_popularity = route_text_popularity[route_text_popularity.find('Relative popularity ')+len('Relative popularity '):route_text_popularity.find('Relative popularity ')+len('Relative popularity ')+4]
    route_text_popularity = re.sub("\D","",route_text_popularity)

    #################################################################
    ############### looking for route quality #######################
    #################################################################
    route_text_quality = soup_route_main_page.findAll("span", {"class":"heading__t"})
    route_text_quality = str(route_text_quality).encode('ascii', 'ignore').decode('ascii')
    route_text_quality_start = route_text_quality.find('Quality')
    route_text_quality_test = route_text_quality[route_text_quality_start+len('Quality'):route_text_quality_start+len('Quality')+5]
    #Onsight = reOnsight = re.sub("\D", "", Onsight)
    route_text_quality_final = re.sub("\D", "", route_text_quality_test)

    if len(route_text_quality_final) == 0:
        route_text_quality_final = -1

    if str(route_text_quality_final).endswith('"'):
        route_text_quality_final = route_text_quality_final[1:-1]

    #################################################################
    ############### looking for route quality barchart #############
    #################################################################
    route_text_quality_barchart = soup_route_main_page.findAll("div", {"class":"barchart-h"})

    # mega classic
    mega_classic = str(route_text_quality_barchart)[str(route_text_quality_barchart).find('Mega Classic')-4:str(route_text_quality_barchart).find('Mega Classic')]
    if mega_classic.startswith('"'):
        mega_classic = mega_classic[1::]
    if mega_classic.startswith('="'):
        mega_classic = mega_classic[2::]

    # classic and mega classic overlap going to have to do some magic
    classic_editted = str(route_text_quality_barchart).replace('Mega Classic',"")
    classic = str(classic_editted)[str(classic_editted).find('Classic')-4:str(classic_editted).find('Classic')]
    if classic.startswith('"'):
        classic = classic[1::]
    if classic.startswith('="'):
        classic = classic[2::]

# very good
    very_good = str(route_text_quality_barchart)[str(route_text_quality_barchart).find('Very Good')-4:str(route_text_quality_barchart).find('Very Good')]
    if very_good.startswith('"'):
        very_good = very_good[1::]
    if very_good.startswith('="'):
        very_good = very_good[2::]

# good Need to edit out very good
    good_editted = str(route_text_quality_barchart).replace('Very Good',"")
    good = str(good_editted)[str(good_editted).find('Good')-4:str(good_editted).find('Good')]
    if good.startswith('"'):
        good = good[1::]
    if good.startswith('="'):
        good = good[2::]

# Average
    average = str(route_text_quality_barchart)[str(route_text_quality_barchart).find('Average')-4:str(route_text_quality_barchart).find('Average')]
    if average.startswith('"'):
        average = average[1::]
    if average.startswith('="'):
        average = average[2::]

# Dont bother
    dont_bother = str(route_text_quality_barchart)[str(route_text_quality_barchart).find("Don't Bother")-4:str(route_text_quality_barchart).find("Don't Bother")]
    if dont_bother.startswith('"'):
        dont_bother = dont_bother[1::]
    if dont_bother.startswith('="'):
        dont_bother = dont_bother[2::]

# Crap
    crap = str(route_text_quality_barchart)[str(route_text_quality_barchart).find("Crap")-4:str(route_text_quality_barchart).find("Crap")]
    if crap.startswith('"'):
        crap = crap[1::]
    if crap.startswith('="'):
        crap = crap[2::]


    number_of_rankings = int(mega_classic)+int(classic)+int(very_good)+int(good)+int(average)+int(dont_bother)+int(crap)
    #print(number_of_rankings)

    ################################################################
    ################## Looking for number of ascentss#######################
    ################################################################
    route_text_num_of_ascents = soup_route_main_page.findAll("span", {"class":"heading__t"})
    route_text_num_of_ascents = str(route_text_num_of_ascents).encode('ascii','ignore').decode('ascii')
    route_text_num_of_ascents = route_text_num_of_ascents[route_text_num_of_ascents.find(' ascent')-4:route_text_num_of_ascents.find(' ascent')]
    route_text_num_of_ascents = route_text_num_of_ascents.replace('-',"")
    route_text_num_of_ascents = route_text_num_of_ascents.replace(' ',"")

    if route_text_num_of_ascents == 'No':
        route_text_num_of_ascents = -1

    print('route_text_num_of_ascents', route_text_num_of_ascents)
    ################################################################
    ################## Looking for tick types#######################
    ################################################################
    route_text_ticks_barchart = soup_route_main_page.findAll("div", {"class":"barchart-h barchart-h--showvals"})
    route_text_ticks_barchart = str(route_text_ticks_barchart)

    if "Onsight" in route_text_ticks_barchart:
        Onsight =  (route_text_ticks_barchart[route_text_ticks_barchart.find("Onsight")-len('ascents"><td class="barchart-h__label">')-6:route_text_ticks_barchart.find("Onsight")-len('ascents"><td class="barchart-h__label">')-2])
        Onsight = re.sub("\D", "", Onsight)
    else:
        Onsight = '0'

    if "Flash" in route_text_ticks_barchart:
        Flash =  str(route_text_ticks_barchart[route_text_ticks_barchart.find("Flash")-len('ascents"><td class="barchart-h__label">')-6:route_text_ticks_barchart.find("Flash")-len('ascents"><td class="barchart-h__label">')-2])
        Flash = re.sub("\D", "", Flash)
    else:
        Flash = '0'

    if "Red point" in route_text_ticks_barchart:
        Red_point = str(route_text_ticks_barchart[route_text_ticks_barchart.find("Red point")-len('ascents"><td class="barchart-h__label">')-6:route_text_ticks_barchart.find("Red point")-len('ascents"><td class="barchart-h__label">')-2])#-3
        Red_point = re.sub("\D", "", Red_point)
    else:
        Red_point = '0'

    if "Pink point" in route_text_ticks_barchart:
        Pink_point = str(route_text_ticks_barchart[route_text_ticks_barchart.find("Pink point")-len('ascents"><td class="barchart-h__label">')-6:route_text_ticks_barchart.find("Pink point")-len('ascents"><td class="barchart-h__label">')-2])#-3
        Pink_point = re.sub("\D", "", Pink_point)
    else:
        Pink_point = '0'

    if "Attempt" in route_text_ticks_barchart:
        Attempt = str(route_text_ticks_barchart[route_text_ticks_barchart.find("Attempt")-len('ascents"><td class="barchart-h__label">')-6:route_text_ticks_barchart.find("Attempt")-len('ascents"><td class="barchart-h__label">')-2])
        Attempt = re.sub("\D", "", Attempt)
    else:
        Attempt = '0'

    if "Tick" in route_text_ticks_barchart:
        Tick = str(route_text_ticks_barchart[route_text_ticks_barchart.find("Tick")-len('ascents"><td class="barchart-h__label">')-6:route_text_ticks_barchart.find("Tick")-len('ascents"><td class="barchart-h__label">')-2])
        Tick = re.sub("\D", "", Tick)
    else:
        Tick = '0'

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
        keyword_list.append(keyword+ " "+fontsize)

        comment_keywords = comment_keywords[comment_end+len('</span>')::]

    ################################################################
    ################ looking for route description ################
    ################################################################
    url_route_main_page = list_of_ascents[route].strip("''")
    url_route_main_page = url_route_main_page.strip('/ascents')
    page_route_main_page = requests.get(url_route_main_page)
    data_route_main_page = page_route_main_page.text
    soup_route_main_page = BeautifulSoup(data_route_main_page, "html.parser")
    route_text_main_page = soup_route_main_page.findAll("div", {"class":"markdown"})

    start_of_description = str(route_text_main_page).find('div class="markdown"><p>')
    end_of_description = str(route_text_main_page).find('.</p>')
    route_description_raw = str(route_text_main_page)[str(route_text_main_page).find('div class="markdown"><p>')+len(str('div class="markdown"><p>')):end_of_description]
    route_description_raw = str(route_description_raw).replace('<img class="emoji" src="//twemoji.maxcdn.com/svg/1f609.svg" title=";)">',"")

    route_description = str(route_description_raw)

# remove emoji from all descriptions

    if '<img class="emoji" src=' in str(route_description_raw):
        strip_emoji_1 = str(route_description_raw)[0:str(route_description_raw).find('<img class="emoji" src=')] # when l search for next thing it should def be the end of the emoji thingy
        strip_emoji_2 = strip_emoji_1.find('">')
        without_emoji_start = str(route_description_raw)[0:str(route_description_raw).find('<img class="emoji" src=')]
        route_description_raw = without_emoji_start + str(route_description_raw)[str(route_description_raw).find('<img class="emoji" src=')+len('<img class="emoji" src="//twemoji.maxcdn.com/svg/1f603.svg" title=":)">')::]

# if ethic included in route description for some reason
    if "Although sport climbing is well entrenched" in str(route_description_raw):
        terminate_at = str(route_description_raw).find("</p>")
        route_description = str(route_description_raw)[0:terminate_at]

        # if ethic is still remaining for some reason
        if "Although sport climbing is well entrenched" in route_description:
            terminate_at = route_description.find("</p>")
            route_description = route_description[0:terminate_at]

 # if climb says left or right of other route and link is hyperlink
 # want to put a loop in here to count number of links
    if 'href="/climbing/australia/blue-mountains' in str(route_description_raw):
        #print('link in descriptions')
        #print('number of links in string', str(route_description_raw).count('href="/climbing/australia/blue-mountains'))

        for links in range(0,str(route_description_raw).count('href="/climbing/australia/blue-mountains')+1):
            if links == 1:
                remove_start = str(route_description_raw).find('<a class="internal"')
                remove_end = str(route_description_raw).find('">')
                route_description_first = str(route_description_raw)[0:remove_start] # works oks
                route_description_end = str(route_description_raw)[remove_end+len('">')::] #1099   # issue with this
                route_description = (route_description_first+route_description_end).replace("</a>'","")
                route_description = (route_description_first+route_description_end).replace("</a>","")

            if links >=2 :
                remove_start = route_description.find('<a class="internal"')
                route_description_first = route_description[0:remove_start]
                remove_end = route_description.find('">')
                route_description_end = route_description[remove_end+len('">')::]
                route_description = (route_description_first+route_description_end).replace("</a>'","")
                route_description = (route_description_first+route_description_end).replace("</a>","")

# if climbing is banned
    if 'The National Parks and Wildlife Service has advised that climbing is not permitted at ' in str(route_description_raw):
        route_description = "route is banned due to national park closure"


# if there is another link in description e.g. description is a link up of two routes
    if 'href="/climbing/australia/blue-mountains' in route_description:
        remove_start = str(route_description).find('<a class="internal"')
        remove_end = str(route_description).find('">')
        route_description_first = str(route_description)[0:remove_start]
        route_description_end = str(route_description)[remove_end+len('">')::]
        route_description = (route_description_first+route_description_end).replace("</a>'","")
        route_description = str(route_description)

# if there is no descripton and ethic is for whatever reason diverted to the description
    if "Although sport climbing is well entrenched as the most popular form of Blueys climbing, mixed-climbing on gear and bolts has generally been the rule over the long term. Please try to use available natural gear where possible, and do not bolt cracks or potential trad climbs. If you do the bolts may be remov" == str(route_description):
        route_description = "empty"

    if "twemoji.maxcdn.com/svg/1f4f9.svg" in str(route_description):
        test1 = str(route_description).find("<a href")
        test_end = str(route_description).rfind(">")
        route_description_1 = str(route_description)[0:test1]
        route_description_2 = str(route_description)[test_end+1::]
        route_description = route_description_1+route_description_2 + "contains video"

    route_description = route_description.replace('</div>, <div class="markdown"><p>Although sport climbing is well entrenched as the most popular form of Blueys climbing, mixed-climbing on gear and bolts has generally been the rule over the long term. Please try to use available natural gear where possible, and do not bolt cracks or potential trad climbs. If you do the bolts may be removed',"")
    route_description = route_description.encode('ascii', 'ignore').decode('ascii')
    route_description = route_description.replace('</a>',"")
    route_description = route_description.replace('</p>',"")
    route_description = route_description.replace('<p>',"")
    route_description = route_description.replace('</div>',"")
    route_description = route_description.replace(', <div class="markdown"><p>',"")
    route_description = route_description.replace('<img class="emoji" src="//twemoji.maxcdn.com/svg/1f603.svg" title=":)">',"")
    route_description = route_description.replace('<img class="emoji" src="//twemoji.maxcdn.com/svg/1f609.svg" title=";)">',"")
    route_description = route_description.replace('.</img>',"")
    route_description = route_description.replace('</img>',"")


    if route_description == 'empty':
        route_description = -1


    print(route+1, 'Route name', route_name, 'Grade AU', route_grade_AU, 'Route length', route_length, 'Quality', route_text_quality_test)
    print(route_description)
    print('Onsight:', Onsight, "Flash:", Flash, "Red Point:", Red_point, "Pink Point:", Pink_point,"Attempt:", Attempt, "Tick:", Tick)
    print('Number of ratings', number_of_rankings, 'Mega Classic:', mega_classic, 'Classic:', classic, 'Very good:', very_good, 'Good:', good, 'Average:', average, "Don't bother:", dont_bother,'Crap:', crap)
    print('Keyword list', keyword_list)
    print('Route location', route_location)
    print('\n')

    column = 0
    worksheet.write(row, column, route_name) #a
    column +=1
    worksheet.write(row, column, route_grade_AU)
    column +=1
    worksheet.write(row, column, route_style)
    column +=1
    worksheet.write(row, column, route_length)
    column +=1
    worksheet.write(row, column, route_text_quality_test)
    column +=1
    worksheet.write(row, column, route_text_popularity)#f
    column +=1
    worksheet.write(row, column, route_description)
    column +=1
    worksheet.write(row, column, number_of_rankings)
    column +=1
    worksheet.write(row, column, mega_classic)
    column +=1
    worksheet.write(row, column, classic)
    column +=1
    worksheet.write(row, column, very_good)
    column +=1
    worksheet.write(row, column, good)
    column +=1
    worksheet.write(row, column, average)
    column +=1
    worksheet.write(row, column, dont_bother)
    column +=1
    worksheet.write(row, column, crap)
    column +=1
    worksheet.write(row, column, route_text_num_of_ascents)
    column +=1
    worksheet.write(row, column, Onsight)
    column +=1
    worksheet.write(row, column, Flash)
    column +=1
    worksheet.write(row, column, Red_point)
    column +=1
    worksheet.write(row, column, Pink_point)
    column +=1
    worksheet.write(row, column, Attempt)
    column +=1
    worksheet.write(row, column, Tick)
    column +=1
    worksheet.write(row, column, str(keyword_list).replace("''","").replace('""',""))
    column +=1     #worksheet.write('T1', 'Location')
    worksheet.write(row, column, str(route_location).replace("''","").replace('""',""))

    row +=1


workbook.close()



'''
    if 'v0' in route_description or 'V0' in route_description:
        print('v0 in route description', route_description)
    if 'v1' in route_description or 'V1' in route_description:
        print('v1 in route description', route_description)
    if 'v2' in route_description or 'V2' in route_description:
        print('v2 in route description', route_description)
    if 'v3' in route_description or 'V3' in route_description:
        print('v4 in route description', route_description)
    if 'v3' in route_description or 'V4' in route_description:
        print('v4 in route description', route_description)
    if 'v5' in route_description or 'V5' in route_description:
        print('v5 in route description', route_description)
    if 'v6' in route_description or 'V6' in route_description:
        print('v6 in route description', route_description)
    if 'v7' in route_description or 'V7' in route_description:
        print('v7 in route description', route_description)
    if 'v8' in route_description or 'V8' in route_description:
        print('v8 in route description', route_description)
    if 'v9' in route_description or 'V9' in route_description:
        print('v9 in route description', route_description)
    if 'v10' in route_description or 'V10' in route_description:
        print('v10 in route description', route_description)
    if 'v11' in route_description or 'V11' in route_description:
        print('v11 in route description', route_description)
    if 'v12' in route_description or 'V12' in route_description:
        print('v12 in route description', route_description)
    if 'v13' in route_description or 'V13' in route_description:
        print('v13 in route description', route_description)
    if 'v14' in route_description or 'V14' in route_description:
        print('v14 in route description', route_description)
    if 'v15' in route_description or 'V15' in route_description:
        print('v15 in route description', route_description)

    ##############################################################
    ###############   looking at comments now  ###################
    ##############################################################

    route_text_string = (str(route_text_raw))
    route_text_string_edit = route_text_string.replace('[<div class="markdown">',"")
    route_text_string_edit = route_text_string.replace('</div>, <div class="markdown">',"")
    route_text_string_edit = route_text_string.split('<p>')

    route_comment = ([r.strip() for r in route_text_string_edit])

    for i in range(0,len(route_comment)):
        route_comment[i] = route_comment[i].replace("[","")
        route_comment[i] = route_comment[i].replace('</div>, <div class="markdown">',"")
        route_comment[i] = route_comment[i].replace('<div class="markdown">',"")
        route_comment[i] = route_comment[i].replace('</p>',"")

        route_comment[i] = route_comment[i].replace('</em>',"")
        route_comment[i] = route_comment[i].replace('</p>',"")

        route_comment[i] = route_comment[i].replace('<em class="enjoyable">',"")
        route_comment[i] = route_comment[i].replace('<em class="tag">',"")
        route_comment[i] = route_comment[i].replace('<em class="strenuous">',"")
        route_comment[i] = route_comment[i].replace('<em class="tag">',"")

        #print('route_comment[i]', route_comment[i])

        #print(any(ele in route_comment[i] for ele in boulder_grades)) # prints false if nothing
        #if (any(ele in route_comment[i] for ele in boulder_grades)) == True:
        #    print('if route check', route_comment[i])
        print(route_comment[i])
        if 'v0' in route_comment[i] or 'V0' in route_comment[i]:
            print('v0 in route comment', route_comment[i])
        if 'v1' in route_comment[i] or 'V1' in route_comment[i]:
            print('v1 in route comment', route_comment[i])
        if 'v2' in route_comment[i] or 'V2' in route_comment[i]:
            print('v2 in route comment', route_comment[i])
        if 'v3' in route_comment[i] or 'V3' in route_comment[i]:
            print('v4 in route comment', route_comment[i])
        if 'v3' in route_comment[i] or 'V4' in route_comment[i]:
            print('v4 in route comment', route_comment[i])
        if 'v5' in route_comment[i] or 'V5' in route_comment[i]:
            print('v5 in route comment', route_comment[i])
        if 'v6' in route_comment[i] or 'V6' in route_comment[i]:
            print('v6 in route comment', route_comment[i])
        if 'v7' in route_comment[i] or 'V7' in route_comment[i]:
            print('v7 in route comment', route_comment[i])
        if 'v8' in route_comment[i] or 'V8' in route_comment[i]:
            print('v8 in route comment', route_comment[i])
        if 'v9' in route_comment[i] or 'V9' in route_comment[i]:
            print('v9 in route comment', route_comment[i])
        if 'v10' in route_comment[i] or 'V10' in route_comment[i]:
            print('v10 in route comment', route_comment[i])
        if 'v11' in route_comment[i] or 'V11' in route_comment[i]:
            print('v11 in route comment', route_comment[i])
        if 'v12' in route_comment[i] or 'V12' in route_comment[i]:
            print('v12 in route comment', route_comment[i])
        if 'v13' in route_comment[i] or 'V13' in route_comment[i]:
            print('v13 in route comment', route_comment[i])
        if 'v14' in route_comment[i] or 'V14' in route_comment[i]:
            print('v14 in route comment', route_comment[i])
        if 'v15' in route_comment[i] or 'V15' in route_comment[i]:
            print('v15 in route comment', route_comment[i])
    #else:
    #    print(list_of_ascents[route] +" has no boulder description")

        #if str(len(list_of_ascents[route])) == number_of_routes:
        #    print('gone over all routes')
'''
