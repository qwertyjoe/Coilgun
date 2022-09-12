$(document).ready(function () {
    let image = document.getElementById("bg");
    let height = image.clientHeight;
    let width = image.clientWidth;
    console.log(width);
    console.log(height);
    window.onload = getCoordinates(width, height, 0);
    function keyEvent(event) {
        var key = event.keyCode;
        console.log(key)
        if (key === 13) {
            getCoordinates(width, height, 1);
        }
        if (key === 32) {
            getCoordinates(width, height, 0);
        }
    }
});