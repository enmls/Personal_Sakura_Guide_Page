function sendMessage() {
    var inputText = document.getElementById("input_text").value;


    if (inputText != "") {
        var chatBox = document.getElementById("chat-box");
        var userInput = document.createElement("div");
        userInput.classList.add("message-from-user");
        userInput.innerHTML = "<p>" + inputText + "</p>";
        chatBox.appendChild(userInput);
        document.getElementById("input_text").disabled = true; // 禁用输入框
        document.getElementById("input_text").placeholder = "思考中...";

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/get_response", true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var gptResponse = xhr.responseText;
                var gptOutput = document.createElement("div");
                gptOutput.classList.add("message-from-gpt");
                gptOutput.innerHTML = "<p>" + gptResponse + "</p>";
                chatBox.appendChild(gptOutput);
                chatBox.scrollTop = chatBox.scrollHeight;
                //document.getElementById("input_text").value = ""; // 清空输入框的文本内容
                document.getElementById("input_text").disabled = false;
                document.getElementById("input_text").placeholder = "这里是输入框";
            }
        };
        xhr.send("input_text=" + inputText);
        document.getElementById("input_text").value = ""; // 清空输入框的文本内容
    }

    return false;
}
function clearInput() {
    document.getElementById("input_text").value = "";
}
