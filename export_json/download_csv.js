// code shamelessly cribbed from https://github.com/bokeh/bokeh/tree/master/examples/app/export_csv
// at this point this code is more or less a direct copy

var data = source.data;
var filetext = 'Year,Player,Share\n';
for (i=0; i < data['Player'].length; i++) {
    var currRow = [data['Year'][i].toString(),
                   data['Player'][i].toString(),
                   data['Share'][i].toString().concat('\n')];

    var joined = currRow.join();
    filetext = filetext.concat(joined);
}

var filename = 'data_result.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
}

else {
    var link = document.createElement("a");
    link = document.createElement('a')
    link.href = URL.createObjectURL(blob);
    link.download = filename
    link.target = "_blank";
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'))
}
