const express = require('express');
const path = require('path');
const app = express();
const fetch = require('node-fetch');
const NodeCache = require('node-cache');	

const myCache = new NodeCache({ stdTTL: 900 });
const cron = require("node-cron");

cron.schedule("59 * * * *", function () {
  console.log("---------------------");
  const res = fetch('http://localhost:8888/api/TME');
  console.log("running a task every 5 minutes");
});


async function child(childparent, data)
{
	arrchild2 = [];
	const keys2 = Object.keys(data)
	
	console.log('---- TEMAS ...........')
   
	//var arrchild = [];
	for (let j=0; j<keys2.length;j++){   // issuelinks do TEMA
		//console.log('issuelink: ' + data[j]['self']);
		//console.log(data['issues'][i]['fields']['issuelinks'][j]);
		const res2 = await fetch(data[j]['self'], {
			headers: {
			  'Accept': 'application/json',
			  'Authorization': 'Bearer NDQ5NjQ4Njc3MjQ0OpEHco38qMrnJPHxptq4hjdzRrxr'		  
					 }
		})
		const data2 = await res2.json();//assuming data is json
	
		arrchild3 = [];
		arr=[];
		arr1=[] ;
		console.log(childparent, data2['outwardIssue']['key']  )
		if (childparent == data2['outwardIssue']['key'] ) {
		  
			try{

			//console.log(data[j]['inwardIssue']['fields']['issuetype']['name']);
			if (data[j]['inwardIssue']['fields']['issuetype']['name'] == 'Epic')
				{
					
				const res3 = await fetch('https://jira.k8s2.grupocgd.com/rest/api/2/search?jql=%22Epic%20Link%22%20%20%3D%20' + data2['inwardIssue']['key'], {
					headers: {
					'Accept': 'application/json',
					'Authorization': 'Bearer NDQ5NjQ4Njc3MjQ0OpEHco38qMrnJPHxptq4hjdzRrxr'		  
							}
				})
					console.log('--- epic --- ' + data2['inwardIssue']['key']);
					const data3 = await res3.json();//assuming data is json
					const keys3 = Object.keys(data3['issues'])
					
					for (let v=0; v<keys3.length;v++){ 
						//console.log('--- issue XXX --- ' + data3['issues'][z]['key'] + ' ' + data3['issues'][z]['self']);
							console.log('--- issue XXX --- ' + data3['issues'][v]['key'] + ' ' +  data3['issues'][v]['fields']['summary'].slice(0, 50)) //+ data3['issues'][v]['self']);
								//console.log(data3['issues'][v]['fields']);
							arr1.push({name: data3['issues'][v]['fields']['summary'].slice(0, 100), text: data3['issues'][v]['fields']['summary'].slice(0, 100), data: { status: data3['issues'][v]['fields']['status']['name'] , priority: data3['issues'][v]['fields']['priority']['name'],  key: "3.1 " + data3['issues'][v]['key']},a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data3['issues'][v]['key'] }, icon: data3['issues'][v]['fields']['issuetype']['iconUrl']  } );
					}
				}
			
			
						
		  
			
		  const res4 = await fetch(data[j]['inwardIssue']['self'], {
				headers: {
				  'Accept': 'application/json',
				  'Authorization': 'Bearer NDQ5NjQ4Njc3MjQ0OpEHco38qMrnJPHxptq4hjdzRrxr'				  
						 }
			  })
			  //console.log('--- data3 ---');
		  const data4 = await res4.json();//assuming data is json
		  const keys4 = Object.keys(data4['fields']['issuelinks'])
		  
		  for (let z=0; z < keys4.length;z++){ 
			  
			  try{
				  
				  a=data4['fields']['issuelinks'][z]['outwardIssue']['fields']['summary']
				  //arrchild3.push({text: data4['fields']['issuelinks'][z]['outwardIssue']['fields']['summary'].slice(0, 100), data: { status: data4['fields']['issuelinks'][z]['outwardIssue']['fields']['status']['name'] , priority: data4['fields']['issuelinks'][z]['outwardIssue']['fields']['priority']['name'],  key: "3.1 " + data4['fields']['issuelinks'][z]['outwardIssue']['key']},a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data4['fields']['issuelinks'][z]['outwardIssue']['key'] }, icon: data4['fields']['issuelinks'][z]['outwardIssue']['fields']['issuetype']['iconUrl']  } );
				  
			  }catch
			  {
				  console.log('--- issue YYY --- ' + data4['fields']['issuelinks'][z]['inwardIssue']['key']);
				  
				  
				  //arr = await child2( data[j]['inwardIssue']['key'], data4['fields']['issuelinks'][z]['inwardIssue']['key'], data4['fields']['issuelinks'][z]['inwardIssue']['self'])
					  
					  // children: arr,
					  
					  
				  // segundo nivel de epicos	
				  if (data4['fields']['issuelinks'][z]['inwardIssue']['fields']['issuetype']['name'] == 'Epic') 
				  {
					  
					  
					  console.log('EPICO......'+data4['fields']['issuelinks'][z]['inwardIssue']['key']);
					  
					  // ----------------------------------------------------- epiclink  nivel 2    
						  const res3 = await fetch('https://jira.k8s2.grupocgd.com/rest/api/2/search?jql=%22Epic%20Link%22%20%20%3D%20' + data4['fields']['issuelinks'][z]['inwardIssue']['key'], {
						  headers: {
							  'Accept': 'application/json',
							  'Authorization': 'Bearer NDQ5NjQ4Njc3MjQ0OpEHco38qMrnJPHxptq4hjdzRrxr'		  
								  }
						  })
						  console.log('--- epic --- ' + data2['inwardIssue']['key']);
						  const data3 = await res3.json();//assuming data is json
						  //console.log(data3)
						  //console.log(data2['inwardIssue']['key'], data3['issues'][j]['fields']['issuelinks'])
						  
						  const keys3 = Object.keys(data3['issues'])
						  console.log('< nivel 1')
							 
						  for (let v=0; v<keys3.length;v++){ 
							  //console.log('--- issue XXX --- ' + data3['issues'][v]['key'] + ' ' + data3['issues'][v]['self']);
							  //console.log(data3['issues'][v]['fields']);
							  
						  arr.push({name: data3['issues'][v]['fields']['summary'].slice(0, 100), text: data3['issues'][v]['fields']['summary'].slice(0, 100), data: { status: data3['issues'][v]['fields']['status']['name'] , priority: data3['issues'][v]['fields']['priority']['name'],  key: "3.2.1 " + data3['issues'][v]['key']},a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data3['issues'][v]['key'] }, icon: data3['issues'][v]['fields']['issuetype']['iconUrl']  } );
							  
							  //console.log(arr)
						  }	
					
					      // ----------------------------------------------------- issueslinks nivel 2    
						  const res5 = await fetch(data4['fields']['issuelinks'][z]['inwardIssue']['self'], {
								  headers: {
								  'Accept': 'application/json',
								  'Authorization': 'Bearer NDQ5NjQ4Njc3MjQ0OpEHco38qMrnJPHxptq4hjdzRrxr'		  
										  }
							  })


						  const data5 = await res5.json(); //assuming data is json
						  const keys5 = Object.keys(data5['fields']['issuelinks'])
							  
						  
						  //arrchild4 = [];
						  
						  for (let v=0; v < keys5.length;v++){ 
							  try{
								  
								  a= data5['fields']['issuelinks'][v]['outwardIssue']['fields']['summary'];

							  }
							  catch (err) {
								  console.log('--- issue XXX --- ' +  data5['fields']['issuelinks'][v]['inwardIssue']['key'] + ' ' +  data5['fields']['issuelinks'][v]['inwardIssue']['self']);	

								  arr.push({text: data5['fields']['issuelinks'][v]['inwardIssue']['fields']['summary'].slice(0, 100), data: { status: data5['fields']['issuelinks'][v]['inwardIssue']['fields']['status']['name'] , priority: data5['fields']['issuelinks'][v]['inwardIssue']['fields']['priority']['name'],  key: "3.4 " + data5['fields']['issuelinks'][v]['inwardIssue']['key'] }, a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data5['fields']['issuelinks'][v]['inwardIssue']['key'] }, icon: data5['fields']['issuelinks'][v]['inwardIssue']['fields']['issuetype']['iconUrl']  } );

							  }
						  }
						  // OUT arr 

						  arrchild3.push({text: data4['fields']['issuelinks'][z]['inwardIssue']['fields']['summary'].slice(0, 100),children: arr, data: { status: data4['fields']['issuelinks'][z]['inwardIssue']['fields']['status']['name'] , priority: data4['fields']['issuelinks'][z]['inwardIssue']['fields']['priority']['name'],  key: "3.2.2 " + data4['fields']['issuelinks'][z]['inwardIssue']['key']},a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data4['fields']['issuelinks'][z]['inwardIssue']['key'] }, icon: data4['fields']['issuelinks'][z]['inwardIssue']['fields']['issuetype']['iconUrl']  } );
						  arr=[];
	  

					  // ----------------------------------------------------- issueslinks nivel 2    
					  				  }
				  else
				  {
						  arrchild3.push({text: data4['fields']['issuelinks'][z]['inwardIssue']['fields']['summary'].slice(0, 100), data: { status: data4['fields']['issuelinks'][z]['inwardIssue']['fields']['status']['name'] , priority: data4['fields']['issuelinks'][z]['inwardIssue']['fields']['priority']['name'],  key: "3.3 " + data4['fields']['issuelinks'][z]['inwardIssue']['key']},a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data4['fields']['issuelinks'][z]['inwardIssue']['key'] }, icon: data4['fields']['issuelinks'][z]['inwardIssue']['fields']['issuetype']['iconUrl']  } );
				  }					
			  
				  
			  }		
			   //console.log(arr)						
				  	
		  
	 
		  }	


		  if (arr1.length > 0){
		
			
			arrchild2.push({text: data2['inwardIssue']['fields']['summary'].slice(0, 100), children: arr1, data: { status: data2['inwardIssue']['fields']['status']['name'] , priority: data2['inwardIssue']['fields']['priority']['name'], key: "4 " + data2['inwardIssue']['key']},a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data2['inwardIssue']['key'] }, icon: data2['inwardIssue']['fields']['issuetype']['iconUrl'] } );
			arr1=[]
		}
		   else{
			arrchild2.push({text: data2['inwardIssue']['fields']['summary'].slice(0, 100), children: arrchild3, data: { status: data2['inwardIssue']['fields']['status']['name'] , priority: data2['inwardIssue']['fields']['priority']['name'], key: "4 " + data2['inwardIssue']['key']},a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data2['inwardIssue']['key'] }, icon: data2['inwardIssue']['fields']['issuetype']['iconUrl'] } );
			arrchild3=[]	
		   }
		   
		  console.log(' nivel 1 >')
							
				
		}
		catch
		{}
	   

	   
		  //		
		  //Array.prototype.push.apply(arr,arr1)

		  }
		//else{		
		//  arr.push({text: data2['outwardIssue']['fields']['summary'].slice(0, 100), data: { status: data2['outwardIssue']['fields']['status']['name'], priority: data2['outwardIssue']['fields']['priority']['name'], key: data2['outwardIssue']['key'] }, a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data2['outwardIssue']['key'] }, icon: data2['outwardIssue']['fields']['issuetype']['iconUrl'] });
		//  //console.log('---------------------');
		
	   //}

	   
	   
	}
	//console.log(arrchild);
	return arrchild2
}

