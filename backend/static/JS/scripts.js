/*let timer = null;
let xhr = null;


function get_color_for_places(value){
    if (value === 0) return 'places-ended';
    else if (value <= 5) return 'places-few';
    else return 'places-many';
}

function popover_start(elem){
    timer = null;
    let hr = elem.children()[0].href;
    let template = elem.children()[1].innerHTML, content_color = ' class="_">';
    xhr = $.ajax(hr).done(
        function(data) {
            xhr = null;
            content_color = content_color.replace('_',  get_color_for_places(data['value']));
            if (data['closing']) template = template.replace('><!-- put is_closing -->', 'class="invisible">');
            elem.popover({
                trigger: 'manual',
                html: true,
                animation: false,
                container: elem,
                content: template.replace('><!-- put color of places here -->', content_color).replace('<!-- put empty places here -->', data['value'])
            }).popover('show');
        }
    );
}

function popover_clear(){
    let cls = false;
    if (timer) {
        clearTimeout(timer);
        timer = null;
        cls = true;
    }
    if (xhr) {
        xhr.abort();
        xhr = null;
        cls = true;
    }
    return cls;
}

function popover_end(event){
    let elem = $(event.currentTarget);
    if (!popover_clear()) elem.popover('hide');
}

function popovers(){
    $('.event_popup').hover(
        function(event) {
            timer = setTimeout(popover_start, 1000, $(event.currentTarget));
        }, popover_end
    );
    $('.event_popup').click(
        function(event) {
            event.preventDefault();
            popover_start($(event.currentTarget));
        }
    );
    document.addEventListener('click', function(e) {
        popover_clear();
        $('.event_popup').popover('hide');
    });
}

function textInput(document, textarea){
    textarea.style.height = '1px';
    textarea.style.height = (textarea.scrollHeight + 6) + 'px';
}

function listenInput(document){
    let areas = document.getElementsByClassName('textarea');
    for (let textarea of areas){
        textarea.oninput = function(){ textInput(document, textarea); };
        textInput(document, textarea);
    }
}

function clickCard(document, card, year=0){
    if (year) document.location.href = '../' + year + '/' + card + '.html';
    else document.location.href = card + '.html';
}

function convert(str) {
    str = str.replace(/&amp;/g, "&");
    str = str.replace(/&gt;/g, ">");
    str = str.replace(/&lt;/g, "<");
    str = str.replace(/&quot;/g, '"');
    str = str.replace(/&#039;/g, "'");
    return str;
}

function parseMD(document) {
    let mds = document.getElementsByClassName('markdown-popup');
    for(let md of mds) md.innerHTML = convert(md.innerHTML.toString());
}

function markdown_popover(md) {
    let clickedTime = new Date().getTime();
    let elem = $(md);
    if (elem.children().length === 3){
        elem.popover('hide');
        md.lastClickTime = clickedTime;
        return;
    }
    if (typeof md.lastClickTime === "undefined" || clickedTime - md.lastClickTime > 1000){
        md.lastClickTime = clickedTime;
        return;
    }
    md.lastClickTime = clickedTime;
    let data = convert(elem.children()[1].innerHTML.toString());
    elem.popover({
        trigger: 'manual',
        html: true,
        animation: true,
        container: elem,
        content: data
    }).popover('show');
}

function showMD(document) {
    let mds = document.getElementsByClassName('markdown-text');
    for(let md of mds) md.onclick = function(){ markdown_popover(md); };
}

function visit(document, url) {
    document.location.href = url;
}

function choice_color(document, value){
    let elements = document.getElementsByClassName('places-choice');
    let name = get_color_for_places(value);
    for (let elem of elements) elem.className = name;
}*/

function box_click(box){
    let children = box.children();
    let chb = $(children[0]).children()[0];
    if (chb.checked){
        children[1].style.display = 'block';
        children[2].style.display = 'none';
    } else{
        children[1].style.display = 'none';
        children[2].style.display = 'block';
    }
}

function listenCheckbox(document){
    let boxes = document.getElementsByClassName('chekable');
    for(let box of boxes){
        box = $(box);
        $(box.children()[0]).children()[0].onclick = function(){ box_click(box); };
        box_click(box);
    }
}

