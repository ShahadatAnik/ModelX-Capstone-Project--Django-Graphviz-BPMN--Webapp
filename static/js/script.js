function saveSvg(svgEl, name) {
    svgEl.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    var svgData = svgEl.outerHTML;
    var preface = '<?xml version="1.0" standalone="no"?>\r\n';
    var svgBlob = new Blob([preface, svgData], {type:"image/svg+xml;charset=utf-8"});
    var svgUrl = URL.createObjectURL(svgBlob);
    var downloadLink = document.createElement("a");
    downloadLink.href = svgUrl;
    downloadLink.download = name;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}


function downloadFiles(data, file_name, file_type) {

    var file = new Blob([data], {type: file_type});
    if (window.navigator.msSaveOrOpenBlob)
        window.navigator.msSaveOrOpenBlob(file, file_name);
    else {
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = file_name;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}



$("#extractFeaturesBtn").click(function(){
    // here goes some variable
    console.log("extractFeaturesBtn clicked");
    var userText = $("#userText").val();
    console.log("this is user Text: ");
    console.log(userText);
    if(userText == ""){
        alert("Please enter some text");
    }
    else{
        ajaxData={userText:userText};
        $.ajax({
            url: "{% url 'keywordExtractorFunc' %}",
            method: "POST",
            data:ajaxData,
            success: function(data){
                console.log("The table writing is still left");
                if(data.status=="extracted"){
                    console.log(data.features)
                }
            }
        });
    }

});

