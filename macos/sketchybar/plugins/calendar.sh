#!/bin/bash

sketchybar --set $NAME icon="$(LANG=ko_KR.UTF-8 date '+%-m월 %-d일 %a')" label="$(date '+%H:%M:%S')"
