function load_results(data) {
    $('#loading').addClass('hidden');
    $('#result_table').removeClass('hidden');
    for(i in data.results){
        $('#result_content').append(wrap_result(data.results[i], data.usercount))
    }
}

function wrap_td(s) {
    return "<td>" + s + "</td>"
}

function wrap_tr(s) {
    return "<tr>" + s + "</tr>"
}

function wrap_result(result, count){
    return wrap_tr(wrap_td(result.place) + wrap_td(result.time) +
                   wrap_td(result.people)+ wrap_td(Math.round(result.rating/count*100)/100 + "/10"))
}