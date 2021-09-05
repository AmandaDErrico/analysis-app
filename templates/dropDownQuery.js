function getMostPurchased() {
     console.log("test133")
     var customerName = document.getElementById("customerName").value;

      $.ajax({
              url: `localhost:5000/mostPurchased?customer_id=${customerName}`,
              type: 'GET',
              dataType: 'json', // added data type
              success: function(res) {
                alert("Data: " + data + "\nStatus: " + status);
              }
          });
}