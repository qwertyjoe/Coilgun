$(document).ready(function () {
    let Forward = 0;
    let Back = 0;
    let Right = 0;
    let Left = 0;
    let TurnRight = 0;
    let TurnLeft = 0;
    let SpeedSign = 1
    var MoveData = [0, 0, 0, 0]
    var speed = 4000
    //lf , rf , lb , rb 
    document.onkeydown = function (e) {
        let ImageHeight = window.innerHeight;
        let ImageWidth = ImageHeight / 3 * 4 / 2;
        let Scale = ImageHeight / 360;
        let horizontal = 0, vertical = 0;
        // W key
        if (!e.repeat) {
            if (e.keyCode == 87 && Forward != 1) {
                //fetch('/?method=forward');
                for (var i = 0; i < 4; i++) {
                    MoveData[i] += 1;
                }
                Move(MoveData, speed);
                Forward = 1;
            }
            // S key
            if (e.keyCode == 83 && Back != 1) {
                //fetch('/?method=backward');
                //Back = 1;
                for (var i = 0; i < 4; i++) {
                    MoveData[i] -= 1;
                }
                Move(MoveData, speed);
                Back = 1;
            }
            
            // A key
            if (e.keyCode == 81 && Right != 1) {
                //fetch('/?method=right');
                //Right = 1;
                //Move(4);
                MoveData[0] -= 1;
                MoveData[1] += 1;
                MoveData[2] -= 1;
                MoveData[3] += 1;
                Move(MoveData, speed)
                Right = 1;
            }
            // D key
            if (e.keyCode == 69 && Left != 1) {
                //fetch('/?method=left');
                //Left = 1;
                //Move(3);
                MoveData[0] += 1;
                MoveData[1] -= 1;
                MoveData[2] += 1;
                MoveData[3] -= 1;
                Move(MoveData, speed)
                Left = 1;
            }
            // Q key
            if (e.keyCode == 65 && TurnRight != 1) {
                MoveData[0] -= 1;
                MoveData[1] += 1;
                MoveData[2] += 1;
                MoveData[3] -= 1;
                Move(MoveData, speed);
                TurnRight = 1;
            }
            
            // E key
            if (e.keyCode == 68 && TurnLeft != 1) {
                MoveData[0] += 1;
                MoveData[1] -= 1;
                MoveData[2] -= 1;
                MoveData[3] += 1;
                Move(MoveData, speed)
                TurnLeft = 1;
            }
            //number keyboard up (boxsize big)
            if (e.keyCode == 38) {
                BoxAdjust(0);
            }
            //number keyboard down (boxsize small)
            if (e.keyCode == 40) {
                BoxAdjust(1);
            }
            //number keyboard 4 left
            if (e.keyCode == 100) {
                HMotorAdjust(1);
            }
            //number keyboard 6 right
            if (e.keyCode == 102) {
                HMotorAdjust(-1);
            }
            //number keyboard 8 up
            if (e.keyCode == 104) {
                VMotorAdjust(0.15);
            }
            //number keyboard 2 down
            if (e.keyCode == 98) {
                VMotorAdjust(-0.15)
            }
        }
    };
    document.onkeyup = function (e) {
        // W key
        if (e.keyCode == 87) {
            //Forward = 0;
            //Move(1);
            for (var i = 0; i < 4; i++) {
                MoveData[i] -= 1;
            }
            Move(MoveData, speed);
            Forward = 0;
        }
        // S key
        if (e.keyCode == 83) {
            //Back = 0;
            //Move(2);
            for (var i = 0; i < 4; i++) {
                MoveData[i] += 1;
            }
            Move(MoveData, speed);
            Back = 0
        } 
        // A key
        if (e.keyCode == 81) {
            //Right = 0;
            //Move(4);
            MoveData[0] += 1;
            MoveData[1] -= 1;
            MoveData[2] += 1;
            MoveData[3] -= 1;
            Move(MoveData, speed);
            Right = 0;
        }
        // D Key
        if (e.keyCode == 69) {
            //Left = 0;
            //Move(3);
            MoveData[0] -= 1;
            MoveData[1] += 1;
            MoveData[2] -= 1;
            MoveData[3] += 1;
            Move(MoveData, speed);
            Left = 0;
        }
        // Q Key 
        if (e.keyCode == 65) {
            MoveData[0] += 1;
            MoveData[1] -= 1;
            MoveData[2] -= 1;
            MoveData[3] += 1;
            Move(MoveData, speed);
            TurnRight = 0;
        }
        // E Key
        if (e.keyCode == 68) {
            MoveData[0] -= 1;
            MoveData[1] += 1;
            MoveData[2] += 1;
            MoveData[3] -= 1;
            Move(MoveData, speed);
            TurnLeft = 0;
        }
        if (e.keyCode == 38 || e.keyCode == 40) {
            BoxAdjust(-1);
        }
        //number keyboard down (boxsize small)
        /*if (e.keyCode == 87 || e.keyCode == 83 || e.keyCode == 65 || e.keyCode == 68 ) {
            if (Forward == 0 && Back ==0 && Right ==0 && Left == 0 && TurnRight ==0 && TurnLeft ==0) {
                fetch('/?method=stop');
            }
        }*/
        // number keyboard left right
        if (e.keyCode == 100 || e.keyCode == 102) {
            HMotorAdjust(0);
        }
        // number keyboard up down
        if (e.keyCode == 104 || e.keyCode == 98) {
            VMotorAdjust(0);
        }
        // J key
        if (e.keyCode == 74) {
            fetch('/?method=shot');
        }
        // L key
        if (e.keyCode == 76) {
            fetch('/?method=re');
        }
        // K key
        if (e.keyCode == 75) {
            fetch('/?method=re stop')
        }
        // Shift key
        if (e.keyCode == 16) {
            if (SpeedSign == 1) {
                SpeedSign = 0;
                speed = 3000;
                Move(MoveData, speed);
            }
            else if (SpeedSign == 0) {
                SpeedSign = 1;
                speed = 4000;
                Move(MoveData, speed);
            }
            fetch('/?method=switch')
        }

        // Enter key
        if (e.keyCode == 13) {
            getCoordinates(1);
            //getCoordinates(ImageWidth, ImageHeight / 2, Scale, 1);
        }
        // Space key
        if (e.keyCode == 32) {
            //getCoordinates(ImageWidth, ImageHeight / 2, Scale, 0);
            getCoordinates(0);
        }
    };

});
