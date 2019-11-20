rem bin\x64\release\mp4client.exe -h
rem bin\x64\release\mp4client.exe -run-for 120 -exit -c GPAC.cfg -logs all@error:dash@debug -log-file dash.log "http://127.0.0.1/dash/dash.mpd"
bin\x64\release\mp4client.exe -run-for 120 -exit -c GPAC.cfg -logs all@error:dash@debug -log-file dash.log "http://172.17.217.51/dash/dash.mpd"
