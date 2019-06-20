var client = require('./connection.js');

// client.indices.delete({index: 'trending'},function(err,resp,status) {  
//   console.log("delete",resp);
// });

client.indices.create({
	index : 'trending'
}, function(err, resp, status){
	if(err){
		console.log(err);
	}
	else{
		console.log("create", resp);
	}
});

client.indices.putMapping({
	index : 'trending',
	body :{
		properties:{
			video_id : {type : "text"},
			text : {type:"text"},
			views : {type:"integer"},
      		likes : {type:"integer"},
      		dislikes : {type:"integer"},
      		creation_date : {type:"text"},
      		trend_score : {type:"float"}
		}
	}
}, function(err, resp, status){
	if(err){
		console.log(err);
	}
	else{
		console.log(resp);
	}
});
