<template>
  <div>
    <section class="main-content-wrapper wrapper">
        <section id="main-content" >
            <div class="row">
                <div class="col-md-12">
					<!-- 操作 -->
					<el-row type="flex" justify="space-between" style="margin-bottom:5px">
						<el-col :inline="true"  style="float:left;">
							<el-select v-if="false" filterable clearable v-model="illegal_categoryid"  style="width:180px;margin-left:20px;" placeholder="违规类别">
								<el-option 
									v-for="item in illegal_categorys"
									:key="item.id"
									:label="item.name"
									:value="item.id">
								</el-option>
							</el-select>
							<el-button v-if="illegal_type_right.ops.indexOf('insert')>=0" type="primary" @click="insert()" style="margin-left:10px;">新增</el-button>
                        </el-col>
                    </el-row>
                    <!-- 资料列表-->
                    <el-table :data="illegal_types" stripe v-loading="loading"
							element-loading-text="资料加载中..."
							:height="theheight" border>
						<el-table-column
							type="index"
							width="50">
						</el-table-column>
						<el-table-column prop="name" style="incenter"
                            label="违规类型">
                        </el-table-column>
						<el-table-column prop="illegal_category_name" style="incenter"
                            label="违规种类">
                        </el-table-column>
                        <el-table-column v-if="illegal_type_right.ops.indexOf('edit')>=0 || illegal_type_right.ops.indexOf('edit')>=0" 
								fixed="right" 
                            label="操       作" width="130">
                            <template slot-scope="scope">
                                <el-button v-if="illegal_type_right.ops.indexOf('delete')>=0" size="mini"  icon="el-icon-delete" @click="remove(scope.row)"></el-button>
                                <el-button v-if="illegal_type_right.ops.indexOf('edit')>=0" size="mini" icon="el-icon-edit" @click="edit(scope.row)"></el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </div>
        </section>
    </section>   
	<el-dialog  ref="dialog" :title="title" class="centers" :visible.sync="dialogVisible" width="30%"
	 :close-on-click-modal="false" :close-on-press-escape="false" :before-close="reset">
        <el-form id="#insertdata"  ref="insertdata" :rules="rules" :model="insertdata"  label-width="60px">
			<el-form-item label="名称" prop="name">
				<el-input v-model="insertdata.name"></el-input>
			</el-form-item>
			<!--<el-form-item label="违规类别" prop="name">
				<el-select filterable v-model="insertdata.illegal_categoryid" 
					clearable  style="margin-left:10px;" @change="selectIllegal_categoryid"
					placeholder="违规类别">
					<el-option 
						v-for="item in illegal_categorys"
						:key="item.id"
						:label="item.name"
						:value="item.id">
					</el-option>
				</el-select>
			</el-form-item>-->
        </el-form>
        <div slot="footer" class="dialog-footer" >
            <el-button @click="reset">取 消</el-button>
            <el-button type="primary" :loading="waitITstatus" @click="submitData()">确 定</el-button>
        </div>
    </el-dialog>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'
export default {
    props: ['illegal_categoryid'],
	data(){
		return {
			theheight:"",
			logicroutes:"",
			optionsForEmp:[],
			//illegal_categoryid:0,
			insertsubcompanyid:'',
			employeeid:"",
			insertdata:{
				name:'',
				illegal_categoryid:'',
            },
			title:'',
			loading:false,
            rules:{
                name: [{ required: true, message: '必填字段', trigger: 'change' }],
            }
		}
	},
	mounted: function() {
		this.theheight=window.innerHeight-190;
		this.$nextTick(() => {
			//this.loadIllegalCategorys();
		})
	},	
	computed: {   
		...mapGetters([
			'illegal_types',
			'illegal_categorys',
			'illegal_type_right',
			'waitITstatus',
			'illegalTypesActionStatus',
		]),
		dialogVisible: {
			get: function () {
			  return (this.illegalTypesActionStatus==1 || this.illegalTypesActionStatus==2)
			},
			set: function () {
			}
		},
	},
	watch:{
		/*illegal_categorys:function(newValue){
			if(newValue.length!=0){
				this.illegal_categoryid=newValue[0].id;
			}
		},*/
		illegal_categoryid: function (val, oldVal) {  
			if(val){
				this.loadIllegalTypes();
			}		
		},
	},
	methods: {
		loadIllegalCategorys(){		
			this.$store.dispatch('loadIllegalCategorys');
		},
		loadIllegalTypes(){	
			this.$store.dispatch('loadIllegalTypes',this.illegal_categoryid);
		},
		loadcompany(){
			this.$store.dispatch('loadSubcompany');
		},
		selectIllegal_categoryid(){
		},
		loadDepart(){
			if (this.insertsubcompanyid){				
				var data={subcompanyid:this.insertsubcompanyid};			
				this.$store.dispatch('loadDepartFE',data);
			}
		},
		loadPosition_type(){
			this.$store.dispatch('loadPosition_typeFE');
		},
		insert(){
		    if(this.illegal_categoryid){
                this.title=chg['illegal_type']+chg['insertdata'];
                this.resetForm();
                this.insertdata.illegal_categoryid=this.illegal_categoryid;
                delete this.insertdata.id;
                this.$store.commit('insertingIllegal_type',this.insertdata);
            }
            else{
                this.$message({
                    showClose: true,
                    message: '请先选择违规类型!',
                    type: 'error'
                });
            }
		},
		edit(data){
			this.title=chg['illegal_type']+chg['updatedata'];
			//this.$refs.dialog.title='资料修改';
			for (var key in data){
				this.insertdata[key]=data[key];
			};
			this.$store.dispatch('editIllegal_type',{id:data.id});
        },
		remove(data){
			this.$confirm('此操作将永久删除该资料, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
			}).then(() => {
				this.$store.dispatch('removeIllegal_type',{id:data.id});
			}).catch(() => {         
			});
        },
		reset() {
			this.$store.commit('cancleIllegal_type');
        },
		submitData(){
			this.$refs.insertdata.validate((valid) => {
				if (valid) {
					this.$store.dispatch('saveIllegal_type',this.insertdata);
				}
                else {
                    return false;
                }
            });
		},
		remoteForEmp(value){
			//this.loadempstatus=true;
			if (value !== ''&&this.illegal_types.length!=0) {
				this.loadempstatus = true;
				setTimeout(() => {
					this.loadempstatus = false;
					this.optionsForEmp = this.illegal_types.filter(item =>item.name.indexOf(value)>-1);
				}, 200);
			} else {
				this.loadempstatus = false;
				this.optionsForEmp = [];
			}
		},
		resetForm(){
			this.insertdata={
				name:'',
				illegal_categoryid:'',
            };
		},
		pageCurrentChange(val) {   //当前页变动时候触发的事件
			this.filter.page = val;
			this.loademployee();
		},
	},	
	destroyed: function() {
		this.$nextTick(() => {
			this.$store.commit('resetemp'); 
		})
	},
}
</script>
<style scope>
	.incenter{
		text-align:center;
	}
</style>
