let counter = 0;
let generateId = () => {
    ++counter;
    return 'grade-' + counter;
}

let formatGrade = (title, grade, details) => {
    let id = generateId();

    return `
    <div class='grade-entry' id=`+id+`>
        <div class='grade-info'>
            <div class='grade-title grade-grid'>
                <h2>` + title + `</h2>
            </div>
            <div class='grade-value grade-grid'>
                <h4 class='center-tool'>
                `+grade+`%
                </h4>
            </div>
            <div class='grade-moreinfo grade-grid' onclick='moreinfo(this)' id=`+id+`b>
                <img src='./static//images/Information_icon.svg'>
                <!-- https://commons.wikimedia.org/wiki/File:Information_icon.svg -->
            </div>
            </div>

            <div class='grade-details grade-grid'>
            <h2>
                Details
            </h2>
            <p>
                `+details+`
            </p>
            <h3 class='submitted-regrade'>
                Regrade Submitted!
            </h3>
            <textarea class='regrade-info' value='details'></textarea>
            <button class='regrade-button' onclick='regrade(this)'>Request Regrade</button>
        </div>
    </div>`;
}

function regrade(e) {
    let text = e.parentElement.getElementsByClassName('regrade-info')[0];
    if (e.innerHTML == 'Request Regrade') {
        text.style.display = 'block';
        e.innerHTML = 'Submit Regrade'
    } else {
        e.style.display = 'none';
        let info = text.value;
        text.style.display = 'none';

        let assignment = e.parentElement.parentElement.getElementsByClassName('grade-title')[0].getElementsByTagName('h2')[0].innerHTML;
        
        let form = new FormData();
        form.append('Assignment', assignment);
        form.append('Content', info);

        let req = new XMLHttpRequest();
        req.open('POST', '/api/regrade');
        req.send(form);
    }
}

let grades = document.getElementsByClassName('grades')[0];

function appendGrade(title, grade, details) {
    grades.innerHTML += formatGrade(title, grade, details);    
}

let moreinfo = (e) => {
    let details = (document.getElementById(e.id.substring(0, e.id.indexOf('b')))).getElementsByClassName('grade-details')[0];

    if (details.style.display == 'flex') {
        details.style.display = 'none';
    } else {
        details.style.display = 'flex';
    }
}

fetch('/api/grade/student').then((res) => {
    return res.json();
}).then((res) => {
    console.log(res)
    for (i in res) {
        appendGrade(res[i][0], res[i][1], res[i][2]);
    }
});