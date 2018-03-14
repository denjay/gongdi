window.Auth={
	loging_page:'',
	username:function(){
			return 'super';
	},
	islogin:function(){
			return true;
	},
	clear:function(){
		//storageRemove('jwt.token');
	},
	logout:function(to){
		//Auth.clear();
		//location=to;
	},
	login:function(){
	   //location=loging_url;
	},
	token:function(){
		return ''
		//return storageGet('jwt.token');
	},
	header_token:function(){
		return '';
		//return 'Bearer '+storageGet('jwt.token');
	}
};