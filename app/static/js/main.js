document.addEventListener('DOMContentLoaded', function () {

    d3.select('#submit').on('click', function() {

        d3.json(URL_FOR_SEARCH, {
            method: 'POST',
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "X-CSRFToken": "{{ form.csrf_token._value() }}"
            },
            body: JSON.stringify({'searchterms': d3.select("#searchterms").node().value, 'csrf_token': d3.select("#csrf_token").node().value})
        })
        .then(data => {
            let container = d3.select("#data_table")
            container.html("")
            tabulate(data["data"], container)

        });
    })

});

function tabulate(data, container) {
    let cols = Object.keys(data[0])

    var table = container.append('table')
    var thead = table.append('thead')
    var	tbody = table.append('tbody');

    // append the header row
    thead.append('tr')
      .selectAll('th')
      .data(cols).enter()
      .append('th')
        .text(c => c);

    // create a row for each object in the data
    var rows = tbody.selectAll('tr')
      .data(data)
      .enter()
      .append('tr');

    // create a cell in each row for each column
    var cells = rows.selectAll('td')
      .data(row => Object.values(row))
      .enter()
      .append('td')
        .text(d => d);

  return table;
}

