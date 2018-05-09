<template>
  <div>
    <section class="main-content-wrapper wrapper">
        <section id="main-content" >
            <div class="row">
                <div class="col-md-12">
					<!-- 操作 -->
					<el-row type="flex" justify="space-between" style="margin-bottom:5px">
						<el-col :inline="true"  style="float:left;">
							<el-select filterable clearable v-model="filter.companyid"  style="width:180px;margin-left:20px;" placeholder="公司名称">
								<el-option 
									v-for="item in companies"
									:key="item.id"
									:label="item.company_name"
									:value="item.id">
								</el-option>
							</el-select>
							<el-input v-model="filter.manager" style="width:180px;" placeholder="负责人"></el-input>							
							<el-button type="primary" @click="loadSubcontractors" style="margin-left:10px;">查询</el-button>
							<el-button v-if="subcontractors_right.ops.indexOf('insert')>=0" type="primary" @click="insert()" style="margin-left:10px;">新增</el-button>
                        </el-col>
                    </el-row>
                    <!-- 资料列表-->
                    <el-table :data="subcontractors" stripe v-loading="loading"
							element-loading-text="资料加载中..."
							:max-height="theheight" border>     
						<el-table-column
							type="index"
							width="50">
						</el-table-column>
						<el-table-column prop="comp_name" style="incenter"
                            label="公司名称">
                        </el-table-column>
						<el-table-column prop="tel" style="incenter"
                            label="电话">
                        </el-table-column>
						<el-table-column prop="manager" style="incenter"
                            label="负责人">
                        </el-table-column>
						<el-table-column prop="license" style="incenter"
                            label="营业执照">
                        </el-table-column>
						<el-table-column prop="email" style="incenter"
                            label="邮件">
                        </el-table-column>
						<el-table-column prop="approach_date" style="incenter"
                            label="进场日期">
                        </el-table-column>
						<el-table-column prop="departure_date" style="incenter"
                            label="离场日期">
                        </el-table-column>
                        <el-table-column v-if="subcontractors_right.ops.indexOf('edit')>=0 || subcontractors_right.ops.indexOf('edit')>=0" 
								fixed="right" 
                            label="操       作" width="130">
                            <template slot-scope="scope">
                                <el-button v-if="subcontractors_right.ops.indexOf('delete')>=0" size="mini"  icon="el-icon-delete" @click="remove(scope.row)"></el-button>
                                <el-button v-if="subcontractors_right.ops.indexOf('edit')>=0" size="mini" icon="el-icon-edit" @click="edit(scope.row)"></el-button>
                            </template>
                        </el-table-column>
                    </el-table>					
					<el-col>
						<el-pagination style="text-align:center"
							:current-page="filter.page"
							:page-size="filter.per_page"
							layout="total, prev, pager, next"
							:total="subcontractorstotal"
							@current-change="pageCurrentChange">
						</el-pagination>
					</el-col>
                </div>
            </div>
        </section>
    </section>   
	<el-dialog  ref="dialog" :title="title" class="centers" :visible.sync="dialogVisible" width="32%" 
	 :close-on-click-modal="false" :close-on-press-escape="false" :before-close="reset">
        <el-form id="#insertdata"  ref="insertdata" :rules="rules" :model="insertdata"  label-width="80px">
			<el-form-item label="公司名称" prop="companyid" style="width:100%">
				<el-select filterable v-model="insertdata.companyid" 
					clearable style="width:100%" @change="selectcompanyid"
					placeholder="公司">
					<el-option 
						v-for="item in companys"
						:key="item.id"
						:label="item.comp_name"
						:value="item.id">
					</el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="电话" prop="tel" style="width:100%">
				<el-input v-model="insertdata.tel"></el-input>
			</el-form-item>
			<el-form-item label="负责人" prop="manager" style="width:100%">
				<el-input v-model="insertdata.manager"></el-input>
			</el-form-item>
			<el-form-item label="营业执照" prop="license" style="width:100%">
				<el-input v-model="insertdata.license"></el-input>
			</el-form-item>
			<el-form-item label="邮件" prop="email" style="width:100%">
				<el-input v-model="insertdata.email"></el-input>
			</el-form-item>
			<el-form-item label="进场日期" prop="approach_date" style="width:100%">
				<el-date-picker
					v-model="insertdata.approach_date"
					align="right"
					type="date"
					placeholder="选择进场日期"
					:picker-options="pickerOptions1"  style="width:100%">
				</el-date-picker>
			</el-form-item>
			<el-form-item label="离场日期" prop="departure_date" style="width:100%">
				<el-date-picker
					v-model="insertdata.departure_date"
					align="right"
					type="date"
					placeholder="选择离场日期"
					:picker-options="pickerOptions1" style="width:100%">
				</el-date-picker>
			</el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer" >
            <el-button @click="reset">取 消</el-button>
            <el-button type="primary" :loading="waitsubcstatus" @click="submitData()">确 定</el-button>
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
			logicroutes:"",
			optionsForEmp:[],
			illegal_categoryid:0,
			insertsubcompanyid:'',
			employeeid:"",
			insertdata:{
				approach_date: "",
				comp_name: "",
				companyid: 1,
				departure_date: "",
				email: "",
				license: "",
				manager: "",
				tel: ""
            },
			title:'',
			loading:false,
			rules:{
                companyid: [{ required: true, message: '请选择公司', trigger: 'change' }],
			},
			filter:{
				comp_name:"",
				manager:"",
				page:1,
				per_page:30,
			},
			companys:[
				{comp_name: "公司一", id: 1},
				{comp_name: "公司二", id: 2},
				{comp_name: "公司三", id: 3},
			],			
			pickerOptions1: {
				disabledDate(time) {
					return time.getTime() > Date.now();
				},
				shortcuts: [{
					text: '今天',
					onClick(picker) {
						picker.$emit('pick', new Date());
					}
				}, {
					text: '昨天',
					onClick(picker) {
						const date = new Date();
						date.setTime(date.getTime() - 3600 * 1000 * 24);
						picker.$emit('pick', date);
					}
				}, {
					text: '一周前',
					onClick(picker) {
						  const date = new Date();
						  date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
						  picker.$emit('pick', date);
					}
				}]
			}
		}
	},
	mounted: function() {
		this.theheight=window.innerHeight-190;
		this.$nextTick(() => {
			this.loadSubcontractors();
			this.$store.dispatch('getCompanies');
		})
	},	 
	computed: {   
		...mapGetters([
			'subcontractors',
			'subcontractorstotal',
            'companies',
			'illegal_categorys',
			'subcontractors_right',
			'waitsubcstatus',
			'subcontractorsActionStatus',
		]),
		dialogVisible: {
			get: function () {
			  return (this.subcontractorsActionStatus==1 || this.subcontractorsActionStatus==2)
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
		},
		illegal_categoryid: function (val, oldVal) {  
			if(val){
				console.log('aaa');
				this.loadIllegalTypes();
			}		
		},*/
	},
	methods: {
		loadSubcontractors(){	
			this.filter.comp_name=this.companys.find((n) => n.id==this.filter.companyid)?this.companys.find((n) => n.id==this.filter.companyid)['comp_name']:'';
			this.$store.dispatch('loadSubcontractors',this.filter);
		},
		loadIllegalTypes(){	
			this.$store.dispatch('loadIllegalTypes',this.illegal_categoryid);S
		},
		loadcompany(){
			this.$store.dispatch('loadSubcompany');
		},
		selectcompanyid(){
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
			this.title=chg['insertdata'];
			this.resetForm();
			delete this.insertdata.id;
			this.$store.commit('insertingSubcontractors',this.insertdata);
		},
		edit(data){
			this.title=chg['updatedata'];
			//this.$refs.dialog.title='资料修改';
			for (var key in data){
				this.insertdata[key]=data[key];
			};
			this.$store.dispatch('editSubcontractors',{id:data.id});
        },
		remove(data){
			this.$confirm('此操作将永久删除该资料, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
			}).then(() => {
				this.$store.dispatch('removeSubcontractors',{id:data.id});
			}).catch(() => {         
			});
        },
		reset() {
			this.$store.commit('cancleSubcontractors');
        },
		submitData(){
			this.$refs.insertdata.validate((valid) => {
				if (valid) {
                    for(var key in this.insertdata){
                        if(!this.insertdata[key]){
                            delete this.insertdata[key]
                        }
                    }
					this.insertdata.comp_name=this.companys.find((item)=>(item.id==this.insertdata.companyid)).comp_name;					
					if(this.insertdata.approach_date) this.insertdata.approach_date=(new Date(this.insertdata.approach_date)).format('yyyy-MM-dd');
					if(this.insertdata.departure_date) this.insertdata.departure_date=(new Date(this.insertdata.departure_date)).format('yyyy-MM-dd');
					this.$store.dispatch('saveSubcontractors',this.insertdata);
				}
                else {
                    return false;
                }
            });
		},
		resetForm(){
			this.insertdata={
				approach_date: "",
				comp_name: "",
				companyid: 1,
				departure_date: "",
				email: "",
				license: "",
				manager: "",
				tel: ""
            };
		},
		pageCurrentChange(val) {   //当前页变动时候触发的事件
			this.filter.page = val;
			this.loadSubcontractors();
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
