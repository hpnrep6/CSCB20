let instrList = document.getElementById('instructors')

fetch('/api/instructors').then( (res) => {
    return res.json();
}).then((instructors) => {
    for (let i = 0; i < instructors.length; ++i) {
        let instr = instructors[i];

        let name = instr[1] + ' ' + instr[2] + ' ' + instr[3];
        instrList.innerHTML += `
            <option value="`+instr[0]+`">`+name+`</option>`;
    }

}).catch((e)=> {

})

function setInstructor(e) {
    if (e.value == 'Instructor') {
        instrList.style.display = 'none';
        document.getElementById('instructor-select').style.display = 'none';
    } else {
        instrList.style.display = 'block';
        document.getElementById('instructor-select').style.display = 'block';
    }
}

function submit(e) {
    let form = document.getElementById('login-form');
    let formdata = new FormData(form);

    let req = new XMLHttpRequest();

    req.onreadystatechange = () => {
        if (req.readyState == 4) {
            if (req.response != 'Success') {
                let notify = document.getElementById('notify');
                notify.style.display = 'block';
                notify.innerHTML = req.response;
            } else {
                location.reload();
            }
        }
    }

    req.open('POST', '/login');
    req.send(formdata);
}