const mapStyle = [{
    'featureType': 'administrative',
    'elementType': 'all',
    'stylers': [{
        'visibility': 'on',
    },
        {
            'lightness': 33,
        },
    ],
},
    {
        'featureType': 'landscape',
        'elementType': 'all',
        'stylers': [{
            'color': '#A3B2A1',
        }],
    },
    {
        'featureType': 'poi.park',
        'elementType': 'geometry',
        'stylers': [{
            'color': '#c5dac6',
        }],
    },
    {
        'featureType': 'poi.park',
        'elementType': 'labels',
        'stylers': [{
            'visibility': 'on',
        },
            {
                'lightness': 20,
            },
        ],
    },
    {
        'featureType': 'road',
        'elementType': 'all',
        'stylers': [{
            'lightness': 20,
        }],
    },
    {
        'featureType': 'road.highway',
        'elementType': 'geometry',
        'stylers': [{
            'color': '#c5c6c6',
        }],
    },
    {
        'featureType': 'road.arterial',
        'elementType': 'geometry',
        'stylers': [{
            'color': '#e4d7c6',
        }],
    },
    {
        'featureType': 'road.local',
        'elementType': 'geometry',
        'stylers': [{
            'color': '#fbfaf7',
        }],
    },
    {
        'featureType': 'water',
        'elementType': 'all',
        'stylers': [{
            'visibility': 'on',
        },
            {
                'color': '#6E8690',
            },
        ],
    },
];

