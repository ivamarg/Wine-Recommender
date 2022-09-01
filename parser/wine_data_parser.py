import requests
import pandas as pd


# parsing data of wines of a certain type (red, white, etc.)
def parse(type_wine):
    # page_number - variable to iterate over pages,
    # count_control - variable for counting the number of duplicate dataframes
    page_number, count_control = 0, 0

    # dataframe for wine data
    df = pd.DataFrame(columns=
                      [
                          'Vintage_wine_id', 'Vintage_wine', 'Year', 'Wine_id', 'Wine', 'Wine_type', 'Ratings_average',
                          'Ratings_count', 'Price(€)', 'Bottle_quantity', 'Price_without_discount(€)', 'Bottle_type_id',
                          'Bottle_type_name', 'Bottle_volume', 'Winery_id', 'Winery', 'Region_id', 'Region', 'Country',
                          'Regions_count', 'Users_count', 'Wineries_count', 'Wines_count', 'Wine_style', 'Acidity',
                          'Body', 'Wine_style_description', 'Wine_region_name', 'Grapes', 'Food', 'Flavor', 'Taste'
                      ])

    while True:
        page_number += 1

        r = requests.get(
            'https://www.vivino.com/api/explore/explore',
            params={
                'country_code': 'IT',
                'min_rating': 'any ratings',
                'order_by': 'price',
                'page': page_number,
                'wine_type_ids[]': type_wine
            },
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/85.0.4183.121 Safari/537.36'
            })

        results = [
            (
                # information about wine
                item['vintage']['id'],  # vintage wine (wine with year) id
                item['vintage']['name'],  # vintage wine name with winery name
                int(item['vintage']['year'])
                if item['vintage']['year'] != 'N.V.' else 'NULL',  # N.V. — non-vintage wine
                item['vintage']['wine']['id'],  # wine (not vintage) id
                item['vintage']['wine']['name'],  # wine name
                int(item['vintage']['wine']['type_id']),  # wine type id (red, white, etc.)

                # statistics (average vintage wine rating and number of vintage wine ratings)
                float(item['vintage']['statistics']['ratings_average']),
                int(item['vintage']['statistics']['ratings_count']),

                # information about price and bottle (name, volume, type of bottle, number of bottle)
                float(item['price']['amount']),  # vintage wine price
                item['price']['bottle_quantity'],
                float(item['price']['discounted_from'])
                if item['price']['discounted_from'] is not None else 'NULL',  # NULL or price without discount
                item['price']['bottle_type']['id'],
                item['price']['bottle_type']['short_name'],
                int(item['price']['bottle_type']['volume_ml']),

                # information about winery
                item['vintage']['wine']['winery']['id'],
                item['vintage']['wine']['winery']['name'],

                # geography of wine (region and country)
                item['vintage']['wine']['region']['id'],
                item['vintage']['wine']['region']['name'],
                item['vintage']['wine']['region']['country']['name'],
                int(item['vintage']['wine']['region']['country']['regions_count']),
                int(item['vintage']['wine']['region']['country']['users_count']),
                int(item['vintage']['wine']['region']['country']['wineries_count']),
                int(item['vintage']['wine']['region']['country']['wines_count']),

                # information about wine style (characteristic, description, popular grapes, suitable food for wine)
                item['vintage']['wine']['style']['name'],  # wine region name with microzone
                item['vintage']['wine']['style']['acidity_description'],
                item['vintage']['wine']['style']['body_description'],
                item['vintage']['wine']['style']['description']
                if item['vintage']['wine']['style']['description'] is not None else 'NULL',
                # NULL or description of wine style
                item['vintage']['wine']['style']['regional_name'],  # wine region name
                [j['name'] for j in item['vintage']['wine']['style']['grapes']],  # list of popular grapes of wine style
                [k['name'] for k in item['vintage']['wine']['style']['food']],  # list of suitable food for wine style

                # taste characteristics (flavor and taste ratings )
                [m['group'] for m in item['vintage']['wine']['taste']['flavor']]
                if item['vintage']['wine']['taste']['flavor'] is not None else 'NULL',
                # NULL or list of flavor from users
                [f'{key}: {int(value)}' for key, value in item['vintage']['wine']['taste']['structure'].items()
                 if value is not None]  # list of items of dict with taste ratings
            )
            for item in r.json()['explore_vintage']['matches']
            if item['vintage']['wine']['region'] is not None and item['vintage']['wine']['style'] is not None
               and item['vintage']['wine']['taste']['structure'] is not None
        ]

        dt = pd.DataFrame(results,
                          columns=
                          [
                              'Vintage_wine_id', 'Vintage_wine', 'Year', 'Wine_id', 'Wine', 'Wine_type',
                              'Ratings_average', 'Ratings_count', 'Price(€)', 'Bottle_quantity',
                              'Price_without_discount(€)', 'Bottle_type_id', 'Bottle_type_name', 'Bottle_volume',
                              'Winery_id', 'Winery', 'Region_id', 'Region', 'Country', 'Regions_count', 'Users_count',
                              'Wineries_count', 'Wines_count', 'Wine_style', 'Acidity', 'Body',
                              'Wine_style_description', 'Wine_region_name', 'Grapes', 'Food', 'Flavor', 'Taste'
                          ])
        # save the current length of the dataframe
        total_size = len(df)

        df = pd.concat([df, dt], ignore_index=False).drop_duplicates(subset=['Vintage_wine_id'])

        # check if new lines have been added
        if len(df) == total_size:
            count_control += 1
            # if the new dataframe has not been encountered 5 times, return the final dataframe
            if count_control == 5:
                return df


# final dataframe with all wine types (1 - red, 2 - white, 3 - sparkling, 4 - rose)
data = pd.concat([parse(1), parse(2), parse(3), parse(4)], ignore_index=True)

# save to csv file
data.to_csv('../data/data.csv', index=False)
