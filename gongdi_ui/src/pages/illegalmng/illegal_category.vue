<template>
  <div>
    <section class="main-content-wrapper wrapper">
        <section id="main-content" >
            <el-col :span="11">
                <div class="row">
                    <div class="col-md-12">
                        <!-- 操作 -->
                        <el-row type="flex" justify="space-between" style="margin-bottom:5px">
                            <el-col :inline="true"  style="float:left;">
                                <el-button v-if="illegal_category_right.ops.indexOf('insert')>=0" type="primary" @click="insert()" style="margin-left:10px;">新增</el-button>
                            </el-col>
                        </el-row>
                        <!-- 资料列表-->
                        <el-table :data="illegal_categorys"  ref="icTable" stripe v-loading="loading" highlight-current-row
                            element-loading-text="资料加载中..." @row-click="chgdetail" :height="theheight" border>
                            <el-table-column
                                type="index"
                                width="50">
                            </el-table-column>
                            <el-table-column prop="name" style="incenter"
                                label="名称">
                            </el-table-column>
                            <el-table-column v-if="illegal_category_right.ops.indexOf('edit')>=0 || illegal_category_right.ops.indexOf('edit')>=0"
                                    fixed="right"
                                label="操       作" width="130">
                                <template slot-scope="scope">
                                    <el-button v-if="illegal_category_right.ops.indexOf('delete')>=0" size="mini"  icon="el-icon-delete" @click="remove(scope.row)"></el-button>
                                    <el-button v-if="illegal_category_right.ops.indexOf('edit')>=0" size="mini" icon="el-icon-edit" @click="edit(scope.row)"></el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </el-col>
            <el-col :span="12" style="float:right;">
                <illegal_type :illegal_categoryid="detailillegal_categoryid">
                </illegal_type>
            </el-col>
        </section>
    </section>
	<el-dialog  ref="dialog" :title="title" class="centers" :visible.sync="dialogVisible" width="30%" 
	 :close-on-click-modal="false" :close-on-press-escape="false" :before-close="reset">
        <el-form id="#insertdata"  ref="insertdata" :rules="rules" :model="insertdata"  label-width="60px">
			<el-form-item label="名称" prop="name">
				<el-input v-model="insertdata.name"></el-input>
			</el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer" >
            <el-button @click="reset">取 消</el-button>
            <el-button type="primary" :loading="waitICStatus" @click="submitData()">确 定</el-button>
        </div>
    </el-dialog>
  </div>
</template>
<script>
import {mapGetters} from 'vuex'
import illegal_type from './illegal_type.vue'
export default {
    components: {
        'illegal_type': illegal_type,
    },
	data(){
		return {
			theheight:"",
			insertdata:{
				name:'',
            },
            detailillegal_categoryid:'',
			title:'',
			loading:false,
			rules:{
                name: [{ required: true, message: '必填字段', trigger: 'change' }],
			},
		}
	},
	mounted: function() {
		this.theheight=window.innerHeight-190;
		this.$nextTick(() => {
			this.loadIllegalCategorys();
            setTimeout(() => {
                if(this.illegal_categorys.length!=0){
                    this.detailillegal_categoryid=this.illegal_categorys[0].id;
                }
            }, 200);
		})
	},
    watch: {
        illegal_categorys: function (val) {
            if (val.length!=0){
                this.detailillegal_categoryid=val[0].id;
                setTimeout(() => {
                    if (val){
                        this.$refs.icTable.setCurrentRow(val[0]);
                    }
                }, 200);
            }
        }
    },
	computed: {
		...mapGetters([
			'illegal_categorys',
			'illegal_category_right',
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
        chgdetail(val){
		    this.detailillegal_categoryid=val.id;
        },
		insert(){		
			this.title=chg['illegal_category']+chg['insertdata'];
			this.resetForm();
			delete this.insertdata.id;
			this.$store.commit('insertingIllegalCategory',this.insertdata);
		},
		edit(data){
			console.log(this.$refs.dialog.title);
			this.title=chg['illegal_category']+chg['updatedata'];
			//this.$refs.dialog.title='资料修改';
			for (var key in data){
				this.insertdata[key]=data[key];
			};
			this.$store.dispatch('editIllegalCategorys',{id:data.id});
        },
		remove(data){
			this.$confirm('此操作将永久删除该资料, 是否继续?', '提示', {
				confirmButtonText: '确定',
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
