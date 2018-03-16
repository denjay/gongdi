<template>	
	<div>
		<el-menu  class="el-menu-vertical-demo" :default-active="$route.path" :router="true">
			<el-submenu index="accident">
				<template slot="title"><i class="el-icon-menu"></i>违规管理</template>	
				<el-menu-item  index="/pages/illegalmng/illegal_category"><i class="fa fa-users"></i>违规类别</el-menu-item>
				<el-menu-item  index="/pages/illegalmng/illegal_type"><i class="fa fa-users"></i>违规类型</el-menu-item>
			</el-submenu>  
			<el-submenu index="accident1">
				<template slot="title"><i class="fa fa-handshake-o"></i>巡检管理</template>	
				<el-menu-item  index="/pages/inspectionmng/danti"><i class="fa fa-building"></i>单体管理</el-menu-item>
				<el-menu-item  index="/pages/inspectionmng/gongdi"><i class="fa fa-cubes"></i>工地管理</el-menu-item>
			</el-submenu> 
			<el-submenu index="base">
				<template slot="title"><i class="el-icon-setting"></i>權限管理</template>
				<el-menu-item v-if="userright" index="/pages/rightmanagemng/appuser"><i class="fa fa-user-circle"></i>用戶權限</el-menu-item>
				<el-menu-item v-if="userright" index="/pages/rightmanagemng/approle"><i class="fa fa-sitemap"></i>角色權限</el-menu-item>
				<el-menu-item index="/pages/rightmanagemng/curruser"><i class="fa fa-pencil-square-o"></i>修改密碼</el-menu-item>
			</el-submenu>
		</el-menu>
	</div>
</template>
<script>
	import {mapGetters} from 'vuex'
	export default {
		props:['rightmng'],
		data() {
            return {
				//userright:'',
				test:'fa fa-print',
            }
        },
		computed: {
			...mapGetters({
				dailyformright:'dailyformright',
				monthlyformright:'monthlyformright',
				hourstatisticsright:'hourstatisticsright',
				lr_settingright:'lr_settingright',
				abnormalstatisticsright:'abnormalstatisticsright',
				employeeright:'employeeright',
				superright:'superright',
				leave_typeright:'leave_typeright',
				position_typeright:'position_typeright',
				departright:'departright',
				leave_applicationright:'leave_applicationright',
				leave_checkright:'leave_checkright',
				annual_leave_balanceright:'annual_leave_balanceright',
				monthly_leaveright:'monthly_leaveright',
			}),			
			dailyview: {
				get: function () {
					if(this.dailyformright){
						try {
							var right=(this.dailyformright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			lr_setview: {
				get: function () {
					if(this.lr_settingright){
						try {
							var right=(this.lr_settingright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　} 
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			hoursview: {
				get: function () {
					if(this.hourstatisticsright){
						try {
							var right=(this.hourstatisticsright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　} 
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			abnormalstatisticsview: {
				get: function () {
					if(this.abnormalstatisticsright){
						try {
							var right=(this.abnormalstatisticsright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			employeeview: {
				get: function () {
					if(this.employeeright){
						try {
							var right=(this.employeeright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			monthview: {
				get: function () {
					if(this.monthlyformright){
						try {
							var right=(this.monthlyformright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			position_typeview: {
				get: function () {
					if(this.position_typeright){
						try {
							var right=(this.position_typeright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			departview: {
				get: function () {
					if(this.departright){
						try {
							var right=(this.departright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			leave_applicationview: {
				get: function () {
					if(this.leave_applicationright){
						try {
							var right=(this.leave_applicationright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			leave_checkview: {
				get: function () {
					if(this.leave_checkright){
						try {
							var right=(this.leave_checkright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			leave_typeview: {
				get: function () {
					if(this.leave_typeright){
						try {
							var right=(this.leave_typeright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			annual_leave_balanceview: {
				get: function () {
					if(this.annual_leave_balanceright){
						try {
							var right=(this.annual_leave_balanceright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			monthly_leaveview: {
				get: function () {
					if(this.monthly_leaveright){
						try {
							var right=(this.monthly_leaveright.ops.indexOf('view')>=0);
							return right;
						}
						catch(err) {
					　　 　　return false;
					　　}
					}
					else{
						return false;
					}
				},
				set: function () {
				}
			},
			userright: {
				get: function () {
					return this.superright;
				},
				set: function () {
				}
			},
		},
        watch: {
            '$route' (to, from){
				this.$store.state.nowurl=to.path
			},
			
        },
		destroyed: function() {
			this.$nextTick(() => {
				this.$store.commit('resetsuperright');
				this.userright = undefined;
			})
		}
    }
</script>
<style>
	ul li {
		min-width: inherit !important;
	}
</style>