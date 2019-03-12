let SEARCH_DATA = {}

document.addEventListener('DOMContentLoaded', function () {

    d3.select('#searchterms').on('keyup', function(d) {

        if(d3.event.key === "Enter"){

            let params = {'searchterms': d3.select("#searchterms").node().value}
            const search_params = new URLSearchParams(params);

            // searchParams.toString() === 'var1=value1&var2=value2'
            d3.json(URL_FOR_SEARCH + "?" + search_params, {
                method: 'GET',
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify()
            })
            .then(display_search_results);
        }


    })

});

function get_summary_data(data) {

    let summary_data = data.map(function(d) {
        let return_dict = {}
        return_dict["Database Name"] = d["db_name"]
        return_dict["Table Name"] = d["tbl_name"]
        return_dict["Column Name"] = d["clm_name"]
        return return_dict
    })

    return summary_data

}

function display_search_results(data) {

    SEARCH_DATA = data["data"]
    let container = d3.select("#summary_table")
    container.html("")

    tabulate_summary_data(SEARCH_DATA, container)

    display_row_details(SEARCH_DATA[0])

}


function display_row_details(d) {

    d3.text(`/db_info/?id=${d["db_id"]}`).then(function(response) {
        d3.select("#database_info").html(response)
    });

    d3.text(`/tbl_info/?id=${d["tbl_id"]}`).then(function(response) {
        d3.select("#table_info").html(response)
    });

    d3.text(`/clm_info/?id=${d["clm_id"]}`).then(function(response) {
        d3.select("#column_info").html(response)
    });

    d3.text(`/sample_code/?clm_id=${d["clm_id"]}`).then(function(response) {
        d3.select("#sample_sql").html(response)
        Prism.highlightAll();
    });


}

function tabulate_summary_data(data, container) {

    let cols_to_display = ["db_name", "tbl_name", "clm_name"]
    let col_headers = ["Database name", "Table name", "Column name"]

    var table = container.append('table')
    table.attr('class', 'search_results')
    var thead = table.append('thead')
    var	tbody = table.append('tbody');

    // append the header row
    thead.append('tr')
      .selectAll('th')
      .data(col_headers).enter()
      .append('th')
        .text(c => c)
        .attr("class", "search_results");

    // create a row for each object in the data
    var rows = tbody.selectAll('tr')
      .data(data)
      .enter()
      .append('tr')
      .attr("class", "search_results");

    rows.on("click", display_row_details)

    // create a cell in each row for each column
    var cells = rows.selectAll('td')
      .data(function(row) {
        let ret_arr = []
        cols_to_display.forEach(d => ret_arr.push(row[d]))

        return ret_arr
      })
      .enter()
      .append('td')
        .text(d => d);

  return table;


}


