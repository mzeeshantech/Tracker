from datetime import datetime, timedelta

from django.core import paginator
from django.utils.timezone import localtime, now, make_aware
from django.shortcuts import render
from django.db import connection
import pandas as pd
from django.http import JsonResponse
from django.utils.timezone import is_aware

from Tracker import settings
from django.utils.timezone import now
from django.core.paginator import Paginator

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


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
        ["16/08/2024 22:04:15", 0, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY S61426"],
        ["16/08/2024 22:04:17", 929000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN By S61426"],
        ["17/08/2024 01:07:55", 0, "8780 132CB A604 [ D-8780_8782_B ] BREAKER CLOSE CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 01:07:57", 845000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER CLOSED By N100497"],
        ["17/08/2024 19:33:21", 0, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 19:33:23", 920000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN By N97685"],
        ["17/08/2024 23:31:43", 221000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:52:48", 248000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN"],
        ["18/08/2024 01:55:00", 637000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:58:37", 868000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN"],
        ["16/08/2024 22:04:15", 0, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY S61426"],
        ["16/08/2024 22:04:17", 929000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN By S61426"],
        ["17/08/2024 01:07:55", 0, "8780 132CB A604 [ D-8780_8782_B ] BREAKER CLOSE CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 01:07:57", 845000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER CLOSED By N100497"],
        ["17/08/2024 19:33:21", 0, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 19:33:23", 920000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN By N97685"],
        ["17/08/2024 23:31:43", 221000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:52:48", 248000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN"],
        ["18/08/2024 01:55:00", 637000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:58:37", 868000000, "8780 132CB A604 [ D-8780_8782_B ] BREAKER OPEN"],
        ["16/08/2024 22:04:15", 0, "8780 132CB A605 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY S61426"],
        ["16/08/2024 22:04:17", 929000000, "8780 132CB A605 [ D-8780_8782_B ] BREAKER OPEN By S61426"],
        ["17/08/2024 01:07:55", 0, "8780 132CB A605 [ D-8780_8782_B ] BREAKER CLOSE CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 01:07:57", 845000000, "8780 132CB A605 [ D-8780_8782_B ] BREAKER CLOSED By N100497"],
        ["17/08/2024 19:33:21", 0, "8780 132CB A605 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 19:33:23", 920000000, "8780 132CB A605 [ D-8780_8782_B ] BREAKER OPEN By N97685"],
        ["17/08/2024 23:31:43", 221000000, "8780 132CB A605 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:52:48", 248000000, "8780 132CB A605 [ D-8780_8782_B ] BREAKER OPEN"],
        ["18/08/2024 01:55:00", 637000000, "8780 132CB A605 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:58:37", 868000000, "8780 132CB A605 [ D-8780_8782_B ] BREAKER OPEN"],
        ["16/08/2024 22:04:15", 0, "8780 132CB A606 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY S61426"],
        ["16/08/2024 22:04:17", 929000000, "8780 132CB A606 [ D-8780_8782_B ] BREAKER OPEN By S61426"],
        ["17/08/2024 01:07:55", 0, "8780 132CB A606 [ D-8780_8782_B ] BREAKER CLOSE CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 01:07:57", 845000000, "8780 132CB A606 [ D-8780_8782_B ] BREAKER CLOSED By N100497"],
        ["17/08/2024 19:33:21", 0, "8780 132CB A606 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 19:33:23", 920000000, "8780 132CB A606 [ D-8780_8782_B ] BREAKER OPEN By N97685"],
        ["17/08/2024 23:31:43", 221000000, "8780 132CB A606 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:52:48", 248000000, "8780 132CB A606 [ D-8780_8782_B ] BREAKER OPEN"],
        ["18/08/2024 01:55:00", 637000000, "8780 132CB A606 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:58:37", 868000000, "8780 132CB A606 [ D-8780_8782_B ] BREAKER OPEN"],
        ["16/08/2024 22:04:15", 0, "8780 132CB A607 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY S61426"],
        ["16/08/2024 22:04:17", 929000000, "8780 132CB A607 [ D-8780_8782_B ] BREAKER OPEN By S61426"],
        ["17/08/2024 01:07:55", 0, "8780 132CB A607 [ D-8780_8782_B ] BREAKER CLOSE CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 01:07:57", 845000000, "8780 132CB A607 [ D-8780_8782_B ] BREAKER CLOSED By N100497"],
        ["17/08/2024 19:33:21", 0, "8780 132CB A607 [ D-8780_8782_B ] BREAKER OPEN CTRL ISSUED BY REMOTE ISC SITE"],
        ["17/08/2024 19:33:23", 920000000, "8780 132CB A607 [ D-8780_8782_B ] BREAKER OPEN By N97685"],
        ["17/08/2024 23:31:43", 221000000, "8780 132CB A607 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:52:48", 248000000, "8780 132CB A607 [ D-8780_8782_B ] BREAKER OPEN"],
        ["18/08/2024 01:55:00", 637000000, "8780 132CB A607 [ D-8780_8782_B ] BREAKER CLOSED"],
        ["18/08/2024 01:58:37", 868000000, "8780 132CB A607 [ D-8780_8782_B ] BREAKER OPEN"],
    ]

    # Column names
    columns = ["ZX", "MS", "TEXT"]

    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Convert the time column to datetime
    df["ZX"] = pd.to_datetime(
        df["ZX"]
    )

    return df



def get_paginated_data(request, df):
    page_size = 10  # Number of items per page
    page = int(request.GET.get('page', 1))  # Get the page number from request
    start = (page - 1) * page_size
    end = page * page_size

    # Slice the DataFrame for pagination
    paginated_df = df.iloc[start:end]

    # Optional: calculate total pages
    total_pages = (len(df) + page_size - 1) // page_size  # Ceiling division

    # JsonResponse
    return ({
        'data': paginated_df,
        'page': page,
        'total_pages': total_pages
    })

def data_processing(df, only_parent_rows = True, only_child_rows = True, do_pagination = False, request = None, for_pdf = False):
    # Extract the breaker ID as the third word in the TEXT column
    df["Breaker_ID"] = df["TEXT"].str.split().str[2]

    # Initialize an empty list to store the results
    durations = []
    breakers_summary = []

    # Group by breaker ID
    grouped = df.groupby("Breaker_ID")
    all_breaker_ids = []

    # Find durations between OPEN and CLOSED for each breaker
    for breaker_id, group in grouped:
        all_breaker_ids.append(breaker_id)
        # group = group.sort_values("ZX")
        trips = []
        open_time = None
        open_by_cmd = False
        close_by_cmd = False
        breaker_trips_total_time = 0
        for i, row in group.iterrows():

            if "OPEN" in row["TEXT"]:
                if "CTRL ISSUED BY" in row["TEXT"]:
                    open_by_cmd = True
                if "CTRL ISSUED BY" in row["TEXT"]:
                    continue

                open_time = row["ZX"]
            elif ("CLOSED" in row["TEXT"] or "CLOSE CTRL" in row["TEXT"]) and open_time is not None:
                closed_time = row["ZX"]

                if "CTRL ISSUED BY" in row["TEXT"]:
                    close_by_cmd = True

                if "CTRL ISSUED BY" in row["TEXT"]:
                    continue



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
                    "operation": "Trip",
                    "location": row["LOCATION"]
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

    if not for_pdf:
        # Flatten data for display
        flat_data = []
        for summary in breakers_summary:
            if only_parent_rows:
                flat_data.append({
                    "breaker_id": summary["breaker_id"],
                    "total_trips": summary["total_trips"],
                    "start_time": None,
                    "end_time": None,
                    "duration": summary["total_trips_time"],
                    "operation": "Summary"
                })
            if only_child_rows:
                for trip in summary["child_rows"]:
                    flat_data.append({
                        "breaker_id": summary["breaker_id"],
                        "total_trips": None,
                        **trip
                    })

        result_df = pd.DataFrame(flat_data)
        # print(result_df)
        return result_df
    else:
        # Flatten data for display
        flat_data = []
        breakers_dict = {}
        for id in all_breaker_ids:
            breakers_dict[id] = []
        for summary in breakers_summary:
            if only_parent_rows:
                breakers_dict[summary["breaker_id"]].append({
                    "breaker_id": summary["breaker_id"],
                    "total_trips": summary["total_trips"],
                    "start_time": None,
                    "end_time": None,
                    "duration": summary["total_trips_time"],
                    "operation": "Summary"
                })
            if only_child_rows:
                for trip in summary["child_rows"]:
                    breakers_dict[summary["breaker_id"]].append({
                        "breaker_id": summary["breaker_id"],
                        "total_trips": None,
                        **trip
                    })

        return breakers_dict



def query_data(location=None, from_date=None, end_date=None, breaker_id=None):

    print(f"location = {location}")
    from_date = from_date.strftime("%d/%m/%Y")

    end_date = end_date.strftime("%d/%m/%Y")
    query_condition = ""
    if location != 'all' and location is not None:
        query_condition = f''' AND "A1"."LOCATION" = '{location}' '''

    if breaker_id != 'all' and breaker_id is not None:
        query_condition = f''' AND "A1"."TEXT" LIKE '%{breaker_id}%' '''

    query = f"""
            SELECT
                "A1"."TIME" as zx,
                "A1"."MS" AS "MS",
                "A1"."TEXT" AS "TEXT",
                "A1"."LOCATION" AS "LOCATION"
            FROM
                "ALARM" "A1"
            WHERE
                "A1"."TIME" >= TO_DATE('{from_date}', 'dd/mm/yyyy hh24:mi:ss')
                AND "A1"."TIME" <= TO_DATE('{end_date}', 'dd/mm/yyyy hh24:mi:ss')
                AND "A1"."TEXT" LIKE '%BREAKER%'
                AND (
                    "A1"."TEXT" LIKE '%OPEN%'
                    OR "A1"."TEXT" LIKE '%CLOSE%'
                )
                AND "A1"."TEXT" LIKE UPPER('%CB%')
                {query_condition}
            ORDER BY
                SUBSTR("A1"."TEXT", 1, INSTR("A1"."TEXT", 'BREAKER') - 2),
                "A1"."TIME"
            """

    # print(f"query = {query}")

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()  # Fetch all rows from the executed query
        columns = [col[0] for col in cursor.description]

    df = pd.DataFrame(rows, columns=columns)
    return df


def get_all_locations():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT location FROM alarm WHERE location IS NOT NULL")
        locations = [row[0] for row in cursor.fetchall()]  # Extract the first column (location)

    return locations

def get_all_breakers():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT REGEXP_SUBSTR(TEXT, '[^ ]+', 1, 3) AS extracted_value FROM ALARM WHERE TEXT IS NOT NULL ")
        breakers = [row[0] for row in cursor.fetchall()]  # Extract the first column (location)

    return breakers



def index(request):
    input_template_name = "hud"
    input_json_file = "hud"

    # template_file = f"./input_htmls/{input_template_name}.html"
    # json_file = f"./input_jsons/{input_json_file}.json"
    # output_html_file = f"./generated_htmls/{input_template_name}_new_html.html"  # Output HTML file (optional)
    # output_pdf_file = f"./generated_pdfs/{input_template_name}_output.pdf"  # Path to the output PDF file

    location = request.GET.get('location', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    breaker = request.GET.get('breaker', None)

    print(breaker)


    if start_date is None and end_date is None:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    df          = query_data(location, start_date, end_date, breaker_id=breaker)
    result      = data_processing(df, only_child_rows=False, do_pagination=True)

    pagniation_data      = get_paginated_data(request, result)

    result = pagniation_data["data"]


    results     = result.to_dict(orient='records')
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    context = {
        'breaker_data': results,
        'locations': get_all_locations(),
        'breakers': get_all_breakers(),
        'selected_location': location,
        'selected_breaker': breaker,
        'start_date' : start_date,
        'end_date' : end_date,
        'current_page_num': pagniation_data['page'],
        'total_pages': pagniation_data['total_pages'],
    }

    return render(request, 'Breaker/index.html', context)



def get_breaker_detail(request):
    location = request.GET.get('location', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    breaker_id = request.GET.get('breaker_id', None)

    if breaker_id is None:
        return JsonResponse({"error": "No breaker ID provided", "data": []}, status=400)

    if start_date is None and end_date is None:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    df = query_data(location, start_date, end_date, breaker_id)
    result = data_processing(df, only_parent_rows=False)
    result["open_by_cmd"] = result["open_by_cmd"].fillna("0")
    result["close_by_cmd"] = result["close_by_cmd"].fillna("0")
    result["total_trips"] = result["total_trips"].fillna("0")

    # Convert datetime to ISO format directly here
    result['start_time'] = result['start_time'].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    result['end_time'] = result['end_time'].apply(lambda x: x.isoformat() if pd.notnull(x) else None)

    # Convert the DataFrame to a list of dicts
    results = result.to_dict(orient='records')
    print(results)

    return JsonResponse({"data": results})


def generate_pdf(request):
    # Retrieve parameters from GET request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    location = request.GET.get('location')
    breaker = request.GET.get('breaker')

    print(request.GET)

    # Convert date strings to datetime objects
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Assume a default range of the last year if not provided
    if not start_date or not end_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

    df = query_data(location=location, from_date=start_date, end_date=end_date, breaker_id=breaker)
    result = data_processing(df, only_parent_rows=True, only_child_rows=True, for_pdf=True)

    data_for_template = {
        'total_records': len(df),
        'data': result,
        'start_date' : start_date,
        'end_date' : end_date,
        'location' : location,
        'breaker' : breaker
    }

    html_string = render_to_string('Breaker/pdf_template.html', data_for_template)
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'

    return response
