#!/bin/bash

# check command line argument for the script and assign a default value if not given
if [ -z $1 ]; then
	test_target="anand-tandon.duckdns.org"
else
	test_target="$1"
fi

echo -e "Testing target $test_target\n"

# generate random strings for each field. shouldn't affect functionality but specified from LMS
rand_name=$(tr -dc A-Za-z </dev/urandom | head -c 13 ; echo '')
rand_email="$(tr -dc A-Za-z </dev/urandom | head -c 13 ; echo '')@gmail.com"
rand_content=$(tr -dc A-Za-z </dev/urandom | head -c 30 ; echo '')

# make a POST request to our timeline API with the randomly generated form data, retrieving only the timeline post's ID
post_id=$(curl -s -X POST $test_target/api/timeline_post -d "name=$rand_name&email=$rand_email&content=$rand_content" | jq '.id')

# make a GET request to the timeline API and get the most recent timeline post (this should be the same test post, unless a POST request sneaked in before)
get_latest=$(curl -s -X GET $test_target/api/timeline_post | jq '.[][0]')

# save the timeline post's fields to variables for usability
get_name=$(echo "$get_latest" | jq -r '.name')
get_email=$(echo "$get_latest" | jq -r '.email')
get_content=$(echo "$get_latest" | jq -r '.content')
get_id=$(echo "$get_latest" | jq '.id')

# visual comparison
echo -e "Name:\n\tGET=$get_name\n\tRAND=$rand_name"
echo -e "Email:\n\tGET=$get_email\n\tRAND=$rand_email"
echo -e "Content:\n\tGET=$get_content\n\tRAND=$rand_content"
echo -e "ID:\n\tGET=$get_id\n\tPOST_RESPONSE=$post_id"

# evaluating comparison
if [[ $get_name == $rand_name && $get_email == $rand_email && $get_content == $rand_content && $get_id -eq $post_id ]]; then
	echo -e '\nThe test timeline post was successfully added'

	# delete timeline post
	delete_response=$(curl -s -X DELETE $test_target/api/timeline_post?id=$post_id | jq -r '.message')
	expected_response="Timeline post $post_id deleted successfully"
	if [[ $delete_response == $expected_response ]]; then		# should have used a second numeric code for confirmation instead of just the response message
		echo -e '\nThe test timeline post was successfully removed for test cleanup'
	else
		echo -e '\nThe test timeline post failed to remove successfully for test cleanup'
	fi
else
	echo -e '\nThe test timeline post failed to add successfully'
fi

