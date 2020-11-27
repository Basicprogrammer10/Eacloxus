const validationServer = "http://localhost:1234/login/";
const version =
  runtimeScene._runtimeGame._variables._variables.items.Version._str;
const remote = require("electron").remote;

function httpGetAsync(theUrl, callback) {
  try {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.timeout = 4000;
    xmlHttp.onreadystatechange = function () {
      if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
        callback(xmlHttp.responseText);
    };
    xmlHttp.open("GET", theUrl, true);
    xmlHttp.send(null);
  } catch {
    message("Error connecting to Authentication Servers");
    remote.getCurrentWindow().close();
  }
}

function receiveValidation(data) {
  var validation = JSON.parse(data);
  console.log(validation);
  if (validation["auth"] == "success") {
    console.log("Sucess!");
  } else if (validation["auth"] == "denied") {
    confirm("You are not allowed to run this Internal Release...");
    remote.getCurrentWindow().close();
  } else {
    confirm("Error connecting to Authentication Servers");
    remote.getCurrentWindow().close();
  }
}

try {
  httpGetAsync(validationServer + "?version=" + version, receiveValidation);
} catch {
  message("Error connecting to Authentication Servers");
  remote.getCurrentWindow().close();
}
