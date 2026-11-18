import pandas as pd 
import os 

class DataLoader:
    def __init__(self, directory, years, months):
        self.directory = directory
        self.years = years
        self.months = months 

    def get_file_location(self, year, month):
        poss_formats = [f"f-{year}-{month}.csv", f"fnew-{year}-{month}.csv", f"fNew {year} {month}.csv", f"f {year} {month}.csv"]
        for x in poss_formats:
            path = os.path.join(self.directory, x)
            if os.path.exists(path):
                print(f"found {year}/{month}")
                return path 
        raise FileNotFoundError(F"couldn't find file {year}/{month} with any of the specified formats")

    def run_on_data(self, func):
        output = []
        for year in self.years:
            for month in self.months:
                loc = self.get_file_location(year, month)
                data = pd.read_csv(loc)
                output.append(func(data))
                print(f"{year}/{month} evaluated")
        return output 


class DemandDataLoader:
    def __init__(self, directory, years, column):
        self.directory = directory
        self.years = years
        self.column = column

    def get_file_location(self, year):
        format = f"demanddata_{year}.csv"
        path = os.path.join(self.directory, format)
        if os.path.exists(path):
            print(f"found {year}")
            return path 
        raise FileNotFoundError(F"couldn't find file {year} with any of the specified formats")

    def run_on_data(self, func):
        output = []
        for year in self.years:
            loc = self.get_file_location(year)
            data = pd.read_csv(loc)
            output.append(func(data, self.column))
            print(f"{year} evaluated")
        return output 
