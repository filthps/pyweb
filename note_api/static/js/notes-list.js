function notes_wall(link, token) {
    let path = document.location + link + '/';
    let time = 0;
    let page = 0;
    let drop_timer;
    function check_cur_url() {
        function get_last_symbol(str) {
            return str.slice(str.length - 2, -1);
        }
        let url = document.location.pathname;
        let last_symbol = get_last_symbol(url);
        last_symbol = last_symbol === "/" ? get_last_symbol() : last_symbol;
        if (!isNaN(last_symbol)) {
            window.location.pathname = url.slice(0, url.indexOf(last_symbol));
        }
    }
    function xhr_request(path, data, callback, token) {
        let loader = new XMLHttpRequest();
        loader.open('POST', path, true);
        loader.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        loader.setRequestHeader('X-CSRFToken', token);
        loader.onload = function (event) {
            if (loader.readyState === 4 && loader.status === 200) {
                callback(loader.response);
            }
        }
        loader.send(data ? JSON.stringify(data) : null);
    }
    load_button = function() {
        let d = document;
        let button = d.createElement("button");
    }
    function parse_content(durty_data) {
            return JSON.parse(durty_data);
        }
    function insert_content(parsed_obj) {
        //
    }
    function content_checker(path, csrf) {
        function body(data) {
            insert_content(parse_content(data));
        }
        let timer_instance = setInterval(function() {
            xhr_request(path, null, body, csrf);
            drop_timer = function() {clearInterval(timer_instance);timer_instance = null;};
            }, 15000);
        xhr_request(path, null, body, csrf);
    }
    check_cur_url(); // Если текущий url кончается числом
    // и исключений на фронте к этому моменту не возникло, то перенаправляемся на
    // спецально обученный url, где предусмотрена работа в режиме ajax
    content_checker(path, token);
}
init_();
