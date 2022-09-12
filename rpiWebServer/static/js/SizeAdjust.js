function BoxAdjust(adjust_sign){
    sign = adjust_sign;
    var data = {
        data: JSON.stringify({
            sign : sign
        }),
    }
    $.ajax({
        url: "tracking_size",
        type: "post",
        data: data,
        dataType: 'html',
        success: function(){
            console.log("send success")
        },
        error: function (thrownError){
            console.log(thrownError);
            alert(thrownError);
        }
    })
}