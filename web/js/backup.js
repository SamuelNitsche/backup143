class Backup {
	constructor(id) {
		this.taskid = id;
	}
	
	get_backups() {
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var self = this;
		var b_html = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/backups",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				var b_backups = $(data).find('amount').text();
				if( b_backups > 0){
					b_html = b_html + "<table>";
					b_html = b_html + "<tr><th>Source</th><th>Destination</th><th>Compare</th><th>Encryption</th><th>Compression</th></tr>";
					$(data).find('backup').each(function(){
						var b_id = $(this).find('id').text();
						var b_pool_src = $(this).find('pool_src').text();
						var b_pool_dst = $(this).find('pool_dst').text();
						var b_compare = $(this).find('compare').text();
						var b_encrypt = $(this).find('encrypt').text();
						var b_compression = $(this).find('compression').text();
						
						var pool = new Pool();
						var srcpoolinfo = pool.get_poolinfo(b_pool_src);
						var dstpoolinfo = pool.get_poolinfo(b_pool_dst);
						
						if(b_encrypt == '0'){
							b_encrypt = 'inactive';
						} else {
							b_encrypt = 'active';
						}
						
						b_html = b_html + "<tr onclick='var backup = new Backup(); backup.open_backupsettings(\""+String(b_id)+"\");'><td>" + srcpoolinfo[1] + "</td><td>" + dstpoolinfo[1] + "</td><td>" + b_compare + "</td><td>" + b_encrypt + "</td><td>" + b_compression + "</td></tr>";
					});
				} else {
					b_html = b_html + "<h3>No Backups!</h3>";
				}
			}
		});
		return b_html;
	}
	
	get_backupinfo(id){
		var req = new XMLHttpRequest();
		req.open('GET', document.location, false);
		req.send(null);
		var apiportheader = req.getResponseHeader('X-APIPORT');
		
		var b_id = "";
		var b_pool_src = "";
		var b_pool_dst = "";
		var b_compare = "";
		var b_encrypt = "";
		var b_compression = "";
		
		$.ajax({
			type: "get",
			url: window.location.protocol + "//" + window.location.hostname + ":" + apiportheader + "/get/backups",
			dataType: "xml",
			async: false,
			xhrFields: { withCredentials:true },
			success: function(data) {
				$(data).find('backup').each(function(){
					if($(this).find('id').text() == id){
						b_id = $(this).find('id').text();
						b_pool_src = $(this).find('pool_src').text();
						b_pool_dst = $(this).find('pool_dst').text();
						b_compare = $(this).find('compare').text();
						b_encrypt = $(this).find('encrypt').text();
						b_compression = $(this).find('compression').text();
					}
				});
			}
		});
		return Array(b_id,b_pool_src,b_pool_dst,b_compare,b_encrypt,b_compression);
	}
	
	open_backupsettings(id){
		var backupinfo = this.get_backupinfo(id);
		var html = "Source Pool: <input type='text' name='name' value='"+backupinfo[1]+"'/><br/>";
		html = html + "Destination Pool: <input type='text' name='system' value='"+backupinfo[2]+"'/><br/>";
		html = html + "Compare: <input type='text' name='host' value='"+backupinfo[3]+"'/><br/>";
		html = html + "Encrypt: <input type='text' name='port' value='"+backupinfo[4]+"'/><br/>";
		html = html + "Compression: <input type='text' name='username' value='"+backupinfo[5]+"'/><br/>";
		html = html + "<button onclick='var backup = new Backup(); backup.delete_backup(\""+String(id)+"\");'>Delete</button><button onclick='var backup = new Backup(); backup.update_backup(\""+String(id)+"\");'>Update</button>";
		showpopup("Settings", html);
	}
	
}

$( document ).ready(function() {
	if ($("#js_backuplist").length > 0){
		var backup = new Backup();
		$('#js_backuplist').html(backup.get_backups());
	}
});