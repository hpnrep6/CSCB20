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
            <h2>` + title + `
            </h2>
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
        <button class='regrade-button'>
            Request Regrade
        </button>
        </div>
    </div>`;
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

appendGrade('Taco taco ate the paco', 54, 'Taco ate paco there daco');
appendGrade('Paco taco ate the paco', 54, 'Taco ate paco there daco');
appendGrade('Xaco taco ate the paco', 54, 'Taco ate paco there daco');
