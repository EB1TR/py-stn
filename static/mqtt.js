// Create a client instance
clientID = "web"
clientID += new Date().getUTCMilliseconds()
client = new Paho.MQTT.Client("192.168.1.110", Number(9001), clientID);

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("Connected");
  client.subscribe("pytofront");
  client.subscribe("stn1/radio1/qrg");
  client.subscribe("stn1/radio2/qrg");
  client.subscribe("stn2/radio1/qrg");
  client.subscribe("stn2/radio2/qrg");
  client.subscribe("stn1/radio1/mode");
  client.subscribe("stn1/radio2/mode");
  client.subscribe("stn2/radio1/mode");
  client.subscribe("stn2/radio2/mode");
  client.subscribe("stn1/radio1/op");
  client.subscribe("stn1/radio2/op");
  client.subscribe("stn2/radio1/op");
  client.subscribe("stn2/radio2/op");
  message = new Paho.MQTT.Message('0');
  message.destinationName = "update";
  client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}


function send_command(comm, dato){
  message = new Paho.MQTT.Message(String(dato));
  message.destinationName = comm;
  client.send(message);
}


// called when a message arrives
function onMessageArrived(message) {
    console.log(message.payloadString)
    if (message.destinationName == "stn1/radio1/qrg") {
        $('#stn1-r1-qrg').text((message.payloadString/100).toFixed(2))
    } else if (message.destinationName == "stn2/radio1/qrg") {
        $('#stn2-r1-qrg').text((message.payloadString/100).toFixed(2))
    } else if (message.destinationName == "stn1/radio2/qrg") {
        console.log("cc")
    } else if (message.destinationName == "stn2/radio2/qrg") {
        console.log("cc")
    } else if (message.destinationName == "stn1/radio1/mode") {
        $('#stn1-r1-mode').text(message.payloadString)
    } else if (message.destinationName == "stn2/radio1/mode") {
        $('#stn2-r1-mode').text(message.payloadString)
    } else if (message.destinationName == "stn1/radio1/op") {
        $('#stn1-op').text(message.payloadString)
    } else if (message.destinationName == "stn2/radio1/op") {
        $('#stn2-op').text(message.payloadString)
    } else {
        json = JSON.parse(message.payloadString)
        if (json.stn1 != undefined) {
            json = JSON.parse(message.payloadString)
            bstn1 = "#stn1-b"+json.stn1.band
            bstn2 = "#stn2-b"+json.stn2.band
            asstn1 = json.stn1.auto
            asstn2 = json.stn2.auto
            ststn11 = json.stacks[json.stn1.band][1]
            ststn12 = json.stacks[json.stn1.band][2]
            ststn13 = json.stacks[json.stn1.band][3]
            ststn21 = json.stacks[json.stn2.band][1]
            ststn22 = json.stacks[json.stn2.band][2]
            ststn23 = json.stacks[json.stn2.band][3]
            so2r = json.so2r
            $('#stn1-an').text(json.stn1.antname)
            $('#stn2-an').text(json.stn2.antname)
            $("#stn1-b0").removeClass("spanitemselected");
            $("#stn1-b160").removeClass("spanitemselected");
            $("#stn1-b80").removeClass("spanitemselected");
            $("#stn1-b40").removeClass("spanitemselected");
            $("#stn1-b20").removeClass("spanitemselected");
            $("#stn1-b15").removeClass("spanitemselected");
            $("#stn1-b10").removeClass("spanitemselected");
            $("#stn2-b0").removeClass("spanitemselected");
            $("#stn2-b160").removeClass("spanitemselected");
            $("#stn2-b80").removeClass("spanitemselected");
            $("#stn2-b40").removeClass("spanitemselected");
            $("#stn2-b20").removeClass("spanitemselected");
            $("#stn2-b15").removeClass("spanitemselected");
            $("#stn2-b10").removeClass("spanitemselected");
            $("#stn1-as").removeClass("spanitemselected");
            $("#stn2-as").removeClass("spanitemselected");
            $("#stn1-stack1").removeClass("spanitemselected");
            $("#stn1-stack2").removeClass("spanitemselected");
            $("#stn1-stack3").removeClass("spanitemselected");
            $("#stn2-stack1").removeClass("spanitemselected");
            $("#stn2-stack2").removeClass("spanitemselected");
            $("#stn2-stack3").removeClass("spanitemselected");
            $(bstn1).addClass("spanitemselected")
            $(bstn2).addClass("spanitemselected")
            if (asstn1 == true) $("#stn1-as").addClass("spanitemselected")
            if (asstn2 == true) $("#stn2-as").addClass("spanitemselected")
            if (ststn11 == true) $("#stn1-stack1").addClass("spanitemselected")
            if (ststn12 == true) $("#stn1-stack2").addClass("spanitemselected")
            if (ststn13 == true) $("#stn1-stack3").addClass("spanitemselected")
            if (ststn21 == true) $("#stn2-stack1").addClass("spanitemselected")
            if (ststn22 == true) $("#stn2-stack2").addClass("spanitemselected")
            if (ststn23 == true) $("#stn2-stack3").addClass("spanitemselected")

        }
    }



}