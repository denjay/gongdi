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
		//console.log(to.path)
		if(to.path=='/pages/formmng/dailyform'){
			if(store.state.mypermissions.data.dailyform){
				valid=store.state.mypermissions.data.dailyform.ops.indexOf('view')>=0;
			}
			else{
				valid=false;
			}
		}
		if (to.path=='/pages/formmng/monthlyform'){
			if(store.state.mypermissions.data.monthlyform){
				valid=store.state.mypermissions.data.monthlyform.ops.indexOf('view')>=0;
			}
			else{
				valid=false;
			}
		}
		if (to.path=='/pages/hourstatisticsmng/hourstatistics'){
			if(store.state.mypermissions.data.hourstatistics){
				valid=store.state.mypermissions.data.hourstatistics.ops.indexOf('view')>=0;
				//console.log(valid);
			}
			else{
				valid=false;
			}	
		}
		if (to.path=='/pages/lr_settingmng/lr_setting'){
			if(store.state.mypermissions.data.lr_setting){
				valid=store.state.mypermissions.data.lr_setting.ops.indexOf('view')>=0;
			}
			else{
				valid=false;
			}
		}
		if (to.path=='/pages/leave_systemmng/leave_type'){
			if(store.state.mypermissions.data.leave_type){
				valid=store.state.mypermissions.data.leave_type.ops.indexOf('view')>=0;
			}
			else{
				valid=false;
			}
		}
		if (to.path=='/pages/leave_systemmng/position_type'){
			if(store.state.mypermissions.data.position_type){
				valid=store.state.mypermissions.data.position_type.ops.indexOf('view')>=0;
			}
			else{
				valid=false;
			}
		}
		if (to.path=='/pages/leave_systemmng/depart'){
			if(store.state.mypermissions.data.depart){
				valid=store.state.mypermissions.data.depart.ops.indexOf('view')>=0;
			}
			else{
				valid=false;
			}
		}
		if (to.path=='/pages/leave_systemmng/leave_application'){
			if(store.state.mypermissions.data.leave_application){
				valid=store.state.mypermissions.data.leave_application.ops.indexOf('view')>=0;
			}
			else{
				valid=false;
			}
		}
		if (to.path=='/pages/leave_systemmng/leave_check'){
			if(store.state.mypermissions.data.leave_check){
				valid=store.state.mypermissions.data.leave_check.ops.indexOf('view')>=0;
			}
			else{
				valid=false;
			}
		}
		if (to.path=='/pages/leave_systemmng/annual_leave_balance'){
			if(store.state.mypermissions.data.annual_leave_balance){
				valid=store.state.mypermissions.data.annual_leave_balance.ops.indexOf('view')>=0;
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