function initMap() {
    // Create the map.
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 6,
        center: { lat: 37.974562, lng: 23.735637 },
        styles: mapStyle,
        mapTypeControl: false
    });

    // Load the stores GeoJSON onto the map.
    map.data.loadGeoJson('../js/stores.json', {idPropertyName: 'storeid'});
    map.data.setStyle(function(feature) {
        return /** @type {google.maps.Data.StyleOptions} */({
            icon: '/images/map/greenmarker.png', //http://maps.google.com/mapfiles/marker.png
        });
    });
    const apiKey = 'AIzaSyAk0_KmOAhS1U750lFVSdtztglJjVAhGFg';
    const infoWindow = new google.maps.InfoWindow();


    // Show the information for a store when its marker is clicked.
    map.data.addListener('click', (event) => {
        const category = event.feature.getProperty('category');
        const name = event.feature.getProperty('name');
        const description = event.feature.getProperty('description');
        const hours = event.feature.getProperty('hours');
        const phone = event.feature.getProperty('phone');
        const position = event.feature.getGeometry().get();
        const content = `
      <h4>${name}</h4><p style="font-size: 16px">${description}</p>
      <p style="font-size: 14px"><b>Open:</b> ${hours}<br/><b>Phone:</b> ${phone}</p>
    `;

        infoWindow.setContent(content);
        infoWindow.setPosition(position);
        infoWindow.setOptions({pixelOffset: new google.maps.Size(0, -30)});
        infoWindow.open(map);
    });


    // Build and add the search bar
    const card = document.createElement('div');
    const titleBar = document.createElement('div');
    const title = document.createElement('div');
    const container = document.createElement('div');
    const input = document.createElement('input');
    const options = {
        types: ['address'],
        componentRestrictions: {country: 'gr'},
    };
    // Search
    card.setAttribute('id', 'pac-card');
    title.setAttribute('id', 'title');
    title.textContent = 'Βρείτε το κοντινότερο κατάστημα';
    titleBar.appendChild(title);
    container.setAttribute('id', 'pac-container');
    input.setAttribute('id', 'pac-input');
    input.setAttribute('type', 'text');
    input.setAttribute('placeholder', 'Εισάγετε διεύθυνση');
    input.className="input-style"
    container.appendChild(input);
    card.appendChild(titleBar);
    card.appendChild(container);
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(card);
    // Make the search bar into a Places Autocomplete search bar and select
    // which detail fields should be returned about the place that
    // the user selects from the suggestions.
    const autocomplete = new google.maps.places.Autocomplete(input, options);
    autocomplete.setFields(['address_components', 'geometry', 'name']);


    // Set the origin point when the user selects an address
    const originMarker = new google.maps.Marker({
        map: map,
        title: 'Η τοποθεσία σας',
        icon: {
            url: '/images/map/youarehere-2.png',
            scaledSize: new google.maps.Size(48, 48)
        }
    });
    originMarker.setVisible(false);
    let originLocation = map.getCenter();

    autocomplete.addListener('place_changed', async () => {
        originMarker.setVisible(false);
        originLocation = map.getCenter();
        const place = autocomplete.getPlace();

        if (!place.geometry) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert('No address available for input: \'' + place.name + '\'');
            return;
        }

        // Recenter the map to the selected address
        originLocation = place.geometry.location;
        map.setCenter(originLocation);
        map.setZoom(13);
        console.log(place);

        originMarker.setPosition(originLocation);
        originMarker.setVisible(true);

        // Use the selected address as the origin to calculate distances
        // to each of the store locations
        const rankedStores = await calculateDistances(map.data, originLocation);
        showStoresList(map.data, rankedStores);

        return;
    });


    // List the closest stores
    async function calculateDistances(data, origin) {
        const stores = [];
        const destinations = [];

        // Build parallel arrays for the store IDs and destinations
        data.forEach((store) => {
            const storeNum = store.getProperty('storeid');
            const storeLoc = store.getGeometry().get();

            stores.push(storeNum);
            destinations.push(storeLoc);
        });

        // Retrieve the distances of each store from the origin
        // The returned list will be in the same order as the destinations list
        const service = new google.maps.DistanceMatrixService();
        const getDistanceMatrix =
            (service, parameters) => new Promise((resolve, reject) => {
                service.getDistanceMatrix(parameters, (response, status) => {
                    if (status != google.maps.DistanceMatrixStatus.OK) {
                        reject(response);
                    } else {
                        const distances = [];
                        const results = response.rows[0].elements;
                        for (let j = 0; j < results.length; j++) {
                            const element = results[j];
                            const distanceText = element.distance.text;
                            const distanceVal = element.distance.value;
                            const distanceObject = {
                                storeid: stores[j],
                                distanceText: distanceText,
                                distanceVal: distanceVal,
                            };
                            distances.push(distanceObject);
                        }

                        resolve(distances);
                    }
                });
            });

        const distancesList = await getDistanceMatrix(service, {
            origins: [origin],
            destinations: destinations,
            travelMode: 'DRIVING',
            unitSystem: google.maps.UnitSystem.METRIC,
        });

        distancesList.sort((first, second) => {
            return first.distanceVal - second.distanceVal;
        });

        return distancesList;
    }


    // Show the stores in order
    function showStoresList(data, stores) {
        if (stores.length == 0) {
            console.log('empty stores');
            return;
        }

        // unhide
        let container = document.getElementById("container")
        container.classList.remove("hidden");

        let panel = document.getElementById("panel")
        // Clear the previous details
        while (panel.lastChild) {
            panel.removeChild(panel.lastChild);
        }

        stores.forEach((store) => {
            // Add store details with text formatting
            const div = document.createElement("div")
            div.classList.add("subcard")
            const name = document.createElement('p');
            name.setAttribute("style","margin:10px")
            name.classList.add('place');
            const currentStore = data.getFeatureById(store.storeid);
            name.textContent = currentStore.getProperty('name');
            div.appendChild(name);
            const distanceText = document.createElement('p');
            distanceText.setAttribute("style","margin:10px")
            distanceText.classList.add('distanceText');
            distanceText.textContent = store.distanceText;
            div.appendChild(distanceText);
            // append final div
            panel.appendChild(div)
        });

        // Open the panel
        panel.classList.add('open');

        return;
    }
}