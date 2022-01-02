window.onload = function () {
    var num_of_circles = 100;

	var canvas = document.getElementById('Canvas');
	var ctx = canvas.getContext('2d');
	var Radius = 5;

	function RandomPos(min, max) {
		return Math.floor(Math.random() * (max - min)) + min;	
    }

    var x = RandomPos(0, canvas.width);
	var y = RandomPos(0, canvas.height);

	var dx = RandomPos(-2, 2);
	var dy = RandomPos(-2, 2);

    var value_array = new Array();


    for (let index = 0; index < num_of_circles; index++) {
        value_array.push([x, y, dx, dy])
        
        var x = RandomPos(0, canvas.width);
        var y = RandomPos(0, canvas.height);

        var dx = RandomPos(-2, 2);
        var dy = RandomPos(-2, 2);
    }


	function drawBall(x_input, y_input) {
		ctx.beginPath();
		ctx.arc(x_input, y_input, Radius, 0, Math.PI*2);
		ctx.fillStyle = "#000000";
		ctx.fill();
		ctx.closePath();
	}


	function draw() {
		ctx.clearRect(0, 0, canvas.width, canvas.height);


        for (let lst_index = 0; lst_index < num_of_circles; lst_index++) {
            drawBall(value_array[lst_index][0], value_array[lst_index][1]);
        }


        for (let index = 0; index < num_of_circles; index++) {
            if ( value_array[index][0] + value_array[index][2] > canvas.width - Radius || value_array[index][0] + value_array[index][2] < Radius) {
                value_array[index][2] = -value_array[index][2]
            }
            if ( value_array[index][1] + value_array[index][3] > canvas.height - Radius || value_array[index][1] + value_array[index][3] < Radius) {
                value_array[index][3] = -value_array[index][3]
            }
    
            value_array[index][0] += value_array[index][2];
            value_array[index][1] += value_array[index][3];    
        }
	};

	setInterval(draw, 30);
};