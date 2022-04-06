let formatAssignment = (title, id) => {
    return `
    <div class='grade-entry' id=`+id+`>
    <div class='grade-info'>
        <div class='grade-title grade-grid'>
            <h2>` + title + `
            </h2>
        </div>
        <div class='grade-moreinfo grade-grid' onclick='moreinfo(this)' id=`+id+`b>
            <img src='./static//images/Information_icon.svg'>
        </div>
        </div>

        <div class='grade-details grade-grid' id=`+id+`g>
        </div>
    </div>`;
}

let grades = document.getElementsByClassName('grades')[0];

function appendAssignment(title, grade, details) {
    grades.innerHTML += formatAssignment(title, grade, details);    
}

let moreinfo = (e) => {
    let details = (document.getElementById(e.id.substring(0, e.id.indexOf('b')))).getElementsByClassName('grade-details')[0];

    if (details.style.display == 'flex') {
        details.style.display = 'none';
    } else {
        details.style.display = 'flex';
    }
}

let appendRegrade = (title, details, id) => {
    let grades = document.getElementById(id + 'g');
    grades.innerHTML += `
    <div class='grade-grid regrade-details'>
        <h2>
            `+ title +`
        </h2>
        <p>
            `+details+`
        </p>
    </div>`;
}

appendAssignment('Xaco taco ate the paco', 'taco');

appendRegrade('taco taco ate paco', 'paco taco', 'taco')
appendRegrade('taco taco ate paco', 'paco taco', 'taco')
appendRegrade('taco taco ate paco', 'paco taco', 'taco')
appendRegrade('taco taco ate paco', 'paco taco', 'taco')