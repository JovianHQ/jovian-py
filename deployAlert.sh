#!/bin/bash
if [ ! -z $SLACK_DEPLOYMENT_HOOK_URL ]
then
  curl -X POST -H 'Content-type: application/json' --data "{
    'text': 'Deploying Library [${1}] [VERSION: ${2}]!:male-technologist:',
    'blocks':[
    {
      'type': 'section',
      'text': {
        'type': 'mrkdwn',
        'text': 'Deploying Library [${1}] [VERSION: ${2}]!:male-technologist:',
      }
    }
  ]}" $SLACK_DEPLOYMENT_HOOK_URL
else
  echo 'SLACK_DEPLOYMENT_HOOK_URL not found'
fi