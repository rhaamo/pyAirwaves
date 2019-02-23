"use strict";// overcome current Chrome and Firefox issues with ECMA6 stuff like let
/***********************************************************
 * Airsuck User Interface Sidebar
 * v. 0.1
 *
 * Creates a slide-out sidebar and loads vehicle data from the vehdata array
 *
 * Licensed under GPL V3
 * https://github.com/ThreeSixes/airSuck
 *
 * Deps: jQuery, vehData array, vehicles.js
 **********************************************************/

// sets up the sidebar on initialization, just DOM stuff
function setupSidebar(){
    // check for an existing sidebar, if none exists, add one
    if ($('#sidebar').length) {
        // sidebar exists, ignore
        if (debug) {console.log('Sidebar setup called but sidebar exists, ignoring.');}
        // Flag sidebar as loaded for giggles.
        sidebarLoaded = true;
    } else {
        if (debug) {console.log('Sidebar setup called, setting up sidebar.');}
        // no sidebar, set it up in the body
        $('body').append('<div id="sidebar" class="sidebar"></div>');
        // setup the sidebar structure
        $('#sidebar').append('<div id="sidebar-upper"></div><div id="sidebar-header"></div><div id="sidebar-body"></div><div id="sidebar-footer"></div>');
        // hide sidebar by default        
        $('#sidebar').hide();
        
        // setup the sidebar header - 1 button for each vehicle type + search
        let index;
        let length = vehicleTypes.length;
        if (debug) {console.log('Sidebar found '+length+' vehicle types.');}
        for (index=0;index<length;++index) {
            if (debug) {console.log('Adding vehicle icon to sidebar header: ' + vehicleTypes[index].protocol);}
            $('#sidebar-header').append('<i id="button-list-' + vehicleTypes[index].domName + '" class="fa ' + vehicleTypes[index].faIcon + ' sidebar-button"></i>');
            // set the first icon to active
            if (index==0) {
                $('#button-list-'+vehicleTypes[index].domName).addClass('active');
            }
        }
        // SEARCH - TO DO
        //$('#sidebar-header').append('<i id="button-search" class="fa fa-search sidebar-button"></i>');
        
        // adjust the size of each button based on the number of buttons
        $('.sidebar-button').css('width',((1/(length))*100) + '%');
        
        // setup the sidebar body containers and related tables - one for each vehicle type + search
        for (index=0;index<length;++index) {
            if (debug) {console.log('Adding vehicle table to sidebar body: ' + vehicleTypes[index].protocol);}
            $('#sidebar-body').append('<div id="container-list-' + vehicleTypes[index].domName + '" class="sidebar-container"></div>');
            // set a table header
            $('#container-list-' + vehicleTypes[index].domName).append('<h1>Vehicles broadcasting over '+vehicleTypes[index].protocol+'</h1>');
            // setup the vehicle table
            $('#container-list-' + vehicleTypes[index].domName).append('<table id="table-'+vehicleTypes[index].domName+'" class="vehicle-table">');
            vehicleTypes[index].buildTable('#table-'+vehicleTypes[index].domName);
            $('#container-list-' + vehicleTypes[index].domName).append('</table>');
            // hide the container
            $('#container-list-' + vehicleTypes[index].domName).hide();
            
            // attach listeners to buttons
            // vehicle type button click
            $('#button-list-' + vehicleTypes[index].domName).click(function(){
                // hide all sidebar containers
                $('.sidebar-container').hide();
                // show the vehicle info sidebar container
                // some ninja to get the type since this doesn't have access to the domName attribute when called
                let domName = this.id.substring(12,this.id.length);
                $('#container-list-' + domName).show();
                // deactivate other sidebar buttons
                $('.sidebar-button').removeClass('active');
                // activate this button
                $(this).addClass('active');
            });
        }
        // SEARCH - TO DO setup the search container
        /*
        $('#sidebar-body').append('<div id="container-search" class="sidebar-container"></div>');
        $('#container-search').hide();
        // search button
        $('#button-search').click(function(){
            // hide all sidebar containers
            $('.sidebar-container').hide();
            // show the vehicle info sidebar container
            $('#container-search').show();
        });*/

        // setup a button on the main UI to show and hide
        $('body').append('<i id="sidebar-icon" class="fa fa-chevron-left"></i>');
        // set the button to slideToggle the sidebar on click
        $('#sidebar-icon').click(function(){
            // check if the sidebar is open or closed and take action
            if ($('#sidebar').css('display') == 'none') {
                // sidebar closed, slide icon, change to fa-chevron-right
                $('#sidebar-icon').removeClass('fa-chevron-left');
                $('#sidebar-icon').addClass('fa-chevron-right');
                // TO-DO, don't hardcode the movement at 32%
                $('#sidebar-icon').animate({right:"31%"});
                // by default, show the SSR vehicle list
                //loadVehicleLists('#container-list-AIS','#container-list-SSR'); // remove
                $('#container-list-SSR').show();
            } else {
                // sidebar open, close it and reset icon
                $('#sidebar-icon').removeClass('fa-chevron-right');
                $('#sidebar-icon').addClass('fa-chevron-left');
                // TO-DO, don't hardcode the movement at 10px
                $('#sidebar-icon').animate({right:"10px"});
            }
            // slide out or in the sidebar
            $('#sidebar').animate({width:"toggle"}); 
        });
        
        // Flag sidebar as loaded.
        sidebarLoaded = true;
    }
};

// sets up the sidebar search tab
function loadSidebarSearch(container){
    // TO DO
}