var PATH = 'ws://localhost:8000/';
var ws;

var active_source = null;

function gid(id){
    return document.getElementById(id);
}

//https://coderwall.com/p/ostduq/escape-html-with-javascript
function escapeHTML(input_str) {
    return input_str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

/*function alive(){
    if(typeof alive.counter === 'undefined')
        alive.counter = 0;
    gid('alive').style.backgroundColor = 'hsla('+alive.counter+', 90%, 60%, 1)';
    alive.counter += 10;
    alive.counter %= 360;
    
}*/

/*function get(path, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if( this.readyState == 4 && this.status == 200 ){
            alive();
            gid('ntwrk').style.backgroundColor = 'green';
            callback(this.responseText);
        }
    };
    gid('ntwrk').style.backgroundColor = 'red';
    xhttp.open('GET', path, true);
    xhttp.send();
    
}*/

function changeSource(e) {
    active_source = e.srcElement.parentElement.getAttribute('id');
    console.log('Switched active source to', active_source);
    fetchImage();
}

function fetchImage() {
    if(active_source) {
        var send = {};
        send[active_source] = {'request':''};
        ws.send(JSON.stringify(send));
    }
}

function setImage(img) {
    var elem = gid('image-display');
    elem.src = 'data:image/' + img.encoding + ';base64, ' + img.data;
}

/*function update(){
    if(source_target == '')
    {
        if(gid('run').checked)
            setTimeout(update, 1000 / FRAMERATE);
        return;
    }
    get(ROOT+source_target, function(resp){
        gid('primary').src = resp;
        if(gid('run').checked)
            setTimeout(update, 1000 / FRAMERATE);
    });
}*/

window.onload = function(){

ws = new WebSocket(PATH);

ws.onopen = function()
{
    console.log("Connected.");
};

ws.onclose = function()
{
    console.log("Closed.");
};

ws.onmessage = function(e)
{
    console.log("Message in:", e.data);
    data = JSON.parse(e.data);
    
    for(const [obj_id, values] of Object.entries(data)) {
        
        var elem = gid(obj_id);
        if(!elem) {
            elem = document.createElement('span');
            elem.setAttribute('id', obj_id);
            elem.classList.add('no-wrap');
            
            var fragment = document.createElement('input');
            fragment.setAttribute('id', obj_id + '_input');
            fragment.setAttribute('name','source_select');
            fragment.setAttribute('type','radio');
            fragment.addEventListener('click', changeSource);
            elem.appendChild(fragment);
            
            var fragment = document.createElement('label');
            fragment.setAttribute('for',obj_id + '_input');
            elem.appendChild(fragment);
            
            gid('selector').appendChild(elem);
        }
        
        
        for(const [attribute, value] of Object.entries(values)) {
            if(attribute == 'name') {
                elem.childNodes[1].innerHTML = escapeHTML(value);
            }
            else if(attribute == 'hidden') {
                if(value)
                    elem.classList.add('hidden');
                else
                    elem.classList.remove('hidden');
            }
            else if(attribute == 'image_event' && value == 'update') {
                if(active_source == obj_id)
                    fetchImage();
            }
            else if(attribute == 'image') {
                setImage(value);
            }
            else {
                console.log("No match attr:", attribute, 'No match value:', value);
            }
        }
    }
    
};

//ws.close()?

/*get(ROOT,buildSelectors);

update();

gid('run').addEventListener('click', function(e){
    if(e.srcElement.checked)
        update();
});

//change: enter, mouse leave arrow
//input: every keystroke, every click
//solution? mouseup + change
gid('a').addEventListener('mouseup', function(e){
    console.log(e.srcElement.value);
});
*/
}