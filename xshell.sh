#!/bin/bash

# 请求参数
login_url="http://login.ssss.com"
login_proxy="http://proxy.com"
login_client_id="bb82"
login_client_secret="spvs"
login_scope="api://dsad/.default"
login_grant_type="client"

esc_url="http://esc.com"
esc_client_id="bb82"
esc_client_secret="spvs"
esc_scope="api://dsad/.default"
esc_grant_type="client"

# 获取access_token
response=$(curl -x "$login_proxy" -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=$login_client_id&client_secret=$login_client_secret&scope=$login_scope&grant_type=$login_grant_type" "$login_url")
access_token=$(echo "$response" | jq -r '.access_token')

# 发送第二个请求
curl -X POST -H "Authorization: Bearer $access_token" -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=$esc_client_id&client_secret=$esc_client_secret&scope=$esc_scope&grant_type=$esc_grant_type" "$esc_url" > 1.txt
