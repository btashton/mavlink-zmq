
c3dl.addMainCallBack(canvasMain, "tutorial");
c3dl.addModel("/static/model/duck.dae");
var duck;
// Create a camera
var cam = new c3dl.FreeCamera();

var imu = {'roll':0,'pitch':0,'yaw':0}
var imu_hist = {'roll':[0],'pitch':[0],'yaw':[0]}
var maxpoints = 300
// The program main
function canvasMain(canvasName){

 // Create new c3dl.Scene object
 scn = new c3dl.Scene();
 scn.setCanvasTag(canvasName);

 // Create GL context
 renderer = new c3dl.WebGL();
 renderer.createRenderer(this);

 // Attach renderer to the scene
 scn.setRenderer(renderer);
 scn.init(canvasName);

 //the isReady() function tests whether or not a renderer
 //is attached to a scene.  If the renderer failed to
 //initialize this will return false but only after you
 //try to attach it to a scene.
 if(renderer.isReady() )
 {
 // Create a Collada object that
 // will contain a imported
 // model of something to put
 // in the scene.
 duck = new c3dl.Collada();

 // If the path is already parsed
 // (as it is in this case)
 // then the model is automatically retrieved
 // from a collada manager.
 duck.init("/static/model/duck.dae");

 // Give the duck a bit of a spin on y
 duck.setAngularVel(new Array(0.0, 0.0, 0.0));

 // Add the object to the scene
 scn.addObjectToScene(duck);



 // Place the camera.
 // WebGL uses a right handed co-ordinate system.
 // move 200 to the right
 // move 300 up
 // move 500 units out
 cam.setPosition(new Array(000.0, 000.0, 500.0));

 // Point the camera.
 // Here it is pointed at the same location as
 // the duck so the duck will appear centered.
 cam.setLookAtPoint(new Array(0.0, 0.0, 0.0));

 // Add the camera to the scene
 scn.setCamera(cam);

 // Start the scene
 scn.startScene();
 }
}

function update_pos(msg)
{
	duck.roll(imu.roll-msg.roll);
	duck.pitch(imu.pitch-msg.pitch);
	duck.yaw(imu.yaw-msg.yaw)
	imu.roll = msg.roll
	imu.yaw = msg.yaw
	imu.pitch = msg.pitch
	if imu_hist.roll.length >= maxpoints
	{
		imu_hist.roll.slice(1)
		imu_hist.yaw.slice(1)
		imu_hist.pitch.slice(1)
	}
	imu_hist.roll.push(msg.roll)
	imu_hist.yaw.push(msg.yaw)
	imu_hist.pitch.push(msg.pitch)

	update_plot();
}


$(function() {

    var WEB_SOCKET_SWF_LOCATION = '/static/js/socketio/WebSocketMain.swf',
        socket = io.connect('/mavlink');
	
	//After connecting to socketio open a stream and subscribe to
	//ATTITUDE information
    socket.on('connect', function () {
        socket.emit('stream zmq', '');
        socket.emit('zmq sub', 'uav1.ATTITUDE');
    });

    socket.on('announcement', function (msg) {
        json_msg = $.parseJSON(msg);
        if (json_msg.mavpackettype == 'ATTITUDE')
        {
			update_pos(json_msg);
		}
    });
});


// setup plot
var options = {
	series: { shadowSize: 0 }, // drawing is faster without shadows
	yaxis: { min: 0, max: 100 },
	xaxis: { show: false }
};
var plot = $.plot($("#imuplot"), imu_hist.roll, options);

function updateplot() {
	plot.setData(imu_hist.roll);
	plot.draw();
}
