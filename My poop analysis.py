# -*- coding: utf-8 -*-
"""
Poop analysis

Created 2020

@author: PClough
"""

import pandas as pd
import numpy as np
import chart_studio
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
from scipy import stats
import datetime as dt
from time import strptime
import calendar

df = pd.read_excel("Poo data.xlsx", engine='openpyxl')

chart_studio.tools.set_credentials_file(username='YOUR USERNAME HERE', api_key='YOUR API HERE')

#%% Violin plot for day of week on x axis and type of poo on y axis

fig2 = go.Figure()

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Remove 'Type ' before the number
df['Type of poop 💩? '] = df['Type of poop 💩? '].str.replace('Type ', '')

Date_column = df['When did the poo occur? '].dt.strftime("%a")

for day in days:
    fig2.add_trace(go.Violin(x = Date_column[Date_column == day],
        y = df['Type of poop 💩? '][Date_column == day],
        name = day,
        box_visible = True,
        meanline_visible = True,
        showlegend = False,
        fillcolor = 'chocolate',
        line = dict(color = 'DarkSalmon')))
    
fig2.update_layout(yaxis = dict(range=[0.5,7.5]), title = "Average poo type over whole year", font = dict(size = 16))
fig2.update_yaxes(ticks="inside", tick0 = 1, dtick = 1, title = "Bristol stool scale index")

plot(fig2)

# %% Ridgeline plot for day of week on x axis and type of poo on y axis

# 12 rows of data, one for each month
# 7 columns of data, averaging that months poo types
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Remove 'Type ' before the number
df['Type of poop 💩? '] = df['Type of poop 💩? '].str.replace('Type ', '')

New_Date_column = df['When did the poo occur? '].dt.strftime("%b")
i = 0
max_val = 0
data = np.zeros([12,100]) # the value of 100 is just massively oversizing it, assuming there will be less than 100 poo's of a single type in one month
for month in months:
    for j in range(1,8):
        data[i, np.sum(df['Type of poop 💩? '][New_Date_column == month] == str(j))] = j-1
        if max_val < np.sum(df['Type of poop 💩? '][New_Date_column == month] == str(j)):
            max_val = np.sum(df['Type of poop 💩? '][New_Date_column == month] == str(j))   
    i += 1
    
# Find where the furthest right hand datapoint is and then cut everything off after that
idx = np.arange(max_val+1, 100)
data  = np.delete(data, idx, axis=1)

data[data == 0] = 'nan'

fig3 = go.Figure()

for data_line in data:
    fig3.add_trace(go.Violin(x=data_line))

fig3.update_traces(orientation='h', side='positive', width=2, points=False)
fig3.update_layout(xaxis_showgrid=False, 
                   xaxis_zeroline=False, 
                   xaxis=dict(range=[0,8]), 
                   title = "Average poo type over whole year", 
                   font = dict(size = 16))

plot(fig3)


#%% Violin plot for day of week on x axis and type of poo on y axis broken out month by month

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

fig4 = make_subplots(rows=2, cols=6, shared_yaxes=True, subplot_titles=(months))

# Remove 'Type ' before the number
df['Type of poop 💩? '] = df['Type of poop 💩? '].str.replace('Type ', '')

Date_column = df['When did the poo occur? '].dt.strftime("%a")

row_num = 1
col_num = 0
for month in months:
    col_num += 1
    if col_num > 6:
        col_num = 1
        row_num = 2
    for day in days:
        fig4.add_trace(go.Violin(x = Date_column[Date_column == day][New_Date_column == month],
            y = df['Type of poop 💩? '][Date_column == day][New_Date_column == month],
            name = month + day,
            box_visible = True,
            meanline_visible = True,
            showlegend = False, 
            fillcolor = 'chocolate',
            line = dict(color = 'DarkSalmon')),
            row = row_num, col = col_num)

fig4.update_layout(yaxis = dict(range=[0.5,7.5]), title = "Average poo type, broken down month-by-month", font = dict(size = 16))
fig4.update_yaxes(ticks="inside", col = 1, tick0 = 1, dtick = 1, title = "Bristol stool scale index")
fig4.update_xaxes(ticks="inside")

plot(fig4)

# %% Calendar plot of each day and number of poos, darker colour for more poos

# Number of poos for each day
Num_of_poos = pd.DataFrame()

