// We need to import the CSS so that webpack will load it.
// The MiniCssExtractPlugin is used to separate it out into
// its own CSS file.
import css from "../css/app.css"

// CSS & JS or just CSS, whatever
import "jquery/dist/jquery";
import "popper.js";
import 'bootstrap';
import 'rainbowvis.js/rainbowvis';
import 'leaflet/dist/leaflet';
import 'leaflet.locatecontrol';
import 'sidebar-v2/js/leaflet-sidebar';
import 'js-logger/src/logger';
import 'leaflet-providers/leaflet-providers';
import '@joergdietrich/leaflet.terminator/L.Terminator';
import 'leaflet-hash/leaflet-hash';

// Own app
import './global';
// Custom markers
import './leaflet.boatmarker';
import './leaflet.planemarker';
// Config
import './config';
// Vehicle types
import './vehicle';  // needs to be before the custom vehicles types
import './airADSB';
import './airAIS';
// Message handling
import './messages';
// The map
import './map_init';
// Magic sauce
import './airsuckLoad';

// webpack automatically bundles all modules in your
// entry points. Those entry points can be configured
// in "webpack.config.js".
//
// Import dependencies
//
import "phoenix_html"

// Import local files
//
// Local files can be imported directly using relative paths, for example:
// import socket from "./socket"