function listenProducts(document){
    let divs = document.getElementsByClassName('product');
    for(let div of divs){
        div.onmouseover = function() { div.style['box-shadow'] = "0px 8px 16px 0px rgba(0,0,0,0.2)"; document.body.style.cursor = "pointer"; }
        div.onmouseout = function() { div.style['box-shadow'] = ""; document.body.style.cursor = "auto"; }
        div.onclick = function() { document.location.href = '../Products/' + $(div).children()[0].innerHTML + '.html'; }
    }
}


var design_image = {
    file: undefined,
    canvas: undefined, ctx: undefined, image: undefined,
    image_w: 0, image_h: 0, image_scale: 1,
    cx: 0, cy: 0, w: 0, h: 0,
    scale_out: undefined, cx_out: undefined, cy_out: undefined, w_out: undefined, h_out: undefined,
    mouse_down: false,

    clear: function(){
    	this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    },

    set_image: function(img){
        this.image = img;
        this.image_w = img.width;
        this.image_h = img.height;

        if (this.image_scale !== ''){
            this.w = this.image_w * this.image_scale;
            this.h = this.image_h * this.image_scale;
        }

        this.scale_out.value = this.image_scale;
        this.cx_out.value = this.cx;
        this.cy_out.value = this.cy;
        this.w_out.value = this.w;
        this.h_out.value = this.h;
    },

    set_scale: function(scale){
        this.image_scale = scale;
        this.w_out.value = this.w = this.image_w * scale;
        this.h_out.value = this.h = this.image_h * scale;
    },

    check_scale: function(){
        if (design_image.image_w * design_image.h !== design_image.image_h * design_image.w) design_image.image_scale = '';
        else design_image.image_scale = design_image.w / design_image.image_w;
        this.scale_out.value = this.image_scale;
    },

    set_pos: function(e){
        if (this.mouse_down && this.image){
    	    const rect = this.canvas.getBoundingClientRect()
            this.cx_out.value = this.cx = e.clientX - rect.left;
            this.cy_out.value = this.cy = e.clientY - rect.top;
    		this.draw();
    	}
    },

    draw: function(){
        this.clear();
        this.ctx.drawImage(this.image, this.cx - this.w / 2, this.cy - this.h / 2, this.w, this.h);
        this.ctx.beginPath();
        this.ctx.arc(this.cx, this.cy, 2, 0, 2 * Math.PI, false);
        this.ctx.lineWidth = 1;
        this.ctx.strokeStyle = 'black';
        this.ctx.stroke();
    },

    save: function(){
         var formData = new FormData();
         if (this.file) formData.append("file", this.file, 'image.png');
	     else formData.append("empty_file", 1);
	     formData.append("cx", this.cx);
	     formData.append("cy", this.cy);
	     formData.append("w", this.w);
	     formData.append("h", this.h);
	     formData.append("aw", this.canvas.width);
	     formData.append("ah", this.canvas.height);
	     return formData
    }
}

function initCanvas(document){
    design_image.canvas = document.getElementById("canvas");
    const image = document.getElementById("image");
    const upload = document.getElementById("upload_file");
    design_image.scale_out = document.getElementById("scale");
    design_image.cx_out = document.getElementById("left");
    design_image.cy_out = document.getElementById("top");
    design_image.w_out = document.getElementById("width");
    design_image.h_out = document.getElementById("height");
    design_image.ctx = design_image.canvas.getContext("2d");

    design_image.cx = this.canvas.width / 2;
    design_image.cy = this.canvas.height / 2;
    resetCanvas();

	upload.onchange = function(e){
	    var img = new Image();

	    img.onload = function(){
	        design_image.set_image(this);
	        design_image.draw();
	    }

	    img.onerror = function(){
	        alert("Не удалось загрузить изображение. Попробуйте ещё раз.");
	    }

	    img.src = URL.createObjectURL(this.files[0]);
	    design_image.file = this.files[0];
	};

	window.addEventListener("resize", function () { resetCanvas(); });

	design_image.scale_out.addEventListener("change", function () {
	    design_image.set_scale(design_image.scale_out.value);
	    design_image.draw();
	});

	design_image.cx_out.addEventListener("change", function () {
	    design_image.cx = design_image.cx_out.value;
	    design_image.draw();
	});

	design_image.cy_out.addEventListener("change", function () {
	    design_image.cy = design_image.cy_out.value;
	    design_image.draw();
	});

	design_image.w_out.addEventListener("change", function () {
	    design_image.w = design_image.w_out.value;
	    design_image.check_scale();
	    design_image.draw();
	});

	design_image.h_out.addEventListener("change", function () {
	    design_image.h = design_image.h_out.value;
	    design_image.check_scale();
	    design_image.draw();
	});

	design_image.canvas.addEventListener("mousedown", function (e) { design_image.mouse_down = true; design_image.set_pos(e); });
	design_image.canvas.addEventListener("mousemove", function (e) { design_image.set_pos(e); });
	document.addEventListener("mouseup", function (e) { design_image.mouse_down = false; });
}

