<template>
	<div style="header"> 			
		<div class="noprint logout addlogout">
			<span class="headfont">工地违规管理</span>
			<a href="#" @click.stop.prevent="logout" class="logoutbtn">{{user}} 登出</a>
		</div>
		<div class="content">
			<div class="menu">
				<sidebar :rightmng="rightmng" v-once></sidebar>
			</div>
			<div style="margin:0px 0px 0px 202px;background-color:white;height: 100%;">
				<router-view></router-view>
			</div>
		</div>
	</div>
</template>
<script>
import { mapGetters } from 'vuex';
import sidebar from './sidebar.vue';
import container from './container.vue';
import axios from 'axios'
import '../../locale/lang/zh_tw.js'
import { Loading } from 'element-ui';
export default {
	data(){
		return{
			theheight:"",
			loadingCount:0,
			rightmng:{
				companyright:'',
				departright:'',
				employeeright:'',
			}
		}
	},
	computed: {
		editableTabs(){
			return this.$store.state.tabs;
		},
		user: {
			get: function () {
			return Auth.username();
			},
			set: function () {
			}
		}
	},
	mounted:function()  {
		//this.$store.dispatch('loadpermissions');
		var me=this;
		axios.interceptors.request.use(function (config){
			if (me.loadingCount==0){
				Loading.service({ fullscreen: true});
				me.loadingCount++;
			}
			return config;
		 }, function (error){
			return Promise.reject(error);
		 });

		axios.interceptors.response.use(function (response) {
			if(response.config.method.toUpperCase()=='PUT'){
				me.$message({
					showClose: true,
					type: 'success',
					message: '修改成功'
				});
			}else if (response.config.method.toUpperCase()=='POST'){
				me.$message({
					showClose: true,
					type: 'success',
					message: '新增成功'
				});
			}else if (response.config.method.toUpperCase()=='DELETE'){
				me.$message({
					showClose: true,
					type: 'success',
					message: '刪除成功'
				});
			}
			me.loadingCount--;
			if (me.loadingCount==0){
				let loadingInstance = Loading.service({ fullscreen: true });
				loadingInstance.close();
			}
			return response;
		}, function (error) {
			if (error.response.status!=401){
				me.loadingCount--;
				if (me.loadingCount==0){
					let loadingInstance = Loading.service({ fullscreen: true });
					loadingInstance.close();
				}
				console.log(error.response.data.error);
				if(error.response.config.method=='post'){
					me.$message({
						showClose: true,
						type: 'error',
						message: error.response.data.error
					});
				}
				else{
					me.$message({
						showClose: true,
						type: 'error',
						message: '操作失敗'
					});
				}
				return Promise.reject(error);
			}
		});
	},
	created() {
		this.setsize();
	},
	methods: {
		setsize(){
			this.theheight =  window.innerHeight-48+ "px";
		},
		logout(){
			var self=this;
			var url='/auth/v1.0/logout';
			//console.log(arguments);
			Auth.logout();
			window.location.reload(url);
		},
		getusername(){
			this.$axios.get( '../../auth/v1.0/user-info').then((response) => {
				this.user=response.data.uname

			})
			.catch((response)=> {
				console.log("錯誤")
			});
		},
	},
	components: {
		'sidebar': sidebar,
		'container':container
	},	
}
</script>
<style>
	@import '../../css/custom.css';
	@import '../../css/test.css';
	html,body {
		height: 100%; 
		padding: 0; 
		margin: 0;
	}	
	.header {
		background-color:#20A0FF;
		color:white;
		height:40px;
		width: 100%;
	}

	.content{
		width: 100%;
		position: absolute;
		top: 40px;
		bottom: 0px;
		left: 0px;
		background-color:#eef1f6;
	}
	.menu{
		width:200px;
		float:left;
		overflow-y:auto;
		height: 100%;
	}   
	.right-menu-item {
      display: inline-block;
      margin: 0 8px;
    }
    .screenfull {
      height: 20px;
    }
</style>