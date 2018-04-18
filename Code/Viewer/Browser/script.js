var PATH = 'ws://localhost:8000/';
var ws;

var EVENT_LUT  = {
    'number' : 'change',
    'text' : 'change',
    'checkbox' : 'change',
    'button' : 'click',
};

var active_source = null;
var last_img_update = new Date().getTime();
var MIN_AGE_DIFF = 50; //ms, 50 -> 20 fps

function gid(id){
    return document.getElementById(id);
}

//https://coderwall.com/p/ostduq/escape-html-with-javascript
function escapeHTML(input_str) {
    return input_str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}



function status_good(elem_id) {
    gid(elem_id).classList.add('good');
}
function status_reset(elem_id) {
    gid(elem_id).classList.remove('good');
}

function status_msg_in() {
    clearTimeout(status_msg_in.timeout);
    status_good('msg_in');
    status_msg_in.timeout = setTimeout(
      function(){status_reset('msg_in');}, 75);
}
function status_msg_out() {
    clearTimeout(status_msg_out.timeout);    
    status_good('msg_out');
    status_msg_out.timeout = setTimeout(
      function(){status_reset('msg_out');}, 75);
}
function status_img() {
    clearTimeout(status_img.timeout);    
    status_good('image_update');
    status_img.timeout = setTimeout(
      function(){status_reset('image_update');}, 75);
}



function changeSource(e) {
    active_source = e.srcElement.parentElement.getAttribute('id');
    console.log('Switched active source to', active_source);
    fetchImage();
}

function fetchImage() {
    if(new Date().getTime() - last_img_update < MIN_AGE_DIFF)
        return;
    last_img_update = new Date().getTime();
    //clearTimeout(fetchImage.timeout);
    //fetchImage.timeout = setTimeout(fetchImage, MIN_AGE_DIFF + 10);
    if(active_source) {
        var send = {};
        send[active_source] = {'request':''};
        status_msg_out();
        ws.send(JSON.stringify(send));
    }
}

function setImage(img) {
    var elem = gid('image-display');
    status_img();
    elem.src = 'data:image/' + img.encoding + ';base64, ' + img.data;
}



function changeParameter(e) {
    console.log('parameter update:', e.srcElement);
    var input = e.srcElement;
    var wrapper = input.parentElement;
    var send = {};
    send[wrapper.getAttribute('id')] = {'input_value' : getValue(input)};
    status_msg_out();
    ws.send(JSON.stringify(send));
}

function getValue(elem) {
    if(elem.tagName != 'INPUT')
        console.log('Trying to get value of a non-input tag!');
    var type = elem.getAttribute('type');
    if(type == null)
        console.log('Type not found when getting value!');
    if(type == 'checkbox')
        return elem.checked;
    return elem.value;
}

function setValue(elem, val) {
    if(elem.tagName != 'INPUT')
        console.log('Trying to set value of a non-input tag!');
    var type = elem.getAttribute('type');
    if(type == null)
        console.log('Type not found when setting value!');
    if(type == 'checkbox')
        elem.checked = val;
    else
        elem.value = val;
    
}



window.onload = function(){

gid('show-hidden').addEventListener('change', function(){
    var style = gid('js-style').sheet;
    if(this.checked)
        style.insertRule('.hidden {display:inline}');
    else
        style.deleteRule(0);
});

ws = new WebSocket(PATH);

ws.onopen = function()
{
    console.log("Connected.");
    status_good('connected');
};

ws.onclose = function()
{
    console.log("Closed.");
    status_reset('connected');
};

ws.onmessage = function(e)
{
    //console.log("Message in:", e.data);
    status_msg_in();
    data = JSON.parse(e.data);
    
    for(const [obj_id, values] of Object.entries(data)) {
        
        var elem = gid(obj_id);
        if(!elem) {
            var elem = document.createElement('span');
            elem.setAttribute('id', obj_id);
            elem.classList.add('no-wrap');
            
            var frag_input = document.createElement('input');
            frag_input.setAttribute('id', obj_id + '_input');
            var frag_label = document.createElement('label');
            frag_label.setAttribute('for',obj_id + '_input');
            
            elem.appendChild(frag_input);
            elem.appendChild(frag_label);
            
            if( values === 'view') {
                frag_input.setAttribute('name','source_select');
                frag_input.setAttribute('type','radio');
                frag_input.addEventListener('click', changeSource);
                
                gid('selector').appendChild(elem);
            }
            else if( values === 'parameter') {
                gid('parameters').appendChild(elem);
            }
            else {
                console.log('Message recieved for non-existant object!');
                return;
            }
        }
        
        else {
            
            var wrapper = elem;
            var input = elem.childNodes[0];
            var label = elem.childNodes[1];
            
            for(const [attribute, value] of Object.entries(values)) {
                if(attribute == 'name') {
                    label.innerHTML = escapeHTML(value);
                }
                else if(attribute == 'hidden') {
                    if(value)
                        wrapper.classList.add('hidden');
                    else
                        wrapper.classList.remove('hidden');
                }
                else if(attribute == 'image_event' && value == 'update') {
                    if(active_source == obj_id)
                        fetchImage();
                }
                else if(attribute == 'image') {
                    setImage(value);
                }
                else if(attribute == 'input_type') {
                    input.setAttribute('type', value);
                    if(value in EVENT_LUT)
                        //DANGER! If type is changed or called again, listeners will stack!
                        input.addEventListener(EVENT_LUT[value], changeParameter);
                    else {
                        console.log('Unknown input_type of', value, '. Defaulting to \'click\'.');
                        input.addEventListener('click', changeParameter);
                    }
                }
                else if(attribute == 'input_value') {
                    setValue(input, value);
                }
                else if(attribute == 'editable') {
                    input.readOnly = !value;
                    if(value)
                        input.removeAttribute('disabled');
                    else
                        input.setAttribute('disabled', 'disabled');
                }
                else {
                    console.log("No match attr:", attribute, 'No match value:', value);
                }
            }
        }
    }
    
};

}
