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

async function child2(arr, key, issue)
{     console.log('CHILD 2:' + key  + ' ' + issue);
   
	  const res = await fetch(issue, {
				  headers: {
					'Accept': 'application/json',
					'Authorization': 'Bearer NDQ5NjQ4Njc3MjQ0OpEHco38qMrnJPHxptq4hjdzRrxr'				  
						   }
				})
				//console.log('--- data3 ---');
	  const data = await res.json();//assuming data is json
	  					//arr.push({key: key});
							
      //console.log(data);
      const keys = Object.keys(data['fields']['issuelinks'])
	  console.log(data['fields']['issuelinks']);

	  for (let j=0; j<keys.length;j++){
		  
				  try{	
					   console.log('CHILD2 KEY: ' + data['fields']['issuelinks'][j]['inwardIssue']['key'])
					   console.log('1-------------');
					   //console.log(arr)
					   
					   arr=child2(arr, data['fields']['issuelinks'][j]['inwardIssue']['key'], data['fields']['issuelinks'][j]['inwardIssue']['self']);
					   
					   arr.push({key: key, child: data['fields']['issuelinks'][j]['inwardIssue']['key'],name: data['fields']['summary'].slice(0, 100),  text: data['fields']['summary'].slice(0, 100), data: { status: data['fields']['status']['name'] , priority: data['fields']['priority']['name'],  key: "3.2 " + data['key']},a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data['key'] }, icon: data['fields']['issuetype']['iconUrl']  } ); 
					   
					   //arr.push({key: key, child: data['fields']['issuelinks'][j]['inwardIssue']['key']});
					   console.log(arr)
					   //console.log('2-------------');		
					 }
					   catch (err) {
							console.log(err);
							console.log('CHILD2 end KEY: ' +  data['key'] + data['fields']['issuelinks'][j]['outwardIssue']['key']);
							
							 arr.push({key: key, child: data['fields']['issuelinks'][j]['outwardIssue']['key'],name: data['fields']['summary'].slice(0, 100),  text: data['fields']['summary'].slice(0, 100), data: { status: data['fields']['status']['name'] , priority: data['fields']['priority']['name'],  key: data['key']},a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data['key'] }, icon: data['fields']['issuetype']['iconUrl']  } );  
							//arr.push({key: key});
					
					  }
		   
        
	  }
	return arr;
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
  
  const res = await fetch('https://jira.k8s2.grupocgd.com/rest/api/2/search?jql=issuekey%20%3D%20%20TMET-2', {
//const res = await fetch('https://jira.k8s2.grupocgd.com/rest/api/2/search?jql=project%20%3D%20%20TMET', {
        
	headers: {
        'Accept': 'application/json',
	    'Authorization': 'Bearer NDQ5NjQ4Njc3MjQ0OpEHco38qMrnJPHxptq4hjdzRrxr'	  
               }
  })
  const data = await res.json();//assuming data is json
  
  const keys = Object.keys(data['issues'])
  var arr = [];
  var arrchild = [];
  for (let i=0; i<keys.length;i++)
  {
  //console.log(data['issues'][i]['key']);
  //console.log(data['issues'][i]['fields']['summary']);
  //console.log(data['issues'][i]['fields']['status']['name']);
   const keys2 = Object.keys(data['issues'][i]['fields']['issuelinks']);
   data2 = data['issues'][i]['fields']['issuelinks']
     for (let j=0; j<keys2.length;j++)
	 {
		  try{
			console.log(data2);
			//arr.push({key: data['issues'][i]['key'], child: data2[j]['inwardIssue']['key'] })
			arr.push({id: i, key: data['issues'][i]['key'], child:data['issues'][i]['key'], name: data['issues'][i]['fields']['summary'].slice(0, 100), text: data['issues'][i]['fields']['summary'].slice(0, 100), parent_id: "0", data:  { status: data['issues'][i]['fields']['status']['name'], key: data['issues'][i]['key'] },
			a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data['issues'][i]['key'] },  icon: data['issues'][i]['fields']['issuetype']['iconUrl'] } )
		
		    console.log('>>>> '+data2[j]['inwardIssue']['key'], data2[j]['inwardIssue']['self']);
			arrchild = await child2(arr, data2[j]['inwardIssue']['key'], data2[j]['inwardIssue']['self'])
		  }
		  catch (err){
			  console.log(err);
		  }
	  
	  //issues[0].fields.issuelinks[1].inwardIssue.self
	  
	  console.log('----------------------')
	  //console.log(arrchild);
	  console.log('----------------------')
     }
	
	  //arr.push({id: i, key: data['issues'][i]['key'], name: data['issues'][i]['fields']['summary'].slice(0, 100), text: data['issues'][i]['fields']['summary'].slice(0, 100), parent_id: "0", children: arrchild, data:  { status: data['issues'][i]['fields']['status']['name'], key: "1 " +  data['issues'][i]['key'] },
	  //a_attr: {  href: "https://jira.k8s2.grupocgd.com/browse/" + data['issues'][i]['key'] },  icon: data['issues'][i]['fields']['issuetype']['iconUrl'] } )
	
  }
 
	arr = arr.sort((a, b) => {
	  if (a.key < b.key) {
		return -1;
	  }
	}); 
	
	arrout=[]
    parentK="";
	id=0;
	console.log(arr);
	
	for (let i=0; i<arr.length;i++)
	{
		
		if (arr[i]['parent_id'] == "0")
		{
		  parentK = {id: i, key: arr[i]['key'],  name:  arr[i]['name'], text:  arr[i]['text'], parent_id: "0", data:  { key: arr[i]['key'] }, a_attr: {  href: arr[i]['a_attr']['href'] },  icon: arr[i]['icon'] } 
		  id=i
		  console.log(parentK);
		}
		else{
				arrchild.push({id: i, key: arr[i]['child'], name: arr[i]['name'], text: arr[i]['name'], parent_id: id, data:  { status: arr[i]['data']['status'], key: arr[i]['key'] }, a_attr: {  href: arr[i]['a_attr']['href'] },  icon: arr[i]['icon'] } )
				console.log(arr[i]['key']);
				if (i==arr.length-1){
						   arrout.push({ id: parentK['i'], key: parentK['key'], name: parentK['name'], text: parentK['text'], parent_id: parentK['parent_id'], children: arrchild, data:  { key: parentK['key'] }, a_attr: {  href: "" },  icon: parentK['icon'] })
				   arrchild=[]
				   parentK="";
				   id=0;
				}
				else
				{
				if (arr[i]['key']  != arr[i+1]['key'] ) 
					{
					   arrout.push({ id: parentK['i'], key: parentK['key'], name: parentK['name'], text: parentK['text'], parent_id: parentK['parent_id'], children: arrchild, data:  { key: parentK['key'] }, a_attr: {  href: "" },  icon: parentK['icon'] })
					   arrchild=[]
					   parentK="";
					   id=0;
					}
				}
		}
			
			
		
	}
	
  return arrout;
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


const port = 8888;
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

