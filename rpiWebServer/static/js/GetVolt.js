$(document).ready(function () {
    function get_volt() {
        fetch('/volt').then(res => res.text()).then(text => document.getElementById("volt").innerHTML = "Volt: " + text + "V");
    }
    window.onload = setInterval(get_volt, 1000);
});