from rcp import get_poll_data
from prettytable import PrettyTable

x = PrettyTable()

td = get_poll_data(
    "https://www.realclearpolitics.com/epolls/other/president_trump_job_approval-6179.html"
)

x.field_names = list(td[0]["data"][0].keys())
x.align = "l"

for row in td[0]["data"]:
    x.add_row(row.values())

print(x)
