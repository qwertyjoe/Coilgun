function MouseClick(e) {
	if (typeof (e.offsetParent) != "undefined") {
		for (var posX = 0, posY = 0; e; e = e.offsetParent) {
			posX += e.offsetLeft;
			posY += e.offsetTop;
		}
		return [posX, posY];
	}
	else {
		return [e.x, e.y];
	}
}
function getCoordinates() {
	var PosX = 0;
	var PosY = 0;
	var ImgPos;
	ImgPos = MouseClick(image);
	if (!e) var e = window.event;
	if (e.pageX || e.pageY) {
		PosX = e.pageX;
		PosY = e.pageY;
	}
	else if (e.clientX || e.clientY) {
		PosX = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
		PosY = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
	}
	PosX = PosX - ImgPos[0];
	PosY = PosY - ImgPos[1];
	document.getElementById("x").innerHTML = PosX;
	document.getElementById("y").innerHTML = PosY;
	var data = {
		data: JSON.stringify({
			x: PosX,
			y: PosY,
			time_count: "1"
		}),
	}
	$.ajax({
		url: "image_roi",
		type: "post",
		data: data,
		dataType: 'html',
		success: function (data) {
			console.log("success");
		},
		error: function (xhr, ajaxOptions, thrownError) {
			console.log(thrownError);
			alert(thrownError);
		}
	})
}
