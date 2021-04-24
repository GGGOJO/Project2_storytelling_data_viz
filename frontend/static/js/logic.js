// 1st GRAPH 
d3.json("http://localhost:5000/api/country").then(function (data) {
    console.log(data)
    var layout = {
        title: 'Nobel Prize Laureates by Country, 1901-2020',
        showlegend: false,
        yaxis: {
            title: 'Number of Winners'
        }
    }

    Plotly.newPlot('plot', data, layout, { displayModeBar: true });
})

// 2nd GRAPH
d3.json("http://localhost:5000/api/winners_state").then(function (data) {
    let stateData = data
    console.log(stateData)

    var layout = {
        title: 'U.S. Nobel Prize Laureates by State, 1901-2020',
        showlegend: false,
    }

    Plotly.newPlot('plot2', stateData, layout)
})

// 3rd GRAPH
// Store API query variables
var myMap = L.map("map", {
    center: [39.0997, -94.5786],
    zoom: 4
});

L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
    tileSize: 512,
    maxZoom: 18,
    zoomOffset: -1,
    id: "mapbox/streets-v11",
    accessToken: API_KEY
}).addTo(myMap);


var baseURL = 'http://localhost:5000/api/usorgs';

// Grab the data with d3
d3.json(baseURL).then(function (response) {

    // Create a new marker cluster group
    var markers = L.markerClusterGroup();
    console.log(response)

    // Loop through data
    for (var index = 0; index < response["org"].length; index++) {

        // Set the data location property to a variable
        let lat = response["lat"][index]
        let lng = response["lng"][index]
        let org = response["org"][index]
        let orgct = response["orgct"][index]

        // Check for location property
        if (lat && lng) {

            // Add a new marker to the cluster group and bind a pop-up
            markers.addLayer(L.marker([lat, lng])
                .bindPopup(org, orgct));
        }
    }
    // Add our marker cluster layer to the map
    myMap.addLayer(markers);
});


// 4th Graph
d3.json("http://localhost:5000/api/seslider").then(function (all_data) {
    console.log(all_data)

    let data = all_data["data"]
    let layout = all_data["layout"]
    layout["title"] = 'Share of Science & Engineering Jobs by State, 2008-2017';
    layout["showtitle"] = false;
    // var layout = {
    //     title: 'Share of Science & Engineering Jobs by State, 2008-2017',
    //     showlegend: false
    // }

    Plotly.newPlot('map2', data, layout, { displayModeBar: true });
})

// 5th Graph
d3.json("http://localhost:5000/api/rdslider").then(function (rd_data) {
    console.log(rd_data)

    let data = rd_data["data"]
    let layout = rd_data["layout"]
    layout["title"] = 'Share of R&D by State, 2008-2017';
    layout["showtitle"] = false;
    // var layout = {
    //     title: 'Share of Science & Engineering Jobs by State, 2008-2017',
    //     showlegend: false
    // }

    Plotly.newPlot('map3', data, layout, { displayModeBar: true });
})