ROOT = 'http://localhost:8000/';
FRAMERATE = 40;

source_target = '';

function gid(id){
    return document.getElementById(id);
}

function alive(){
    if(typeof alive.counter === 'undefined')
        alive.counter = 0;
    gid('alive').style.backgroundColor = 'hsla('+alive.counter+', 90%, 60%, 1)';
    alive.counter += 10;
    alive.counter %= 360;
    
}

function get(path, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if( this.readyState == 4 && this.status == 200 ){
            alive();
            callback(this.responseText);
        }
    };
    xhttp.open('GET', path, true);
    xhttp.send();
    
}

function buildSelectors(selector_string){
    var items = selector_string.split('\n');
    console.log(items);
    var target = gid('selector');
    for(var i = 0; i < items.length; i++) {
        var fragment = document.createElement('input');
        fragment.setAttribute('name','source_select');
        fragment.setAttribute('type','radio');
        fragment.setAttribute('value',items[i]);
        fragment.addEventListener('click', changeSource);
        fragment.setAttribute('id','remote_'+items[i]);
        target.appendChild(fragment);
        var fragment = document.createElement('label');
        fragment.setAttribute('for','remote_'+items[i]);
        fragment.innerHTML = items[i];
        target.appendChild(fragment);
    }
}

function changeSource(e){
    source_target = e.srcElement.getAttribute('value');
    console.log("Swap to:", e.srcElement, source_target);
}

function update(){
    if(source_target == '')
    {
        setTimeout(update, 1000 / FRAMERATE);
        return;
    }
    get(ROOT+source_target, function(resp){
        gid('primary').src = resp;
        setTimeout(update, 1000 / FRAMERATE);
    });
}

window.onload = function(){


get(ROOT,buildSelectors);

update();

}