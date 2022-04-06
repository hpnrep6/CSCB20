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

let setUser = (utorid, first, middle, last, email, status) => {
    let name = first + ' ' + middle + ' ' + last;
    info.innerHTML += accFormat('Name', name);
    info.innerHTML += accFormat('UtorID', utorid);
    info.innerHTML += accFormat('Email', email);
    info.innerHTML += accFormat('Status', status);

    let initials = '';

    if (first.length > 0) {
        initials += first[0];
    }

    if (last.length > 0) {
        initials += last[0];
    }
    initial.innerHTML = initials;
}

setUser('taco23', 'the', 'biggest', 'mara', 'a.@asdm', 'taco');