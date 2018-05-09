<template>	
	<div>
		<el-menu  class="el-menu-vertical-demo" :default-active="$route.path" :router="true">
			<el-submenu index="accident">
				<template slot="title"><i class="el-icon-menu"></i>违规管理</template>
				<el-menu-item v-if="view('illegal_category_right')" index="/pages/illegalmng/illegal_category"><i class="fa fa-list-ol"></i>违规类别</el-menu-item>
				<el-menu-item v-if="false && view('illegal_type_right')" index="/pages/illegalmng/illegal_type"><i class="fa fa-list-ul"></i>违规类型</el-menu-item>
				<el-menu-item v-if="view('subcontractors_right')" index="/pages/illegalmng/subcontractors"><i class="fa fa-building"></i>分包商</el-menu-item>
				<el-menu-item v-if="view('emp_illegal_right')" index="/pages/illegalmng/emp_illegal"><i class="fa fa-times-circle"></i>员工违规</el-menu-item>
				<el-menu-item v-if="view('subcon_illegal_right')" index="/pages/illegalmng/subcon_illegal"><i class="fa fa-times-circle"></i>分包商违规</el-menu-item>
			</el-submenu>  
			<el-submenu index="inspection">
				<template slot="title"><i class="el-icon-view"></i>巡检管理</template>	
				<el-menu-item v-if="view('danti_right')" index="/pages/inspectionmng/danti"><i class="fa fa-building"></i>单体管理</el-menu-item>
				<el-menu-item v-if="view('gongdi_right')" index="/pages/inspectionmng/gongdi"><i class="fa fa-cubes"></i>工地管理</el-menu-item>
				<el-menu-item v-if="view('buwei_right')" index="/pages/inspectionmng/buwei"><i class="fa fa-cube"></i>部位管理</el-menu-item>
				<el-menu-item v-if="view('inspect_right')" index="/pages/inspectionmng/inspect"><i class="fa fa-check"></i>巡检管理</el-menu-item>
			</el-submenu> 
			<el-submenu index="jishu">
				<template slot="title"><i class="el-icon-document"></i>技术管理</template>	
				<el-menu-item v-if="view('guifan_right')" index="/pages/jishumng/guifan"><i class="fa fa-compass"></i>规范管理</el-menu-item>
				<el-menu-item v-if="view('tuzhi_right')" index="/pages/jishumng/tuzhi"><i class="fa fa-file-image-o"></i>图纸管理</el-menu-item>
				<el-menu-item v-if="view('tuji_right')" index="/pages/jishumng/tuji"><i class="fa fa-folder-open-o"></i>图集管理</el-menu-item>
				<el-menu-item v-if="view('jiaodi_right')" index="/pages/jishumng/jiaodi"><i class="fa fa-handshake-o"></i>交底管理</el-menu-item>
			</el-submenu> 
			<el-submenu index="base">
				<template slot="title"><i class="el-icon-setting"></i>权限管理</template>
				<el-menu-item v-if="super_right" index="/pages/rightmanagemng/appuser"><i class="fa fa-user-circle"></i>用户权限</el-menu-item>
				<el-menu-item v-if="super_right" index="/pages/rightmanagemng/approle"><i class="fa fa-sitemap"></i>角色权限</el-menu-item>
				<el-menu-item index="/pages/rightmanagemng/curruser"><i class="fa fa-pencil-square-o"></i>修改密码</el-menu-item>
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
		methods: {
			view(name){
				if(this[name]){
					try {
						var right=(this[name].ops.indexOf('view')>=0);
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
		},
		computed: {
			...mapGetters({
				illegal_category_right:"illegal_category_right",
				illegal_type_right:"illegal_type_right",
				subcontractors_right:"subcontractors_right",
				emp_illegal_right:"emp_illegal_right",
				subcon_illegal_right:"subcon_illegal_right",
				super_right:'super_right',
				danti_right:'danti_right',
				gongdi_right:'gongdi_right',
				buwei_right:'buwei_right',
				inspect_right:'inspect_right',
				guifan_right:'guifan_right',
				tuzhi_right:'tuzhi_right',
				tuji_right:'tuji_right',
				jiaodi_right:'jiaodi_right',
			}),
		},
        watch: {
            '$route' (to, from){
				this.$store.state.nowurl=to.path
			},
			
        },
		destroyed: function() {
			this.$nextTick(() => {
				this.$store.commit('resetsuperright');
			})
		}
    }
</script>
<style>
	ul li {
		min-width: inherit !important;
	}
</style>