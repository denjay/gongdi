<template>
  <div>
    <section class="main-content-wrapper wrapper">
        <section id="main-content" >
            <div class="row">
                <div class="col-md-12">
					<!-- 操作 -->
					<el-row type="flex" justify="space-between" style="margin-bottom:5px">
						<el-col :inline="true"  style="float:left;">
							<el-button v-if="employeeright.ops.indexOf('insert')>=0" type="primary" @click="insert()" style="margin-left:10px;">新增</el-button>
            </el-col>
          </el-row>
                    <!-- 資料列表-->
                    <el-table :data="illegal_categorys" stripe v-loading="loading"
						element-loading-text="資料加載中..."
						:max-height="theheight" border>     
						<el-table-column
							type="index"
							width="50">
						</el-table-column>
						<el-table-column prop="name" style="incenter"
                            label="名称">
                        </el-table-column>
                        <el-table-column v-if="employeeright.ops.indexOf('edit')>=0 || employeeright.ops.indexOf('edit')>=0" 
								fixed="right" 
                            label="操       作" width="130">
                            <template slot-scope="scope">
                                <el-button v-if="employeeright.ops.indexOf('delete')>=0" size="mini"  icon="el-icon-delete" @click="remove(scope.row)"></el-button>
                                <el-button v-if="employeeright.ops.indexOf('edit')>=0" size="mini" icon="el-icon-edit" @click="edit(scope.row)"></el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </div>
        </section>
    </section>   
	<el-dialog  ref="dialog" :title="title" class="centers" :visible.sync="dialogVisible" width="30%" 
	 :close-on-click-modal="false" :close-on-press-escape="false" :before-close="reset">
        <el-form id="#insertdata"  ref="insertdata" :rules="rules" :model="insertdata"  label-width="50px">				
			<el-form-item label="名称" prop="name">
				<el-input v-model="insertdata.name"></el-input>
			</el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer" >
            <el-button @click="reset">取 消</el-button>
            <el-button type="primary" :loading="waitICStatus" @click="submitData()">確 定</el-button>
        </div>
    </el-dialog>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'
export default {
	data(){
		return {
			theheight:"",
			insertdata:{
				name:'',
            },
			title:'',
			loading:false,
			rules:{
			},
		}
	},
	mounted: function() {
		this.theheight=window.innerHeight-190;
		this.$nextTick(() => {
			this.loadIllegalCategorys();
		})
	},	
	computed: {
		...mapGetters([
			'illegal_categorys',
			'employeeright',
			'waitICStatus',
			'illegalCategoryActionStatus',
		]),
		dialogVisible: {
			get: function () {
			  return (this.illegalCategoryActionStatus==1 || this.illegalCategoryActionStatus==2)
			},
			set: function () {
			}
		},
	},
	methods: {
		loadIllegalCategorys(){		
			this.$store.dispatch('loadIllegalCategorys');
		},
		insert(){		
			this.title=chg['insertdata'];
			this.resetForm();
			delete this.insertdata.id;
			this.$store.commit('insertingIllegalCategory',this.insertdata);
		},
		edit(data){
			console.log(this.$refs.dialog.title);
			this.title=chg['updatedata'];
			//this.$refs.dialog.title='資料修改';
			for (var key in data){
				this.insertdata[key]=data[key];
			};
			this.$store.dispatch('editIllegalCategorys',{id:data.id});
        },
		remove(data){
			this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
				confirmButtonText: '確定',
				cancelButtonText: '取消',
			}).then(() => {
				this.$store.dispatch('removeIllegalCategorys',{id:data.id});
			}).catch(() => {         
			});
        },
		reset() {
			this.$store.commit('cancleIllegalCategorys');
        },
		submitData(){
			this.$refs.insertdata.validate((valid) => {
				if (valid) {
					this.$store.dispatch('saveIllegalCategorys',this.insertdata);
				}
                else {
                    return false;
                }
            });
		},
		resetForm(){
			this.insertdata={
                name:'',
            };
		},
	},	
	destroyed: function() {
		this.$nextTick(() => {
			this.$store.commit('resetillegal_category'); 
		})
	},
}
</script>
<style scope>
	.incenter{
		text-align:center;
	}
</style>
