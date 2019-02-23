// Socket.IO
socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function () {
    socket.emit('my event', {data: 'I\'m connected!'});
});
socket.on('adsb-new', function (data) {
    console.log('adsb-new: ' + data.message);
    if (data.message.field15 && data.message.field16) {
        console.log('lat: ' + data.message.field15 + " lon: " + data.message.field16);
        let plane = L.planeMarker(map.getCenter(), {color: '#f1c40f'}).addTo(map);
        plane.setLatLng([data.message.field15, data.message.field16]);
    }
});
