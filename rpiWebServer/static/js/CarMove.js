function Move(move, speed) {
    MoveSign = move;
    lf = MoveSign[0];
    rf = MoveSign[1];
    lb = MoveSign[2];
    rb = MoveSign[3];
    
    if(lf > 1){
	    lf = 1;
    }
    if(lf < -1){
        lf = -1;
    }

    if(rf > 1){
	    rf = 1;
    }
    if(rf < -1){
        rf = -1;
    }

    if(lb > 1){
	    lb = 1;
    }
    if(lb < -1){
        lb = -1;
    }

    if(rb > 1){
	    rb = 1;
    }
    if(rb < -1){
        rb = -1
    }

    lf = lf * speed;
    rf = rf * speed;
    lb = lb * speed;
    rb = rb * speed;
    var movedata = {
        data: JSON.stringify({
            lf: lf,
            rf: rf,
            lb: lb,
            rb: rb,
        }),
    }
    $.ajax({
        url: "wheels",
        type: "post",
        data: movedata,
        dataType: 'html',
        success: function () {
            console.log("send success")
        },
    })
    // W = 1 , S = 2 
    // A = 3 , D = 4
    // Q = 5 , E = 6
    // Shift = 7
}
