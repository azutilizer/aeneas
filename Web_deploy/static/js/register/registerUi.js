var _data = []

const PreviewImg = document.getElementById("alignResult");


$(document).ready(function(){
    var _audioData;
    var _textData;
    var _cur_auidoID = 0;
    var _cur_textID = 0;
    var _audio_count = 0;
    var _text_count = 0;
    var _audioArray = new Array();
    var _textArray = new Array();

    var _bChooseUploadFiles = false,
        _bUploaded = true;

    // init UI
    _audioArray.length = 0;
    _textArray.length = 0;
    _cur_audioID = 0;
    _cur_textID = 0;

    var audioElem = document.getElementById("Add-Audio");
    var audioSelected = null;
    audioElem.onclick = function(e) {
        audioSelected = this.value;
        this.value = null;
    }

    var textElem = document.getElementById("Add-Text");
    var textSelected = null;
    textElem.onclick = function(e) {
        textSelected = this.value;
        this.value = null;
    }

    audioElem.value = null;
    audioElem.onchange = function(e) { // will trigger each time
        PreviewImg.value = "";
        if (!this.files) return;

        _audio_count = this.files.length;
        _audioArray.length = 0;
        _cur_audioID = 0;
        var upload_status = true;
        for(var i=0; i<_audio_count && upload_status; i++) {
            var reader = new FileReader();
            reader.onload = function (e) {
                _audioData = e.target.result;
                _audioArray.push(_audioData);                
            };
            reader.readAsDataURL(this.files[i]);
        }
    };

    textElem.value = null;
    textElem.onchange = function(e) { // will trigger each time
        if (!this.files) return;

        _text_count = this.files.length;
        _textArray.length = 0;
        _cur_textID = 0;
        var upload_status = true;
        for(var i=0; i<_text_count && upload_status; i++) {
            var reader = new FileReader();
            reader.onload = function (e) {
                _textData = e.target.result;
                _textArray.push(_textData);
            };
            reader.readAsDataURL(this.files[i]);
        }
    };

    function handleFileDialog(changed) {
        // boolean parameter if the value has changed (new select) or not (canceled)

    }

    $(".submit-btn").click(function (e) {
        if (_audio_count == 0 && _text_count == 0) {
            alert("please select audio and text file.");
            return;
        }

        _audioData = _audioArray.pop()
        _textData = _textArray.pop()

        $.ajax({
            url: "/register/upload",
            type: "POST",
            data: {
                audio_data: _audioData,
                text_data: _textData
            },
            success: function (response) {
                PreviewImg.value = response
            },
            error: function (request, response) {
                if (upload_status == true)
                    alert("Web server Error. Try again later.");
                upload_status = false;
                return ;
            },
            complete: function(response) {
            }
        });
            

        if(_audioArray.length === _audio_count) {
            PreviewImg.src = _audioArray[0];
            _bChooseUploadFiles = true;
            _bUploaded = false;
        }
    });

});
