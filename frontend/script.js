const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const statusText = document.getElementById("status");

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        video.srcObject = stream;
        statusText.textContent = "המצלמה פועלת ✅";

        // אחרי שהמצלמה נפתחה — נתחיל לשלוח תמונה כל שנייה
        setInterval(captureAndAnalyze, 1000);

    } catch (error) {
        console.error(error);
        statusText.textContent = "לא ניתן לפתוח מצלמה ❌";
    }
}

async function captureAndAnalyze() {
    try {
        const context = canvas.getContext("2d");

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // הופך את הפריים לתמונה בפורמט Base64
        const imageBase64 = canvas.toDataURL("image/jpeg");

        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                image: imageBase64
            })
        });

        const data = await response.json();

        if (data.emotion) {
            statusText.textContent = `הרגש שזוהה: ${data.emotion}`;
            console.log("Emotion:", data.emotion);
        } else {
            statusText.textContent = "לא זוהה רגש";
            console.log(data);
        }

    } catch (error) {
        console.error("Error analyzing emotion:", error);
        statusText.textContent = "שגיאה בזיהוי הרגש";
    }
}

startCamera();