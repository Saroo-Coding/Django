
document.getElementById("linkSpan").addEventListener("click", function () {
    var linkText = this.textContent;
    var tempInput = document.createElement("input");
    tempInput.value = linkText;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    document.getElementById("noti").textContent = "Link copied ! Send this link to your opponent to connect.";
    // Return to original content after 30 seconds
    setTimeout(function () {
        document.getElementById("noti").textContent = "Click to copy ! ";
    }, 15000);
});


