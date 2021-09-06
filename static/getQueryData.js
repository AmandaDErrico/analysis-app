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
              document.getElementById("mostPurchasedProduct").innerHTML = "";
              console.log(res)
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

function getCustomerMemberAndRanking() {
//              # get html element by id or by class
//              # insert rows inside the table
      console.log("test")
      $.ajax({
              url: '/memberAndRanking',
              type: 'GET',
              dataType: 'json', // added data type
              success: function(res) {
              // clear table here
              document.getElementById("customerMemberAndRanking").innerHTML = "";
              console.log(res)
              var table = $("#customerMemberAndRanking")
              // res.product_name is ramen
                table.append(
                "<thead>" +
                "<td>customer_id</td>" +
                "<td>order_date</td>" +
                "<td>product_name</td>" +
                "<td>price</td>" +
                "<td>member</td>" +
                "<td>ranking</td>" +
                "</thead>");
//                console.log(res[0])
                for (var row in res) {
//                    console.log(row)
                    var jsonData = res[row]
                    table.append(
                    "<tr>" +
                    "<td>" + jsonData.customer_id + "</td>" +
                    "<td>" + jsonData.order_date + "</td>" +
                    "<td>" + jsonData.product_name + "</td>" +
                    "<td>" + jsonData.price + "</td>" +
                    "<td>" + jsonData.member + "</td>" +
                    "<td>" + jsonData.ranking + "</td>" +
                    "</tr>"
                    );
                }
              },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(thrownError);
              }
          });
}