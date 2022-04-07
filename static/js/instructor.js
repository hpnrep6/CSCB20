let instr = document.getElementById('instr')

fetch('/api/utorid').then( (res) => {
    return res.json();
}).then((res) => {
    instr.value = res.UtorID;
}).catch((e)=> {
    console.log(e)
})