function sendMessage() {
    var userInput = document.getElementById("user-input").value;

    if (userInput != "") {
        fetch('/bot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 'input': userInput })
        })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                var conversationList = document.querySelector("ul.m-b-0.conversation");

                // Xóa nội dung trường nhập liệu sau khi người dùng gửi tin nhắn
                document.getElementById("user-input").value = "";

                // Tạo một phần tử <li> mới cho tin nhắn từ người dùng
                var userItem = document.createElement("li");
                userItem.className = "clearfix";
                var userDiv = document.createElement("div");
                userDiv.className = "message other-message float-right";
                userDiv.textContent = userInput; 
                userItem.appendChild(userDiv);

                // Chèn phần tử <li> của tin nhắn từ người dùng vào danh sách
                conversationList.appendChild(userItem);

                // Tạo một phần tử <li> mới cho tin nhắn từ bot
                var botItem = document.createElement("li");
                botItem.className = "clearfix";
                var botDiv = document.createElement("div");
                botDiv.className = "message my-message";
                botDiv.textContent = data; 
                botItem.appendChild(botDiv);

                // Chèn phần tử <li> của tin nhắn từ bot vào danh sách
                conversationList.appendChild(botItem);

                // Cuộn màn hình tới vị trí của phần tử mới được thêm vào
                window.scrollTo(0,conversationList.scrollHeight);
            })
    }

}
