var data = source.data;
var filetext = 'charity_id,name,activities,website,latest_income,activity_keyword_match,grant_keyword_match\n';
for (var i = 0; i < data['charity_id'].length; i++) {
    var currRow = [data['charity_id'][i].toString(),
                   '"' + data['name'][i] + '"',
                   '"' + data['activities'][i] + '"',
                   '"' + data['website'][i] + '"',
                   data['latest_income'][i],
                   data['activity_keyword_match'][i],
                   data['grant_keyword_match'][i].toString().concat('\n')];
                   // data['latest_income'][i].toString(),
                   // data['activity_keyword_match'][i].toString(),
                   // data['grant_keyword_match'][i].toString().concat('\n')];

    var joined = currRow.join();
    filetext = filetext.concat(joined);
}

var filename = 'data_result.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
} else {
    var link = document.createElement("a");
    link = document.createElement('a')
    link.href = URL.createObjectURL(blob);
    link.download = filename
    link.target = "_blank";
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'))
}
