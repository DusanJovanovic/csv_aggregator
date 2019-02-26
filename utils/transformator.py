import pandas as pd

aggregations = {
    'week': 'W',
    'month': 'M',
    'quarter': 'Q',
    'year': 'Y',
}


def load_csv_to_data_frame(csv_file):
    df = pd.read_csv(csv_file)
    # Remove all completely NaN rows
    df = df.dropna(how='all')
    return df


def check_column_names(df):
    column_names = list(df.columns.values)
    # First column should be date.
    if column_names[0] != 'Date':
        return False
    # If column name is missing, return False.
    # Missing column names are automatically named "Unnamed: {column_index}".
    unnamed_list = [x for x in column_names if 'Unnamed' in x]
    return unnamed_list == []


def check_asset_values(df):
    column_names = list(df.columns.values)
    # Check if there is any asset column
    if len(column_names) < 2:
        return 
    # Check if values from asset column has the same type
    for column in column_names[1:]:
        if str(df[column].dtype) == 'object':
            return False
    return True


def find_missing_asset_values(df):
    # make dataframe out of rows with missing values
    missing_values = df[df.isnull().any(axis=1)]
    if missing_values.empty:
        return None

    column_names = list(df.columns.values)
    nan_dict = {}
    # iterate over rows
    for row in missing_values.iterrows():
        # set temp_date to be added to dict with nan values
        temp_date = row[1][0]
        # iterate over column names
        for ind, elem in enumerate(column_names):
            # if value is 'nan' add temp_date to list where key is column name
            if str(row[1][ind]) == 'nan':
                nan_dict[elem] = nan_dict.get(elem, [])
                nan_dict[elem].append(temp_date)
    if nan_dict:
        # Every key, value pair from dict with nan values
        # must be put to separate list
        return_list = []
        for key, values in nan_dict.items():
            # TODO: This is a hack. Instead of modifying date string
            # it should convert to Timestamp and retrieve date from it. 
            date_list = []
            for value in values:
                value = value[:-2] + '20' + value[-2:]
                date_list.append(value)
            return_list.append({key.lower(): date_list})
        return return_list
    return nan_dict


def check_for_missing_date(df):
    try:
        # This will raise an error if date values are invalid type
        # time_range is expected time range from csv
        time_range = pd.period_range(min(df.Date), max(df.Date))
    except ValueError:
        return None

    df['Date'] = pd.to_datetime(df['Date'])
    # difference between expected(time_range) and actual time range (df.Date)
    missing_dates_timestamp = time_range.to_timestamp().difference(df.Date)
    # convert timestamps to string and populate the list with missing dates
    missing_dates = [f'{x.month}/{x.day}/{x.year}' for x in missing_dates_timestamp]
    return missing_dates


def resample_df(df, agg):
    # resample the data frame to aggregate by time
    df1 = pd.DataFrame()
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index(df['Date'], inplace=True)
    for column in df.columns[1:]:
        df1[column] = df[column].resample(agg).sum()
    return df1


def transform_csv(file_, agg_value):
    df = load_csv_to_data_frame(file_)
    if not check_column_names(df) or not check_asset_values(df):
        return {'code': 1, 'error': 'Wrong format'}, 422
    missing_asset_values = find_missing_asset_values(df)
    if missing_asset_values:
        return {
            'code': 3,
            'error': 'Missing data',
            'details': {
                'data': missing_asset_values,
            }
         }, 422
    missing_dates = check_for_missing_date(df)
    if missing_dates is None:
        return {'code': 1, 'error': 'Wrong format'}, 422
    if missing_dates:
        return {
            'code': 2,
            'error': 'Missing dates',
            'details': {
                'dates': missing_dates,
            }
        }, 422

    return resample_df(df, aggregations[agg_value]), 200
