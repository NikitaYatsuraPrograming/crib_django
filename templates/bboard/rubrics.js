let domain = 'http://127.0.0.1:8000/bboard/api/rubrics';

window.onload = function () {
    let list = document.getElementById('list');

    let rubricsListLoader = new XMLHttpRequest()
    rubricsListLoader.onreadystatechange = function () {
        if (rubricsListLoader.readyState === 4){
            if (rubricsListLoader.status === 200){
                let data = JSON.parse(rubricsListLoader.responseText);
                let s = '<ul>';
                for (let i = 0; i < data.length; i++){
                    s += '<li>' + data.length + '</li>';
                }
                s += '</ul>';
                list.innerHTML = s;
            }
        }
    }
    
    function rubricListLoad() {
        rubricsListLoader.open('GET', domain, true);
        // console.log(domain + 'api/rubrics', true);
        rubricsListLoader.send();
    }

    rubricListLoad();

};