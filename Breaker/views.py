from datetime import datetime

from django.utils.timezone import localtime, now, make_aware
from django.shortcuts import render
from django.db import connection
import pandas as pd
from django.utils.timezone import is_aware

from Tracker import settings
from django.utils.timezone import now


def convert_minutes_to_dhms(minutes):
    """Convert minutes to a string format of days, hours, minutes, and seconds."""
    total_seconds = int(minutes * 60)
    days = total_seconds // (24 * 3600)
    total_seconds %= (24 * 3600)
    hours = total_seconds // 3600
    total_seconds %= 3600
    mins = total_seconds // 60
    seconds = total_seconds % 60

    # Format output based on presence of days
    if days > 0:
        return "{} Days {}h {}m {}s".format(days, hours, mins, seconds)
    else:
        return "{}h {}m {}s".format(hours, mins, seconds)


def dummy_data():
    # Data provided
    data = [
        ["16/08/2024 22:04:15", 0, "8780 132CB A602 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY S61426"],
        ["16/08/2024 22:04:17", 929000000, "8780 132CB A602 [ D-8780_8782_B ] BREAKER OPEN By S61426"],
        ["17/08/2024 01:07:55", 0, "8780 132CB A602 [ D-8780_8782_B ] BREAKER CLOSE CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 01:07:57", 845000000, "8780 132CB A602 [ D-8780_8782_B ] BREAKER CLOSED By N100497"],
        ["17/08/2024 19:33:21", 0, "8780 132CB A602 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 19:33:23", 920000000, "8780 132CB A602 [ D-8780_8782_B ] BREAKER OPEN By N97685"],
        ["17/08/2024 23:31:43", 221000000, "8780 132CB A602 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:52:48", 248000000, "8780 132CB A602 [ D-8780_8782_B ] BREAKER OPEN"],
        ["18/08/2024 01:55:00", 637000000, "8780 132CB A602 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:58:37", 868000000, "8780 132CB A602 [ D-8780_8782_B ] BREAKER OPEN"],
        ["18/08/2024 20:51:32", 0, "8780 132CB A602 [ D-8780_8782_B ] BREAKER CLOSE CTRL ISSUED BY REMOTE ISC SITE"],
        ["18/08/2024 20:51:33", 900000000, "8780 132CB A602 [ D-8780_8782_B ] BREAKER CLOSED By N97685"],
        ["25/04/2024 11:45:50", 323000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By SCADA"],
        ["25/04/2024 14:11:31", 323000000, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN"],
        ["25/04/2024 14:12:07", 717000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By SCADA"],
        ["26/04/2024 10:33:26", 883000000, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN"],
        ["26/04/2024 10:33:29", 185000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By SCADA"],
        ["26/04/2024 11:23:11", 883000000, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN"],
        ["26/04/2024 23:10:54", 533000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By SCADA"],
        ["26/04/2024 23:40:53", 883000000, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN"],
        ["26/04/2024 23:40:56", 569000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By SCADA"],
        ["27/04/2024 00:50:30", 883000000, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN"],
        ["27/04/2024 00:50:33", 606000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By SCADA"],
        ["27/04/2024 18:38:22", 116000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By SCADA"],
        ["28/04/2024 12:28:39", 546000000, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN"],
        ["28/04/2024 12:29:51", 599000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By SCADA"],
        ["26/09/2024 12:48:12", 0, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN CTRL ISSUED BY REMOTE ISC SITE"],
        ["26/09/2024 12:48:13", 775000000, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN By N75436"],
        ["26/09/2024 16:31:42", 0, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSE CTRL ISSUED BY REMOTE ISC SITE"],
        ["26/09/2024 16:31:43", 73000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By N75436"],
        ["26/09/2024 21:35:46", 0, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN CTRL ISSUED BY REMOTE ISC SITE"],
        ["26/09/2024 21:35:48", 414000000, "8780 132CB A603 [ W603 - T601 ] BREAKER OPEN By N97685"],
        ["26/09/2024 22:02:11", 0, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSE CTRL ISSUED BY REMOTE ISC SITE"],
        ["26/09/2024 22:02:12", 737000000, "8780 132CB A603 [ W603 - T601 ] BREAKER CLOSED By N97685"],
    ]

    # Column names
    columns = ["ETA_MASTER.HISTIME.FORMATTIME(TIME,'11','DD/MM/YYYYHH24:MI:SS')", "MS", "TEXT"]

    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Convert the time column to datetime
    df["ETA_MASTER.HISTIME.FORMATTIME(TIME,'11','DD/MM/YYYYHH24:MI:SS')"] = pd.to_datetime(
        df["ETA_MASTER.HISTIME.FORMATTIME(TIME,'11','DD/MM/YYYYHH24:MI:SS')"]
    )

    return df


def testing(df):
    # Extract the breaker ID as the third word in the TEXT column
    df["Breaker_ID"] = df["TEXT"].str.split().str[2]

    # Initialize an empty list to store the results
    durations = []
    breakers_summary = []

    # Group by breaker ID
    grouped = df.groupby("Breaker_ID")

    # Find durations between OPEN and CLOSED for each breaker
    for breaker_id, group in grouped:
        group = group.sort_values("ETA_MASTER.HISTIME.FORMATTIME(TIME,'11','DD/MM/YYYYHH24:MI:SS')")
        trips = []
        open_time = None
        open_by_cmd = False
        close_by_cmd = False
        breaker_trips_total_time = 0
        for i, row in group.iterrows():
            # print(i)
            # print(row)
            # print(group.iloc[1])
            # exit()

            if "OPEN" in row["TEXT"]:
                if "OPEN BY" in row["TEXT"]:
                    continue
                if "CTRL ISSUED BY" in row["TEXT"]:
                    open_by_cmd = True

                open_time = row["ETA_MASTER.HISTIME.FORMATTIME(TIME,'11','DD/MM/YYYYHH24:MI:SS')"]
            elif ("CLOSED" in row["TEXT"] or "CLOSE CTRL" in row["TEXT"]) and open_time is not None:
                closed_time = row["ETA_MASTER.HISTIME.FORMATTIME(TIME,'11','DD/MM/YYYYHH24:MI:SS')"]
                if "CLOSED BY" in row["TEXT"]:
                    continue

                if "CTRL ISSUED BY" in row["TEXT"]:
                    close_by_cmd = True

                if isinstance(closed_time, str):
                    closed_time = datetime.strptime(closed_time, "%d/%m/%Y %H:%M:%S")  # Adjust the format as needed

                if isinstance(open_time, str):
                    open_time = datetime.strptime(open_time, "%d/%m/%Y %H:%M:%S")

                duration = (closed_time - open_time).total_seconds() / 60  # duration in minutes
                breaker_trips_total_time += duration
                trips.append({
                    "start_time": open_time,
                    "end_time": closed_time,
                    "duration": convert_minutes_to_dhms(duration),
                    "open_by_cmd": open_by_cmd,
                    "close_by_cmd": close_by_cmd,
                    "operation": "Trip"
                })
                open_time = None  # Reset after finding a pair
                open_by_cmd = False
                close_by_cmd = False

        # Append summary row for the breaker
        breakers_summary.append({
            "breaker_id": breaker_id,
            "total_trips_time": convert_minutes_to_dhms(breaker_trips_total_time),
            "total_trips": len(trips),
            "child_rows": trips
        })

    # Flatten data for display
    flat_data = []
    for summary in breakers_summary:
        flat_data.append({
            "breaker_id": summary["breaker_id"],
            "total_trips": summary["total_trips"],
            "start_time": None,
            "end_time": None,
            "duration": summary["total_trips_time"],
            "operation": "Summary"
        })
        for trip in summary["child_rows"]:
            flat_data.append({
                "breaker_id": summary["breaker_id"],
                "total_trips": None,
                **trip
            })

    result_df = pd.DataFrame(flat_data)
    # print(result_df)
    return result_df


def query_data(location=None, from_date='2024-01-01 00:00:00'):
    # SQL query
    sql_query = """
    SELECT 
        id,
        TO_CHAR("time", 'DD/MM/YYYY HH24:MI:SS') AS "ETA_MASTER.HISTIME.FORMATTIME(TIME,'11','DD/MM/YYYYHH24:MI:SS')",
        "ms" AS "MS",
        "text" AS "TEXT"
    FROM 
        "alarm"
    WHERE 
        "time" >= TO_TIMESTAMP('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
        AND "time" <= TO_TIMESTAMP('2024-11-25 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
        AND "text" ILIKE '%BREAKER%'
        AND (
            "text" ILIKE '%OPEN%'
            OR "text" ILIKE '%CLOSE%'
        )
        AND "text" ILIKE '%CB%'
    """

    # Add location filter if a location is selected
    if location:
        sql_query += " AND \"location\" = '{}'".format(location)
        params = [location]  # Use parameterized query to avoid SQL injection
    else:
        params = []  # No parameters needed if no location filter

    # Add ORDER BY clause
    sql_query += """
        ORDER BY 
            SUBSTRING("text" FROM 1 FOR POSITION('BREAKER' IN "text") - 1), 
            "time"
        """
    # Execute the raw query
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()  # Fetch all rows from the executed query
        columns = [col[0] for col in cursor.description]

    df = pd.DataFrame(rows, columns=columns)
    return df


def get_all_locations():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT location FROM alarm WHERE location IS NOT NULL")
        locations = [row[0] for row in cursor.fetchall()]  # Extract the first column (location)

    return locations


def fetch_data(request):
    location = request.GET.get('location', None)
    df = query_data(location=location)
    # df = dummy_data()
    result = testing(df)
    # results = result.to_json(orient='records')
    results = result.to_dict(orient='records')

    context = {
        'breaker_data': results,
        'locations': get_all_locations(),
        'selected_location': location
    }

    return render(request, 'Breaker/index.html', context)


def index(request):
    location = request.GET.get('location', None)
    df = query_data()
    # df = dummy_data()
    result = testing(df)
    # results = result.to_json(orient='records')
    results = result.to_dict(orient='records')

    context = {
        'breaker_data': results,
        'locations': get_all_locations(),
        'selected_location': location
    }

    return render(request, 'Breaker/index.html', context)
