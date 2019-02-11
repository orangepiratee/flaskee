
var xmlhttp;
function loadXMLDoc(url,cfunc) {
    if (window.XMLHttpRequest){
        // IE7, FIREFOX, CHROME, OPERA, SAFARI
        xmlhttp = new XMLHttpRequest();
    }else{
        //IE5, IE6
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
    }
    xmlhttp.onreadystatechange = cfunc;
    xmlhttp.open('GET', url, true);
    xmlhttp.send();
}

function countUnRead() {
    loadXMLDoc('/count/unread',function () {
        if (xmlhttp.readyState ==4 && xmlhttp.status == 200){
            document.getElementById('num_tips').innerHTML = xmlhttp.responseText;
        }
    });

}

