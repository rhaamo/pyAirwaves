<template>
  <div>
    <div id="header">
        <div id="left">
          <router-link :to="{name:'home'}">Home</router-link>
          -
          <router-link :to="{name:'about'}">About</router-link>
        </div>
        <div id="right">
            <span id="socket_state" class="fa fa-question-circle-o" title="WebSocket status unknown"></span> <a href="https://github.com/rhaamo/pyAirwaves" target="_blank">pyAirwaves</a></div>
    </div>
    <router-view/>
  </div>
</template>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-size: 10px;
    font-family: Helvetica,
    Arial,
    "Lucida Grande",
    sans-serif;
}

.msgBx {
    width: 100%;
    border: 1px solid #000000;
    background-color: #cccccc;
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    opacity: 0.85;
}

.dbgActive {
    z-index: 9999;
}

html, body {
    height: 100%;
    margin: 0;
    padding: 0;
}

#map {
    height: 100%;
}

#mapStyleBox {
    text-align: left;
    font-family: Roboto, Arial, sans-serif;
    position: absolute;
    top: 5px !important;
    left: 35px !important;
}

.mapStyleSelector {
    font-size: 12px;
    z-index: 9999;
}

#header {
    background-color: #dddddd;
    height: 2em;
    padding-left: 1em;
    padding-right: 1em;
}

#header #left {
    float: left;
}

#header #right {
    float: right;
}

span.icon-socket-ok {
    color: green;
}

span.icon-socket-nok {
    color: red;
}
</style>
