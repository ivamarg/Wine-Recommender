import pandas as pd
import requests
import re
import time

"""
    User profile data
"""

# test user id
user_id = '287095'


# function if receiving a response to a request for each page with user's rated wines
def get_user_data(user_id, page_num):
    param = {'page': page_num, 'order': 'top-ratings'}
    header = {'accept': 'text/javasript, application/javascript, application/ecmascript, '
                        'application/x-ecmascript, */*; q=0.01',
              'x-requested-with': 'XMLHttpRequest',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/85.0.4183.121 Safari/537.36'
              }
    r = requests.get(f'https://www.vivino.com/users/{user_id}/activities', headers=header, params=param)
    data = r.text
    return data


# page number
page_number = 1
# duplicate counter
count_dupl = 0

# dataframe with user data
df_user = pd.DataFrame(columns=['wine_id', 'rating'])

# loop through all pages containing the required data (up to 5 attempts to obtain unique wines)
while count_dupl < 5:
    # request result
    raw_data = get_user_data(user_id, page_number)
    # list of user-rated wines
    wines = []

    # id and rating of each wine tasted by the user
    for wine in raw_data.split('data-id')[1:]:
        wine_id = re.findall(r"(?<=data-vintage-id=\\')\d*", wine)[0]
        rating = sum(map(int, re.findall(r"(?<=icon-)\d*(?=-pct)", wine))) / 100

        wines.append((wine_id, rating))

    # number of unique wines before update
    count_items_before = df_user.shape[0]
    # wines obtained from the current page
    df_curr_page = pd.DataFrame(wines, columns=['wine_id', 'rating'])
    # adding only new wines to the final dataframe
    df_user = pd.concat([df_user, df_curr_page], ignore_index=False).drop_duplicates('wine_id')
    # number of unique wines after update
    count_items_after = df_user.shape[0]

    # checking for new unique rows
    if count_items_before == count_items_after:
        # no new wines added in current iteration
        count_dupl += 1

    page_number += 1
    time.sleep(1)

# save to csv file
df_user.to_csv('../data/df_user.csv', index=False)


