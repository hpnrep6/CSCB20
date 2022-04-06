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

appendFeedback('taco paco taco', '2022,22,22', 'staco')