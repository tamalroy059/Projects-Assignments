
'use strict'

const AWS = require('aws-sdk');

new AWS.Config({
	secret_access_key: "QN2cT5ZIMKpxex742dvPFkUi9B8uKicCIMMMSuzi",
	access_key_id: "AKIAIWIKL4SPIWBDWSQA",
	region: "us-east-1"
});

const LAMBDA = new AWS.Lambda();
const SQS = new AWS.SQS();


function hello (event, context, callback) {



	var sqs_queue_url='https://sqs.'+process.env.region+'.amazonaws.com/822605674378/'+process.env.sqs;


	// let param_scrape = {
	// 	FunctionName: process.env.scrape,
	// 	InvocationType: 'Event',
	// 	LogType: 'None'
	// };
	// for(let i = 0; i <= 3; i++){
	// 	LAMBDA.invoke(param_scrape, function(){
	// 		console.log('started scrape function')
	// 	});
	// };



  let params = {
		FunctionName: process.env.process,
		InvocationType: 'Event',
		LogType: 'None'
	};

	for(let i = 0; i <= 0; i++){

		LAMBDA.invoke(params, function(){
			console.log('started', i)
		});

	};



}

module.exports = {hello }
