import Vue from 'vue'
import ElementUI from 'element-ui'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import axios from 'axios'
window.adapterUrl='../kong/';
Vue.prototype.$axios = axios
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import routeConfig from './router-config'
Vue.use(VueRouter)
Vue.use(Vuex)
//import locale from 'element-ui/lib/locale/lang/zh-TW'
//Vue.use(ElementUI, { locale })
import store from './store/index'
import './font/font-awesome/css/font-awesome.min.css'

Vue.use(ElementUI)

const router = new VueRouter({
	routes: routeConfig
});
axios.defaults.headers.common['Authorization'] =Auth.header_token();
//console.log(Auth.header_token());
axios.interceptors.response.use(function (response) {
	return	response;
}, function (error) {
	//console.log('response error',error,error.response);
	//console.log("response error");
	if (error.response.status==401 ||error.response.status==403){
		Auth.login();
		return Promise.reject(null)
	}
	else
		return Promise.reject(error);

	//return Promise.reject(error);
});

router.beforeEach(function(to,from,next) {
	function ispermission(to,from,next){
		let valid=true;
		const paths = [
			"/pages/illegalmng/illegal_category",
			"/pages/illegalmng/illegal_type",
			"/pages/illegalmng/subcontractors",
			"/pages/illegalmng/emp_illegal",
			"/pages/illegalmng/subcon_illegal",
			"/pages/inspectionmng/danti",
			"/pages/inspectionmng/gongdi",
			"/pages/inspectionmng/buwei",
			"/pages/inspectionmng/inspect",
			"/pages/jishumng/guifan",
			"/pages/jishumng/tuzhi",
			"/pages/jishumng/tuji",
			"/pages/jishumng/jiaodi"
		]
		var index = paths.indexOf(to.path)
		if(index>=0){
			var right_name = to.path.split("/").slice(-1)
			if(store.state.mypermissions.data[right_name]){
				valid=store.state.mypermissions.data[right_name].ops.indexOf('view')>=0;
			}
			else{
				valid=false;
			}
		}
		if (to.path=='/rightmanage/appuser'){
			valid=store.state.mypermissions.superright;	
		}
		if (to.path=='/rightmanage/approle'){
			valid=store.state.mypermissions.superright;	
		}
		if (valid){
			next();
		}else{
			//next(false);
			next('/');
		}
	}
	if(to.path!='/login' && store.state.mypermissions.loaded==false){
		store.dispatch('loadpermissions');	
		setTimeout(function(){
			ispermission(to,from,next);
		}.bind(this),1000);
	}else{
		ispermission(to,from,next);
	}
});
Date.prototype.format = function(fmt)  
{ 
    var o = {  
        "M+" : this.getMonth()+1,                 //月份
        "d+" : this.getDate(),                    //日
        "h+" : this.getHours(),                   //小时
        "m+" : this.getMinutes(),                 //分
        "s+" : this.getSeconds(),                 //秒
        "q+" : Math.floor((this.getMonth()+3)/3), //季度
        "S"  : this.getMilliseconds()             //毫秒
    };  
    if(/(y+)/.test(fmt))  
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));  
    for(var k in o)  
        if(new RegExp("("+ k +")").test(fmt))  
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));  
    return fmt;  
};

new Vue({
	router,
	el: '#app',		
	store:store,
	render: h => h(App)
})