function resetCanvas(){
	image.width = design_image.canvas.width;
	image.height = design_image.canvas.height;
	design_image.canvas.setAttribute("style", "top: " + image.offsetTop + "px; left: " + image.offsetLeft + "px;");
}


function modal(document){
    $('#modal_element').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var button_type = button.data('whatever');
        var modal = $(this);
        if (button_type === "product"){
            var title = $('#page_content').children()[0].innerHTML;
            var cost = $('h3')[0].innerHTML;
            var body = document.getElementsByClassName('modal-body')[0];
            body.innerHTML = '';

            var srcImage = document.getElementById("image");
            var image = document.createElement("img");
            image.setAttribute("class", srcImage.getAttribute("class"));
            image.setAttribute("src", srcImage.getAttribute("src"));
            image.setAttribute('height', "450px");
            image.setAttribute('width', "450px");

            var srcCanvas = document.getElementById("canvas");
            var canvas = document.createElement("canvas");
            canvas.setAttribute("class", srcCanvas.getAttribute("class"));
            canvas.setAttribute('height', "450px");
            canvas.setAttribute('width', "450px");
            var ctx = canvas.getContext("2d");
            ctx.drawImage(srcCanvas, 0, 0, canvas.width, canvas.height);

            var p = document.createElement("p");
            p.innerHTML = '<br><table><tr><td width="25%"/><td width="50%"/><td width="25%"/></tr><tr><td><h3>' + cost +
            '</h3></td><td><label>Количество: <input type="number" id="count" title="Количество" value="1" min="0"></label></td><td id="sum">Итого: ' + cost + '</td></tr></table>'
            body.appendChild(canvas);
            body.appendChild(image);
            body.appendChild(p);
            image.setAttribute("style", "top: " + canvas.offsetTop + "px; left: " + canvas.offsetLeft + "px;");

            modal.find('.modal-title').text(title);
            modal.find('.btn-secondary').text('Закрыть');
            modal.find('.btn-primary').text('В корзину');

            document.getElementById("count").addEventListener("change", function () {
                if (this.value < 0) this.value = 0;
                let price = cost.substring(0, cost.length - 2) * this.value;
                document.getElementById("sum").innerHTML = 'Итого: ' + price + cost.substring(cost.length - 2);
	        });

	        document.getElementsByClassName("btn-primary")[0].onclick = function(e){
	            let cnt = document.getElementById("count").value;
	            $('#modal_element').modal('hide');
	            var formData = design_image.save();
	            var curURL = window.location.pathname.split('/');
	            curURL = curURL[curURL.length - 1].split('.')[0];
	            formData.append('product', curURL);

	            var xhr = new XMLHttpRequest();
                xhr.open("POST", "../save_design");
                xhr.responseType = 'json';
                xhr.send(formData);

                xhr.onload = function() {
                    if (xhr.status != 200 || xhr.response.id < 0) alert('Не удалось сохранить дизайн, попробуйте ещё раз!');
                    else {
                        var basket = localStorage.getItem('basket');
                        if (basket === null) basket = {}
                        else basket = JSON.parse(basket);
                        basket[xhr.response.id] = cnt;
                        localStorage.setItem('basket', JSON.stringify(basket));
                        let links = document.getElementsByTagName("a");

                        document.getElementsByClassName('modal-body')[0].innerHTML = '';
                        modal.find('.modal-title').text('Товар добавлен');
                        modal.find('.btn-secondary').text('Продолжить покупки');
                        modal.find('.btn-primary').text('Перейти в корзину');
                        document.getElementsByClassName('btn-secondary')[0].onclick = function(){
                            document.getElementsByClassName('btn-secondary')[0].onclick = null;
                            window.location.href = links[links.length - 1].href;
                        };
                        document.getElementsByClassName('btn-primary')[0].onclick = function(){
                            document.getElementsByClassName('btn-primary')[0].onclick = null;
                            window.location.href = '../basket.html';
                        };
                        $('#modal_element').modal('show');
                    }
                };

                xhr.onerror = function() {
                    alert('Не удалось сохранить дизайн, попробуйте ещё раз!');
                };
	        }
        }
    });
}

