class User {
	constructor(id) {
		this.taskid = id;
	}
	
	update_password(){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		
		var password = $('#user_password').val();
		
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/changepw",
			dataType: "xml",
			async: false,
			data: { "password": password },
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					showpopup("Success", "Successfully changed Password!");
				} else {
					var error = $(data).find('message').text()
					showpopup("ERROR", error);
				}
			}
		});
	}
    
    update_email(){
        var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		
		var email = $('#user_email').val();
		
		$.ajax({
			type: "post",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/post/changemail",
			dataType: "xml",
			async: false,
			data: { "email": email },
			xhrFields: { withCredentials:true },
			success: function(data) {
				var apistatus = $(data).find('status').text();
				if(apistatus == "OK"){
					showpopup("Success", "Successfully changed E-Mail!");
				} else {
					var error = $(data).find('message').text()
					showpopup("ERROR", error);
				}
			}
		});
    }
    
}