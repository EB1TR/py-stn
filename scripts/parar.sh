#!/bin/bash
sudo kill -9 $(ps aux | grep '[p]ython3' | awk '{print $2}')
