// Create a client instance
clientID = "web"
clientID += new Date().getUTCMilliseconds()
client = new Paho.MQTT.Client("192.168.43.6", Number(9001), clientID);

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});

// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("Connected");
  alert("Conexión establecida")
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
    $("#tablestn").addClass("blink");
    alert("Conexión perdida")
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
            astn1 = "#stn1-a"+json.stn1.ant
            astn2 = "#stn2-a"+json.stn2.ant
            fstn1 = "#stn1-f"+json.stn1.fil
            fstn2 = "#stn2-f"+json.stn2.fil
            bstn1 = "#stn1-b"+json.stn1.band
            bstn2 = "#stn2-b"+json.stn2.band
            asstn1 = json.stn1.auto
            asstn2 = json.stn2.auto
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
            $("#stn1-as").removeClass("spanitemselected");
            $("#stn1-fs").removeClass("spanitemselected");
            $("#stn2-as").removeClass("spanitemselected");
            $("#stn2-fs").removeClass("spanitemselected");
            $(astn1).addClass("spanitemselected")
            $(astn2).addClass("spanitemselected")
            $(bstn1).addClass("spanitemselected")
            $(bstn2).addClass("spanitemselected")
            $(fstn1).addClass("spanitemselected")
            $(fstn2).addClass("spanitemselected")
            if (asstn1 == true) $("#stn1-as").addClass("spanitemselected")
            if (asstn2 == true) $("#stn2-as").addClass("spanitemselected")
        }
    }
}