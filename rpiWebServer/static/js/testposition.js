$(document).ready(function () {
	getCoordinates(0);
});
function getCoordinates(track_sign) {
    sign = track_sign;
	var data = {
		data: JSON.stringify({
			time_count: "1",
            track_sign: sign
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
			alert("data send fail")
		}
	})
}
