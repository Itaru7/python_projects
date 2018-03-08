import requests
from bs4 import BeautifulSoup
import datetime
import pickle
import re

out_file = open('pickle.text', 'wb')
all_names = []


# Return True if the date is before Feb 1, 2014. False, otherwise.
def check_first_date(html_soup):
    date = html_soup.find('span', class_='views-field views-field-created')
    string_date = date.span.text
    data_object = datetime.datetime.strptime(string_date, '%A, %B %d, %Y')
    return False if data_object > datetime.datetime(2014, 12, 1) else True


def scrape_a_page(html_soup):
    suffix = ['Jr', 'Sr', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

    # Take text in the <div align="center">
    narratives_containers = html_soup.find_all('div', {'align': 'center'})

    # Extract text inside of the tag
    all_texts = [x.text for x in narratives_containers]

    for x in all_texts:
        # Cut off if it's more than 250 words
        if len(x) <= 250:
            # Omit sentences
            if not re.search(' by | to | the |:|\xa0| at | about | in | before | after | up | down ', x):
                x = x.strip()
                separate_names = re.split(r', and |, | with ', x)
                i = 0
                while i < len(separate_names):
                    # Take (blah blah)
                    if re.search('\(.*\)', separate_names[i]):
                        separate_names[i] = re.sub(r' \(.*\)', '', separate_names[i])

                    # Take titles
                    if re.search('Co-Chair |Mayor |Dr. ', separate_names[i]):
                        separate_names[i] = re.sub(r'(Gala)?\s?Co-Chair |Mayor |Dr\. |Executive Director |Mr\. |Mrs\. '
                                                   r'|Mr\. and Mrs\. |CEO |ANDRUS (Director|Acting President)?'
                                                   r'Institutional Advancement', '', separate_names[i])

                    # Decompose 'and'
                    if re.search(' and ', separate_names[i]):
                        spilitted = separate_names[i].split(' and ')
                        temp = [x.split(' ') for x in spilitted]
                        # print(temp[1])
                        if len(temp[0]) < 2 and len(temp[1]) >= 2:
                            temp[0][0] += ' ' + temp[1][1]
                        elif len(temp[0]) >= 2:
                            temp[0] = [temp[0][0].__add__(' ' + temp[0][1])]
                        if len(temp[1]) >= 2:
                            temp[1] = [temp[1][0].__add__(' ' + temp[1][1])] if not re.search('friends?|family|guests?',
                                                                                          separate_names[i]) else ''
                        new_temp = [item for sublist in temp for item in sublist]
                        separate_names[i] = new_temp
                        [all_names.append(x) for x in new_temp]
                    else:
                        # If it has suffix, combine
                        if i + 1 < len(separate_names) and separate_names[i + 1] in suffix:
                            all_names.append(separate_names[i] + ' ' + separate_names[i + 1])
                            i += 1
                        else:
                            all_names.append(separate_names[i])
                    i += 1


def web_scraping():
    url = 'http://www.newyorksocialdiary.com/party-pictures?page'
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # Get last page number ------------------------------------
    last_page = html_soup.find('a', title='Go to last page')
    last_page_number = int((last_page['href'].split('page='))[1])
    # ---------------------------------------------------------
    first_before_dec_2014 = 0
    for i in range(1, last_page_number + 1):
        url = 'http://www.newyorksocialdiary.com/party-pictures?page=%d' % i
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        # if date is before Feb 01, 2014, do this
        if check_first_date(html_soup):
            first_before_dec_2014 += 1
            # Check the page where has before and after December 1, 2014------------------------------
            if first_before_dec_2014 is 1:
                url = 'http://www.newyorksocialdiary.com/party-pictures?page=%d' % (i - 1)
                response = requests.get(url)
                html_soup = BeautifulSoup(response.text, 'html.parser')
                date = html_soup.select('span[class="views-field views-field-created"] > span')
                str_dates = [x.text for x in date]
                data_objects = [datetime.datetime.strptime(x, '%A, %B %d, %Y') for x in str_dates]

                titles = html_soup.select('span[class="views-field views-field-title"] > span > a')
                str_title_links = [x['href'] for x in titles]

                paired_list = []
                for x, y in zip(data_objects, str_title_links):
                    paired_list += [(x, y)]

                valid_pair = []
                for i in range(len(paired_list)):
                    if paired_list[i][0] < datetime.datetime(2014, 12, 1):
                        valid_pair += ((paired_list[i][0]), (paired_list[i][1]))
                #print(valid_pair)
                j = 1
                while j < len(valid_pair):
                    url = 'http://www.newyorksocialdiary.com%s' % valid_pair[j]
                    response = requests.get(url)
                    html_soup = BeautifulSoup(response.text, 'html.parser')
                    scrape_a_page(html_soup)
                    j += 2
            # -----------------------------------------------------------------------------------------
            print('Reading page ' + str(i))
            url = 'http://www.newyorksocialdiary.com/party-pictures?page=%d' % i
            response = requests.get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            titles = html_soup.select('span[class="views-field views-field-title"] > span > a')
            str_title_links = [x['href'] for x in titles]
            for k in str_title_links:
                url = 'http://www.newyorksocialdiary.com%s' % k
                response = requests.get(url)
                html_soup = BeautifulSoup(response.text, 'html.parser')
                scrape_a_page(html_soup)
        else:
            print('after Feb 01, 2014')
    pickle.dump(all_names, open("pickle.text", "wb"))
    out_file.close()
    all_unique_list = set(all_names)
    return len(all_unique_list)


if __name__ == "__main__":
    # execute only if run as a script
    print(web_scraping())
