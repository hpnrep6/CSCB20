let feedback = document.getElementById('feedback');

let appendFeedback = (title, date, details) => {
    feedback.innerHTML += `
    <div class="feedback-item">
        <h2>
        `+title+`
        </h2>
        <h4>
        `+date+`
        </h4>
        <p>
        `+details+`
        </p>
    </div>`;
}

fetch('/api/feedback').then((res) => {
    return res.json()
}).then((res) => {
    for (i in res) {
        let response = res[i];

        appendFeedback('', '', response[0]);
    }
})
