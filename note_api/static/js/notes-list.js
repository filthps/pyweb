function notes_wall(link, token) {
    function create_load_button() {
        var d = document;
        var button = d.createElement("")
    };
    function content_checker(path, csrf) {
        function parse_content(durty_data) {
            return JSON.parse(durty_data);
        }
        function insert_content(parsed_obj) {
            //
        }
        let loader = new XMLHttpRequest('POST', function(event) {
            insert_content(parse_content(event.data))
        });
        loader.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        let drop_timer;
        let timer_instance = setInterval(function() {
            loader.send(null);
            drop_timer = function() {clearInterval(timer_instance);timer_instance = null;};
            }, 15000);
    }
    content_checker(link, token);
}
