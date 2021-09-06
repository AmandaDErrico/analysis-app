function getMostPurchased() {
      $.ajax({
              url: '/mostPurchased',
              type: 'GET',
              dataType: 'json', // added data type
              success: function(res) {
              // clear table here
              document.getElementById("mostPurchasedProduct").innerHTML = "";
              // get div matching the table from the first query and append
              var table = $("#mostPurchasedProduct")
                // append one record
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
      $.ajax({
              url: '/memberAndRanking',
              type: 'GET',
              dataType: 'json', // added data type
              success: function(res) {
              // clear table here
              document.getElementById("customerMemberAndRanking").innerHTML = "";
              var table = $("#customerMemberAndRanking")
                // append headers
                table.append(
                "<thead>" +
                "<td>customer_id</td>" +
                "<td>order_date</td>" +
                "<td>product_name</td>" +
                "<td>price</td>" +
                "<td>member</td>" +
                "<td>ranking</td>" +
                "</thead>");

                // get each object in json array
                for (var row in res) {
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

function getQueries() {
    window.location = "http://localhost:5000/query"
}