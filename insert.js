var client = require('./connection.js'), inputfile = require("./data.json"), bulk = [];

var makebulk = function(json_list,callback){
  for (var current in json_list){
    bulk.push(
      { index: {_index: 'trending', _id: json_list[current].Sort_val } },
      {
        'video_id': json_list[current].Video_Id,
        'text': json_list[current].Text,
        'views': json_list[current].Views,
        'likes' : json_list[current].Likes,
        'dislikes' : json_list[current].Dislikes,
        'creation_date' : json_list[current].Creation_Date,
        'trend_score' : json_list[current].Trend_Score
      }
    );
  }
  callback(bulk);
}

var indexall = function(madebulk,callback) {
  client.bulk({
    maxRetries: 5,
    index: 'trending',
    body: madebulk
  },function(err,resp,status) {
      if (err) {
        console.log(err);
      }
      else {
        callback(resp.items);
      }
  })
}

makebulk(inputfile,function(response){
  console.log("Bulk content prepared");
  indexall(response,function(response){
    console.log(response);
  })
});