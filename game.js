// Initialize variables
var canvas;
var canvasContext;
var xSpeed = 0;
var ySpeed = 0;
var snakeX = 10;
var snakeY = 10;
var gridSize = 20;
var appleX = 15;
var appleY = 15;
var snakeTrail = [];
var tailSize = 5;

// Initialize the game
function gameInitialize() {
	canvas = document.getElementById("gameCanvas");
	canvasContext = canvas.getContext("2d");
	
	setInterval(gameLoop, 1000/15); // 15 frames per second
}

// Update the game
function gameLoop() {
	// Move the snake
	snakeX += xSpeed;
	snakeY += ySpeed;
	
	// Check for collision with the apple
	if (snakeX == appleX && snakeY == appleY) {
		tailSize++;
		appleX = Math.floor(Math.random() * gridSize);
		appleY = Math.floor(Math.random() * gridSize);
	}
	
	// Update the game speed
// Update the game speed
if (xSpeed != 0 || ySpeed != 0) {
	for (var i = snakeTrail.length - 1; i > 0; i--) {
		snakeTrail[i] = {x: snakeTrail[i - 1].x, y: snakeTrail[i - 1].y};
	}
	
	snakeTrail[0] = {x: snakeX, y: snakeY};
	
	// shorten the snake's tail if it's too long
	while (snakeTrail.length > tailSize) {
		snakeTrail.pop();
	}
}
	// Check for collision with the snake
// Check for collision with the apple
if (snakeX == appleX && snakeY == appleY) {
	tailSize++; // increase the length of the snake
	appleX = Math.floor(Math.random() * gridSize);
	appleY = Math.floor(Math.random() * gridSize);
	
	// add a new segment to the snake's tail
	snakeTrail.push({x: snakeX, y: snakeY});
}

	
	// Draw the canvas, snake, and apple
	canvasContext.fillStyle = "gray";
	canvasContext.fillRect(0, 0, canvas.width, canvas.height);
	
	canvasContext.fillStyle = "green";
	for (var i = 0; i < snakeTrail.length; i++) {
		canvasContext.fillRect(snakeTrail[i].x * gridSize, snakeTrail[i].y * gridSize, gridSize - 2, gridSize - 2);
	}
	
	canvasContext.fillStyle = "red";
	canvasContext.fillRect(appleX * gridSize, appleY * gridSize, gridSize - 2, gridSize - 2);
	
	// Handle keyboard input
	if (keysPressed[37]) {
		xSpeed = -1;
		ySpeed = 0;
	}
	if (keysPressed[38]) {
		xSpeed = 0;
		ySpeed = -1;
	}
	if (keysPressed[39]) {
		xSpeed = 1;
		ySpeed = 0;
	}
	if (keysPressed[40]) {
		xSpeed = 0;
		ySpeed = 1;
	}
}

// Handle keyboard input
var keysPressed = {};

document.addEventListener("keydown", function(event) {
	keysPressed[event.keyCode] = true;
});

document.addEventListener("keyup", function(event) {
	delete keysPressed[event.keyCode];
});

// Start the game
gameInitialize();
