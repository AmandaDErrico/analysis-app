function getMostPurchased() {
//              # get html element by id or by class
//              # insert rows inside the table
      console.log("test123")
      $.ajax({
              url: '/mostPurchased',
              type: 'GET',
              dataType: 'json', // added data type
              success: function(res) {
              // clear table here
              console.log(res)
//              var json = JSON.parse
//              va mostPurchasedTab = res["mostPurchasedTable"]
//              console.log(mostPurchasedTab)
              var table = $("#mostPurchasedProduct")
              // res.product_name is ramen
                table.append(
                "<thead>" +
                "<td>product_name</td>" +
                "<td>numPurchased</td>" +
                "</thead>" +
                      "<tr>" +
                        "<td>" + res.product_name + "</td>" +
                        "<td>" + res.numPurchased + "</td>" +
                      "</tr>"
                );
              },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(thrownError);
              }
          });
}