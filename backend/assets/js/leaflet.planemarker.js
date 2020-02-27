/*
 * LEAFLET.PLANEMARKER based on LEAFLET.BOATMARKER
 * v1.1.0
 * Thomas Brüggemann
 * https://github.com/thomasbrueggemann/leaflet.boatmarker
 * See LICENSE.other in airSuck for icon source
 */

/* BOAT ICON */
L.PlaneIcon = L.Icon.extend({

	// OPTIONS
	options: {
		iconSize: new L.Point(30, 30),
		className: "leaflet-plane-icon",
		course: 0,
		speed: 0,
		color: "#8ED6FF",
	},

	// PROPERTIES
	x: 30, // same as L.Point size
	y: 30, // same as L.Point size
	x_fac: 0.18,
	y_fac: 0.18,
	ctx: null,
	lastHeading: 0,

	// CREATE ICON
	// setup the icon and start drawing
	createIcon: function () {
		var e = document.createElement("canvas");
		this._setIconStyles(e, "icon");
		var s = this.options.iconSize;

		e.width = s.x;
		e.height = s.y;
		this.lastHeading = 0;   // reset in case the marker is removed and added again

		this.ctx = e.getContext("2d");
		this.draw(this.ctx, s.x, s.y);

		return e;
	},

	// DRAW
	// renders the boat icon onto the canvas element
	draw: function(ctx, w, h) {
		// Corner is bottom left or something like that
		if (!ctx) {
			return;	
		}
		// Clear whole canvas
		ctx.clearRect(0, 0, w, h);

		
		// If you want to saw its bounding box
		// ctx.fillRect(0, 0, w, h);

		// Rotate depending on course
		// Translate is here to keep the rotation on center of canvas
		ctx.translate(w/2, h/2);
		ctx.rotate(this.options.course*Math.PI/180);
		ctx.translate(-w/2, -h/2);

		const x = 2;
		const y = 2;

		// Draw a plane
		ctx.beginPath(); // start a new path
		ctx.moveTo(8.958330+x, 25.864580+y);
		ctx.lineTo(8.95833+x,23.53125+y);
		ctx.lineTo(11.45833+x,21.53125+y);
		ctx.lineTo(11.45833+x,15.53125+y);
		ctx.lineTo(0.375+x,19.19792+y);
		ctx.lineTo(0.375+x,16.28125+y);
		ctx.lineTo(11.375+x,9.61458+y);
		ctx.lineTo(11.375+x,1.44792+y);
		ctx.bezierCurveTo(11.375+x,+0.3020799999999999+y,14.20833+x,+0.3020799999999999+y,14.20833+x,1.44792+y);
		ctx.lineTo(14.20833+x,9.61458+y);
		ctx.lineTo(25.375+x,16.28125+y);
		ctx.lineTo(25.375+x,19.19792+y);
		ctx.lineTo(14.29167+x,15.61458+y);
		ctx.lineTo(14.29167+x,21.53125+y);
		ctx.lineTo(16.79167+x,23.53125+y);
		ctx.lineTo(16.79167+x,25.86458+y);
		ctx.lineTo(12.875+x,24.61458+y);
		ctx.lineTo(8.4+x, 25.864580+y);
		ctx.stroke();
		ctx.fillStyle = this.options.color;
		ctx.fill();
		ctx.closePath();
	},

	// SET HEADING
	// sets the boat heading and
	// update the boat icon accordingly
	setHeading: function(heading) {
		this.options.course = (heading % 360) - this.lastHeading;
		this.lastHeading = heading % 360;

		var s = this.options.iconSize;
		this.draw(this.ctx, s.x, s.y);
	},

	// SET SPEED
	// sets the boat speed value and
	// update the boat icon accordingly
	setSpeed: function(speed) {
		this.options.speed = speed;

		var s = this.options.iconSize;
		this.draw(this.ctx, s.x, s.y);
	}
});

L.PlaneMarker = L.Marker.extend({
  	setHeading: function(heading) {
  		this.options.icon.setHeading(heading);
  	},

	setSpeed: function(speed) {
		this.options.icon.setSpeed(speed);
	}
});

L.planeMarker = function(pos, options) {

	var c = ("color" in options) ? options.color : "#f1c40f";
	options.icon = new L.PlaneIcon({ color: c });

    return new L.PlaneMarker(pos, options);
};
