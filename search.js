const fs = require('fs');
var client = require('./connection.js');
var jsonData = client.search({  
  index: 'trending',
  body: {
    "from": 0,
    "size": 439,
    sort : [{"trend_score" : {"order" : "desc"}}],
    query: {
      "match_all": {}
    }
  }
}).then(function(resp) {
    console.log(resp.hits.hits);
    console.log()
}, function(err) {
    console.trace(err.message);
});
