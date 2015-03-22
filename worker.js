function kmlayer() {
        var view = new ol.View();

        var style = new ol.style.Style({
                image: new ol.style.Icon({
                        opacity: 1,
                        src: "/marker.png"
                })
        });

        var vector = new ol.layer.Vector({
                style: style,
                source: new ol.source.KML({
                        projection: "EPSG:3857",
                        url: "/overhead.kml",
                        extractStyles: false
                })
        });

        var listenerKey = vector.getSource().on("change", function(e) {
                if (vector.getSource().getState() == "ready") {
                        var first_feat = vector.getSource().getFeatures()[0];
                        var first_feat_coords = first_feat.getGeometry().getCoordinates();
                        view.setCenter(first_feat_coords);
                        view.setZoom(15);
                        vector.getSource().unByKey(listenerKey); // Disconnect
                }
        });

        var tiles = new ol.layer.Tile({
                source: new ol.source.OSM(),
        });

        var map = new ol.Map({
                target: document.getElementById("map"),
                layers: [tiles, vector],
                view: view
        });

        window.setInterval("vector.changed()", 1000);
}

// vim: sts=4 ts=4 sw=4 et
