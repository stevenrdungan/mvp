var data = source.data;
var arr = []
for (i=0; i < data['Player'].length; i++) {
    var currRow = {};
    currRow['Year'] = data['Year'][i];
    currRow['Player'] = data['Player'][i];
    currRow['Share'] = data['Share'][i];
    arr.push(currRow);
}

var filename = 'data_result_json.json';
var blob = new Blob([JSON.stringify(arr)], { type: 'text/json;charset=utf-8;' });

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