j = 0
for i in df['When did the poo occur? '].dt.strftime("%x").unique():
    Num_of_poos.loc[j, 'Date'] = i
    Num_of_poos.loc[j, 'Day'] = pd.to_datetime(i).strftime("%d")
    Num_of_poos.loc[j, 'Month'] = pd.to_datetime(i).strftime("%b")
    Num_of_poos.loc[j, 'Count'] = (df['When did the poo occur? '].dt.strftime("%x") == i).sum()
    j += 1

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

total_poos_in_month = []
plot_titles = []
j = 0
for i in months:
    total_poos_in_month.append(int(Num_of_poos['Count'][Num_of_poos['Month'] == i].sum()))
    plot_titles.append(i + '<br>Total poopies = ' + str(total_poos_in_month[j]))
    j += 1

fig7 = make_subplots(rows = 2, cols = 6, shared_yaxes = True, subplot_titles = plot_titles)

year = 2020
row_num = 1
col_num = 0
for month in months:
    col_num += 1
    if col_num > 6:
        col_num = 1
        row_num = 2
    
    MyMonthData = calendar.monthcalendar(2020, strptime(month, '%b').tm_mon)
    z = MyMonthData[::-1]
    
    m = 0
    for i in z:
        n = 0
        for j in i:
            if j == 0:
                z[m].pop(n)
                z[m].insert(n, '')
            elif any((Num_of_poos['Day'] == str(j).zfill(2)) & (Num_of_poos['Month'] == month)) == False:
                z[m].pop(n)
                z[m].insert(n, 0)
            else:
                z[m].pop(n)
                z[m].insert(n, int(Num_of_poos.loc[(Num_of_poos['Day'] == str(j).zfill(2)) & (Num_of_poos['Month'] == month), 'Count']))
            n += 1
        m += 1
    
    name = []
    for a in calendar.Calendar().monthdatescalendar(year, strptime(month, '%b').tm_mon):
        for b in a:
               name.append(b.strftime("%d %b %Y"))
    
    name = np.reshape([inner for inner in name], (len(MyMonthData), 7))
    name = name[::-1]
    
    fig7.add_trace(go.Heatmap(
        x = days,
        y = list(range(len(MyMonthData), 0)),
        z = z,
        meta = name,
        hovertemplate = 'Date: %{meta} <br>Number of poos: %{z}<extra></extra>',
        xgap = 1, ygap = 1,
        zmin = 0, zmax = max(Num_of_poos['Count']), 
#        colorscale = "turbid"),
        colorscale = [
        [0, 'rgb(249, 238, 229)'], # 0 for the prettiness 
        [0.14, 'rgb(249, 230, 217)'], # 0
        [0.29, 'rgb(204, 153, 102)'], # 1
        [0.43, 'rgb(153, 102, 51)'], # 2
        [0.57, 'rgb(115, 77, 38)'], # 3
        [0.71, 'rgb(77, 51, 25)'], # 4
        [1, 'rgb(38, 26, 13)']]), # 5
        row = row_num, col = col_num)

fig7['layout'].update(plot_bgcolor = 'white', 
                      title_text = "Poopy calendar", 
                      yaxis_showticklabels = False, 
                      yaxis7_showticklabels = False, 
                      font = dict(size = 16))


plot(fig7)

# %% Distribution of poos on stool scale per day

days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Remove 'Type ' before the number
df['Type of poop 💩? '] = df['Type of poop 💩? '].str.replace('Type ', '')

Date_column = df['When did the poo occur? '].dt.strftime("%a")

Total_poos = len(df['Type of poop 💩? '])
ydata = []
for day in days:
        ydata.append((len(df['Type of poop 💩? '][Date_column == day])/Total_poos)*100)
    
fig9 = go.Figure()    
fig9.add_trace(go.Bar(x = days,
        y = ydata,
        hovertemplate = '%{y:.1f}%<extra></extra>',
        name = day,
        showlegend = False,
        marker_color = ('rgb(166,86,50)')))
    
fig9.update_layout(title = "Poo distribution by day", font = dict(size = 16))
fig9.update_yaxes(range=[0, 20], ticks = "inside", title = "Percentage of poos / %")
fig9.update_xaxes(title = "Day of week")

plot(fig9)


#should make this a stacked bar chart of type of poo stacked with the total number of poos as the overall height. 

#%% Most frequent time of day

timerange = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
X_titles = [t + ':00' for t in timerange]

