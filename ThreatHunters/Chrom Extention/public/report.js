function showAlert(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    
    // Access the form data
    var form = event.target.form;
    var url = form.re_url.value;
    var type = form.type_url.value;
    
    // Perform any necessary processing
    
    // Display the value as an alert
    alert("URL: " + url + "\nType: " + type);
    
    // You can also submit the form to a server-side script using AJAX if needed
    // Example using jQuery:
    // $.post("server_script.php", { url: url, type: type }, function(response) {
    //   alert(response);
    // });
  }