document.addEventListener('DOMContentLoaded', function () {


    d3.select('#submit').on('click', function() {

        d3.json(URL_FOR_SEARCH, {
            method: 'POST',
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "X-CSRFToken": "{{ form.csrf_token._value() }}"
            },
            body: JSON.stringify({'searchterms': 'hello', 'csrf_token': d3.select("#csrf_token").node().value})
        })
        .then(json => {
            debugger;
            console.log(json)
        });
    })

});