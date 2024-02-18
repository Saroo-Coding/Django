let firstKeyPress = true;

function pressKey(value) {
    if (document.getElementById('screen').innerText == "0") {
        document.getElementById('screen').innerText = "";
        document.getElementById('screen_input').value = "";
    }
    //ko cho dau + * / dung truoc
    if(firstKeyPress){
        switch(value) {
            case "+":
            case "*":
            case "/":
            case ".":
                firstKeyPress = true;
                document.getElementById('screen').innerText = "0";
                document.getElementById('screen_input').value = "0";
                break;
            default:
                firstKeyPress = false;
                document.getElementById('screen').innerText += value;
                document.getElementById('screen_input').value += value;
        }
    }
    else{ //2 phep tinh lien nhau
        var char = document.getElementById('screen').innerText.charAt(document.getElementById('screen').innerText.length - 1);
        switch (char) {
            case ".":
                if (value !== char && !isOperator(value)) {
                    document.getElementById('screen').innerText += value;
                    document.getElementById('screen_input').value += value;
                }
                break;
            case "+":
            case "-":
            case "*":
            case "/":
                if (value !== char && value !== "." && !isOperator(value)) {
                    document.getElementById('screen').innerText += value;
                    document.getElementById('screen_input').value += value;
                }
                break;
            default:
                document.getElementById('screen').innerText += value;
                document.getElementById('screen_input').value += value;
        }
    }
}

function isOperator(char) {
    return char === "+" || char === "-" || char === "*" || char === "/";
}

function clearScreen() {
    firstKeyPress = true;
    document.getElementById('screen').innerText = '0';
    document.getElementById('screen_input').value = '0';
}

function delChar() {
    var screen = document.getElementById('screen');
    var currentText = screen.innerText;
    if (currentText.length > 1)
    {
        screen.innerText = currentText.substring(0, currentText.length - 1);
        document.getElementById('screen_input').value = document.getElementById('screen_input').value.substring(0, document.getElementById('screen_input').value.length - 1);
    }
    else{
        firstKeyPress = true;
        screen.innerText = "0";
        document.getElementById('screen_input').value = "0";
    }
}
