// Setup layers
let baseLayers = {
    "Black and White": L.tileLayer.provider("OpenStreetMap.BlackAndWhite"),
    "OpenStreetMap": L.tileLayer.provider('OpenStreetMap.Mapnik'),
    "OpenTopo": L.tileLayer.provider('OpenTopoMap'),
    "Stamen Terrain": L.tileLayer.provider('Stamen.Terrain'),
    "Esri Ocean Basemap": L.tileLayer.provider('Esri.OceanBasemap')
};

let overlaysLayers = {
    "OpenSeaMap": L.tileLayer.provider('OpenSeaMap')
};

layers = Object.assign({}, baseLayers, overlaysLayers);

// Setup the map object
map = L.map(document.getElementById("world")).setView([config.defaultLat, config.defaultLon], config.defaultZoom);
map.addLayer(layers["Black and White"]);
map.addLayer(layers["OpenSeaMap"]);

// Add control layer
L.control.layers(baseLayers, overlaysLayers).addTo(map);

mapLoaded = true;
