/*
 * LEAFLET.BOATMARKER
 * v1.1.0
 * Thomas Brüggemann
 * https://github.com/thomasbrueggemann/leaflet.boatmarker
 */

/* BOAT ICON */
L.PlaneIcon = L.Icon.extend({

	// OPTIONS
	options: {
		iconSize: new L.Point(100, 100),
		className: "leaflet-plane-icon",
		course: 0,
		speed: 0,
		color: "#8ED6FF",
		labelAnchor: [23, 0],
		wind: false,
		windDirection: 0,
		windSpeed: 0,
		idleCircle: false
	},

	// PROPERTIES
	x: 66,
	y: 85,
	x_fac: 0.18,
	y_fac: 0.18,
	ctx: null,
	lastHeading: 0,
	lastWindDirection: 0,

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
		if(!ctx) return;
		var x = this.x;
		var y = this.y;

		var x_fac = this.x_fac;
		var y_fac = this.y_fac;

		ctx.clearRect(0, 0, w, h);

		ctx.translate(w/2, h/2);
		ctx.rotate(this.options.course*Math.PI/180);
		ctx.translate(-w/2, -h/2);

		//ctx.fillRect(0,0,w,h);

		ctx.beginPath();

		// draw idle boat shape
		if(this.options.idleCircle === true && this.options.speed === 0) {
			ctx.arc(x+(50*x_fac), y-(50*y_fac), 50*x_fac, 0, 2 * Math.PI);
		}
		// draw boat shape in motion
		else {
			// Offset
			let xx = 10;
			let yy = 10;

			//ctx.scale(1.5, 1.5);

			// Move origin
			ctx.moveTo(x, y);

			// Main body
            ctx.beginPath(); // start a new path
            ctx.lineWidth=2;
            ctx.moveTo(8.958330+xx, 25.864580+yy);
            ctx.lineTo(8.95833+xx,23.53125+yy);
            ctx.lineTo(11.45833+xx,21.53125+yy);
            ctx.lineTo(11.45833+xx,15.53125+yy);
            ctx.lineTo(0.375+xx,19.19792+yy);
            ctx.lineTo(0.375+xx,16.28125+yy);
            ctx.lineTo(11.375+xx,9.61458+yy);
            ctx.lineTo(11.375+xx,1.44792+yy);
            ctx.bezierCurveTo(11.375+xx,+0.3020799999999999+yy,14.20833+xx,+0.3020799999999999+yy,14.20833+xx,1.44792+yy);
            ctx.lineTo(14.20833+xx,9.61458+yy);
            ctx.lineTo(25.375+xx,16.28125+yy);
            ctx.lineTo(25.375+xx,19.19792+yy);
            ctx.lineTo(14.29167+xx,15.61458+yy);
            ctx.lineTo(14.29167+xx,21.53125+yy);
            ctx.lineTo(16.79167+xx,23.53125+yy);
            ctx.lineTo(16.79167+xx,25.86458+yy);
            ctx.lineTo(12.875+xx,24.61458+yy);
            ctx.lineTo(8.4+xx, 25.864580+yy);
            ctx.stroke();
            ctx.fillStyle = this.options.color;
            ctx.fill();

            // Arrow thingy
            ctx.beginPath(); // start a new path
            ctx.lineWidth=0.5;
            ctx.moveTo(30.79167, 35.864580);
            ctx.lineTo(w/2, h/2);
            // The Arrow
			// up-left
            ctx.moveTo(w/2, h/2); // move to origin
			ctx.lineTo((w/2)-5, (h/2)-5);
			// up-right
            ctx.moveTo(w/2, h/2); // move to origin
            ctx.lineTo((w/2)+5, (h/2)-5);
			// bot-left
            ctx.moveTo(w/2, h/2); // move to origin
            ctx.lineTo((w/2)-5, (h/2)+5);
			// bot-right
            ctx.moveTo(w/2, h/2); // move to origin
            ctx.lineTo((w/2)+5, (h/2)+5);

            // Whatever
            ctx.fill();
            ctx.stroke();
		}


		ctx.closePath();

	},

	setHeadingWind: function(heading, windSpeed, windDirection) {
		this.options.wind = true;

		this.options.course = (heading % 360) - this.lastHeading;
		this.lastHeading = heading % 360;

		this.options.windDirection = (windDirection % 360) - (heading % 360);
		this.lastHeading += this.options.windDirection;

		this.options.windSpeed = windSpeed;

		var s = this.options.iconSize;
		this.draw(this.ctx, s.x, s.y);
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
  	setHeadingWind: function(heading, windSpeed, windDirection) {
  		this.options.icon.setHeadingWind(heading, windSpeed, windDirection);
  	},

  	setHeading: function(heading) {
  		this.options.icon.setHeading(heading);
  	},

	setSpeed: function(speed) {
		this.options.icon.setSpeed(speed);
	}
});

L.planeMarker = function(pos, options) {

	var c = ("color" in options) ? options.color : "#f1c40f";
	var i = ("idleCircle" in options) ? options.idleCircle : false;
	options.icon = new L.PlaneIcon({ color: c, idleCircle: i});

    return new L.PlaneMarker(pos, options);
};
