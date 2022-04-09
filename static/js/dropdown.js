let dropdowns = document.getElementsByClassName('dropdown-content');

let dropdownShow = (e) => {
    let dropdown = document.getElementById(e.id + '-drop');
    let element = document.getElementById(e.id);

    dropdown.style.display = 'flex';
    dropdown.style.left = element.getBoundingClientRect().left + 'px';
    dropdown.style.top = element.getBoundingClientRect().bottom + 3 + window.scrollY + 'px';
    dropdown.style.width = Math.max(element.getBoundingClientRect().width, dropdown.getBoundingClientRect().width) + 'px';
}

let clearDropdowns = () => {
    for (let i = 0; i < dropdowns.length; ++i) {
        dropdowns[i].style.display = 'none';
    }
}

let setHeaderMobile = (header) => {
    if (header.getElementsByClassName('dropdown-element').length > 0) {
        return;
    }

    let headerElements = document.getElementById('dropdowns').getElementsByClassName('dropdown-element');
    
    for (let i = 0; i < headerElements.length; ++i) {
        let copy = headerElements[i].cloneNode(true);
        header.appendChild(copy);
    }
}

let setHeaderDesktop = (header) => {
    if (header.getElementsByClassName('dropdown-element').length == 0) {
        return;
    }

    let headerElements = header.getElementsByClassName('dropdown-element');
    for (let i = 0; i < headerElements.length; ++i) {
        headerElements[i].remove();
    }
}

window.onresize = (e) => {
    clearDropdowns();
}

window.onscroll = (e) => {
    clearDropdowns();
}

document.onmouseup = (e) => {
    clearDropdowns();
}

let personal = document.getElementById('personal-drop');

if (personal != undefined) {
    fetch('/api/status').then((res) => {
        return res.json();
    }).then((res) => {
        if (res == 'Student') {
            personal.innerHTML += `
            <a class="header-element dropdown-element" href="grades.html">Grades</a>
            <a class="header-element dropdown-element" href="account.html">Account</a>
            <a class="header-element dropdown-element" href="logout">Log Out</a>
            `;
        } else {
            personal.innerHTML += `
            <a class="header-element dropdown-element" href="regrades.html">Regrades</a>
            <a class="header-element dropdown-element" href="feedback.html">Feedback</a>
            <a class="header-element dropdown-element" href="students.html">Students</a>
            <a class="header-element dropdown-element" href="instructor.html">Instructor Centre</a>
            <a class="header-element dropdown-element" href="account.html">Account</a>
            <a class="header-element dropdown-element" href="logout">Log Out</a>
            `;
        }

        setHeaderDesktop(document.getElementById('header'));
    })
} else {
    setHeaderMobile(document.getElementById('header'));
}