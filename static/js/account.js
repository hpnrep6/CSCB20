let accFormat = (title, name) => {
    return `        
    <div class='info'>
        <h2>
            ` + title + `
        </h2>
        <p>
            `+ name +`
        </p>
    </div>`;
}

let info = document.getElementById('all-info');
let initial = document.getElementById('initials');

let setUser = (utorid, first, middle, last, status, instructor = undefined) => {
    let name = first + ' ' + middle + ' ' + last;
    info.innerHTML += accFormat('Name', name);
    info.innerHTML += accFormat('UtorID', utorid);
    info.innerHTML += accFormat('Status', status);
    
    if (instructor != undefined) {
        info.innerHTML += accFormat('Instructor', instructor);
    }

    let initials = '';

    if (first.length > 0) {
        initials += first[0];
    }

    if (last.length > 0) {
        initials += last[0];
    }
    initial.innerHTML = initials;
}

fetch('/api/user').then((res) => {
    return res.json();
}).then((res) => {
    setUser(res[0], res[1], res[2], res[3], res[4], res[5], res[6] != null ? res[6] : undefined);
})