function add(tr, content){
    let td = document.createElement("td");
    td.innerHTML = content
	tr.appendChild(td);
	return td;
}

function basketPage(document){
    var table = document.getElementsByClassName("table")[0];
    var orderSum = 0;
    var basket = localStorage.getItem('basket');
    if (basket === null) basket = {}
    else basket = JSON.parse(basket);
    var i = 1;
    for (let key in basket) {
        let tr = document.createElement("tr");
        table.appendChild(tr);
        let formData = new FormData();
        formData.append("design", key);
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "get_design");
        xhr.responseType = 'json';
	    xhr.send(formData);

	    add(tr, i++);

	    xhr.onload = function() {
	        add(tr, xhr.response.name);
	        add(tr, '<img width="100px" height="100px" src="design_image?id=' + key + '">');
	        add(tr, xhr.response.cost);
	        let cnt = add(tr, '<input type="number" title="Количество" value="' + basket[key] + '">');
	        let sum = add(tr, basket[key] * xhr.response.cost);
	        cnt.addEventListener("change", function () {
	            orderSum -= +sum.innerHTML;
	            cnt.firstChild.value = Math.max(cnt.firstChild.value, 0);
	            sum.innerHTML = cnt.firstChild.value * xhr.response.cost;
	            orderSum += +sum.innerHTML;
	            document.getElementById('order-sum').innerHTML = 'Итого: ' + orderSum + ' &#8381;'
	        });
	        orderSum += +sum.innerHTML;
	        document.getElementById('order-sum').innerHTML = 'Итого: ' + orderSum + ' &#8381;'
	    };
    }
    var orderButton = document.getElementById("order-button");
    orderButton.onclick = function(){
        var table = $(document.getElementsByClassName("table")[0]);
        var child = table.children();
        var info = [];
        for (var i = 1; i < child.length; ++i){
            let row = $(child[i]).children();
            let img = $(row[2]).children()[0].src.split('=')[1];
            let cnt = $(row[4]).children()[0].value;
            info.push(img + '=' + cnt);
        }
        info = info.join('=');
        console.log(info);

        let formData = new FormData();
        formData.append("info", info);
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "add_order");
        xhr.responseType = 'json';
	    xhr.send(formData);

	    xhr.onload = function() {
	        if (xhr.status != 200){
	            alert('Не удалось сохранить заказ, попробуйте ещё раз!');
	            return;
	        }

	        localStorage.setItem('basket', JSON.stringify({}));

	        var modal = $(document.getElementById('modal_element'));
	        document.getElementsByClassName('modal-body')[0].innerHTML =
	            '<p>Запомните номер Вашего заказа: ' + xhr.response.id + ', он понадобится, когда вы будете забирать Ваши товары.</p>' +
	            '<p>Чтобы оплатить перейдите по <a target="_blank" href="' + xhr.response.url + '">ссылке</a>.</p>';
            modal.find('.modal-title').text('Заказ сохранён');
            modal.find('.btn-secondary').text('Закрыть');
            modal.find('.btn-primary').text('Открыть ссылку');
            document.getElementsByClassName('btn-secondary')[0].onclick = function(){
                document.getElementsByClassName('btn-secondary')[0].onclick = null;
                document.getElementsByClassName('btn-primary')[0].onclick = null;
            };
            document.getElementsByClassName('btn-primary')[0].onclick = function(){
                document.getElementsByClassName('btn-secondary')[0].onclick = null;
                document.getElementsByClassName('btn-primary')[0].onclick = null;
                window.open(xhr.response.url, '_blank').focus();
            };
            $('#modal_element').modal('show');
	    }

        xhr.onerror = function() {
            alert('Не удалось сохранить заказ, попробуйте ещё раз!');
        };
    };
}
