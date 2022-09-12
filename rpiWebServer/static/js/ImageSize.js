$(document).ready(function () {
    window.onload = setInterval(ChangeSzie, 1000);

    function ChangeSzie() {
        let Image = document.getElementById("bg");
        let ScreenHeight = window.innerHeight;
        let ScreenWidth = window.innerWidth;
        let ImageHeight = ScreenHeight;
        let ImageWidth = ScreenHeight / 3 * 4;
        //console.log("ImageSize:" + ImageHeight + " " + ImageWidth);
        Image.style.height = ImageHeight + "px";
        Image.style.width = ImageWidth + "px";
        Image.style.marginLeft = (ScreenWidth - ImageWidth) / 2 + "px";
        Image.style.marginRight = (ScreenWidth - ImageWidth) / 2 + "px";
    }
});