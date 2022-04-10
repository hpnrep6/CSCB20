let content = []
content.push(document.getElementById('feedback-content0'));
content.push(document.getElementById('feedback-content1'));
content.push(document.getElementById('feedback-content2'));
content.push(document.getElementById('feedback-content3'));

let instructor_name = '';

fetch('/api/instructor').then((res) => {
    return res.json();
}).then( (res) => {
    instructor_name = res;
    document.getElementById('feedback-instructor').innerHTML = 'Your instructor: ' + 
    instructor_name[1] + ' ' + instructor_name[2] + ' ' + instructor_name[3];

});

function submitFeedback(e) {
    let form = new FormData();

    let text = '';
    text += 'What did you like about your instructor\'s teaching?\n\n';
    text += content[0].value;
    text += '\n\nHow could your instructor improve their teaching?\n\n';
    text += content[1].value;
    text += '\n\nWhat did you like about the labs?\n\n';
    text += content[2].value;
    text += '\n\nWhat do you recommend the lab instructors do to improve?\n\n';
    text += content[3].value;
    form.append('Content', text);
    form.append('Instructor', instructor_name[0])

    let req = new XMLHttpRequest();
    req.open('POST', '/api/feedback');
    req.send(form);
    
    for (i in content) {
        content[i].value = '';
    }
    e.innerHTML = 'Feedback Submitted!'
}