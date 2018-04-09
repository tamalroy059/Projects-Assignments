#!/bin/bash

current_date_time="`date +%Y%m%d%H%M%S`";
python /home/zhengdao/cronjob/facebook_insights/facebook_insights/run_facebook_adset_insights.py &> /home/zhengdao/cronjob/facebook_insights/facebook_insights/output/facebook_adset_insights_log_$current_date_time.log
