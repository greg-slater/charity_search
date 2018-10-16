# from bokeh.models import  ColumnDataSource, Legend, CustomJS, Select
# from bokeh.plotting import figure
# from bokeh.palettes import Category10
# from bokeh.layouts import row

from os.path import dirname, join

from bokeh.layouts import row, column, layout, widgetbox
from bokeh.models import ColumnDataSource, CustomJS, Div
from bokeh.models.widgets import RangeSlider, Select, TextInput, Button, DataTable, TableColumn, Tabs, Panel, NumberFormatter, HTMLTemplateFormatter

import pandas as pd
import math

from bokeh.server.server import Server

# from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

def modify_doc(doc):

    df = pd.read_csv(join(dirname(__file__), 'charity_input.csv'))

    source = ColumnDataSource(data=dict())

    table_title_div = Div(text="")

    m_dict = dict({'True': True, 'False': False})

    # calculate min and max of latest_income, to nearest £100,000
    inc_min = math.floor(min(df['latest_income'])/100000)*100000
    inc_max = math.ceil(max(df['latest_income'])/100000)*100000

    # Create lists of all regions and districts present in dataset to use in dropdown filter
    regions = sorted(list(set(df['region'][df.region.notnull()].values)))
    regions.insert(0,'All')
    districts = sorted(list(set(df['district'][df.district.notnull()].values)))
    districts.insert(0,'All')

    # function to quickly return sorted list of values from current selection,
    # used to update dropdown filter below
    def col_list(table, col):
        l1 = ['All']
        l2 = sorted(list(set(table[col][table[col].notnull()].values)))
        l1.extend(l2)
        return l1

    def update():

        # conditions of filters to create current selection
        current = df[(df['latest_income'] >= inc_slider.value[0]) &
                     (df['latest_income'] <= inc_slider.value[1])]

        if act_match.value != "All":
            current = current[current['activity_keyword_match'] == m_dict[act_match.value]]
        if gr_match.value != "All":
            current = current[current['grant_keyword_match'] == m_dict[gr_match.value]]
        if district_input.value != "All":
            current = current[current['district'] == district_input.value]
        if name_input.value != "":
            current = current[current.name.str.contains(name_input.value)]
        if id_input.value != "":
            current = current[current.charity_id == int(id_input.value)]

        if region_input.value != "All":
            current = current[current['region'] == region_input.value]
            district_input.options = col_list(current, 'district')
        else: district_input.options = districts

        # define source data as dictionary of current selection
        source.data = current.to_dict('list')

        # update selection counter div based on length of current
        table_title = "<b>%s</b> charities selected" % "{:,}".format(len(current))
        table_title_div.update(text=table_title)

    match_options = ["All", "True", "False"]

    inc_slider = RangeSlider(title="Latest Income", start=inc_min, end=inc_max, value=(inc_min, inc_max), step=100000, format="0,0")
    act_match = Select(title="Activity Keyword Match", options=match_options, value="All")
    gr_match = Select(title="Grant Keyword Match", options=match_options, value="All")
    region_input = Select(title="Region", options=regions, value="All")
    district_input = Select(title="District", options=districts, value="All")
    name_input = TextInput(value="", title="Charity Name Search")
    id_input = TextInput(value="", title="Charity ID Search")


    bok_cols = [#TableColumn(field='charity_id', title='Charity ID', width=100),
                TableColumn(field='charity_id', title='Charity ID', width=100, #),
                            formatter=HTMLTemplateFormatter(template='<a href="http://beta.charitycommission.gov.uk/charity-details/?regid=<%= value %>&subid=0"target="_blank"><%= value %></a>')),
                TableColumn(field='name', title='Name', width=200),
                TableColumn(field='activities', title='Activities', width=300),
                TableColumn(field='website', title='Website', width=200,
                            formatter=HTMLTemplateFormatter(template='<a href="http://<%= value %>"target="_blank"><%= value %></a>')),
                TableColumn(field='latest_income', title='Latest Income', width=100,
                            formatter=NumberFormatter(format='£ 0,0'))]


    data_table = DataTable(source=source, columns=bok_cols, width=1000, height=600)

    controls = [inc_slider, act_match, gr_match, region_input, district_input,name_input, id_input] #
    for control in controls:
        control.on_change('value', lambda attr, old, new: update())


    button = Button(label="Download", button_type="success")
    button.callback = CustomJS(args=dict(source=source),
                               code=open(join(dirname(__file__), "download.js")).read())


    table = widgetbox(data_table)
    table_section = column(table_title_div, data_table)
    filters = widgetbox(*controls, button, sizing_mode='scale_width')

    desc = Div(text=open(join(dirname(__file__), 'templates/index.html')).read(), width=1000)


    l1 = layout([
        [desc],
        [filters, table_section]
        # [Div()],
        # [filters, table_section],
    ], sizing_mode='fixed')

    update()

    doc.add_root(l1)



def run():

    server = Server({'/': modify_doc}, num_procs=1)
    server.start()

    print('Opening Bokeh application on http://localhost:5006/')

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
