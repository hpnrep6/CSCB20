class Student {
    static assignmentCount = 0;

    ref;
    root;
    name;
    status;
    avg;
    assignments_elem;
    assignments = [];

    addAssignment(name, grade) {
        let a = new Assignment();
        a.parent = this;
        a.title  = name;
        a.grade = grade;

        ++Student.assignmentCount;
        let str = `
        <div class="center-tool limit-width" id=s`+Student.assignmentCount+`>
            <div class="assignment-grid">
            <div class="assignment-container">
                <h3>
                `+name+`
                </h3>
                <div class='grade-display'>
                <h3>`+grade+`</h3>
                <textarea class="grade-edit"></textarea>
                <div class='center-tool'>
                    <button>Save</button>
                    </div>
                </div>
            </div>
            </div>
        </div>
        `;

        this.assignments_elem.innerHTML += str;

        let element = document.getElementById('s' + Student.assignmentCount);
        
        a.root = element;
        a.button = element.getElementsByClassName('grade-display')[0].getElementsByTagName('h3')[0];
        a.h3 = element.getElementsByClassName('grade-display')[0].getElementsByTagName('h3')[0];
        a.save = element.getElementsByTagName('button')[0];
        a.edit = element.getElementsByTagName('textarea')[0];

        a.h3.onclick = () => { a.editGrade() };
        a.save.onclick = () => { a.saveGrade() };

        this.assignments.push(a);
        this.updateAverage();
    }

    updateAverage() {
        let total = 0.0;
        for (let i = 0; i < this.assignments.length; ++i) {
            console.log(this.assignments[i])
            total += this.assignments[i].grade;
        }

        total /= this.assignments.length;
        total = total.toString();
        total = total.substring(0, 4);

        this.avg.innerHTML = total;
    }
}

class Assignment {
    parent;
    title;
    grade;
    root;
    button;
    edit;
    h3;
    save;

    editGrade() {
        this.h3.style.display = 'none';
        this.edit.style.display = 'block';
        this.save.style.display = 'block';
    }

    saveGrade() {
        this.h3.style.display = 'block';
        this.edit.style.display = 'none';
        this.save.style.display = 'none';

        let nGrade = this.edit.innerHTML;

        this.parent.updateAverage();
    }
}

let idCount = 0;
let idMap = new Map();
let students = document.getElementById('class');

function createStudent(name, ref, status='Student') {
    idCount += 1;
    id = idCount;
    let str = `
    <div class="student-all" id=c`+id+`>
    <div class="student">
        <div class="name">
        <h2>
            `+name+`
        </h2>
        </div>

        <div class="status">
        <h2>
            `+status+`
        </h2>
        </div>
        <div class="grades-avg">
        <h2>
            NA
        </h2>
        </div>
        <div class="grades-dropdown">
        <h2>
            <img src="./static/images/Information_icon.svg">
        </h2>
        </div>
    </div>
        <div class="student-assignments">
        </div>
    </div>`;
    students.innerHTML += str;
    
    let student = new Student();
    console.log(students);
    let element = document.getElementById(('c' + id));

    student.root = element;
    student.name = element.getElementsByClassName('name')[0].getElementsByTagName('h2')[0];
    student.status = element.getElementsByClassName('status')[0].getElementsByTagName('h2')[0];
    student.avg = element.getElementsByClassName('grades-avg')[0].getElementsByTagName('h2')[0];

    student.assignments_elem = element.getElementsByClassName('student-assignments')[0];

    idMap.set(id, student);

    return student;
}


fetch('/api/grade').then((res) => {
    return res.json();
}).then( (res) => {
    for (i in res) {
        let a = res[i];
        let utorid = a[0];

        if (idMap.has(utorid)) {
            idMap.get(utorid).addAssignment(a[4], a[5])
        } else {
            let s = createStudent(a[1] + ' ' + a[3], a[0]);
            idMap.set(utorid, s);
            s.addAssignment(a[4], a[5])
        }
    }
})
