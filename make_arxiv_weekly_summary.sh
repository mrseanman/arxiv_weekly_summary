#!/bin/bash

# Takes in a filter file with an email at the top. Makes the relevant weekly update, then sends that email the weekly update

construct_summary_and_send_email() {
  store_dir="/home/sean/google_drive/arxiv_summaries_per_email/"
  read -r send_email < "$1"
  echo "sending update email to $send_email"

  specific_email_store_dir="$store_dir$send_email"
  echo "storing update html in $specific_email_store_dir"

  if [[ ! -d $specific_email_store_dir ]]
  then
      mkdir "$specific_email_store_dir"
      echo "made directory $specific_email_store_dir"
  fi

  update_html=$(/home/sean/.local/arxiv_weekly_summary/env/bin/python3 /home/sean/.local/arxiv_weekly_summary/src/main.py t t $1 $specific_email_store_dir)
  echo "generated file $update_html"

  if [[ -n $update_html ]]
  then
    mutt -e 'set content_type=text/html' -s 'Weekly Arxiv Update' $send_email < $update_html
    echo "sent email containing $update_html to $send_email"
  fi
}

filter_dir="/home/sean/google_drive/arxiv_summaries_per_email/filters/"

for filter_file in "$filter_dir"*
do
  if [[ -f $filter_file && -s $filter_file ]]
  then
    echo "-------------------------------------"
    echo "collected filter file $filter_file"
    construct_summary_and_send_email "$filter_file"
  fi
done

