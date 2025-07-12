#!/bin/bash

rand_name=$(tr -dc A-Za-z </dev/urandom | head -c 13 ; echo '')
rand_email="$(tr -dc A-Za-z </dev/urandom | head -c 13 ; echo '')@gmail.com"
rand_content=$(tr -dc A-Za-z </dev/urandom | head -c 30 ; echo '')

post_id=$(curl -s -X POST 127.0.0.1:5000/api/timeline_post -d "name=$rand_name&email=$rand_email&content=$rand_content" | jq '.id')

get_latest=$(curl -s -X GET 127.0.0.1:5000/api/timeline_post | jq '.[][0]')

get_name=$(echo "$get_latest" | jq -r '.name')
get_email=$(echo "$get_latest" | jq -r '.email')
get_content=$(echo "$get_latest" | jq -r '.content')
get_id=$(echo "$get_latest" | jq '.id')

echo -e "Name:\n\tGET=$get_name\n\tRAND=$rand_name"
echo -e "Email:\n\tGET=$get_email\n\tRAND=$rand_email"
echo -e "Content:\n\tGET=$get_content\n\tRAND=$rand_content"
echo -e "ID:\n\tGET=$get_id\n\tPOST_RESPONSE=$post_id"

if [[ $get_name == $rand_name && $get_email == $rand_email && $get_content == $rand_content && $get_id -eq $post_id ]]; then
	echo -e '\nThe test timeline post was successfully added'

	delete_response=$(curl -s -X DELETE 127.0.0.1:5000/api/timeline_post?id=$post_id | jq -r '.message')
	expected_response="Timeline post $post_id deleted successfully"
	if [[ $delete_response == $expected_response ]]; then
		echo -e '\nThe test timeline post was successfully removed for test cleanup'
	else
		echo -e '\nThe test timeline post failed to remove successfully for test cleanup'
	fi
else
	echo -e '\nThe test timeline post failed to add successfully'
fi

