const validationServer =
  "https://connorcode.com/Downloads/EacloxusStatus.json/";
const ipServer = "https://ipinfo.io/ip";

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
async function message(text) {
  confirm(text);
}
function receiveValidation(data) {
  window.validationIp = JSON.parse(data);
  httpGetAsync(ipServer, receiveLocalIp);
}
function receiveLocalIp(data) {
  try {
    window.LocalIp = data.split("\n")[0];
    var gameVersion =
      runtimeScene._runtimeGame._variables._variables.items.Version._str;
    if (window.validationIp.version[gameVersion].includes(window.LocalIp)) {
      console.log("Success! Logged in with Ip: " + window.LocalIp);
    } else {
      message("You are not allowed to run this Internal Release...");
      remote.getCurrentWindow().close();
    }
  } catch {
    message("Error connecting to Authentication Servers");
    remote.getCurrentWindow().close();
  }
}

try {
  httpGetAsync(validationServer, receiveValidation);
} catch {
  message("Error connecting to Authentication Servers");
  remote.getCurrentWindow().close();
}

runtimeScene
  .getVariables()
  .get("random")
  .setString(Math.floor(Math.random() * 100));
