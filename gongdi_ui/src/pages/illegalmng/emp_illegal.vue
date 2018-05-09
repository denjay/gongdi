<template>
  <div>
    <section class="main-content-wrapper wrapper">
        <section id="main-content" >
            <div class="row">
                <div class="col-md-12">
					<!-- 操作 -->
					<el-row type="flex" justify="space-between" style="margin-bottom:5px">
						<el-col :inline="true"  style="float:left;">
							<el-select filterable clearable v-model="filter.illegal_typeid" style="width:180px;margin-left:20px;" placeholder="违规类别">
								<el-option 
									v-for="item in illegaltyplks"
									:key="item.id"
									:label="item.name"
									:value="item.id">
								</el-option>
							</el-select>
							<el-select filterable clearable v-model.number="auditing_status" style="width:180px;margin-left:20px;" placeholder="审核状态">
								<el-option
										v-for="item in auditing_statuss"
										:key="item.id"
										:label="item.name"
										:value="item.id">
								</el-option>
							</el-select>
							<el-input v-model="filter.illegal_emp_name"  style="width:180px;margin-left:20px;" placeholder="请输入违规人"></el-input>
							<el-button v-if="emp_illegal_right.ops.indexOf('view')>=0" type="primary" @click="loadEmpIllegals()" style="margin-left:10px;">查询</el-button>
							<el-button v-if="emp_illegal_right.ops.indexOf('insert')>=0" type="primary" @click="insert()" style="margin-left:10px;">新增</el-button>
                        </el-col>
                    </el-row>
                    <!-- 资料列表-->
                    <el-table :data="emp_illegals" stripe v-loading="loading"
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
						<el-table-column prop="comp_name" style="incenter"
                            label="公司名">
                        </el-table-column>
						<el-table-column prop="illegal_emp_name" style="incenter"
                            label="违规人">
                        </el-table-column>
                        <el-table-column v-if="emp_illegal_right.ops.indexOf('edit')>=0 || emp_illegal_right.ops.indexOf('edit')>=0" 
								fixed="right"
                            label="操       作" width="130">
                            <template slot-scope="scope">
                                <el-button v-if="emp_illegal_right.ops.indexOf('delete')>=0" size="mini"  icon="el-icon-delete" @click="remove(scope.row)"></el-button>
                                <el-button v-if="emp_illegal_right.ops.indexOf('edit')>=0" size="mini" icon="el-icon-edit" @click="edit(scope.row)"></el-button>
                            </template>
                        </el-table-column>
                    </el-table>
					<el-col>
						<el-pagination style="text-align:center"
						   :current-page="filter.page"
						   :page-size="filter.per_page"
						   layout="total, prev, pager, next"
						   :total="emp_illegalstotal"
						   @current-change="pageCurrentChange">
						</el-pagination>
					</el-col>
                </div>
            </div>
        </section>
    </section>   
	<el-dialog  ref="dialog" :title="title" class="centers" :visible.sync="dialogVisible" width="40%"
	 :close-on-click-modal="false" :close-on-press-escape="false" :before-close="reset" style="margin-top:-50px">
		<el-form id="#insertdata"  ref="insertdata" :rules="rules" :model="insertdata"  label-width="100px">
		    <el-tabs v-model="activeName" @tab-click="handleClick">
				<el-tab-pane label="违规管理" name="first"  style="overflow-y:scroll;height:400px;">
					<el-form-item label="违规时间" prop="illegal_time" style="width:90%">
						<el-date-picker
							v-model="insertdata.illegal_time"
							align="right"
							type="datetime"
							placeholder="选择违规时间"
							:picker-options="pickerOptions" style="width:100%">
						</el-date-picker>
					</el-form-item>
					<el-form-item label="整改时间" prop="rectify_time" style="width:90%">
						<el-date-picker
							v-model="insertdata.rectify_time"
							align="right"
							type="datetime"
							placeholder="选择整改时间"
							:picker-options="pickerOptions1" style="width:100%">
						</el-date-picker>
					</el-form-item>
					<el-form-item label="违规明细" prop="memo" style="width:90%">
						<el-input v-model="insertdata.memo"></el-input>
					</el-form-item>
					<el-form-item prop="recorder" label="记录员" style="width:90%">
						<el-input v-model="insertdata.recorder"></el-input>
					</el-form-item>
					<el-form-item prop="auditing_status" label="审状态核" style="width:90%">
						<el-radio-group v-model.number="insertdata.auditing_status">
							<el-radio :label="0">未审核</el-radio>
							<el-radio :label="1">审核通过</el-radio>
							<el-radio :label="2">审核未通过</el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="违规人" prop="rectify_empid" style="width:90%">
						<el-select filterable v-model="insertdata.illegal_empid"
								   clearable  @change="selectRectify_empid"
								   placeholder="违规人" style="width:100%">
							<el-option
									v-for="item in employees"
									:key="item.id"
									:label="item.name"
									:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="整改人" prop="rectify_empid" style="width:90%">
						<el-select filterable v-model="insertdata.rectify_empid" 
							clearable  @change="selectRectify_empid"
							placeholder="整改人" style="width:100%">
							<el-option 
								v-for="item in employees"
								:key="item.id"
								:label="item.name"
								:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="公司" prop="companyid"  style="width:90%">
						<el-select filterable v-model="insertdata.companyid"
								   clearable
								   placeholder="公司名" style="width:100%">
							<el-option
									v-for="item in companies"
									:key="item.id"
									:label="item.company_name"
									:value="item.id">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item label="违规类型" prop="casillegal_typeid" style="width:90%">
						<el-cascader style="width:100%"
							expand-trigger="hover" :show-all-levels="false"
							:options="illegal_typetrees"
							@change="cashandleChange" v-model="insertdata.casillegal_typeid">
						</el-cascader>
					</el-form-item>			
				</el-tab-pane>    
				<el-tab-pane label="图片管理" name="second"  style="overflow-y:scroll;height:400px;">
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
							<el-button  v-if="illegal_pic_right.ops.indexOf('insert')>=0" slot="trigger" size="small" type="primary">选取文件</el-button>
							<el-button  v-if="illegal_pic_right.ops.indexOf('insert')>=0" style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
						</el-upload>
					</el-form-item>
					<el-table
						:data="eillegal_pics"
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
						<!--<el-table-column label="预览">
							<template scope="scope">
								<image :src="scope.row.file_name" width="30" height="80"/>
							</template>
						</el-table-column>-->
						<el-table-column label="文件大小" prop="pic_size">
						</el-table-column>
						<el-table-column label="操作" width="130">
							<template slot-scope="scope">
								<el-button v-if="illegal_pic_right.ops.indexOf('delete')>=0" @click="removePic(scope.row)" size="mini" icon="el-icon-delete"></el-button>
								<el-button v-if="illegal_pic_right.ops.indexOf('view')>=0" size="mini" @click="oppic(`/kong/gongdi_mng/v1.0/illegal_pics/${scope.row.id}`)" icon="el-icon-view"></el-button>
							</template>
						</el-table-column>
					</el-table>
				</el-tab-pane> 
			</el-tabs>
		</el-form>
        
        <div slot="footer" class="dialog-footer" >
            <el-button @click="reset">取 消</el-button>
            <el-button type="primary" :loading="waitETstatus" @click="submitData()">确 定</el-button>
        </div>
    </el-dialog>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'
