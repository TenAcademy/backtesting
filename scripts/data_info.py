# imports
import os
import sys
sys.path.append(os.path.abspath(os.path.join('../scripts')))


class DataInfo:
    def __init__(self, df):
        self.df = df.copy()

    # shape of the dataframe
    def shape_df(self):
        '''
        Display number of rows and columns in the given Dataframe
        '''
        print(f"Dataframe contains {self.df.shape[0]} rows and " +
              f"{self.df.shape[1]} columns")
        # return (self.df.shape[0],self.df.shape[1])
        # logger.info('data info: displaying shape of the dataframe')

    # info
    def detail_info(self):
        '''
        Display detail Dataframe info
        '''
        print(self.df.info())
        # logger.info('data info: displaying detail information ')

    # statistical description
    def describe_stat(self):
        '''
        Display the statistical description of the given dataframe
        '''
        return self.df.describe()
        # logger.info('data info: displaying statistical information')

    # null percentage
    def null_percentage(self):
        '''
        Display Total Null percentage of the Data Frame
        '''
        number_of_rows, number_of_columns = self.df.shape
        df_size = number_of_rows * number_of_columns
        null_size = (self.df.isnull().sum()).sum()
        percentage = round((null_size / df_size) * 100, 2)
        print(f"Dataframe contains null values of { percentage }% out of " +
              "the given dataset")
        # logger.info('data info: displaying null percentage in the datasets')

    # counts null
    def get_count_null(self):
        print(self.df.isnull().sum())
        # logger.info('data info: displaying null sum')

    # duplication
    def get_duplication(self):
        print(self.duplicated().any().sum())
        # logger.info('data info: checking duplication')

    # datatypes
    def get_types(self):
        print(self.dtypes)

    # converting
    # logger.info('data info: displaying datatype')
    def convert_labels(df):
        df.columns = [column.replace(' ', '_').lower()
                      for column in df.columns]
        return df
        # logger.info('data info: displaying shape of the dataframe')
