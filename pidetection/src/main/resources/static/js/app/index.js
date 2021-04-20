var main = {
    init: function () {
        var _this = this;
        $('#btn-result').on("click", function () {
            _this.result();
        });

        $('#btn-upload').on("click",function(){
            _this.upload()
        });
    },


    result: function () {
        var file = $("#btn-input-file")[0].files;
        // var image =new Blob([file],{type:"image/jpg"})
        // reader.readAsArrayBuffer(file);


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

    upload : function (){
        var formData = new FormData();
        var InputFileElement = document.getElementById("input-file");
        formData.append("input-file",InputFileElement.files[0]);
        console.log(InputFileElement.files[0]);
        console.log(formData);

        $.ajax({
            type:'POST',
            url:'/api/detection/input',
            dataType: false,
            processData: false,
            data:formData

        }).done(function(){
            alert("파일 업로드 완료.");
            window.location.href="wait-page";
        }).fail(function(error){
            alert("파일 업로드 실패: "+JSON.stringify(error));
        })
    }


};

main.init();