# Remove 'Type ' before the number
df['Type of poop 💩? '] = df['Type of poop 💩? '].str.replace('Type ', '')

Time_column = df['When did the poo occur? '].dt.strftime("%H")

Total_poos = len(df['Type of poop 💩? '])
ydata = []
for t in timerange:
        ydata.append((len(df['Type of poop 💩? '][Time_column == t])/Total_poos)*100)
    
fig10 = go.Figure()    
fig10.add_trace(go.Bar(x = timerange,
        y = ydata,
        hovertemplate = '%{y:.1f}%<extra></extra>',
        showlegend = False,
        marker_color = ('rgb(166,86,50)')))
    
fig10.update_layout(title = "Poo distribution by time", font = dict(size = 16))
fig10.update_yaxes(range=[0, 20], ticks = "inside", title = "Percentage of poos / %")
fig10.update_xaxes(ticks = "inside", title = "Time of day", tickmode = 'array', tickvals = [int(t) for t in timerange], ticktext = X_titles)

plot(fig10)

# %% Distribution by type

Type_of_poop = [str(i) for i in range(1,8)] # 1 to 7

# Remove 'Type ' before the number
df['Type of poop 💩? '] = df['Type of poop 💩? '].str.replace('Type ', '')

Total_poos = len(df['Type of poop 💩? '])
ydata = []
for poo in Type_of_poop:
        ydata.append((sum(df['Type of poop 💩? '] == poo)/Total_poos)*100)
    
fig11 = go.Figure()    
fig11.add_trace(go.Bar(x = Type_of_poop,
        y = ydata,
        hovertemplate = '%{y:.1f}%<extra></extra>',
        showlegend = False,
        marker_color = ('rgb(166,86,50)')))
    
fig11.update_layout(title = "Poo distribution by type", font = dict(size = 16))
fig11.update_yaxes(range=[0, 60], ticks = "inside", title = "Percentage of poos / %")
fig11.update_xaxes(title = "Type of poo")

plot(fig11)


# %% Distribution by type excluding Jan and Feb

Type_of_poop = [str(i) for i in range(1,8)] # 1 to 7
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Remove 'Type ' before the number
df['Type of poop 💩? '] = df['Type of poop 💩? '].str.replace('Type ', '')

Total_poos = len(df['Type of poop 💩? '])
ydata = []
for poo in Type_of_poop:
        ydata.append(sum(np.logical_and(df['Type of poop 💩? '] == poo, df['When did the poo occur? '].dt.strftime("%m") > '02')/Total_poos)*100)
    
fig12 = go.Figure()    
fig12.add_trace(go.Bar(x = Type_of_poop,
        y = ydata,
        hovertemplate = '%{y:.1f}%<extra></extra>',
        showlegend = False,
        marker_color = ('rgb(166,86,50)')))
    
fig12.update_layout(title = "Poo distribution by type (excluding Jan and Feb)", font = dict(size = 16))
fig12.update_yaxes(range=[0, 60], ticks = "inside", title = "Percentage of poos / %")
fig12.update_xaxes(title = "Type of poo")

plot(fig12)

#%% Poo stats

# Remove 'Type ' before the number
df['Type of poop 💩? '] = df['Type of poop 💩? '].str.replace('Type ', '')

# Number of poos for each day
Num_type_of_poos = pd.DataFrame()

j = 0
for i in df['When did the poo occur? '].dt.strftime("%x").unique():
    Num_type_of_poos.loc[j, 'Date'] = i
    Num_type_of_poos.loc[j, 'Day'] = pd.to_datetime(i).strftime("%d")
    Num_type_of_poos.loc[j, 'Month'] = pd.to_datetime(i).strftime("%b")
    Num_type_of_poos.loc[j, 'Count'] = (df['When did the poo occur? '].dt.strftime("%x") == i).sum()
    Num_type_of_poos.loc[j, 'Type'] = np.abs(int(df['Type of poop 💩? '][j]) - 4)
    j += 1

