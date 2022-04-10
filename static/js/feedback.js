let feedback = document.getElementById('feedback');

let appendFeedback = (details) => {
    feedback.innerHTML += `
    <div class="feedback-item">
        <topcurve></topcurve>
        <p>
        `+details+`
        </p>
        <bottomcurve></bottomcurve>
    </div>`;
}

fetch('/api/feedback').then((res) => {
    return res.json()
}).then((res) => {
    for (i in res) {
        let response = res[i];

        appendFeedback(response[0]);
    }
})
