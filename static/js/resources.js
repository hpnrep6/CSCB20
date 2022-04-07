let content = document.getElementById('feedback-content')
let instructor_name = '';

fetch('/api/instructor').then((res) => {
    return res.json();
}).then( (res) => {
    instructor_name = res;
    document.getElementById('feedback-instructor').innerHTML = 'Your instructor: ' + 
    instructor_name[1] + ' ' + instructor_name[2] + ' ' + instructor_name[3];
})

function submitFeedback() {
    let form = new FormData();
    form.append('Content', content.value);
    form.append('Instructor', instructor_name[0])

    let req = new XMLHttpRequest();
    req.open('POST', '/api/feedback');
    req.send(form);
    
    content.value = '';
}