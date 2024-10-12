document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65431;
var server_addr = "10.0.1.138";   // the IP address of your Raspberry PI

function client(){

    const net = require('net');
    var input = document.getElementById("message").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        //document.getElementById("bluetooth").innerHTML = data;
        

        const json_data = JSON.parse(data.toString());

        document.getElementById("Temperature").innerHTML = json_data['Temperature'];
        document.getElementById("Orientation").innerHTML = json_data['Orientation'];
        document.getElementById("X").innerHTML = json_data['X'];
        document.getElementById("Y").innerHTML = json_data['Y'];
        document.getElementById("DistanceTraveled").innerHTML = json_data['Distance Traveled From Start'];


        console.log(JSON.stringify(json_data));


        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

function send_data(direction) {
    const net = require('net');
    console.log('Arrow clicked:', direction);
    switch(direction) {
        case 'up':
            var input = "forward"
            break;
        case 'left':
            var input = "left"
            break;
        case 'right':
            var input = "right"
            break;
        case 'down':
            var input = "backward"
            break;
    }
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log('connected to server!');
        client.write(`${input}\r\n`);
    });

    client.on('data', (data) => {
        const json_data = JSON.parse(data.toString());

        document.getElementById("Temperature").innerHTML = json_data['Temperature'];
        document.getElementById("Orientation").innerHTML = json_data['Orientation'];
        document.getElementById("X").innerHTML = json_data['X'];
        document.getElementById("Y").innerHTML = json_data['Y'];
        document.getElementById("DistanceTraveled").innerHTML = json_data['Distance Traveled From Start'];


        console.log(JSON.stringify(json_data));
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}
// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("up");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("down");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("left");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("right");
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}


// update data for every 50ms
function update_data(){
    setInterval(function(){
        // get image from python server
        client();
    }, 50);
}


