'''
28-09
Looking to analysis comments from climbs around australiaThis is an accompayment to thecrag scraper

'''

from bs4 import BeautifulSoup, SoupStrainer
import requests
import time
import re
import xlsxwriter
import os


list_of_ascents = []
#boulder_grades = ['v1', 'V1', 'v2', 'V2','v3', 'V3','v4', 'V4','v5', 'V5','v6', 'V6','v7', 'V7','v9', 'V9','v10', 'V10','v11', 'V11','v12', 'V12','v13', 'V13', 'v14', 'V14', 'v15', 'V15']
number_of_routes_counter = 0
number_of_routes_list = []


row = 1 # Due to heading
column = 0
workbook = xlsxwriter.Workbook('C:/Users/Declan/.atom/BlueMountainsRoutes_1starmin_grade_23_39_length_5_45m_sport_and_trad_comments.xlsx') #"C:\Users\Declan\.atom\thecrag_scraper_11_09_trying_pagination.py"
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Route Name')
worksheet.write('B1', 'Grade')
worksheet.write('C1', 'v0_desc')
worksheet.write('D1', 'v1_desc')
worksheet.write('E1', 'v2_desc')
worksheet.write('F1', 'v3_desc')
worksheet.write('G1', 'v4_desc')
worksheet.write('H1', 'v5_desc')
worksheet.write('I1', 'v6_desc')
worksheet.write('J1', 'v7_desc')
worksheet.write('K1', 'v8_desc')
worksheet.write('L1', 'v9_desc')
worksheet.write('M1', 'v10_desc')
worksheet.write('N1', "v11_desc")
worksheet.write('O1', 'v12_desc')
worksheet.write('P1', 'v13_desc')
worksheet.write('Q1', 'v14_desc')
worksheet.write('R1', 'v15_desc')
worksheet.write('S1', 'v0_count')
worksheet.write('T1', 'v1_count')
worksheet.write('U1', 'v2_count')
worksheet.write('V1', 'v3_count')
worksheet.write('W1', 'v4_count')
worksheet.write('X1', 'v5_count')
worksheet.write('Y1', 'v6_count')
worksheet.write('Z1', 'v7_count')
worksheet.write('AA1', 'v8_count')
worksheet.write('AB1', 'v9_count')
worksheet.write('AV1', 'v10_count')
worksheet.write('AD1', 'v11_count')
worksheet.write('AE1', 'v12_count')
worksheet.write('AF1', 'v13_count')
worksheet.write('AG1', 'v14_count')
worksheet.write('AH1', 'v15_count')
worksheet.write('AI1', 'comments ')
#worksheet.write('AH1', 'v_count')
#worksheet.write('AC1', '')


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





    print('\n')

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

    #################################################################
    ############### looking for route grade AU #####################
    #################################################################
    if soup_route_main_page.findAll("span", {"class":"gb4"}):
        route_text_grade_AU = soup_route_main_page.findAll("span", {"class":"gb4"})
    elif soup_route_main_page.findAll("span", {"class":"gb3"}):
        route_text_grade_AU = soup_route_main_page.findAll("span", {"class":"gb3"})
    else:
        print("couldn't find grade")

    route_text_grade_AU_start = str(route_text_grade_AU).find('Set using AU grade config">')
    route_grade_AU = str(route_text_grade_AU)[route_text_grade_AU_start+len('Set using AU grade config">'):route_text_grade_AU_start+len('Set using AU grade config">')+2]

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

    if 'href="/climbing/australia/blue-mountains' in str(route_description_raw):

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

    if 'v0' in str(route_description) or 'V0' in str(route_description):   #type int not iterable????
        v0_desc = 1
        print('v0 in route description', route_description)
    else:
        v0_desc = 0
    if 'v1' in str(route_description) or 'V1' in str(route_description):
        v1_desc = 1
        print('v1 in route description', route_description)
    else:
        v1_desc = 0
    if 'v2' in str(route_description) or 'V2' in str(route_description):
        v2_desc = 1
        print('v2 in route description', route_description)
    else:
        v2_desc = 0
    if 'v3' in str(route_description) or 'V3' in str(route_description):
        v3_desc = 1
        print('v4 in route description', route_description)
    else:
        v3_desc = 0
    if 'v4' in str(route_description) or 'V4' in str(route_description):
        v4_desc = 1
        print('v4 in route description', route_description)
    else:
        v4_desc = 0
    if 'v5' in str(route_description) or 'V5' in str(route_description):
        v5_desc = 1
        print('v5 in route description', route_description)
    else:
        v5_desc = 0
    if 'v6' in str(route_description) or 'V6' in str(route_description):
        v6_desc = 1
        print('v6 in route description', route_description)
    else:
        v6_desc = 0
    if 'v7' in str(route_description) or 'V7' in str(route_description):
        v7_desc = 1
        print('v7 in route description', route_description)
    else:
        v7_desc = 0
    if 'v8' in str(route_description) or 'V8' in str(route_description):
        v8_desc = 1
        print('v8 in route description', route_description)
    else:
        v8_desc = 0
    if 'v9' in str(route_description) or 'V9' in str(route_description):
        v9_desc = 1
        print('v9 in route description', route_description)
    else:
        v9_desc = 0
    if 'v10' in str(route_description) or 'V10' in str(route_description):
        v10_desc = 1
        print('v10 in route description', route_description)
    else:
        v10_desc = 0
    if 'v11' in str(route_description) or 'V11' in str(route_description):
        v11_desc = 1
        print('v11 in route description', route_description)
    else:
        v11_desc = 0
    if 'v12' in str(route_description) or 'V12' in str(route_description):
        v12_desc = 1
        print('v12 in route description', route_description)
    else:
        v12_desc = 0
    if 'v13' in str(route_description) or 'V13' in str(route_description):
        v13_desc = 1
        print('v13 in route description', route_description)
    else:
        v13_desc = 0
    if 'v14' in str(route_description) or 'V14' in str(route_description):
        v14_desc = 1
        print('v14 in route description', route_description)
    else:
        v14_desc = 0
    if 'v15' in str(route_description) or 'V15' in str(route_description):
        v15_desc = 1
        print('v15 in route description', route_description)
    else:
        v15_desc = 0

    ##############################################################
    ###############   looking at comments now  ###################
    ##############################################################

    route_text_string = (str(route_text_raw))
    route_text_string_edit = route_text_string.replace('[<div class="markdown">',"")
    route_text_string_edit = route_text_string.replace('</div>, <div class="markdown">',"")
    route_text_string_edit = route_text_string.split('<p>')

    route_comment = ([r.strip() for r in route_text_string_edit])

    v0_counter = 0
    v1_counter = 0
    v2_counter = 0
    v3_counter = 0
    v4_counter = 0
    v5_counter = 0
    v6_counter = 0
    v7_counter = 0
    v8_counter = 0
    v9_counter = 0
    v10_counter = 0
    v11_counter = 0
    v12_counter = 0
    v13_counter = 0
    v14_counter = 0
    v15_counter = 0

    comments_users_list = []
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
        comments_users_list.append(str(route_comment[i]))

        # might need to moe this outside loop
        '''
        v0_counter = 0
        v1_counter = 0
        v2_counter = 0
        v3_counter = 0
        v4_counter = 0
        v5_counter = 0
        v6_counter = 0
        v7_counter = 0
        v8_counter = 0
        v9_counter = 0
        v10_counter = 0
        v11_counter = 0
        v12_counter = 0
        v13_counter = 0
        v14_counter = 0
        v15_counter = 0
        '''
        comment_grade_list = []
        #print(route_comment[i])
        if 'v0' in route_comment[i] or 'V0' in route_comment[i]:
            v0_counter += 1
            print('v0 in route comment', route_comment[i])
        if 'v1' in route_comment[i] or 'V1' in route_comment[i]:
            v1_counter += 1
            print('v1 in route comment', route_comment[i])
        if 'v2' in route_comment[i] or 'V2' in route_comment[i]:
            v2_counter += 1
            print('v2 in route comment', route_comment[i])
        if 'v3' in route_comment[i] or 'V3' in route_comment[i]:
            v3_counter += 1
            print('v3 in route comment', route_comment[i])
        if 'v4' in route_comment[i] or 'V4' in route_comment[i]:
            v4_counter += 1
            print('v4 in route comment', route_comment[i])
        if 'v5' in route_comment[i] or 'V5' in route_comment[i]:
            v5_counter += 1
            print('v5 in route comment', route_comment[i])
        if 'v6' in route_comment[i] or 'V6' in route_comment[i]:
            v6_counter += 1
            print('v6 in route comment', route_comment[i])
        if 'v7' in route_comment[i] or 'V7' in route_comment[i]:
            v7_counter += 1
            print('v7 in route comment', route_comment[i])
        if 'v8' in route_comment[i] or 'V8' in route_comment[i]:
            v8_counter += 1
            print('v8 in route comment', route_comment[i])
        if 'v9' in route_comment[i] or 'V9' in route_comment[i]:
            v9counter += 1
            print('v9 in route comment', route_comment[i])
        if 'v10' in route_comment[i] or 'V10' in route_comment[i]:
            v10_counter += 1
            print('v10 in route comment', route_comment[i])
        if 'v11' in route_comment[i] or 'V11' in route_comment[i]:
            v11_counter += 1
            print('v11 in route comment', route_comment[i])
        if 'v12' in route_comment[i] or 'V12' in route_comment[i]:
            v12_counter += 1
            print('v12 in route comment', route_comment[i])
        if 'v13' in route_comment[i] or 'V13' in route_comment[i]:
            v13_counter += 1
            print('v13 in route comment', route_comment[i])
        if 'v14' in route_comment[i] or 'V14' in route_comment[i]:
            v14_counter += 1
            print('v14 in route comment', route_comment[i])
        if 'v15' in route_comment[i] or 'V15' in route_comment[i]:
            v15_counter += 1
            print('v15 in route comment', route_comment[i])

        '''
        v0_comments = 'v0_comments' + v0_counter
        v1_comments = 'v1_comments' + v1_counter
        v2_comments = 'v2_comments' + v2_counter
        v3_comments = 'v3_comments' + v3_counter
        v4_comments = 'v4_comments' + v4_counter
        v5_comments = 'v5_comments' + v5_counter
        v6_comments = 'v6_comments' + v6_counter
        v7_comments = 'v7_comments' + v7_counter
        v8_comments = 'v8_comments' + v8_counter
        v9_comments = 'v9_comments' + v9_counter
        v10_comments = 'v10_comments' + v10_counter
        v11_comments = 'v11_comments' + v11_counters
        v12_comments = 'v12_comments' + v12_counter
        v13_comments = 'v13_comments' + v13_counter
        v14_comments = 'v14_comments' + v14_counter
        v15_comments = 'v15_comments' + v15_counter
        '''

    column = 0
    worksheet.write(row, column, route_name) #a
    column +=1
    worksheet.write(row, column, route_grade_AU)
    column +=1
    worksheet.write(row, column, v0_desc)
    column +=1
    worksheet.write(row, column, v1_desc)
    column +=1
    worksheet.write(row, column, v2_desc)
    column +=1
    worksheet.write(row, column, v3_desc)
    column +=1
    worksheet.write(row, column, v4_desc)
    column +=1
    worksheet.write(row, column, v5_desc)
    column +=1
    worksheet.write(row, column, v6_desc)
    column +=1
    worksheet.write(row, column, v7_desc)
    column +=1
    worksheet.write(row, column, v8_desc)
    column +=1
    worksheet.write(row, column, v9_desc)
    column +=1
    worksheet.write(row, column, v10_desc)
    column +=1
    worksheet.write(row, column, v11_desc)
    column +=1
    worksheet.write(row, column, v12_desc)
    column +=1
    worksheet.write(row, column, v13_desc)
    column +=1
    worksheet.write(row, column, v14_desc)
    column +=1
    worksheet.write(row, column, v15_desc)
    column +=1
    worksheet.write(row, column, v0_counter)
    column +=1
    worksheet.write(row, column, v1_counter)
    column +=1
    worksheet.write(row, column, v2_counter)
    column +=1
    worksheet.write(row, column, v3_counter)#f
    column +=1
    worksheet.write(row, column, v4_counter)
    column +=1
    worksheet.write(row, column, v5_counter)
    column +=1
    worksheet.write(row, column, v6_counter)
    column +=1
    worksheet.write(row, column, v7_counter)
    column +=1
    worksheet.write(row, column, v8_counter)
    column +=1
    worksheet.write(row, column, v9_counter)
    column +=1
    worksheet.write(row, column, v10_counter)
    column +=1
    worksheet.write(row, column, v11_counter)
    column +=1
    worksheet.write(row, column, v12_counter)
    column +=1
    worksheet.write(row, column, v13_counter)
    column +=1
    worksheet.write(row, column, v14_counter)
    column +=1
    worksheet.write(row, column, v15_counter)
    column +=1
    worksheet.write(row, column, str(comments_users_list))


    row +=1

workbook.close()
    #comment_grade_list.append()





#else:
#    print(list_of_ascents[route] +" has no boulder description")

    #if str(len(list_of_ascents[route])) == number_of_routes:
    #    print('gone over all routes')