export default {
	data(){
		return {
    		//:disabled="this.insertdata.id!=''"
			theheight:"",
			logicroutes:"",
			optionsForEmp:[],
			//illegal_categoryid:0,
            illegal_typeid:"",
			insertsubcompanyid:'',
			employeeid:"",
			employees:[],
			insertdata:{
				"auditing_status": 0,
				"companyid": '',
				"id": '',
				"illegal_empid": '',
				"illegal_time": "",
				"illegal_typeid": '',
				"memo": "",
				"recorder": "",
				"rectify_empid": '',
				"rectify_time": "",
                casillegal_typeid:[],
            },
			title:'',
			fileList:[],
			activeName: 'first',
			loading:false,
			rules:{
                companyid: [{ required: true, message: '请选择公司', trigger: 'change' }],
                casillegal_typeid: [{ required: true, message: '请选择违规类型', trigger: 'change' }],
			},
            auditing_status:-1,
			filter:{
				auditing_status:0,
				illegal_emp_name:null,
				illegal_typeid:null,
				page:1,
				per_page:30,
			},
            pickerOptions: {
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
            },
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
			},
            auditing_statuss:[
				{"id":-1,"name":"未审核"},
                {"id":1,"name":"审核通过"},
				{"id":2,"name":"审核未通过"}
			]
		}
	},
	mounted: function() {
		this.theheight=window.innerHeight-190;
		this.$nextTick(() => {
			this.loadEmpIllegals();
            this.loadIllegaltypetree();
            this.loadIllegaltype();
            this.$store.dispatch('getCompanies');
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
			'emp_illegals',
			'illegal_types',
			'illegaltyplks',
            'companies',
			'emp_illegalstotal',
			'illegal_typetrees',
			'emp_illegal_right',
			'illegal_pic_right',
			'waitETstatus',
			'empIllegalActionStatus',
			'eillegal_pics'
		]),
		dialogVisible: {
			get: function () {
			  return (this.empIllegalActionStatus==1 || this.empIllegalActionStatus==2)
			},
			set: function () {
			}
		},
	},
	watch:{
	},
	methods: {
        submitUpload() {
            this.$refs.upload.submit();
        },
        oppic(url){
            window.open(url,'_blank','')
        },
		handleClick(tab, event) {
			console.log(tab, event);
		},
        cashandleChange(val){
			console.log(val);
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
            this.$store.dispatch('getEIllegal_pics',{id:this.insertdata.id});
		},
        handleChange(file, fileList) {
			this.insertdata.fileList = fileList;
        },
	    loadEmpIllegals(){
            for(var key in this.filter){
				if(!this.filter[key]){
                	delete this.filter[key]
				}
            }
            if(this.auditing_status && this.auditing_status==-1){
                this.filter.auditing_status=0;
            }
            else if(this.auditing_status){
                this.filter.auditing_status=this.auditing_status;
            }
            this.$store.dispatch('loadEmpIllegals',this.filter);
		},
        loadIllegaltypetree(){
            this.$store.dispatch('loadIllTyeTree');
        },
        loadIllegaltype(){
            this.$store.dispatch('loadIllegalTypelks');
        },
		loadcompany(){
			this.$store.dispatch('loadSubcompany');
		},
		loadEmployee(){
			//this.$store.dispatch('loadEmployeeLk');
			this.employees=[{'name':'jack',id:1},{'name':'macheal',id:2},{'name':'rose',id:3}];
		},		
		selectRectify_empid(){
		},
		/*loadDepart(){
			if (this.insertsubcompanyid){				
				var data={subcompanyid:this.insertsubcompanyid};			
				this.$store.dispatch('loadDepartFE',data);
			}
		},*/
		insert(){		
			console.log('1111111111111');
			this.title=chg['insertdata'];
			this.fileList = []
			this.loadEmployee();
			this.$store.commit('clearEIllegal_pics');
			this.loadSubcontractorLks();
			this.resetForm();
			delete this.insertdata.id;
			this.$store.commit('insertingEmpIllegal',this.insertdata);
		},
		loadSubcontractorLks(){	
			this.$store.dispatch('loadSubcontractorLks');
		},
		edit(data){
			this.title=chg['updatedata'];
            this.fileList = []
			this.loadEmployee();
            this.loadIllegaltypetree();
			this.loadSubcontractorLks();
			for (var key in data){
				this.insertdata[key]=data[key];
			}
			console.log(this.insertdata);
            this.insertdata.casillegal_typeid=data.illegal_typetree;
			console.log(this.insertdata.casillegal_typeid);
			this.getPics();
			this.$store.dispatch('editEmpIllegal',{id:data.id});
        },
		remove(data){
			this.$confirm('此操作将永久删除该资料, 是否继续?', '提示', {
				confirmButtonText: '确定',
				cancelButtonText: '取消',
			}).then(() => {
				this.$store.dispatch('removeEmpIllegal',{id:data.id});
			}).catch(() => {         
			});
        },
        removePic(data){
            this.$confirm('确定删除该图片, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
            }).then(() => {
                this.$store.dispatch('removeEPic',data);
            })
        },
		reset() {
			this.$store.commit('cancleEmpIllegal');
        },
		submitData(){
			this.$refs.insertdata.validate((valid) => {
				if (valid) {
                    for(var key in this.insertdata){
                        if(!this.insertdata[key]){
                            delete this.insertdata[key]
                        }
                    }
					if(this.insertdata.casillegal_typeid.length==2){
                        this.insertdata.illegal_typeid=parseInt(this.insertdata.casillegal_typeid[this.insertdata.casillegal_typeid.length-1]);
                    }
					var a=new Date();
					this.insertdata.id=a.getFullYear()+a.getHours()+a.getMilliseconds();
                    delete this.insertdata.illegal_typetree;
                    //delete this.insertdata.casillegal_typeid;
					this.$store.dispatch('saveEmpIllegal',this.insertdata);
                    /*this.$axios.post('/kong/gongdi_mng/v1.0/emp_illegals',data)
                        .then(function(response){
                            this.picillegalid=response.id;  //picillegalid上传的data
                            this.$refs.upload.submit();
                            commit('insertedEmpIllegal',{isSuccess:true,data:response.data});
                        }).catch(function(error){
                        commit('insertedEmpIllegal',{isSuccess:false})
                    })*/
                    //this.$refs.upload.submit();
				}
                else {
                    return false;
                }
            });
		},
		remoteForEmp(value){
			//this.loadempstatus=true;
			if (value !== ''&&this.emp_illegals.length!=0) {
				this.loadempstatus = true;
				setTimeout(() => {
					this.loadempstatus = false;
					this.optionsForEmp = this.emp_illegals.filter(item =>item.name.indexOf(value)>-1);
				}, 200);
			} else {
				this.loadempstatus = false;
				this.optionsForEmp = [];
			}
		},
		resetForm(){
			this.insertdata={
                "auditing_status": 0,
                "companyid": '',
                "id": '',
                "illegal_empid": '',
                "illegal_time": "",
                "illegal_typeid": '',
                "memo": "",
                "recorder": "",
                "rectify_empid": '',
                "rectify_time": "",
                casillegal_typeid:[]
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
