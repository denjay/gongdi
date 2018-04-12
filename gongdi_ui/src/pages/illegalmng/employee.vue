<template>
  <div>
    <section  class="main-content-wrapper wrapper">
        <section id="main-content" >
            <div class="row">
                <div class="col-md-12">
					<!-- 操作 -->
					<el-row type="flex" justify="space-between" style="margin-bottom:5px">
						<el-col :inline="true"  style="float:left;">
							<el-select filterable clearable v-model="subcompanyid"  style="margin-left:20px;width:20%;" placeholder="公司">
								<el-option 
								  v-for="item in subcompanys"
								  :key="item.id"
								  :label="item.name"
								  :value="item.id">
								</el-option>
							</el-select>
							<el-button v-if="employeeright.ops.indexOf('insert')>=0" type="primary" @click="insert()" style="margin-left:10px;">新增</el-button>
                            <!--<el-button type="primary" :disabled="selected.length==0" @click="removeDatas()"  >批量删除</el-button>-->
                        </el-col>
                    </el-row>
                    <!-- 资料列表-->
                    <el-table :data="employees" stripe v-loading="loading"
							element-loading-text="资料加载中..."
							:max-height="theheight" border>     
						<el-table-column
							type="index"
							width="50">
						</el-table-column>
						<el-table-column prop="name" style="incenter"
                            label="员工姓名">
                        </el-table-column>
						<el-table-column prop="code" style="incenter" width="120px"
							label="代码">
                        </el-table-column>                   
                        <el-table-column prop="allowance"
                            label="津贴">
                        </el-table-column>
						<el-table-column prop="departmentname"
                            label="部门">
                        </el-table-column>
						<el-table-column prop="position_typename"
                            label="职务">
                        </el-table-column>
						<el-table-column prop="address" width="120px"
                            label="现住地址">
                        </el-table-column>
						<el-table-column prop="isdimission" inline-template
										 label="是否离职"
										 width="100">
						   <div>{{ row.isdimission |  isdimissionchg}}</div>
						</el-table-column>
						 <el-table-column prop="accessiondate" width="120"
                            label="入职日期">
                        </el-table-column>
						 <el-table-column prop="dimissiondate" width="120"
                            label="离职日期">
                        </el-table-column>
						 <el-table-column prop="remark"
                            label="备注">
                        </el-table-column>
						<el-table-column prop="sex" 
										 label="性别"
										 width="100">
						    <template slot-scope="scope">
								{{ scope.row.sex |  sexchg}}
							</template>
						</el-table-column>
						 <el-table-column prop="mobtelphone"
                            label="电话">
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
					<div class="block">
						<el-pagination style="text-align:center"
							:current-page="filter.page"
							:page-size="filter.perpage"
							layout="total, prev, pager, next"
							:total="employeestotal"
							@current-change="pageCurrentChange">
						</el-pagination>
					</div>
                </div>
            </div>
        </section>
    </section>   
	<el-dialog  ref="dialog" :title="title" class="centers" :visible.sync="dialogVisible" size="large" 
	 :close-on-click-modal="false" :close-on-press-escape="false" :before-close="reset">
        <el-form id="#insertdata"  ref="insertdata" :rules="rules" :model="insertdata"  label-width="100px">
			<el-row>
				<el-col :span="12">			
					<el-form-item label="公司">
						<el-select style="width:100%;" filterable clearable v-model="insertsubcompanyid" placeholder="请选择">
							<el-option
								v-for="item in subcompanys"
								:key="item.id"
								:label="item.name"
								:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>				
					<el-form-item label="代码" prop="code">
						<el-input v-model="insertdata.code"></el-input>
					</el-form-item>
					<el-form-item label="津贴">
						<el-input v-model.number="insertdata.allowance"></el-input>
					</el-form-item>
					<el-form-item label="地址">
						<el-input v-model="insertdata.address"></el-input>
					</el-form-item>	 
					<el-form-item :inline="true" label="是否离职" style="width:100%">
						<el-radio-group  v-model="insertdata.isdimission">
							<el-radio  :label='0' style="margin-left:50px;">否</el-radio>
							<el-radio  :label='1' style="margin-left:50px;">是</el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="电话">
						<el-input v-model="insertdata.mobtelphone"></el-input>
					</el-form-item>
				</el-col>
				<el-col :span="12">				
					<el-form-item label="员工姓名" prop="name">	
						<el-input v-model="insertdata.name"></el-input>
					</el-form-item>
					<el-form-item :inline="true" label="性别" class="">
						<el-radio-group class="" v-model.number="insertdata.sex">
							<el-radio  :label='0' style="margin-left:50px;">男</el-radio>
							<el-radio  :label='1' style="margin-left:50px;">女</el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="部门">
						<el-select style="width:100%;" filterable clearable v-model="insertdata.departmentid" placeholder="请选择">
							<el-option
								v-for="item in departFEdatas"
								:key="item.id"
								:label="item.depart_name"
								:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="入职日期">
						<el-date-picker type="date" v-model="insertdata.accessiondate"
							class="width100" :picker-options="pickstart"></el-date-picker>
					</el-form-item>
					<el-form-item label="离职日期">
						<el-date-picker type="date" v-model="insertdata.dimissiondate"
							class="width100" :picker-options="leave_disable"></el-date-picker>
					</el-form-item>
					<el-form-item label="职务">
						<el-select style="width:100%;" filterable clearable v-model="insertdata.position_typeid" placeholder="请选择">
							<el-option
								v-for="item in position_typeFEdatas"
								:key="item.id"
								:label="item.name"
								:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>
				</el-col>
				<el-col>
					<el-form-item label="备注">
						<el-input v-model="insertdata.remark"></el-input>
					</el-form-item>
				</el-col>
			</el-row>
        </el-form>
        <div slot="footer" class="dialog-footer" >
            <el-button @click="reset">取 消</el-button>
            <el-button type="primary" :loading="waitEmpStatus" @click="submitData()">确 定</el-button>
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
			subcompanyid:"",
			insertsubcompanyid:'',
			employeeid:"",
			//totallrs:0,
			insertdata:{
				name:'',
				code:'',
				subcompanyid:'',
				allowance:'',
				sex:'',
				mobtelphone:'',
				address:'',
				isdimission:'',
				accessiondate:new Date(),
				remark:'',
				dimissiondate:new Date(),
				id:'',
				departmentid:'',
				position_typeid:'',
            },
			title:'',
			loading:false,
			rules:{
			},
			filter:{
				perpage: 20, // 页大小
				page: 1, // 当前页
				subcompanyid:"",
			},
			pickstart:{
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
			},
			leave_disable:{
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
				}],
				disabledDate: (time) =>{
					let begindateVal = this.insertdata.accessiondate;
					if (begindateVal) {
						return time.getTime() < begindateVal;
					}
				}
			},
		}
	},
	mounted: function() {
		this.theheight=window.innerHeight-190;
		this.$nextTick(() => {
			this.loadcompany();
			//this.subcompanyid=this.subcompanys[0].id;
			if(this.subcompanys.length!=0){
				this.subcompanyid=this.subcompanys[0].id;
			}
		})
		//this.loadlogicroute();
	},
	watch:{
		subcompanyid: function (val, oldVal) {
			this.loademployee();
		},
		subcompanys:function(newValue){
			if(newValue.length!=0){
				this.subcompanyid=newValue[0].id;
			}
		},
		insertsubcompanyid: function (val, oldVal) {
			if(val){
				this.loadDepart();
			}
			else{
			}
		},
		departFEdatas: function (val, oldVal) {
			if(val==''){
				this.insertdata.departmentid='';
			}
		},
	},	
	filters: {
		sexchg: function (value) {  
			if(value==0){return '男';}  
			if(value==1){return '女';}
		},
		isdimissionchg: function (value) {  
			if(value){return '是';}  
			else{return '否';}
		},
	}, 
	computed: {
		...mapGetters([
			'employees',
			'employeestotal',
			'employeeActionStatus',
			'departFEdatas',
			'position_typeFEdatas',
			'employeeright',
			'subcompanys',
			'waitEmpStatus',
		]),
		dialogVisible: {
			get: function () {
			  return (this.employeeActionStatus==1 || this.employeeActionStatus==2)
			},
			set: function () {
			}
		},
		totallrs:{
			get: function () {
				return (this.employees.total)
			},
			set: function () {
			}
		},
	},
	methods: {
		loademployee(){		
			this.filter.subcompanyid=this.subcompanyid;
			this.$store.dispatch('loademployee',this.filter);
		},
		loadcompany(){
			this.$store.dispatch('loadSubcompany');
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
			this.loadPosition_type();
			/*var initData={
                name:'',
				code:'',
				subcompanyid:sc_id,
				allowance:'',
				sex:0,
				mobtelphone:'',
				address:'',
				isdimission:0,
				accessiondate:'',
				remark:'',
				dimissiondate:'',
            };
			for (var key in initData){
				this.insertdata[key]=initData[key];
			};*/
			this.resetForm();
			//this.subcompanyid=this.insertdata.subcompanyid;
			delete this.insertdata.id;
			if ((this.subcompanys)&&(toString.call(this.subcompanys) === '[object Array]')&&(this.subcompanys.length>0)){
				this.insertsubcompanyid=this.subcompanys[0]['id'];
			}else{
				this.insertsubcompanyid='';
			}
			delete this.insertdata.subcompanyname;
			this.$store.commit('insertingEmployee',this.insertdata);
		},
		edit(data){
			console.log(this.$refs.dialog.title);
			this.loadPosition_type();
			this.title=chg['updatedata'];
			//this.$refs.dialog.title='资料修改';
			for (var key in data){
				this.insertdata[key]=data[key];
			};
			if(data.isdimission)
				this.insertdata.isdimission=1;
			else
				this.insertdata.isdimission=0;
			this.insertsubcompanyid=this.insertdata.subcompanyid;
			//this.subcompanyid=this.insertdata.subcompanyid;
			this.$store.dispatch('editEmployee',{id:data.id});
        },
		remove(data){
			this.$confirm('此操作将永久删除该资料, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
			}).then(() => {
				this.$store.dispatch('removeEmployee',{id:data.id});
			}).catch(() => {         
			});
        },
		reset() {
			this.$store.commit('cancleEmployee');
        },
		submitData(){
			this.$refs.insertdata.validate((valid) => {
				if (valid) {
					//this.insertdata.subcompanyid=this.subcompanyid;
					if(this.insertdata.isdimission==0)
						this.insertdata.isdimission=false;
					else
						this.insertdata.isdimission=true;
					this.insertdata.subcompanyid=this.insertsubcompanyid;
					// console.log(this.insertdata.accessiondate,typeof(this.insertdata.accessiondate));
					//this.insertdata.accessiondate='2017-07-28 10:03:38';
					//this.insertdata.dimissiondate='2017-07-28 10:03:38';
					if(this.insertdata.accessiondate) this.insertdata.accessiondate=(new Date(this.insertdata.accessiondate)).format('yyyy-MM-dd hh:mm:ss');
					if(this.insertdata.dimissiondate) this.insertdata.dimissiondate=(new Date(this.insertdata.dimissiondate)).format('yyyy-MM-dd hh:mm:ss');
					this.$store.dispatch('saveEmployee',this.insertdata);
				}
                else {
                    return false;
                }
            });
		},
		remoteForEmp(value){
			//this.loadempstatus=true;
			if (value !== ''&&this.employees.length!=0) {
				this.loadempstatus = true;
				setTimeout(() => {
					this.loadempstatus = false;
					this.optionsForEmp = this.employees.filter(item =>item.name.indexOf(value)>-1);
				}, 200);
			} else {
				this.loadempstatus = false;
				this.optionsForEmp = [];
			}
		},
		resetForm(){
			this.insertdata={
                name:'',
				code:'',
				subcompanyid:'',
				allowance:'',
				sex:0,
				mobtelphone:'',
				address:'',
				isdimission:0,
				accessiondate:new Date(),
				remark:'',
				dimissiondate:new Date(),				
				departmentid:'',
				position_typeid:'',
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
	.el-dialog--large {
		width: 70%!important;
	}
</style>
