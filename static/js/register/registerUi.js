var _audioData;
var _textData;
var _cur_auidoID = 0;
var _cur_textID = 0;
var _audio_count = 0;
var _text_count = 0;
var _audioArray = new Array();
var _textArray = new Array();

const PreviewImg = document.getElementById("transcript");
var player = document.getElementById("myAudio");

$(document).ready(function(){

    // init UI
    var isStart = false;
    _audioArray.length = 0;
    _textArray.length = 0;
    _cur_audioID = 0;
    _cur_textID = 0;

    function cs_change_audio(new_uri)
    {
        player.pause();
        player.setAttribute('src', new_uri);
        player.load();
        // player.play();
    }

    var hyperaudiolite = (function () {

      var hal = {},
        transcriptId,
        transcript,
        playerId,
        player,
        melarr = [];

      function init() {
        var mels = document.querySelectorAll('[data-m]');
        for (var i = 0; i < mels.length; ++i) {
          var m = parseInt(mels[i].getAttribute('data-m'));
          var p = mels[i].parentNode;
          while (p !== document) {
            if (p.tagName.toLowerCase() === 'p' || p.tagName.toLowerCase() === 'figure' || p.tagName.toLowerCase() === 'ul') {
              break;
            };
            p = p.parentNode;
          };
          melarr[i] = { 'n': mels[i], 'm': m, 'p': p }
        };

        melarr.sort(function(a, b) { return a['m'] - b['m']; });

        for (var i = 0; i < melarr.length; ++i) {
          melarr[i].n.className = "unread";
        };
      };

      function setPlayHead(e) {
        var datam = parseInt(e.target.getAttribute("data-m"));

        if (!isNaN(datam)) {
          //player.currentTime = datam / 1000;
          //player.play();
          play_slice(datam/1000);
        };
      };

      function checkPlayHead(e) {
        // binary search via http://stackoverflow.com/a/14370245
        var l = 0, r = melarr.length - 1;
        while (l <= r) {
          var m = l + ((r - l) >> 1);
          var comp = melarr[m].m / 1000 - player.currentTime;
          if (comp < 0) // arr[m] comes before the element
            l = m + 1;
          else if (comp > 0) // arr[m] comes after the element
            r = m - 1;
          else { // this[m] equals the element
            l = m;
            break;
          };
        };

        for (var i = 0; i < l; ++i) {
          melarr[i].n.className = "read";
        };
        for (var i = l; i < melarr.length; ++i) {
          melarr[i].n.className = "unread";
        };
      };

      hal.init = function(transcriptId, mediaElementId) {
        transcriptId = transcriptId;
        transcript = document.getElementById(transcriptId);
        playerId = mediaElementId;
        player = document.getElementById(playerId);
        init();
        player.addEventListener("timeupdate", checkPlayHead, false);
        transcript.addEventListener("click", setPlayHead, false);
      };

      return hal;

    })();

    var hyperaudiocontrols = (function () {

      var hac = {},
        transcriptId,
        transcript,
        playerId,
        player,
        resetplay,
        resetpause,
        playanimId,
        playanim,
        pauseanimId,
        pauseanim;

      // https://gist.github.com/mrdoob/838785
      if (!window.requestAnimationFrame) {
        window.requestAnimationFrame = (function() {
          return window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame ||
          window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
          function( /* function FrameRequestCallback */ callback, /* DOMElement Element */ element ) {
            window.setTimeout( callback, 1000 / 60 );
          };
        })();
      };

      function togglePlayer(e) {
        if (!isStart)
            return;
        var ui = null;

        if (e.target.getAttribute('data-m') === null && e.target.id !== playerId && e.target.tagName.toLowerCase() !== 'a') {
          if (player.paused) {
            ui = playanim;
            play_slice(0);
          } else {
            ui = pauseanim;
            play_slice(-1);
          };
        } else if (e.target.id !== playerId && e.target.tagName.toLowerCase() !== 'a') {
          ui = playanim;
        };
        if (ui !== null) {
            var pagex = e.pageX;
            var pagey = e.pageY;
            if (pagex === undefined) {
            var rect = canvas.getBoundingClientRect();
              var pagex = e.clientX - rect.left;
              var pagey = e.clientY - rect.top;
            };

            window.requestAnimationFrame(function() {
            ui.className = 'icondiv';
            ui.style.left = pagex + 'px';
            ui.style.top = pagey + 'px';
            ui.style.display = '';
            window.requestAnimationFrame(function() {
              ui.className = 'icondiv icongrow';
              if (ui.id === playanimId) {
                if (resetplay) {
                  clearTimeout(resetplay);
                };
                resetplay = setTimeout(function() {
                  ui.className = 'icondiv';
                  ui.style.display = 'none';
                }, 510);
              };
              if (ui.id === pauseanimId) {
                if (resetpause) {
                  clearTimeout(resetpause);
                };
                resetpause = setTimeout(function() {
                  ui.className = 'icondiv';
                  ui.style.display = 'none';
                }, 510);
              };
            });
            });
        };
      };

      function playCursor() {
        document.documentElement.className = "play";
      };

      function pauseCursor() {
        document.documentElement.className = "pause";
      };

      hac.init = function(transcriptId, mediaElementId, playId, pauseId) {
        transcriptId = transcriptId;
        transcript = document.getElementById(transcriptId);
        playerId = mediaElementId;
        playanimId = playId;
        player = document.getElementById(playerId);
        playanim = document.getElementById(playanimId);
        pauseanimId = pauseId;
        pauseanim = document.getElementById(pauseanimId);
        document.documentElement.addEventListener("click", togglePlayer, false);
        player.addEventListener("canplay", playCursor, false);
        player.addEventListener("pause", playCursor, false);
        player.addEventListener("playing", pauseCursor, false);
      };

      return hac;

    })();


    hyperaudiolite.init("click-text", "myAudio");
    hyperaudiocontrols.init("click-text", "myAudio", "play", "pause");

    function sendBlob(blob) {
        var reader = new FileReader();
        reader.onloadend = function() {
            audio_base64 = reader.result;
            // sendBase64(audio_base64);
            _audioArray.push(audio_base64);
        }
        reader.readAsDataURL(blob);
    }

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

        var reader = new FileReader();
        reader.readAsArrayBuffer(this.files[0]);
        //myAudio.src = e.srcElement.files[0];
        
        reader.onload = function(event) {
            wavbuffer = event.target.result;
            var view = new DataView(wavbuffer);
            var blob = new Blob([view], {type: 'audio/mpeg'});
            sendBlob(blob);
        };
        /*
        for(var i=0; i<_audio_count; i++) {
            var reader = new FileReader();
            reader.onload = function (e) {
                _audioData = e.target.result;
                _audioArray.push(_audioData);
            };
            reader.readAsDataURL(this.files[i]);
        }
        */
    };

    textElem.value = null;
    textElem.onchange = function(e) { // will trigger each time
        if (!this.files) return;

        _text_count = this.files.length;
        _textArray.length = 0;
        _cur_textID = 0;
        for(var i=0; i<_text_count; i++) {
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
        $("#loading").show();

        var lang = $('input[name=language]:checked').val();

        var mode = $('input[name=textfile]:checked').val();
        if (mode == "file") {
            _textData = _textArray.pop()
        } else {
            _textData = PreviewImg.value;
        }

        if (_audio_count == 0 && _text_count == 0) {
            alert("please select audio and text file.");
            return;
        }

        _audioData = _audioArray.pop()
        var jsonObj = {
            mode: mode,
            audio_data: _audioData,
            text_data: _textData,
            language: lang
        }

        $.ajax({
            url: "/get_aeneas_result",
            type: "POST",
            contentType:"application/json; charset=utf-8",
            data: JSON.stringify(jsonObj),
            dataType: "json",
            success: function (response) {
                isStart = true;
                var result = response['alignment'];

                $(".result").hide();

                var i, html='<ul>';
                var tm1, tm2, ttext;
                for(i=0; i<result.length; i++){
                    tm1 = result[i]['time'][0];
                    tm2 = result[i]['time'][1];
                    tm = parseFloat(tm1) * 1000;
                    tm = tm.toString();
                    // ttext = result[i]['sentence'] + "     [" + tm1 + ", " + tm2 + "]";
                    // html += '<li><a href="javascript:;" style="color: white;" onclick="clickEvent(this)">' + ttext + '</a></li>';
                    ttext = result[i]['sentence'];
                    html += ('<span data-m=' + tm + '>' + ttext + ' </span>');
                }
                html += '</ul>';
                $("#click-text").html(html);
                $("#click-text").show();
                // PreviewImg.value = response
                $("#loading").hide();
            },
            error: function (request, response) {
                isStart = false;
                alert("Web server Error. Try again later.");
                return ;
            },
            complete: function(response) {
            }
        });
    });

});


function clickEvent(index) {
    var x = document.createElement("AUDIO");
    x.src = _audioData;

    var text = $(index).text();
    var n1 = text.indexOf("[");
    var n2 = text.indexOf("]");
    var res = text.substring(n1+1, n2);

    var dot_pos = res.indexOf(",");
    var st_tm = res.substring(0, dot_pos);
    var ed_tm = res.substring(dot_pos+2);

    x.currentTime = parseFloat(st_tm);
    x.play();

    x.addEventListener('timeupdate', function (){
        if (x.currentTime >= parseFloat(ed_tm)) {
            x.pause();
        }
    }, false);
}

function play_slice(tm) {
    // var x = document.createElement("AUDIO");
    var x = document.getElementById("myAudio");
    x.src = _audioData;

    if (tm == -1) {
        x.pause();
        return;
    }
    x.currentTime = parseFloat(tm);
    x.play();
}

