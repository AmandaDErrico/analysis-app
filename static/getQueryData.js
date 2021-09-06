function getMostPurchased() {
//              # get html element by id or by class
//              # insert rows inside the table
      $.ajax({
              url: 'localhost:5000/mostPurchased',
              type: 'GET',
              dataType: 'json', // added data type
              success: function(res) {
              // clear table here
              var table = $("#tbl")
                table.append("test this works");


              }
          });
}