# Max number of poos in a day, week, month
Max_poopys = np.max(Num_type_of_poos['Count'])
print('Max poos in a day =', Max_poopys
      
# Total poos in a year
Total_annual_poos = np.size(Num_type_of_poos, 0)
print('Total poos in a year =', Total_annual_poos)

# Total days without poos

# Create a list of dates in each year
# Remove dates based on if the year is not 2020 and then remove duplicate dates (check order duplicates though)
flat_list = []
for sublist in calendar.Calendar().yeardatescalendar(2020):
    for item3 in sublist:
        for item2 in item3:
            for item in item2:
                if item.strftime("%Y") != '2020':
                    continue
                else:
                    flat_list.append(item)

# Remove duplicates
flat_list = list(dict.fromkeys(flat_list))

# Produce list of dates of poos
new_date_list = []
for i in Num_type_of_poos['Date']:
    new_date_list.append(dt.datetime.strptime(i, '%m/%d/%y').date())


Total_no_poo_days = 0
for i in flat_list:
    if i not in new_date_list:
        Total_no_poo_days += 1

print('Total number of days without a poo =', Total_no_poo_days)

# Total days with 3 or more poos


# Average poo's per day, week, month


# Longest poo streak
Longest_poo_streak = 0
poo_streak = 0
for i in flat_list:
    if i in new_date_list:
        poo_streak += 1
    else:
        poo_streak = 0
    # print(poo_streak)
    if poo_streak > Longest_poo_streak:
        date_of_end = i
        # date_of_start = i
        Longest_poo_streak = poo_streak
        
print('Longest poo streak =', Longest_poo_streak, '   ended =', dt.datetime.strftime(date_of_end, "%d %B %Y"))


# Longest time between poos    
Longest_time_between_poos = dt.timedelta(0)
poo_time = dt.timedelta(0)
prev_time = df['When did the poo occur? '][0]
for i in df['When did the poo occur? '][1::]:
    poo_time = i - prev_time
    prev_time = i
    if poo_time > Longest_time_between_poos:
        date_of_end = i
        Longest_time_between_poos = poo_time
        
print('Longest time between poos =', Longest_time_between_poos, '   ended =', dt.datetime.strftime(date_of_end, "%d %B %Y %H:%M:%S"))

# Shortest time between poos
Shortest_time_between_poos = dt.timedelta(0)
poo_time = dt.timedelta(0)
prev_time = df['When did the poo occur? '][0]
for i in df['When did the poo occur? '][1::]:
    poo_time = i - prev_time
    prev_time = i
    if poo_time < Shortest_time_between_poos:
        date_of_end = i
        Shortest_time_between_poos = poo_time
        if Shortest_time_between_poos.days < 0:
            Shortest_time_between_poos = dt.timedelta(days=0, seconds=Shortest_time_between_poos.seconds, microseconds=Shortest_time_between_poos.microseconds)
        
print('Shortest time between poos =', Shortest_time_between_poos, '   ended =', dt.datetime.strftime(date_of_end, "%d %B %Y %H:%M:%S"))

# Average and median time between poos
poo_time = []
prev_time = df['When did the poo occur? '][0]
for i in df['When did the poo occur? '][1::]:
    poo_time.append(i - prev_time)
    prev_time = i
    
Average_time_between_poos = np.mean(poo_time) 
print('Average time between poos =', Average_time_between_poos)

Median_time_between_poos = np.median(poo_time) 
print('Median time between poos =', Median_time_between_poos)

Mode_time_between_poos = stats.mode(poo_time) 
print('Mode time between poos =', Mode_time_between_poos)

#%% Plot distribution of poos
# x = time between poos in 1 hour time ranges
# y = frequency of poos in time ranges

x_data = range(0, int(max(poo_time).seconds/3600 + max(poo_time).days*24))

# convert the list of timedeltas to hours
pt = []
for j in poo_time:
    pt.append(j.seconds/3600 + j.days*24)

# count how many fall within the hourly time brackets
prev_i = x_data[0]
y_data = []
count = 0
for i in x_data[1::]:
    for j in pt:
        if j < i and j > prev_i:
            count += 1
    y_data.append(count)
    count = 0
    prev_i = i

fig13 = go.Figure()
fig13.add_trace(go.Bar(x = list(x_data),
        y = y_data,
        hovertemplate = '%{y:.1f}%<extra></extra>',
        showlegend = False,
        marker_color = ('rgb(166,86,50)')))
    
fig13.update_layout(title = "Poo distribution by time since last poo", font = dict(size = 16))
fig13.update_yaxes(range=[0, 40], ticks = "inside", title = "Percentage of poos / %")
fig13.update_xaxes(title = "Time since last poo (hours)")

plot(fig13)


