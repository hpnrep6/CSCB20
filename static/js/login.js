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
    console.log(3)
}).catch((e)=> {
    console.log(e)
})

function setInstructor(e) {
    if (e.value == 'Instructor') {
        instrList.style.display = 'none';
    } else {
        instrList.style.display = 'block';
    }
}