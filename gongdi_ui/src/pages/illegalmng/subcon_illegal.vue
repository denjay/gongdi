<template>
  <div>
    <section class="main-content-wrapper wrapper">
        <section id="main-content" >
            <div class="row">
                <div class="col-md-12">
					<!-- 操作 -->
					<el-row type="flex" justify="space-between" style="margin-bottom:5px">
						<el-col :inline="true"  style="float:left;">
							<el-select filterable clearable v-model="illegal_categoryid"  style="width:180px;margin-left:20px;" placeholder="违规类别">
								<el-option 
									v-for="item in illegal_categorys"
									:key="item.id"
									:label="item.name"
									:value="item.id">
								</el-option>
							</el-select>
							<el-button v-if="employeeright.ops.indexOf('insert')>=0" type="primary" @click="insert()" style="margin-left:10px;">新增</el-button>
                        </el-col>
                    </el-row>
                    <!-- 资料列表-->
                    <el-table :data="subcon_illegals" stripe v-loading="loading"
							element-loading-text="资料加载中..."
							:max-height="theheight" border>     
						<el-table-column
							type="index"
							width="50">
						</el-table-column>
						<el-table-column prop="illegal_time" style="incenter" :formatter="dateFormat"
                            label="违规时间">
                        </el-table-column>
						<el-table-column prop="rectify_time" style="incenter" :formatter="dateFormat"
                            label="整改时间">
                        </el-table-column>
						<el-table-column prop="memo" style="incenter"
                            label="违规明细">
                        </el-table-column>
						<el-table-column prop="recorder" style="incenter"
                            label="记录员">
                        </el-table-column>
						<el-table-column label="审核状态"  width="90">
							<template slot-scope="scope">
								<template>
									<div>{{ scope.row.auditing_status |  auditing_statuschg}}</div>
								</template>
							</template>								
						</el-table-column>
						<el-table-column prop="rectify_emp_name" style="incenter"
                            label="整改人">
                        </el-table-column>
						<el-table-column prop="illegal_type_name" style="incenter"
                            label="违规类型">
                        </el-table-column>
						<el-table-column prop="company_name" style="incenter"
                            label="公司名">
                        </el-table-column>
						<el-table-column prop="subcon_com_name" style="incenter"
                            label="分包商公司名">
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
	<el-dialog  ref="dialog" :title="title" class="centers" :visible.sync="dialogVisible" width="32%" 
	 :close-on-click-modal="false" :close-on-press-escape="false" :before-close="reset">
        <el-form id="#insertdata"  ref="insertdata" :rules="rules" :model="insertdata"  label-width="100px">	
			 <el-tabs v-model="activeName" @tab-click="handleClick">
				<el-tab-pane label="违规管理" name="first" style="overflow-y:scroll;height:330px;">
					<el-form-item label="违规时间" prop="illegal_time">
						<el-date-picker
							v-model="insertdata.illegal_time"
							align="right"
							type="datetime"
							placeholder="选择违规时间"
							:picker-options="pickerOptions1">
						</el-date-picker>
					</el-form-item>
					<el-form-item label="整改时间" prop="rectify_time">
						<el-date-picker
							v-model="insertdata.rectify_time"
							align="right"
							type="datetime"
							placeholder="选择整改时间"
							:picker-options="pickerOptions1">
						</el-date-picker>
					</el-form-item>
					<el-form-item label="违规明细" prop="memo">
						<el-input v-model="insertdata.memo"></el-input>
					</el-form-item>
					<el-form-item prop="recorder" label="记录员">
						<el-input v-model="insertdata.recorder"></el-input>
					</el-form-item>
					<el-form-item prop="auditing_status" label="审状态核">
						<el-input v-model.number="insertdata.auditing_status"></el-input>
					</el-form-item>
					<el-form-item label="整改人" prop="rectify_empid">
						<el-select filterable v-model="insertdata.rectify_empid" 
							clearable  style="margin-left:10px;" @change="selectIllegal_categoryid"
							placeholder="整改人">
							<el-option 
								v-for="item in employees"
								:key="item.id"
								:label="item.name"
								:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="违规类型" prop="illegal_categoryid">
						<el-select filterable v-model="insertdata.illegal_typeid"
							clearable  style="margin-left:10px;"
							placeholder="违规类型">
							<el-option 
								v-for="item in illegal_categorys"
								:key="item.id"
								:label="item.name"
								:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="公司名" prop="companyid">
						<el-select filterable v-model="insertdata.companyid" 
							clearable  style="margin-left:10px;"
							placeholder="公司名">
							<el-option 
								v-for="item in companys"
								:key="item.id"
								:label="item.comp_name"
								:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="分包商公司名" prop="subcontractorid">
						<el-select filterable v-model="insertdata.subcontractorid" 
							clearable  style="margin-left:10px;"
							placeholder="公司名">
							<el-option 
								v-for="item in subcontractorlks"
								:key="item.id"
								:label="item.comp_name"
								:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>
				</el-tab-pane>
				 <el-tab-pane label="图片管理" name="second"  style="overflow-y:scroll;height:330px;">
					 <el-form-item>
						 <el-upload
								 class="upload-demo"
								 ref="upload"
								 action="/kong/gongdi_mng/v1.0/illegal_pics"
								 multiple
								 name="pic"
								 :data={illegalid:insertdata.id}
								 :before-remove="beforeRemove"
								 :on-change="handleChange"
								 :on-success="handleAvatarSuccess"
								 :auto-upload="false"
								 :file-list="fileList">
							 <el-button size="small" style="margin-left:-20px;" type="primary">选择文件</el-button>
						 </el-upload>
					 </el-form-item>
					 <el-table
							 :data="sillegal_pics"
							 border
							 style="width: 100%">
						 <el-table-column
								 type="index"
								 width="50">
						 </el-table-column>
						 <el-table-column
								 prop="file_name"
								 label="文件名">
						 </el-table-column>
						 <el-table-column label="操作" width="130">
							 <template slot-scope="scope">
								 <el-button @click="removePic(scope.row)" size="mini" icon="el-icon-delete"></el-button>
							 </template>
						 </el-table-column>
					 </el-table>
				 </el-tab-pane>
			 </el-tabs>
		</el-form>
        <div slot="footer" class="dialog-footer" >
            <el-button @click="reset">取 消</el-button>
            <el-button type="primary" :loading="waitSIstatus" @click="submitData()">确 定</el-button>
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
			employees:[],
			insertsubcompanyid:'',
			employeeid:"",
			insertdata:{
				auditing_status:'',
				companyid:'',
				illegal_time:'',
				//illegal_type_name:'',
				illegal_typeid:'',
				memo:'',
				recorder:'',
				//rectify_emp_name:'',
				rectify_empid:'',
				rectify_time:'',
				//subcon_com_name:'',
				subcontractorid:'',
				fileList:[],
            },
			title:'',
			fileList:[],
			activeName: 'first',
			loading:false,
			illegal_categoryid:'',
			rules:{
			},
			filter:{
				auditing_status:0,
				subcon_name:"",
				illegal_typeid:0,
				page:1,
				per_page:30,
			},	
			companys:[
				{comp_name: "模拟公司一", id: 1},
				{comp_name: "模拟公司二", id: 2},
				{comp_name: "模拟公司三", id: 3},			
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
            this.loadSubconIllegals();
        })
	},	
	filters: {
		auditing_statuschg: function (value) {  
			if(value==0){return '未审核';}  
			if(value==1){return '审核通过';}
			if(value==2){return '审核未通过';}
		},
	}, 
	computed: {   
		...mapGetters([
			'subcontractorlks',
			'subcon_illegals',
			'illegal_categorys',
			'employeeright',
			'waitSIstatus',
			'subconIllegalStatus',
            'sillegal_pics'
		]),
		dialogVisible: {
			get: function () {
			  return (this.subconIllegalStatus==1 || this.subconIllegalStatus==2)
			},
			set: function () {
			}
		},
	},
	watch:{
	},
	methods: {
        handleClick(tab, event) {
            console.log(tab, event);
        },
        beforeRemove(file, fileList) {
            return this.$confirm(`确定移除 ${ file.name }？`);
        },
        handleAvatarSuccess(file) {
            this.getPics();
            this.$message({
                message: '文件上传成功',
                type: 'success'
            });
            this.fileList=[];
        },
        getPics(){
            this.$store.dispatch('getSIllegal_pics',{id:this.insertdata.id});
        },
        handleChange(file, fileList) {
            this.insertdata.fileList = fileList;
        },
        loadSubconIllegals(){
            this.$store.dispatch('loadSubconIllegals',this.filter);
        },
		loadcompany(){
			this.$store.dispatch('loadSubcompany');
		},		
		loadEmployee(){
			//this.$store.dispatch('loadEmployeeLk');
			this.employees=[{'name':'jack',id:1},{'name':'macheal',id:2},{'name':'rose',id:3}];
		},
		loadSubcontractorLks(){	
			this.$store.dispatch('loadSubcontractorLks');
		},
		selectIllegal_categoryid(){
		},
		insert(){		
			this.title=chg['insertdata'];
			this.resetForm();
            this.fileList = [];
            this.$store.commit('clearSIllegal_pics');
			this.loadEmployee();
			this.loadSubcontractorLks();
			delete this.insertdata.id;
			this.$store.commit('insertingSubconIllegal',this.insertdata);
		},
		edit(data){
			this.title=chg['updatedata'];
			this.loadEmployee();
            this.fileList = [];
			this.loadSubcontractorLks();
			for (var key in data){
				this.insertdata[key]=data[key];
			};
            this.getPics();
			this.$store.dispatch('editSubconIllegal',{id:data.id});
        },
		remove(data){
			this.$confirm('此操作将永久删除该资料, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
			}).then(() => {
				this.$store.dispatch('removeSubconIllegal',{id:data.id});
			}).catch(() => {         
			});
        },
        getPics(){
            this.$store.dispatch('getSIllegal_pics',{id:this.insertdata.id});
        },
        removePic(data){
            this.$confirm('确定删除该图片, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
            }).then(() => {
                this.$store.dispatch('removeSPic',data);
            })
        },
		reset() {
			this.$store.commit('cancleSubconIllegal');
        },
		submitData(){
			this.$refs.insertdata.validate((valid) => {
				if (valid) {
					this.$refs.upload.submit();
					//this.$store.dispatch('saveSubconIllegal',this.insertdata);
				}
                else {
                    return false;
                }
            });
		},
		remoteForEmp(value){
			//this.loadempstatus=true;
			if (value !== ''&&this.subcon_illegals.length!=0) {
				this.loadempstatus = true;
				setTimeout(() => {
					this.loadempstatus = false;
					this.optionsForEmp = this.subcon_illegals.filter(item =>item.name.indexOf(value)>-1);
				}, 200);
			} else {
				this.loadempstatus = false;
				this.optionsForEmp = [];
			}
		},
		resetForm(){
			this.insertdata={
				auditing_status:'',
				companyid:'',
				illegal_time:'',
				//illegal_type_name:'',
				illegal_typeid:'',
				memo:'',
				recorder:'',
				//rectify_emp_name:'',
				rectify_empid:'',
				rectify_time:'',
				//subcon_com_name:'',
				subcontractorid:'',
            };
		},
		pageCurrentChange(val) {   
			this.filter.page = val;
			this.loademployee();
		},
		dateFormat:function(row, column) {  
            var date = row[column.property];  
			if (date == undefined) {  
                return "";  
			}  
			return date.split("T")[0]; 
			//return date.split("T")[0]+' '+date.split("T")[1].split(".")[0];
        } 
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
