var main = {
    init: function () {
        var _this = this;
        $('#btn-result').on("click", function () {
            _this.result();
        })
    },

    result: function () {
        var file = $("#btn-input-file")[0].files;
        // var image =new Blob([file],{type:"image/jpg"})
        // reader.readAsArrayBuffer(file);

        console.log(image)

        var data ={
            url : "test url",
            image: image
        };

        $.ajax({
            type: 'POST',
            url: '/api/face/result',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data)
        }).done(function () {
            alert("데이터 전송 성공")
        }).fail(function (error) {
            alert("데이터 전송 실패: " + JSON.stringify(error))
        });

    },

    input : function (){
        var formData = new FormData();
        var InputFileElement = document.getElementById("input-img");
        formData.append("input-image",InputFileElement.files[0]);
    }


};

main.init();


