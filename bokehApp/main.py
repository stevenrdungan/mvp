# code shamelessly cribbed from https://github.com/bokeh/bokeh/tree/master/examples/app/export_csv

from os.path import dirname, join
import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, Button, DataTable, TableColumn, NumberFormatter, RangeSlider
from bokeh.io import curdoc

df = pd.read_csv(join(dirname(__file__), 'dataframe.csv')).loc[:,['Year','Player','Share']]
source = ColumnDataSource(data=dict())

def update():
    current = df[(df['Share'] >= range_slider.range[0]) & (df['Share'] <= range_slider.range[1])].dropna().reset_index(drop=True)
    source.data = {
        'Year'             : current.Year,
        'Player'           : current.Player,
        'Share'            : current.Share.map(lambda x: '{0:.3g}'.format(x))
,
    }

range_slider = RangeSlider(title="Share Range", start=0.0, end=1.0, step=.01, range = (0.0,1.0))
range_slider.on_change('range', lambda attr, old, new: update())

button1 = Button(label="Export CSV", button_type="success")
button1.callback = CustomJS(args=dict(source=source),
                           code=open(join(dirname(__file__), "download_csv.js")).read())

button2 = Button(label="Export JSON", button_type="success")
button2.callback = CustomJS(args=dict(source=source),
                           code=open(join(dirname(__file__), "download_json.js")).read())

columns = [
    TableColumn(field="Year", title="Year"),
    TableColumn(field="Player", title="Player"),
    TableColumn(field="Share", title="Share")
]

data_table = DataTable(source=source, columns=columns, width=800, height=600)

controls = widgetbox(range_slider, button1, button2)
table = widgetbox(data_table)

curdoc().add_root(row(controls, table))
curdoc().title = "Export JSON"

update()