async function get_request(project){
	
  // application code that gets the data
  
  try
  {
	  console.log(project);
  }
  catch (err) {
    console.log(err);
    project = "TME";
  
  }
  
  //%20and%20issuekey%3DTME-32
  const res = await fetch('https://jira.k8s2.grupocgd.com/rest/api/2/search?jql=project%20%3D%20' + project + '%20and%20issuetype%3DTheme%20and%20status%20not%20in%20(Done)&maxResults=1000', {
      headers: {
        'Accept': 'application/json',
	    'Authorization': 'Bearer NDQ5NjQ4Njc3MjQ0OpEHco38qMrnJPHxptq4hjdzRrxr'	  
               }
  })
  const data = await res.json();//assuming data is json
  
  const keys = Object.keys(data['issues'])
  var arr = [];
  for (let i=0; i<keys.length;i++)
  {
  //console.log(data['issues'][i]['key']);
  //console.log(data['issues'][i]['fields']['summary']);
  //console.log(data['issues'][i]['fields']['status']['name']);
   
	  arrchild = await child( data['issues'][i]['key'], data['issues'][i]['fields']['issuelinks'])
	  
	//  console.log('----------------------')
//	  console.log(arrchild);
//	  console.log('----------------------')
	  console.log('< nivel 0 >')
	  arr.push({id: i, key: data['issues'][i]['key'], name: data['issues'][i]['fields']['summary'].slice(0, 100), text: data['issues'][i]['fields']['summary'].slice(0, 100), parent_id: "0", children: arrchild, data:  { status: data['issues'][i]['fields']['status']['name'], key: "1 " +  data['issues'][i]['key'] },
	  a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data['issues'][i]['key'] },  icon: data['issues'][i]['fields']['issuetype']['iconUrl'] } )
		
  }
  //console.log(arr);
  return arr;
}

process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0;

app.use(express.static(path.join(__dirname, '.')));
// handle every other route with index.html, which will contain
// a script tag to your application's JavaScript file(s).

app.get('/api/:project',  async function  (request, response) {

 try {
    // try to get from the cache
    let data = myCache.get('data');

    
    if (data == null) {
	  console.log('Getting not in cache', request.params.project );
	  const data =  await get_request(request.params.project)
	  
      // time-to-live is set to 360 seconds. After this period
      // the entry for `allPosts` will be removed from the cache
      // and the next request will hit the API again
	  console.log('DDDDDDDDDDDDDDDDDDD')
	  console.log(data );
	  console.log('DDDDDDDDDDDDDDDDDDD')
      myCache.set('data', data , 240);
	  response.send(data);
    }
	else{
		console.log('using cache');
		response.send(data);
	}

  } catch (err) {
    console.log(err);
    response.sendStatus(500);
  }
  
  //console.log(data);
  //response.send(data);
});

app.get('/*', function (req, res) {
  console.log(req.query.project);
  res.sendFile(path.join(__dirname, '.', 'index.html'));
});


const port = 8889;
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

