# code shamelessly cribbed from https://github.com/bokeh/bokeh/tree/master/examples/app/export_csv

from os.path import dirname, join
import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, Button, DataTable, TableColumn, NumberFormatter
from bokeh.io import curdoc

df = pd.read_csv(join(dirname(__file__), 'dataframe.csv')).loc[:,['Year','Player','Share']]
source = ColumnDataSource(data=dict())

def update():
    current = df[df['Share'] <= slider.value].dropna()
    source.data = {
        'Year'             : current.Year,
        'Player'           : current.Player,
        'Share'            : current.Share,
    }

slider = Slider(title="Vote Share", start=0.0, end=1.0, value=1.0, step=.01)
slider.on_change('value', lambda attr, old, new: update())

button = Button(label="Export CSV", button_type="success")
button.callback = CustomJS(args=dict(source=source),
                           code=open(join(dirname(__file__), "download_csv.js")).read())

columns = [
    TableColumn(field="Year", title="Year"),
    TableColumn(field="Player", title="Player"),
    TableColumn(field="Share", title="Share")
]

data_table = DataTable(source=source, columns=columns, width=800)

controls = widgetbox(slider, button)
table = widgetbox(data_table)

curdoc().add_root(row(controls, table))
curdoc().title = "Export JSON"

update()
