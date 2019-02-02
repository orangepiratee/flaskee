
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
    loadXMLDoc('/item/count_un_read',function () {
        if (xmlhttp.readyState ==4 && xmlhttp.status == 200){
            document.getElementById('unRead').innerHTML = xmlhttp.responseText;
        }
    });
}