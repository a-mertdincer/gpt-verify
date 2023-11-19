/* static/scripts.js */

function checkDockerfile() {
    var dockerfileContent = document.getElementById("dockerfileContent").value;
    var dockerfileHeader = document.getElementById("dockerfileHeader").innerText;

    sendDockerfileToAPI(dockerfileHeader, dockerfileContent);
}

function sendDockerfileToAPI(header, content) {
    var apiUrl = "/check_dockerfile";

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            header: header,
            content: content,
        }),
    })
    .then(response => response.json())
    .then(data => handleApiResponse(data))
    .catch(error => console.error('API Hatası:', error));
}

function handleApiResponse(responseData) {
    console.log('API Cevabı:', responseData);
    var outputDiv = document.getElementById("output");
    outputDiv.innerHTML = `<p>${responseData.message}</p>`;
}
