import pandas as pd
import os


def process_data():

    """Process monthly data files and calculate key metrics to explore. Concatenate and return as a single DataFrame"""

    directory = "data"
    df = pd.DataFrame()
    for file_name in os.listdir(directory):

        if "checkpoint" in file_name:
            continue

        month_year = "-".join(file_name.split("-")[:2])

        month_df = pd.read_csv(directory + "/" + file_name)
        month_df = month_df[month_df["Org name"].notnull()]
        month_df = month_df[month_df["Org name"].str.contains("TRUST")].copy()

        month_df["Total attendances"] = (
            month_df["A&E attendances Type 1"]
            + month_df["A&E attendances Type 2"]
            + month_df["A&E attendances Other A&E Department"]
            + month_df["A&E attendances Booked Appointments Type 1"]
            + month_df["A&E attendances Booked Appointments Type 2"]
            + month_df["A&E attendances Booked Appointments Other Department"]
        )
        month_df["Total emergency admissions via A&E"] = (
            month_df["Emergency admissions via A&E - Type 1"]
            + month_df["Emergency admissions via A&E - Type 2"]
            + month_df["Emergency admissions via A&E - Other A&E department"]
        )
        month_df["Total emergency admissions"] = (
            month_df["Total emergency admissions via A&E"]
            + month_df["Other emergency admissions"]
        )
        month_df["Attendances over 4hrs"] = (
            month_df["Attendances over 4hrs Type 1"]
            + month_df["Attendances over 4hrs Type 2"]
            + month_df["Attendances over 4hrs Other Department"]
            + month_df["Attendances over 4hrs Booked Appointments Type 1"]
            + month_df["Attendances over 4hrs Booked Appointments Type 2"]
            + month_df["Attendances over 4hrs Booked Appointments Other Department"]
        )
        month_df["Percentage in 4 hours or less"] = round(
            100
            * (1 - (month_df["Attendances over 4hrs"] / month_df["Total attendances"])),
            1,
        )

        month_df["Patients spending 4+ hours from DTA to admission"] = (
            month_df["Patients who have waited 4-12 hs from DTA to admission"]
            + month_df["Patients who have waited 12+ hrs from DTA to admission"]
        )

        month_df["Proportion of patients spending 4+ hours from DTA to admission"] = (
            month_df["Patients spending 4+ hours from DTA to admission"]
            / month_df["Total emergency admissions"]
        )
        month_df["Proportion of patients spending 12+ hours from DTA to admission"] = (
            month_df["Patients who have waited 12+ hrs from DTA to admission"]
            / month_df["Total emergency admissions"]
        )

        month_df = month_df[
            [
                "Parent Org",
                "Org name",
                "Percentage in 4 hours or less",
                "Attendances over 4hrs",
                "Total attendances",
                "Total emergency admissions via A&E",
                "Total emergency admissions",
                "Proportion of patients spending 4+ hours from DTA to admission",
                "Proportion of patients spending 12+ hours from DTA to admission",
            ]
        ]

        month_df["Period"] = month_year
        month_df["Period"] = pd.to_datetime(month_df["Period"], format="%B-%Y")

        df = pd.concat([df, month_df])

        df = df[df["Total attendances"] > 0]
        trusts_100 = df[df['Percentage in 4 hours or less']==100]['Org name'].unique().tolist()
        df = df[~df['Org name'].isin(trusts_100)]

    return df


def produce_total_df(df):
    
    '''Aggregate data from trust level to overall. Return as DataFrame.'''

    df = (
        df.groupby("Period")
        .agg({"Attendances over 4hrs": "sum", "Total attendances": "sum"})
        .reset_index()
    )

    df["Percentage in 4 hours or less"] = round(
        100 * (1 - (df["Attendances over 4hrs"] / df["Total attendances"])), 1
    )

    df["Total attendances (millions)"] = df["Total attendances"] / 1000000

    return df


def produce_region_df(df):

    '''Aggregate data from trust level to region level. Return as DataFrame.'''
    
    df = (
        df.groupby(["Period", "Parent Org"])
        .agg({"Attendances over 4hrs": "sum", "Total attendances": "sum"})
        .reset_index()
    )

    df["Percentage in 4 hours or less"] = round(
        100 * (1 - (df["Attendances over 4hrs"] / df["Total attendances"])), 1
    )

    return df
