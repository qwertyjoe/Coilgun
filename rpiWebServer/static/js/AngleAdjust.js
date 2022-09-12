function HMotorAdjust(horizontal) {
    Horizontal_sign = horizontal;
    if (Horizontal_sign == 1){
        HStartAngle = 62
    }
    if (Horizontal_sign == -1){
        HStartAngle = 108
    }
    if (Horizontal_sign == 0){
        HStartAngle = 85
    }
    var hordata =
        JSON.stringify({
            horizontal: HStartAngle,
        })

    console.log(hordata)
    $.ajax({
        url: "Hrotation",
        type: "post",
        contentType: "application/json",
        data: hordata,
        dataType: 'json',
        success: function () {
            console.log("send success")
        },
        error: function (thrownError) {
            console.log(thrownError);
        }
    })
}

function VMotorAdjust(vertical) {
    Vertical_sign = vertical;
    var verdata =
        JSON.stringify({
            vertical: Vertical_sign,
        })

    $.ajax({
        url: "Vrotation",
        type: "post",
        contentType: "application/json",
        data: verdata,
        dataType: 'html',
        success: function () {
            console.log("send success")
        },
        error: function (thrownError) {
            console.log(thrownError);
        }
    })
}