let cont = document.getElementById('class');

let grid = [];
grid[0] = [];
grid[0][0] = 0;
let aMap = new Map();
let edited = [];

class Student {
    key;
    name;
    constructor(key, name) {
        this.key = key;
        this.name = name;
    }
}

class vec2 {
    x;
    y;
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

function renderTable() {
    let table = document.getElementById('student-grades');
    let edit_table = document.getElementById('edit-grades')
    let header = document.getElementById('grade-header');
    let edit = document.getElementById('edit-header');
    for (let i = 1; i < grid[0].length; ++i) {
        let title = `
            <div class='entry col' id=g_0x`+i+`>` + grid[0][i] + `</div>
        `;
        header.innerHTML += title;
        edit.innerHTML += title;
    }

    for (let y = 1; y < grid.length; ++y) {
        let id = 'g_' + y
        table.innerHTML += `
            <div class='row' id=`+id+`>
            </div>        
        `

        edit_table.innerHTML += `
        <div class='row' id=e_`+id+`>
        </div>        
    `

        let elem = document.getElementById(id);
        let edit_elem = document.getElementById('e_' + id);

        for (let x = 0; x < grid[y].length; ++x) {
            let id = 'g_' + y+'x'+x
            let entry = grid[y][x];

            if (x == 0) {
                entry = grid[y][x].name;
            }

            if (entry == null) {
                entry = 'NA'
            }

            if (x != 0) {
                elem.innerHTML += `
                    <div id=`+id+` class='entry col'>`+entry+`</div>
                `
            } else {
                elem.innerHTML += `
                    <div id=`+id+` class='entry names col'>`+entry+`</div>
                `
            }

            if (entry == 'NA') {
                entry = -1;
            }


            if (isNaN(entry)) {
                edit_elem.innerHTML += `
                    <div id=e_`+id+` class='entry names col'>`+entry+`</div>
                `
                continue;
            }

            edit_elem.innerHTML += `
                <div class='entry col'>
                    <div class='center-tool'>
                        <input onclick='editGrade(this)' id=e_`+id+` type='number' value=`+entry+`>
                        </input>
                    </div>
                </div>
            `
        }
    }
}

function updateGrades(e) {
    for (let y = 1; y < grid.length; ++y) {
        for (let x = 1; x < grid[y].length; ++x) {
            let edited_grade = document.getElementById('e_g_'+y+'x'+x).value;
            let displayed_grade = document.getElementById('g_'+y+'x'+x);

            if (edited_grade >= 0)
                displayed_grade.innerHTML = edited_grade;
            else 
                displayed_grade.innerHTML = 'NA';
        }
    }

    if (e.innerHTML == 'Edit Grades') {
        e.innerHTML = 'Save Grades';
        document.getElementById('edit-grades').style.display = 'table';
        document.getElementById('student-grades').style.display = 'none';
    } else {
        e.innerHTML = 'Edit Grades';
        document.getElementById('edit-grades').style.display = 'none';
        document.getElementById('student-grades').style.display = 'table';

        for (let y = 0; y < edited.length; ++y) {
            for (let x = 0; x < edited[y].length; ++x) {
                // if (edited[y][x] == 1) {
                if (x > 0 && y > 0) {
                    edited[y][x] = 0;

                    let grade = document.getElementById('e_g_'+y+'x'+x).value;
                    if (grade < 0) {
                        grade = 'null';
                    }

                    let utorid = grid[y][0].key;
                    let aName = grid[0][x];

                    let form = new FormData();
                    form.append('UtorID', utorid);
                    form.append('Grade', grade);
                    form.append('Assignment', aName);

                    let req = new XMLHttpRequest();
                    req.open('POST', '/api/grade');
                    req.send(form);
                }
            }
        }
    }
}

function editGrade(e) {
    let id = e.id;

    let y = parseInt(id.substring(id.indexOf('g_') + 2, id.indexOf('x')));
    let x = parseInt(id.substring(id.indexOf('x') + 1));

    edited[y][x] = 1;
}

fetch('/api/grade').then((res) => {
    return res.json();
}).then((res) => {
    let assignments = res['_assignments'];
    let length = 0;
    edited[0] = [];
    
    for (i in assignments) {
        grid[0].push(assignments[i][0]);
        // cont.innerHTML += `
        // <div class="col" id=g_0-`+i+`>
        //     <div class="entry assignment-name">
        //         `+assignments[i]+`
        //     </div>
        // </div>
        // `
        aMap[assignments[i]] = parseInt(i) + 1;
        edited[0].push(0);
        ++length;
    }
    let st_c = 1;

    let students = document.getElementById('student-name')
    for (let key in res) {
        if (key == '_assignments') {
            continue;
        }

        let student = res[key];
        // students.innerHTML += `
        //     <div class="entry" id=sname_`+aNameId+`>
        //         `+key+`
        //     </div>
        // `
 
        let st_obj = new Student(key, student[0][0][0] + ' ' + student[0][0][2])
        grid[st_c] = []
        grid[st_c][0] = st_obj;
        edited[st_c] = [];
        edited[st_c][0] = 0;


        for (let i = 0; i < length; ++i) {
            grid[st_c][i + 1] = 0;
            edited[st_c][i + 1] = 0;
        }

        for (i in student) {
            if (i == 'id') {
                continue;
            }

            let index = aMap[student[i][0][3]];
            grid[st_c][index] = student[i][0][4];
            // let a = document.getElementById('aname_' + index);
            // a.innerHTML += `
            // <div class="entry" id=grade_`+sNameId+`+`+index+`>
            //     `+student[i][4]+`
            // </div>
            // `
        }

        st_c++;
    }
    renderTable();
})

