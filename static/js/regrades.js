let formatAssignment = (title, id) => {
    id = id.replaceAll(' ', '_-_');
    id = id.replaceAll('g', '_-_');
    id = id.replaceAll('b', '_-_');
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

function appendAssignment(title, id) {
    grades.innerHTML += formatAssignment(title, id);    
}

let moreinfo = (e) => {
    let details = (document.getElementById(e.id.substring(0, e.id.indexOf('b')))).getElementsByClassName('grade-details')[0];
    if (details.style.display == 'flex') {
        details.style.display = 'none';
    } else {
        details.style.display = 'flex';
    }
}

let appendRegrade = (title, details, id, dummy = false) => {
    id = id.replaceAll(' ', '_-_');
    id = id.replaceAll('g', '_-_');
    id = id.replaceAll('b', '_-_');
    let grades = document.getElementById(id + 'g');

    if (dummy) {
        grades.innerHTML += `
        No regrade requests (for now) :)`;
    } else {
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
}

fetch('/api/regrade').then((res) => {
    return res.json();
}).then((res) => {
    for (key in res) {
        let regrade_count = res[key].length
        appendAssignment(key + ' (' + regrade_count + ')', key);

        for (i in res[key]) {
            let student = res[key][i];

            appendRegrade('Regrade request by ' + student[1] + ' ' + student[2] + ' (' + student[0] + ')', student[3], key);
        }

        if (res[key].length == 0) {
            appendRegrade('', '', key, true);
        }
    }
});
