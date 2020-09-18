// Create a client instance
clientID = "web"
clientID += new Date().getUTCMilliseconds()
client = new Paho.MQTT.Client("192.168.33.10", Number(9001), clientID);

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
  message = new Paho.MQTT.Message('0');
  message.destinationName = "refrescar";
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
    if (message.destinationName == "stn1/radio1/qrg") {
        $('#stn1-qrg').text(message.payloadString)
    } else if (message.destinationName == "stn1/radio2/qrg") {
        $('#stn2-qrg').text(message.payloadString)
    } else if (message.destinationName == "stn2/radio1/qrg") {
        console.log("cc")
    } else if (message.destinationName == "stn2/radio2/qrg") {
        console.log("cc")
    } else {
        json = JSON.parse(message.payloadString)
        if (json.stn1 != undefined) {
            json = JSON.parse(message.payloadString)
            astn1 = "#stn1-a"+json.stn1.ant
            astn2 = "#stn2-a"+json.stn2.ant
            fstn1 = "#stn1-f"+json.stn1.fil
            fstn2 = "#stn2-f"+json.stn2.fil
            asstn1 = json.stn1.auto
            asstn2 = json.stn2.auto
            fsstn1 = json.stn1.bpf
            fsstn2 = json.stn2.bpf
            so2r = json.so2r
            $('#stn1-an').text(json.stn1.antname)
            $('#stn2-an').text(json.stn2.antname)
            $("#stn1-a0").removeClass("spanitemselected");
            $("#stn1-a1").removeClass("spanitemselected");
            $("#stn1-a2").removeClass("spanitemselected");
            $("#stn1-a3").removeClass("spanitemselected");
            $("#stn1-a4").removeClass("spanitemselected");
            $("#stn1-a5").removeClass("spanitemselected");
            $("#stn1-a6").removeClass("spanitemselected");
            $("#stn2-a0").removeClass("spanitemselected");
            $("#stn2-a1").removeClass("spanitemselected");
            $("#stn2-a2").removeClass("spanitemselected");
            $("#stn2-a3").removeClass("spanitemselected");
            $("#stn2-a4").removeClass("spanitemselected");
            $("#stn2-a5").removeClass("spanitemselected");
            $("#stn2-a6").removeClass("spanitemselected");
            $("#stn1-f0").removeClass("spanitemselected");
            $("#stn1-f1").removeClass("spanitemselected");
            $("#stn1-f2").removeClass("spanitemselected");
            $("#stn1-f3").removeClass("spanitemselected");
            $("#stn1-f4").removeClass("spanitemselected");
            $("#stn1-f5").removeClass("spanitemselected");
            $("#stn1-f6").removeClass("spanitemselected");
            $("#stn2-f0").removeClass("spanitemselected");
            $("#stn2-f1").removeClass("spanitemselected");
            $("#stn2-f2").removeClass("spanitemselected");
            $("#stn2-f3").removeClass("spanitemselected");
            $("#stn2-f4").removeClass("spanitemselected");
            $("#stn2-f5").removeClass("spanitemselected");
            $("#stn2-f6").removeClass("spanitemselected");
            $("#stn1-as").removeClass("spanitemwselected");
            $("#stn1-fs").removeClass("spanitemwselected");
            $("#stn2-as").removeClass("spanitemwselected");
            $("#stn2-fs").removeClass("spanitemwselected");
            $("#stn1-so2r").removeClass("spanitemwselected");
            $("#stn2-so2r").removeClass("spanitemwselected");
            $(astn1).addClass("spanitemselected")
            $(astn2).addClass("spanitemselected")
            $(fstn1).addClass("spanitemselected")
            $(fstn2).addClass("spanitemselected")
            if (asstn1 == true) $("#stn1-as").addClass("spanitemwselected")
            if (fsstn1 == true) $("#stn1-fs").addClass("spanitemwselected")
            if (asstn2 == true) $("#stn2-as").addClass("spanitemwselected")
            if (fsstn2 == true) $("#stn2-fs").addClass("spanitemwselected")
            if (so2r == "1") $("#stn1-so2r").addClass("spanitemwselected")
            if (so2r == "2") $("#stn2-so2r").addClass("spanitemwselected")
        }
    }



}